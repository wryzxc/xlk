import os
import json
import subprocess
import tempfile
import time
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps

# Import course data
from course_data import COURSES, LESSONS, EXERCISES, EXAMS, EXAM_QUESTIONS
from course_enhancements import (
    get_course_enhancement, get_lesson_enhancement, get_learning_tools,
    COURSE_ENHANCEMENTS, LESSON_ENHANCEMENTS, LEARNING_TOOLS
)

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'python-learning-platform-2024-dev'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

# 会话安全配置
app.config.update(
    SESSION_COOKIE_SECURE=False,      # 开发环境关闭，生产环境设为True
    SESSION_COOKIE_HTTPONLY=True,     # 防止XSS窃取会话
    SESSION_COOKIE_SAMESITE='Lax',    # CSRF防护
    PERMANENT_SESSION_LIFETIME=timedelta(hours=2)  # 会话2小时过期
)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    # HSTS仅在HTTPS环境下启用
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.after_request
def add_static_cache(response):
    if request.path.startswith('/static/'):
        if '.css' in request.path or '.js' in request.path:
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        elif '.ico' in request.path or '.png' in request.path or '.jpg' in request.path:
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https:;"
    return response

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('需要管理员权限', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student')
    department = db.Column(db.String(100), nullable=True)
    class_name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)
    progress_records = db.relationship('LearningProgress', backref='user', lazy=True)
    submissions = db.relationship('Submission', backref='user', lazy=True)
    posts = db.relationship('ForumPost', backref='author', lazy=True)
    learning_logs = db.relationship('LearningLog', backref='user', lazy=True, order_by='LearningLog.created_at.desc()')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_course_progress(self, course_id):
        """获取用户在指定课程的学习进度"""
        lessons = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order).all()
        if not lessons:
            return 0
        completed = 0
        for lesson in lessons:
            progress = LearningProgress.query.filter_by(
                user_id=self.id, lesson_id=lesson.id, completed=True
            ).first()
            if progress:
                completed += 1
        return int((completed / len(lessons)) * 100)
    
    def can_access_lesson(self, lesson):
        return True

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(20), default='beginner')
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    lessons = db.relationship('Lesson', backref='course', lazy=True, order_by='Lesson.order')
    
    @property
    def lesson_count(self):
        return len(self.lessons)
    
    @property
    def estimated_minutes(self):
        return self.lesson_count * 25
    
    @property
    def difficulty_label(self):
        labels = {'beginner': '入门', 'intermediate': '进阶', 'advanced': '高级'}
        return labels.get(self.level, '入门')
    
    @property
    def difficulty_color(self):
        colors = {'beginner': 'success', 'intermediate': 'warning', 'advanced': 'danger'}
        return colors.get(self.level, 'success')

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    estimated_minutes = db.Column(db.Integer, default=25)
    key_points = db.Column(db.Text, nullable=True)
    code_examples = db.Column(db.Text, nullable=True)
    
    @property
    def is_first(self):
        return self.order == 1
    
    @property
    def prev_lesson(self):
        return Lesson.query.filter_by(
            course_id=self.course_id, order=self.order - 1
        ).first()
    
    @property
    def next_lesson(self):
        return Lesson.query.filter_by(
            course_id=self.course_id, order=self.order + 1
        ).first()

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, default='')
    expected_output = db.Column(db.Text, nullable=True)
    test_cases = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(20), default='easy')
    category = db.Column(db.String(50), nullable=False)
    hints = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0)
    related_lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)
    related_lesson = db.relationship('Lesson', backref='exercises')
    
    @property
    def difficulty_label(self):
        labels = {'easy': '简单', 'medium': '中等', 'hard': '困难'}
        return labels.get(self.difficulty, '简单')
    
    @property
    def difficulty_color(self):
        colors = {'easy': 'success', 'medium': 'warning', 'hard': 'danger'}
        return colors.get(self.difficulty, 'success')

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    exercise = db.relationship('Exercise', backref='submissions')

class LearningProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    progress_percentage = db.Column(db.Float, default=0.0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    course = db.relationship('Course', backref='progress_records')
    lesson = db.relationship('Lesson', backref='progress_records')

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    passing_score = db.Column(db.Float, default=60.0)
    level = db.Column(db.String(20), default='beginner')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship('ExamQuestion', backref='exam', lazy=True)

class ExamQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='multiple_choice')
    options = db.Column(db.Text, nullable=True)
    correct_answer = db.Column(db.Text, nullable=False)
    points = db.Column(db.Float, default=10.0)
    order = db.Column(db.Integer, default=0)

class ExamAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    answers = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, default=0.0)
    passed = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='in_progress')
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    auto_saved_at = db.Column(db.DateTime, nullable=True)
    remaining_seconds = db.Column(db.Integer, nullable=True)
    exam = db.relationship('Exam', backref='attempts')

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    replies = db.relationship('ForumReply', backref='post', lazy=True)

class ForumReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('User', backref='replies')

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class LearningLog(db.Model):
    """用户学习行为日志 - 全面追踪学习活动"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    log_type = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    target_id = db.Column(db.Integer, nullable=True)
    target_name = db.Column(db.String(200), nullable=True)
    target_type = db.Column(db.String(50), nullable=True)
    detail = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def formatted_time(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def formatted_duration(self):
        if not self.duration_seconds:
            return '-'
        minutes = self.duration_seconds // 60
        seconds = self.duration_seconds % 60
        if minutes > 0:
            return f'{minutes}分{seconds}秒'
        return f'{seconds}秒'


class LessonViewLog(db.Model):
    """课程观看记录 - 详细追踪课程学习"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    watch_duration = db.Column(db.Integer, default=0)
    completion_percentage = db.Column(db.Float, default=0.0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    lesson = db.relationship('Lesson', backref='view_logs')
    course = db.relationship('Course', backref='lesson_view_logs')


class ExerciseAttemptLog(db.Model):
    """练习尝试记录 - 详细追踪练习完成"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    code_submitted = db.Column(db.Text, nullable=True)
    output_result = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')
    attempt_count = db.Column(db.Integer, default=1)
    time_spent_seconds = db.Column(db.Integer, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    exercise = db.relationship('Exercise', backref='attempt_logs')


class ExamParticipationLog(db.Model):
    """考试参与记录 - 详细追踪考试情况"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    answers = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, default=0.0)
    passed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)
    correct_count = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=0)
    exam = db.relationship('Exam', backref='participation_logs')


# ===================== 辅助函数 =====================

def get_learning_path():
    """获取完整的学习路径（按难度排序的课程）"""
    level_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
    courses = Course.query.filter_by(is_published=True).all()
    return sorted(courses, key=lambda c: (level_order.get(c.level, 99), c.order))

def get_user_stats(user_id):
    """获取用户学习统计"""
    total_lessons = Lesson.query.count()
    completed_lessons = LearningProgress.query.filter_by(
        user_id=user_id, completed=True
    ).count()
    
    total_exercises = Exercise.query.count()
    passed_exercises = Submission.query.filter_by(
        user_id=user_id, status='passed'
    ).count()
    
    exam_attempts = ExamAttempt.query.filter_by(user_id=user_id).all()
    passed_exams = len([e for e in exam_attempts if e.passed])
    
    # 计算平均分
    avg_score = 0
    user_submissions = Submission.query.filter_by(user_id=user_id).all()
    if user_submissions:
        avg_score = sum(s.score for s in user_submissions) / len(user_submissions)

    return {
        'lesson_progress': int((completed_lessons / max(total_lessons, 1)) * 100),
        'completed_lessons': completed_lessons,
        'total_lessons': total_lessons,
        'exercise_progress': int((passed_exercises / max(total_exercises, 1)) * 100),
        'passed_exercises': passed_exercises,
        'total_exercises': total_exercises,
        'passed_exams': passed_exams,
        'total_exams': Exam.query.count(),
        'avg_score': avg_score
    }

def get_platform_stats():
    """获取平台全局统计数据（用于首页动态展示）"""
    return {
        'total_courses': Course.query.filter_by(is_published=True).count(),
        'total_lessons': Lesson.query.count(),
        'total_exercises': Exercise.query.count(),
        'total_exams': Exam.query.count()
    }

# ===================== 路由 =====================

@app.route('/')
def index():
    courses = get_learning_path()
    stats = None
    if current_user.is_authenticated:
        stats = get_user_stats(current_user.id)
    platform_stats = get_platform_stats()
    return render_template('index.html', courses=courses, stats=stats, platform_stats=platform_stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
            flash('请填写所有必填字段', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('两次输入的密码不一致', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'danger')
            return render_template('register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            # 更新最后登录时间
            user.last_login_at = datetime.utcnow()
            db.session.commit()
            # 记录登录日志
            log = LearningLog(
                user_id=user.id,
                log_type='auth',
                action='用户登录',
                target_id=user.id,
                target_name=user.username,
                target_type='user',
                detail=f'用户 {user.username} 登录系统',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string if request.user_agent else None
            )
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    from datetime import datetime, timedelta
    progress = LearningProgress.query.filter_by(user_id=current_user.id).all()
    submissions = Submission.query.filter_by(user_id=current_user.id).order_by(Submission.submitted_at.desc()).limit(10).all()
    exam_attempts = ExamAttempt.query.filter_by(user_id=current_user.id).order_by(ExamAttempt.started_at.desc()).limit(5).all()
    stats = get_user_stats(current_user.id)

    # 计算连续学习天数
    streak_days = 0
    today = datetime.utcnow().date()
    for i in range(365):
        check_date = today - timedelta(days=i)
        has_activity = Submission.query.filter(
            Submission.user_id == current_user.id,
            db.func.date(Submission.submitted_at) == check_date
        ).first() is not None
        if has_activity:
            streak_days += 1
        else:
            break

    # 技能掌握度数据
    skills = [
        {'name': 'Python基础', 'level': min(100, stats.get('lesson_progress', 0))},
        {'name': '数据结构', 'level': min(100, stats.get('exercise_progress', 0))},
        {'name': '面向对象', 'level': min(100, stats.get('passed_exams', 0) * 20)},
        {'name': '文件操作', 'level': min(100, stats.get('passed_exercises', 0) * 5)},
        {'name': '高级特性', 'level': min(100, stats.get('passed_exams', 0) * 15)},
    ]

    # 成就徽章系统
    achievements = [
        {'name': '初学者', 'description': '完成第一个练习', 'icon': '&#127891;', 'unlocked': stats.get('passed_exercises', 0) >= 1},
        {'name': '代码达人', 'description': '完成10个练习', 'icon': '&#128187;', 'unlocked': stats.get('passed_exercises', 0) >= 10},
        {'name': '学习先锋', 'description': '完成50%课程', 'icon': '&#128640;', 'unlocked': stats.get('lesson_progress', 0) >= 50},
        {'name': '考试通过', 'description': '通过第一次考试', 'icon': '&#127942;', 'unlocked': stats.get('passed_exams', 0) >= 1},
        {'name': '全勤奖', 'description': '连续学习7天', 'icon': '&#128197;', 'unlocked': streak_days >= 7},
        {'name': '满分王者', 'description': '获得一次满分', 'icon': '&#11088;', 'unlocked': any(s.score == 100 for s in submissions)},
        {'name': '探索者', 'description': '尝试所有课程', 'icon': '&#127758;', 'unlocked': stats.get('completed_lessons', 0) >= 5},
        {'name': '专家', 'description': '通过所有考试', 'icon': '&#127941;', 'unlocked': stats.get('passed_exams', 0) >= 3},
    ]
    unlocked_achievements = sum(1 for a in achievements if a['unlocked'])
    total_achievements = len(achievements)

    # 学习热力图数据（过去53周）
    heatmap_data = []
    for i in range(371):  # 53周 * 7天
        date = today - timedelta(days=i)
        count = Submission.query.filter(
            Submission.user_id == current_user.id,
            db.func.date(Submission.submitted_at) == date
        ).count()
        level = 0
        if count >= 5:
            level = 4
        elif count >= 3:
            level = 3
        elif count >= 1:
            level = 2
        elif count > 0:
            level = 1
        heatmap_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count,
            'level': level
        })
    heatmap_data.reverse()

    # 最近活动
    recent_activities = []
    for sub in submissions[:5]:
        recent_activities.append({
            'icon': '&#9997;',
            'type': 'success',
            'title': f'提交了 "{sub.exercise.title}"',
            'detail': f'得分: {int(sub.score)}% - {"通过" if sub.status == "passed" else "未通过"}',
            'time': sub.submitted_at.strftime('%Y-%m-%d %H:%M')
        })
    for attempt in exam_attempts[:3]:
        recent_activities.append({
            'icon': '&#127942;',
            'type': 'warning',
            'title': f'参加了 "{attempt.exam.title}" 考试',
            'detail': f'得分: {int(attempt.score)}% - {"通过" if attempt.passed else "未通过"}',
            'time': attempt.started_at.strftime('%Y-%m-%d %H:%M')
        })
    recent_activities.sort(key=lambda x: x['time'], reverse=True)

    return render_template('profile.html',
                         progress=progress,
                         submissions=submissions,
                         exam_attempts=exam_attempts,
                         stats=stats,
                         streak_days=streak_days,
                         skills=skills,
                         achievements=achievements,
                         unlocked_achievements=unlocked_achievements,
                         total_achievements=total_achievements,
                         heatmap_data=heatmap_data,
                         recent_activities=recent_activities,
                         total_exercises=stats.get('total_exercises', 0),
                         completed_exercises=stats.get('passed_exercises', 0),
                         avg_score=stats.get('avg_score', 0),
                         passed_exams=stats.get('passed_exams', 0),
                         total_exams=stats.get('total_exams', 0))

@app.route('/courses')
def courses():
    category = request.args.get('category', 'all')
    level = request.args.get('level', 'all')
    search = request.args.get('search', '').strip()
    
    query = Course.query.filter_by(is_published=True)
    if category != 'all':
        query = query.filter_by(category=category)
    if level != 'all':
        query = query.filter_by(level=level)
    if search:
        query = query.filter(
            db.or_(
                Course.title.like(f'%{search}%'),
                Course.description.like(f'%{search}%'),
                Course.category.like(f'%{search}%')
            )
        )
    
    all_courses = query.order_by(Course.order).all()
    
    # 获取用户进度
    user_progress = {}
    if current_user.is_authenticated:
        for course in all_courses:
            user_progress[course.id] = current_user.get_course_progress(course.id)
    
    return render_template('courses.html', courses=all_courses, 
                         current_category=category, current_level=level, 
                         search_query=search, user_progress=user_progress)

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    lessons = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order).all()
    
    # 获取用户各课时完成状态
    lesson_status = {}
    if current_user.is_authenticated:
        for lesson in lessons:
            progress = LearningProgress.query.filter_by(
                user_id=current_user.id, lesson_id=lesson.id, completed=True
            ).first()
            lesson_status[lesson.id] = progress is not None
    else:
        for lesson in lessons:
            lesson_status[lesson.id] = False
    
    course_progress = 0
    if current_user.is_authenticated:
        course_progress = current_user.get_course_progress(course_id)
    
    course_enhancement = get_course_enhancement(course_id)
    learning_tools = get_learning_tools()

    return render_template('course_detail.html', course=course, lessons=lessons,
                         lesson_status=lesson_status, course_progress=course_progress,
                         enhancement=course_enhancement, learning_tools=learning_tools)

@app.route('/lesson/<int:lesson_id>')
def lesson_detail(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if current_user.is_authenticated:
        # 记录访问
        progress = LearningProgress.query.filter_by(
            user_id=current_user.id, lesson_id=lesson_id
        ).first()
        if not progress:
            progress = LearningProgress(user_id=current_user.id, lesson_id=lesson_id, course_id=lesson.course_id)
            db.session.add(progress)
            db.session.commit()

        # 记录课程观看日志
        view_log = LessonViewLog.query.filter_by(
            user_id=current_user.id, lesson_id=lesson_id
        ).order_by(LessonViewLog.started_at.desc()).first()

        if not view_log or (view_log.ended_at and (datetime.utcnow() - view_log.ended_at).total_seconds() > 300):
            # 创建新的观看记录（如果上次观看已结束超过5分钟）
            view_log = LessonViewLog(
                user_id=current_user.id,
                lesson_id=lesson_id,
                course_id=lesson.course_id,
                started_at=datetime.utcnow()
            )
            db.session.add(view_log)
            db.session.commit()

        # 记录学习行为日志
        learning_log = LearningLog(
            user_id=current_user.id,
            log_type='lesson',
            action='开始学习课时',
            target_id=lesson_id,
            target_name=lesson.title,
            target_type='lesson',
            detail=f'用户 {current_user.username} 开始学习课时: {lesson.title}',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None
        )
        db.session.add(learning_log)
        db.session.commit()
    
    # 获取前后课时
    prev_lesson = lesson.prev_lesson
    next_lesson = lesson.next_lesson
    
    # 获取相关练习
    related_exercises = Exercise.query.filter_by(related_lesson_id=lesson_id).all()
    
    # 获取课时增强内容
    lesson_enhancement = get_lesson_enhancement(lesson_id)
    course_enhancement = get_course_enhancement(lesson.course_id)

    return render_template('lesson_detail.html', lesson=lesson,
                         prev_lesson=prev_lesson, next_lesson=next_lesson,
                         related_exercises=related_exercises,
                         enhancement=lesson_enhancement,
                         course_enhancement=course_enhancement)

@app.route('/exercises')
def exercises():
    category = request.args.get('category', 'all')
    difficulty = request.args.get('difficulty', 'all')
    
    query = Exercise.query
    if category != 'all':
        query = query.filter_by(category=category)
    if difficulty != 'all':
        query = query.filter_by(difficulty=difficulty)
    
    all_exercises = query.order_by(Exercise.order).all()
    return render_template('exercises.html', exercises=all_exercises, 
                         current_category=category, current_difficulty=difficulty)

@app.route('/exercise/<int:exercise_id>')
@login_required
def exercise_detail(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return render_template('exercise_detail.html', exercise=exercise)

import ast
import re

def validate_code_safety(code):
    """使用AST分析进行代码安全验证"""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f'语法错误: {e}'
    
    # 危险节点类型
    dangerous_nodes = (
        ast.Import, ast.ImportFrom, ast.Call, ast.With,
        ast.Try, ast.ExceptHandler, ast.ClassDef,
        ast.AsyncFor, ast.AsyncFunctionDef, ast.Await
    )
    
    # 危险函数名
    dangerous_names = {
        'open', 'eval', 'exec', 'compile', '__import__',
        'input', 'raw_input', 'exit', 'quit',
        'os', 'sys', 'subprocess', 'socket', 'urllib',
        'requests', 'ftplib', 'telnetlib', 'pickle',
        'marshal', 'ctypes', 'platform', 'shutil',
        'pathlib', 'fileinput', 'tempfile', 'glob',
        'importlib', 'imp', 'builtins', '__builtins__'
    }
    
    for node in ast.walk(tree):
        # 检查导入语句
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in dangerous_names:
                    return False, f'不允许导入模块: {alias.name}'
        
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in dangerous_names:
                return False, f'不允许从模块导入: {node.module}'
        
        # 检查危险函数调用
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in dangerous_names:
                    return False, f'不允许使用函数: {node.func.id}'
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr in dangerous_names:
                    return False, f'不允许调用方法: {node.func.attr}'
    
    # 正则检查字符串拼接绕过
    patterns = [
        r'__\s*import\s*__',
        r'eval\s*\(',
        r'exec\s*\(',
        r'open\s*\(',
        r'subprocess',
        r'os\s*\.\s*system',
        r'sys\s*\.\s*modules',
    ]
    for pattern in patterns:
        if re.search(pattern, code, re.IGNORECASE):
            return False, '检测到可疑代码模式'
    
    return True, None


@app.route('/run_code', methods=['POST'])
@login_required
def run_code():
    code = request.json.get('code', '')
    
    if not code.strip():
        return jsonify({'success': False, 'error': '代码不能为空'})
    
    # 代码长度限制
    if len(code) > 5000:
        return jsonify({'success': False, 'error': '代码长度超过限制（最大5000字符）'})
    
    # AST安全分析
    is_safe, error_msg = validate_code_safety(code)
    if not is_safe:
        return jsonify({'success': False, 'error': f'代码安全检查失败: {error_msg}'})
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write('# -*- coding: utf-8 -*-\n')
            f.write(code)
            f.flush()
            temp_file = f.name
        
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        os.unlink(temp_file)
        
        return jsonify({
            'success': True,
            'output': result.stdout,
            'error': result.stderr,
            'return_code': result.returncode
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': '代码执行超时'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'执行错误: {str(e)}'})

@app.route('/submit_exercise/<int:exercise_id>', methods=['POST'])
@login_required
def submit_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    code = request.json.get('code', '')
    
    submission = Submission(
        user_id=current_user.id,
        exercise_id=exercise_id,
        code=code,
        status='running'
    )
    db.session.add(submission)
    db.session.commit()
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write('# -*- coding: utf-8 -*-\n')
            f.write(code)
            f.flush()
            temp_file = f.name
        
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        os.unlink(temp_file)
        
        submission.output = result.stdout
        score = 0
        status = 'failed'
        
        if exercise.expected_output and result.stdout.strip() == exercise.expected_output.strip():
            score = 100.0
            status = 'passed'
        elif not result.stderr:
            score = 50.0
            status = 'partial'
        
        submission.score = score
        submission.status = status
        db.session.commit()

        # 记录练习尝试日志
        attempt_log = ExerciseAttemptLog(
            user_id=current_user.id,
            exercise_id=exercise_id,
            code_submitted=code,
            output_result=result.stdout,
            score=score,
            status=status,
            submitted_at=datetime.utcnow()
        )
        db.session.add(attempt_log)

        # 记录学习行为日志
        learning_log = LearningLog(
            user_id=current_user.id,
            log_type='exercise',
            action='完成练习',
            target_id=exercise_id,
            target_name=exercise.title,
            target_type='exercise',
            detail=f'用户 {current_user.username} 完成练习 "{exercise.title}"，得分: {score}%',
            score=score,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None
        )
        db.session.add(learning_log)
        db.session.commit()

        return jsonify({
            'success': True,
            'score': score,
            'status': status,
            'output': result.stdout,
            'error': result.stderr
        })
        
    except subprocess.TimeoutExpired:
        submission.status = 'timeout'
        submission.output = '执行超时'
        db.session.commit()
        return jsonify({'success': False, 'error': '代码执行超时'})
    except Exception as e:
        submission.status = 'error'
        submission.output = str(e)
        db.session.commit()
        return jsonify({'success': False, 'error': f'执行错误: {str(e)}'})

@app.route('/exams')
def exams():
    all_exams = Exam.query.order_by(Exam.created_at.desc()).all()
    return render_template('exams.html', exams=all_exams)

@app.route('/exam/<int:exam_id>')
@login_required
def exam_detail(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    
    existing = ExamAttempt.query.filter_by(
        user_id=current_user.id, exam_id=exam_id, status='in_progress'
    ).first()
    if existing:
        return redirect(url_for('take_exam', exam_id=exam_id))
    
    return redirect(url_for('take_exam', exam_id=exam_id))

@app.route('/exam/<int:exam_id>/take')
@login_required
def take_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    
    attempt = ExamAttempt.query.filter_by(
        user_id=current_user.id, exam_id=exam_id, status='in_progress'
    ).first()
    
    if not attempt:
        attempt = ExamAttempt(
            user_id=current_user.id,
            exam_id=exam_id,
            answers='{}',
            status='in_progress',
            started_at=datetime.utcnow()
        )
        db.session.add(attempt)
        db.session.commit()
    
    questions = ExamQuestion.query.filter_by(exam_id=exam_id).order_by(ExamQuestion.order).all()
    
    question_types = {}
    for q in questions:
        qtype = q.question_type
        if qtype not in question_types:
            question_types[qtype] = []
        question_types[qtype].append({
            'id': q.id, 'text': q.question_text, 'type': qtype,
            'options': q.options, 'answer': q.correct_answer,
            'points': q.points, 'order': q.order
        })
    
    return render_template('take_exam.html',
        exam=exam, questions=questions, attempt=attempt,
        question_types=question_types,
        total_questions=len(questions)
    )

@app.route('/exam/auto_save', methods=['POST'])
@login_required
def exam_auto_save():
    data = request.get_json()
    exam_id = data.get('exam_id')
    answers = data.get('answers', {})
    remaining = data.get('remaining_seconds')
    
    attempt = ExamAttempt.query.filter_by(
        user_id=current_user.id, exam_id=exam_id, status='in_progress'
    ).first()
    
    if attempt:
        attempt.answers = json.dumps(answers)
        attempt.auto_saved_at = datetime.utcnow()
        attempt.remaining_seconds = remaining
        db.session.commit()
        return jsonify({'success': True, 'saved_at': attempt.auto_saved_at.isoformat()})
    
    return jsonify({'success': False, 'error': 'No active exam session'}), 404

@app.route('/exam/<int:exam_id>/submit', methods=['POST'])
@login_required
def submit_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    data = request.get_json()
    user_answers = data.get('answers', {})
    remaining = data.get('remaining_seconds', 0)
    
    questions = ExamQuestion.query.filter_by(exam_id=exam_id).order_by(ExamQuestion.order).all()
    
    total_score = 0
    max_score = 0
    correct_count = 0
    results = {}
    
    for q in questions:
        max_score += q.points
        user_ans = str(user_answers.get(str(q.id), '')).strip()
        correct_ans = str(q.correct_answer).strip()
        
        is_correct = False
        qtype = q.question_type
        
        if qtype in ('single_choice', 'true_false', 'code_reading'):
            is_correct = user_ans.upper() == correct_ans.upper()
        elif qtype == 'fill_blank':
            is_correct = user_ans.lower() == correct_ans.lower()
        elif qtype == 'short_answer':
            is_correct = len(user_ans) >= 10
        elif qtype == 'programming':
            is_correct = False
        
        if is_correct:
            total_score += q.points
            correct_count += 1
        
        results[str(q.id)] = {'correct': is_correct, 'user_answer': user_ans, 'correct_answer': correct_ans}
    
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    passed = percentage >= exam.passing_score
    
    attempt = ExamAttempt.query.filter_by(
        user_id=current_user.id, exam_id=exam_id, status='in_progress'
    ).first()
    
    if attempt:
        attempt.answers = json.dumps({'answers': user_answers, 'results': results})
        attempt.score = percentage
        attempt.passed = passed
        attempt.status = 'completed'
        attempt.completed_at = datetime.utcnow()
        attempt.remaining_seconds = remaining
    else:
        attempt = ExamAttempt(
            user_id=current_user.id, exam_id=exam_id,
            answers=json.dumps({'answers': user_answers, 'results': results}),
            score=percentage, passed=passed, status='completed',
            started_at=datetime.utcnow(), completed_at=datetime.utcnow(),
            remaining_seconds=remaining
        )
        db.session.add(attempt)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'attempt_id': attempt.id,
        'score': round(percentage, 1),
        'passed': passed,
        'total_points': round(total_score, 1),
        'max_points': round(max_score, 1),
        'correct_count': correct_count,
        'total_questions': len(questions)
    })

@app.route('/exam/<int:exam_id>/timeout', methods=['POST'])
@login_required
def exam_timeout(exam_id):
    data = request.get_json()
    user_answers = data.get('answers', {})
    
    exam = Exam.query.get_or_404(exam_id)
    questions = ExamQuestion.query.filter_by(exam_id=exam_id).order_by(ExamQuestion.order).all()
    
    total_score = 0
    max_score = 0
    correct_count = 0
    results = {}
    
    for q in questions:
        max_score += q.points
        user_ans = str(user_answers.get(str(q.id), '')).strip()
        correct_ans = str(q.correct_answer).strip()
        
        is_correct = False
        if q.question_type in ('single_choice', 'true_false', 'code_reading'):
            is_correct = user_ans.upper() == correct_ans.upper()
        elif q.question_type == 'fill_blank':
            is_correct = user_ans.lower() == correct_ans.lower()
        elif q.question_type == 'short_answer':
            is_correct = len(user_ans) >= 10
        
        if is_correct:
            total_score += q.points
            correct_count += 1
        results[str(q.id)] = {'correct': is_correct, 'user_answer': user_ans}
    
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    passed = percentage >= exam.passing_score
    
    attempt = ExamAttempt.query.filter_by(
        user_id=current_user.id, exam_id=exam_id, status='in_progress'
    ).first()
    
    if attempt:
        attempt.answers = json.dumps({'answers': user_answers, 'results': results})
        attempt.score = percentage
        attempt.passed = passed
        attempt.status = 'timeout'
        attempt.completed_at = datetime.utcnow()
        attempt.remaining_seconds = 0
    else:
        attempt = ExamAttempt(
            user_id=current_user.id, exam_id=exam_id,
            answers=json.dumps({'answers': user_answers, 'results': results}),
            score=percentage, passed=passed, status='timeout',
            started_at=datetime.utcnow(), completed_at=datetime.utcnow(),
            remaining_seconds=0
        )
        db.session.add(attempt)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'attempt_id': attempt.id,
        'score': round(percentage, 1),
        'passed': passed,
        'message': '考试时间已到，系统已自动提交'
    })

@app.route('/exam_result/<int:attempt_id>')
@login_required
def exam_result(attempt_id):
    attempt = ExamAttempt.query.get_or_404(attempt_id)
    if attempt.user_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    questions = ExamQuestion.query.filter_by(exam_id=attempt.exam_id).order_by(ExamQuestion.order).all()
    
    user_answers = {}
    try:
        stored = json.loads(attempt.answers) if attempt.answers else {}
        if 'answers' in stored:
            user_answers = stored['answers']
        else:
            user_answers = stored
    except:
        user_answers = {}

    type_labels = {
        'single_choice': '\u5355\u9009\u9898',
        'true_false': '\u5224\u65ad\u9898',
        'fill_blank': '\u586b\u7a7a\u9898',
        'code_reading': '\u7a0b\u5e8f\u9605\u8bfb\u9898',
        'short_answer': '\u7b80\u7b54\u9898',
        'programming': '\u7f16\u7a0b\u9898'
    }

    type_scores = {}
    for q in questions:
        qtype = q.question_type
        if qtype not in type_scores:
            type_scores[qtype] = {'total': 0, 'earned': 0, 'correct': 0, 'count': 0}
        type_scores[qtype]['total'] += q.points
        type_scores[qtype]['count'] += 1
        user_ans = str(user_answers.get(str(q.id), '')).strip()
        correct_ans = q.correct_answer.strip() if q.correct_answer else ''

        if qtype in ('single_choice', 'true_false', 'code_reading'):
            is_correct = user_ans.upper() == correct_ans.upper()
        elif qtype == 'fill_blank':
            is_correct = user_ans.lower() == correct_ans.lower()
        elif qtype == 'short_answer':
            is_correct = len(user_ans) >= 10
        else:
            is_correct = False

        if is_correct:
            type_scores[qtype]['earned'] += q.points
            type_scores[qtype]['correct'] += 1

    question_details = []
    for q in questions:
        user_ans = str(user_answers.get(str(q.id), '')).strip()
        correct_ans = q.correct_answer.strip() if q.correct_answer else ''
        qtype = q.question_type

        if qtype in ('single_choice', 'true_false', 'code_reading'):
            correct_flag = user_ans.upper() == correct_ans.upper()
        elif qtype == 'fill_blank':
            correct_flag = user_ans.lower() == correct_ans.lower()
        elif qtype == 'short_answer':
            correct_flag = len(user_ans) >= 10
        else:
            correct_flag = False

        question_details.append({
            'id': q.id,
            'order': q.order,
            'text': q.question_text[:120],
            'question_type': qtype,
            'type_label': type_labels.get(qtype, qtype),
            'points': q.points,
            'user_answer': user_ans[:200],
            'correct_answer': correct_ans,
            'is_correct': correct_flag
        })

    total_points = sum(v['total'] for v in type_scores.values())
    earned_points = sum(v['earned'] for v in type_scores.values())
    score_pct = round(earned_points / total_points * 100, 1) if total_points > 0 else 0.0

    return render_template('exam_result.html',
        attempt=attempt, questions=questions, type_scores=type_scores,
        type_labels=type_labels, question_details=question_details,
        total_points=total_points, earned_points=earned_points,
        score_pct=score_pct)

@app.route('/progress')
@login_required
def progress():
    progress_records = LearningProgress.query.filter_by(user_id=current_user.id).all()
    stats = get_user_stats(current_user.id)
    
    course_progress = {}
    for record in progress_records:
        if record.course_id:
            if record.course_id not in course_progress:
                course_progress[record.course_id] = {'completed': 0, 'total': 0}
            course_progress[record.course_id]['total'] += 1
            if record.completed:
                course_progress[record.course_id]['completed'] += 1
    
    return render_template('progress.html', progress_records=progress_records, 
                         course_progress=course_progress, stats=stats)

@app.route('/community')
def community():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template('community.html', posts=posts)

@app.route('/community/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('标题和内容不能为空', 'danger')
            return render_template('new_post.html')
        
        post = ForumPost(title=title, content=content, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('community'))
    
    return render_template('new_post.html')

@app.route('/community/post/<int:post_id>')
def view_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)

@app.route('/community/post/<int:post_id>/reply', methods=['POST'])
@login_required
def reply_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    content = request.form.get('content')
    
    if not content:
        flash('回复内容不能为空', 'danger')
        return redirect(url_for('view_post', post_id=post_id))
    
    reply = ForumReply(post_id=post_id, author_id=current_user.id, content=content)
    db.session.add(reply)
    db.session.commit()
    
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/resources')
def resources():
    category = request.args.get('category', 'all')
    query = Resource.query
    if category != 'all':
        query = query.filter_by(category=category)
    
    all_resources = query.order_by(Resource.uploaded_at.desc()).all()
    return render_template('resources.html', resources=all_resources, current_category=category)

@app.route('/report')
@login_required
def report():
    submissions = Submission.query.filter_by(user_id=current_user.id).all()
    exam_attempts = ExamAttempt.query.filter_by(user_id=current_user.id).all()
    progress = LearningProgress.query.filter_by(user_id=current_user.id).all()
    stats = get_user_stats(current_user.id)
    
    total_submissions = len(submissions)
    passed_submissions = len([s for s in submissions if s.status == 'passed'])
    avg_score = sum([s.score for s in submissions]) / total_submissions if total_submissions > 0 else 0
    
    exam_scores = [e.score for e in exam_attempts]
    avg_exam_score = sum(exam_scores) / len(exam_scores) if exam_scores else 0
    
    completed_lessons = len([p for p in progress if p.completed])
    total_lessons = len(progress) if progress else 1
    completion_rate = (completed_lessons / total_lessons * 100)
    
    category_scores = {}
    for sub in submissions:
        exercise = db.session.get(Exercise, sub.exercise_id)
        if exercise:
            if exercise.category not in category_scores:
                category_scores[exercise.category] = []
            category_scores[exercise.category].append(sub.score)
    
    for category in category_scores:
        category_scores[category] = sum(category_scores[category]) / len(category_scores[category])
    
    return render_template('report.html',
                         total_submissions=total_submissions,
                         passed_submissions=passed_submissions,
                         avg_score=avg_score,
                         avg_exam_score=avg_exam_score,
                         completion_rate=completion_rate,
                         category_scores=category_scores,
                         stats=stats)

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)

    # 基础统计
    user_count = User.query.count()
    course_count = Course.query.count()
    exercise_count = Exercise.query.count()
    submission_count = Submission.query.count()
    exam_count = Exam.query.count()
    exam_attempt_count = ExamAttempt.query.count()
    total_lessons = Lesson.query.count()

    # 今日新增用户
    new_users_today = User.query.filter(
        db.func.date(User.created_at) == today
    ).count()

    # 近7日提交趋势
    chart_labels = []
    submission_trend = []
    dau_trend = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        chart_labels.append(date.strftime('%m-%d'))
        sub_count = Submission.query.filter(
            db.func.date(Submission.submitted_at) == date
        ).count()
        submission_trend.append(sub_count)
        # 活跃用户 = 当天有提交的用户数
        active_users = db.session.query(db.func.count(db.distinct(Submission.user_id))).filter(
            db.func.date(Submission.submitted_at) == date
        ).scalar()
        dau_trend.append(active_users or 0)

    # 用户活跃度分布
    active_threshold = today - timedelta(days=7)
    active_users = User.query.filter(
        User.submissions.any(Submission.submitted_at >= active_threshold)
    ).count()
    inactive_users = user_count - active_users
    activity_distribution = [active_users, max(0, inactive_users // 2), max(0, inactive_users - inactive_users // 2)]

    # 课程进度统计
    course_progress = []
    for course in Course.query.all():
        total_users = User.query.count()
        if total_users == 0:
            continue
        # 计算完成课程所有课时的用户数
        lessons = Lesson.query.filter_by(course_id=course.id).all()
        lesson_ids = [l.id for l in lessons]
        completed_users = 0
        for user in User.query.all():
            completed = LearningProgress.query.filter(
                LearningProgress.user_id == user.id,
                LearningProgress.lesson_id.in_(lesson_ids),
                LearningProgress.completed == True
            ).count()
            if completed >= len(lesson_ids) and len(lesson_ids) > 0:
                completed_users += 1
        progress = int((completed_users / max(total_users, 1)) * 100)
        course_progress.append({
            'title': course.title,
            'progress': progress,
            'completed_users': completed_users,
            'total_users': total_users
        })

    # 用户列表（带详细统计）
    users = []
    for user in User.query.order_by(User.created_at.desc()).all():
        total_lessons_all = Lesson.query.count()
        completed_lessons = LearningProgress.query.filter_by(
            user_id=user.id, completed=True
        ).count()
        lesson_progress = int((completed_lessons / max(total_lessons_all, 1)) * 100)
        submission_count_user = Submission.query.filter_by(user_id=user.id).count()
        passed_exams = ExamAttempt.query.filter_by(user_id=user.id, passed=True).count()
        users.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at,
            'lesson_progress': lesson_progress,
            'submission_count': submission_count_user,
            'passed_exams': passed_exams
        })

    # 课程详细数据
    courses_detail = []
    for course in Course.query.all():
        lessons = Lesson.query.filter_by(course_id=course.id).all()
        lesson_ids = [l.id for l in lessons]
        # 学习人数 = 有该课程学习进度的用户数
        learner_count = db.session.query(db.func.count(db.distinct(LearningProgress.user_id))).filter(
            LearningProgress.course_id == course.id
        ).scalar() or 0
        # 完成率
        total_progress = db.session.query(db.func.avg(LearningProgress.progress_percentage)).filter(
            LearningProgress.course_id == course.id
        ).scalar() or 0
        courses_detail.append({
            'id': course.id,
            'title': course.title,
            'category': course.category,
            'level': course.level,
            'difficulty_label': course.difficulty_label,
            'lesson_count': len(lessons),
            'learner_count': learner_count,
            'completion_rate': int(total_progress),
            'is_published': course.is_published
        })

    # 最近提交记录
    recent_submissions = []
    for sub in Submission.query.order_by(Submission.submitted_at.desc()).limit(50).all():
        recent_submissions.append({
            'id': sub.id,
            'username': sub.user.username if sub.user else '未知',
            'exercise_title': sub.exercise.title if sub.exercise else '未知',
            'score': int(sub.score),
            'status': sub.status,
            'submitted_at': sub.submitted_at
        })

    # 通过率分布
    passed_count = Submission.query.filter_by(status='passed').count()
    failed_count = Submission.query.filter_by(status='failed').count()
    pending_count = submission_count - passed_count - failed_count
    pass_rate_distribution = [passed_count, failed_count, max(0, pending_count)]

    # 考试成绩分布
    exam_score_distribution = [0, 0, 0, 0, 0]
    for attempt in ExamAttempt.query.all():
        score = attempt.score
        if score < 60:
            exam_score_distribution[0] += 1
        elif score < 70:
            exam_score_distribution[1] += 1
        elif score < 80:
            exam_score_distribution[2] += 1
        elif score < 90:
            exam_score_distribution[3] += 1
        else:
            exam_score_distribution[4] += 1

    # 系统日志（模拟数据）
    system_logs = []
    log_actions = [
        ('login', '用户登录', '成功登录系统'),
        ('submit', '提交练习', '完成了练习提交'),
        ('course', '课程学习', '开始学习新课程'),
        ('exam', '参加考试', '完成了一次考试')
    ]
    import random
    for i in range(20):
        log_type, action, detail = random.choice(log_actions)
        log_time = datetime.utcnow() - timedelta(hours=random.randint(1, 48))
        system_logs.append({
            'timestamp': log_time.strftime('%Y-%m-%d %H:%M:%S'),
            'username': random.choice(['张三', '李四', '王五', 'admin']),
            'action': action,
            'detail': detail,
            'type': log_type
        })

    return render_template('admin.html',
                         user_count=user_count,
                         course_count=course_count,
                         exercise_count=exercise_count,
                         submission_count=submission_count,
                         exam_count=exam_count,
                         exam_attempt_count=exam_attempt_count,
                         total_lessons=total_lessons,
                         new_users_today=new_users_today,
                         chart_labels=chart_labels,
                         submission_trend=submission_trend,
                         dau_trend=dau_trend,
                         activity_distribution=activity_distribution,
                         course_progress=course_progress,
                         users=users,
                         courses_detail=courses_detail,
                         recent_submissions=recent_submissions,
                         pass_rate_distribution=pass_rate_distribution,
                         exam_score_distribution=exam_score_distribution,
                         system_logs=system_logs)

@app.route('/admin/course/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_course():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        level = request.form.get('level')
        content = request.form.get('content')
        
        existing = Course.query.filter_by(title=title).first()
        if existing:
            flash(f'课程"{title}"已存在，请勿重复创建', 'warning')
            return render_template('new_course.html')
        
        course = Course(title=title, description=description, category=category, level=level, content=content)
        db.session.add(course)
        db.session.commit()
        
        flash('课程创建成功', 'success')
        return redirect(url_for('course_detail', course_id=course.id))
    
    return render_template('new_course.html')

@app.route('/admin/exercise/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_exercise():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        starter_code = request.form.get('starter_code', '')
        expected_output = request.form.get('expected_output', '')
        difficulty = request.form.get('difficulty')
        category = request.form.get('category')
        hints = request.form.get('hints', '')
        
        exercise = Exercise(title=title, description=description, starter_code=starter_code,
                          expected_output=expected_output, difficulty=difficulty, 
                          category=category, hints=hints)
        db.session.add(exercise)
        db.session.commit()
        
        flash('练习创建成功', 'success')
        return redirect(url_for('exercises'))
    
    return render_template('new_exercise.html')

@app.route('/lesson/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    progress = LearningProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
    if progress:
        progress.completed = True
        progress.progress_percentage = 100.0
        db.session.commit()

        # 更新课时观看日志
        view_log = LessonViewLog.query.filter_by(
            user_id=current_user.id, lesson_id=lesson_id
        ).order_by(LessonViewLog.started_at.desc()).first()
        if view_log:
            view_log.is_completed = True
            view_log.completion_percentage = 100.0
            if not view_log.ended_at:
                view_log.ended_at = datetime.utcnow()
                if view_log.started_at:
                    view_log.watch_duration = int((view_log.ended_at - view_log.started_at).total_seconds())
            db.session.commit()

        # 记录完成日志
        lesson = Lesson.query.get(lesson_id)
        learning_log = LearningLog(
            user_id=current_user.id,
            log_type='lesson',
            action='完成课时',
            target_id=lesson_id,
            target_name=lesson.title if lesson else 'Unknown',
            target_type='lesson',
            detail=f'用户 {current_user.username} 完成课时: {lesson.title if lesson else "Unknown"}',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None
        )
        db.session.add(learning_log)
        db.session.commit()

        return jsonify({'success': True})
    return jsonify({'success': False})


# ===================== 学习行为追踪管理后台 =====================

@app.route('/admin/learning_logs')
@login_required
@admin_required
def admin_learning_logs():
    """学习行为日志管理"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    log_type = request.args.get('log_type', '')
    user_id = request.args.get('user_id', type=int)
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    query = LearningLog.query

    if log_type:
        query = query.filter_by(log_type=log_type)
    if user_id:
        query = query.filter_by(user_id=user_id)
    if date_from:
        query = query.filter(LearningLog.created_at >= date_from)
    if date_to:
        query = query.filter(LearningLog.created_at <= date_to + ' 23:59:59')

    logs = query.order_by(LearningLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    users = User.query.all()

    return render_template('admin_learning_logs.html',
                         logs=logs,
                         users=users,
                         log_type=log_type,
                         user_id=user_id,
                         date_from=date_from,
                         date_to=date_to)


@app.route('/admin/lesson_views')
@login_required
@admin_required
def admin_lesson_views():
    """课程观看记录管理"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    user_id = request.args.get('user_id', type=int)
    course_id = request.args.get('course_id', type=int)

    query = LessonViewLog.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if course_id:
        query = query.filter_by(course_id=course_id)

    views = query.order_by(LessonViewLog.started_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    users = User.query.all()
    courses = Course.query.all()

    return render_template('admin_lesson_views.html',
                         views=views,
                         users=users,
                         courses=courses,
                         user_id=user_id,
                         course_id=course_id)


@app.route('/admin/exercise_attempts')
@login_required
@admin_required
def admin_exercise_attempts():
    """练习尝试记录管理"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    user_id = request.args.get('user_id', type=int)
    exercise_id = request.args.get('exercise_id', type=int)
    status = request.args.get('status', '')

    query = ExerciseAttemptLog.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if exercise_id:
        query = query.filter_by(exercise_id=exercise_id)
    if status:
        query = query.filter_by(status=status)

    attempts = query.order_by(ExerciseAttemptLog.submitted_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    users = User.query.all()
    exercises = Exercise.query.all()

    return render_template('admin_exercise_attempts.html',
                         attempts=attempts,
                         users=users,
                         exercises=exercises,
                         user_id=user_id,
                         exercise_id=exercise_id,
                         status=status)


@app.route('/admin/exam_participations')
@login_required
@admin_required
def admin_exam_participations():
    """考试参与记录管理"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    user_id = request.args.get('user_id', type=int)
    exam_id = request.args.get('exam_id', type=int)
    passed = request.args.get('passed', '')

    query = ExamParticipationLog.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if exam_id:
        query = query.filter_by(exam_id=exam_id)
    if passed:
        query = query.filter_by(passed=(passed == 'true'))

    participations = query.order_by(ExamParticipationLog.started_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    users = User.query.all()
    exams = Exam.query.all()

    return render_template('admin_exam_participations.html',
                         participations=participations,
                         users=users,
                         exams=exams,
                         user_id=user_id,
                         exam_id=exam_id,
                         passed=passed)


@app.route('/admin/export_logs')
@login_required
@admin_required
def export_learning_logs():
    """导出学习行为日志为CSV"""
    import csv
    import io
    from flask import Response

    log_type = request.args.get('log_type', '')
    user_id = request.args.get('user_id', type=int)
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    query = LearningLog.query

    if log_type:
        query = query.filter_by(log_type=log_type)
    if user_id:
        query = query.filter_by(user_id=user_id)
    if date_from:
        query = query.filter(LearningLog.created_at >= date_from)
    if date_to:
        query = query.filter(LearningLog.created_at <= date_to + ' 23:59:59')

    logs = query.order_by(LearningLog.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', '用户ID', '用户名', '日志类型', '操作', '目标ID', '目标名称',
                     '目标类型', '得分', '时长(秒)', 'IP地址', '创建时间', '详情'])

    for log in logs:
        writer.writerow([
            log.id,
            log.user_id,
            log.user.username if log.user else '',
            log.log_type,
            log.action,
            log.target_id,
            log.target_name,
            log.target_type,
            log.score,
            log.duration_seconds,
            log.ip_address,
            log.formatted_time,
            log.detail
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=learning_logs.csv'}
    )


@app.route('/admin/export_lesson_views')
@login_required
@admin_required
def export_lesson_views():
    """导出课程观看记录为CSV"""
    import csv
    import io
    from flask import Response

    user_id = request.args.get('user_id', type=int)
    course_id = request.args.get('course_id', type=int)

    query = LessonViewLog.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if course_id:
        query = query.filter_by(course_id=course_id)

    views = query.order_by(LessonViewLog.started_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', '用户ID', '用户名', '课程', '课时', '观看时长(秒)',
                     '完成百分比', '开始时间', '结束时间', '是否完成'])

    for view in views:
        writer.writerow([
            view.id,
            view.user_id,
            view.user.username if view.user else '',
            view.course.title if view.course else '',
            view.lesson.title if view.lesson else '',
            view.watch_duration,
            view.completion_percentage,
            view.started_at.strftime('%Y-%m-%d %H:%M:%S') if view.started_at else '',
            view.ended_at.strftime('%Y-%m-%d %H:%M:%S') if view.ended_at else '',
            '是' if view.is_completed else '否'
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=lesson_views.csv'}
    )


@app.route('/admin/export_exercise_attempts')
@login_required
@admin_required
def export_exercise_attempts():
    """导出练习尝试记录为CSV"""
    import csv
    import io
    from flask import Response

    user_id = request.args.get('user_id', type=int)
    exercise_id = request.args.get('exercise_id', type=int)

    query = ExerciseAttemptLog.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if exercise_id:
        query = query.filter_by(exercise_id=exercise_id)

    attempts = query.order_by(ExerciseAttemptLog.submitted_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', '用户ID', '用户名', '练习', '得分', '状态',
                     '尝试次数', '耗时(秒)', '提交时间'])

    for attempt in attempts:
        writer.writerow([
            attempt.id,
            attempt.user_id,
            attempt.user.username if attempt.user else '',
            attempt.exercise.title if attempt.exercise else '',
            attempt.score,
            attempt.status,
            attempt.attempt_count,
            attempt.time_spent_seconds,
            attempt.submitted_at.strftime('%Y-%m-%d %H:%M:%S') if attempt.submitted_at else ''
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=exercise_attempts.csv'}
    )


@app.route('/admin/export_exam_participations')
@login_required
@admin_required
def export_exam_participations():
    """导出考试参与记录为CSV"""
    import csv
    import io
    from flask import Response

    user_id = request.args.get('user_id', type=int)
    exam_id = request.args.get('exam_id', type=int)

    query = ExamParticipationLog.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if exam_id:
        query = query.filter_by(exam_id=exam_id)

    participations = query.order_by(ExamParticipationLog.started_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', '用户ID', '用户名', '考试', '得分', '是否通过',
                     '正确数', '总题数', '开始时间', '完成时间', '耗时(秒)'])

    for p in participations:
        writer.writerow([
            p.id,
            p.user_id,
            p.user.username if p.user else '',
            p.exam.title if p.exam else '',
            p.score,
            '是' if p.passed else '否',
            p.correct_count,
            p.total_questions,
            p.started_at.strftime('%Y-%m-%d %H:%M:%S') if p.started_at else '',
            p.completed_at.strftime('%Y-%m-%d %H:%M:%S') if p.completed_at else '',
            p.duration_seconds
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=exam_participations.csv'}
    )

@app.route('/robots.txt')
def robots():
    """搜索引擎爬虫规则"""
    return """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /login
Disallow: /register
Disallow: /profile
Disallow: /progress
Disallow: /report

Sitemap: /sitemap.xml
""", 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/sitemap.xml')
def sitemap():
    """动态生成XML站点地图"""
    from xml.etree.ElementTree import Element, SubElement, tostring
    from datetime import datetime

    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    def add_url(loc, priority='0.5', changefreq='weekly'):
        url = SubElement(urlset, 'url')
        SubElement(url, 'loc').text = loc
        SubElement(url, 'lastmod').text = datetime.utcnow().strftime('%Y-%m-%d')
        SubElement(url, 'changefreq').text = changefreq
        SubElement(url, 'priority').text = priority

    base = request.url_root.rstrip('/')

    # 核心页面
    add_url(f'{base}/', priority='1.0', changefreq='daily')
    add_url(f'{base}/courses', priority='0.9', changefreq='weekly')
    add_url(f'{base}/exercises', priority='0.8', changefreq='weekly')
    add_url(f'{base}/exams', priority='0.8', changefreq='weekly')
    add_url(f'{base}/community', priority='0.6', changefreq='daily')
    add_url(f'{base}/resources', priority='0.6', changefreq='weekly')

    # 课程页面
    for course in Course.query.filter_by(is_published=True).all():
        add_url(f'{base}/course/{course.id}', priority='0.7', changefreq='monthly')
        for lesson in course.lessons:
            add_url(f'{base}/lesson/{lesson.id}', priority='0.6', changefreq='monthly')

    # 练习页面
    for exercise in Exercise.query.all():
        add_url(f'{base}/exercise/{exercise.id}', priority='0.5', changefreq='monthly')

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(urlset, encoding='unicode')
    return xml, 200, {'Content-Type': 'application/xml; charset=utf-8'}

# ===================== 初始化数据 =====================

def init_data():
    """初始化课程、课时、练习和考试数据"""
    if Course.query.first():
        return
    
    # 从course_data模块导入数据
    # 创建课程
    courses = []
    for c_data in COURSES:
        course = Course(**c_data)
        db.session.add(course)
        courses.append(course)
    db.session.commit()
    
    # 创建课时
    for l_data in LESSONS:
        lesson = Lesson(
            title=l_data['title'],
            course_id=courses[l_data['course'] - 1].id,
            order=l_data['order'],
            estimated_minutes=l_data['minutes'],
            content=l_data['content'],
            key_points=l_data['key_points'],
            code_examples=l_data['code']
        )
        db.session.add(lesson)
    db.session.commit()
    
    # 创建练习
    for e_data in EXERCISES:
        # 找到对应的课时ID
        lesson = Lesson.query.filter_by(
            course_id=courses[e_data['course'] - 1].id,
            order=e_data['lesson']
        ).first()
        exercise = Exercise(
            title=e_data['title'],
            description=e_data['desc'],
            starter_code=e_data['starter'],
            expected_output=e_data['expected'],
            difficulty=e_data['diff'],
            category=e_data['cat'],
            order=1,
            related_lesson_id=lesson.id if lesson else None,
            hints=e_data['hints']
        )
        db.session.add(exercise)
    db.session.commit()
    
    # 创建考试
    exams = []
    for exam_data in EXAMS:
        exam = Exam(
            title=exam_data['title'],
            description=exam_data['desc'],
            duration_minutes=exam_data['duration'],
            passing_score=exam_data['passing'],
            level=exam_data['level']
        )
        db.session.add(exam)
        exams.append(exam)
    db.session.commit()
    
    # 创建考试题目
    for q_data in EXAM_QUESTIONS:
        question = ExamQuestion(
            exam_id=exams[q_data['exam'] - 1].id,
            question_text=q_data['text'],
            question_type=q_data['type'],
            options=q_data['options'],
            correct_answer=q_data['answer'],
            points=q_data['points'],
            order=q_data['order']
        )
        db.session.add(question)
    db.session.commit()
    
    # 创建考试与课程的关联记录（用于知识点分析）
    # 注：Exam模型目前无course_id字段，此关联通过考试描述中的course_id逻辑维护
    
    # 创建管理员（如果不存在）
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@platform.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

with app.app_context():
    db.create_all()
    init_data()

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
