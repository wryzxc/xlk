"""Initialize database with all tables and seed data"""
from app import app, db, User, Course, Lesson, Exercise, Exam, ExamQuestion, Resource
from werkzeug.security import generate_password_hash
from datetime import datetime

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created")

    # Create admin user (if not exists)
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created")

    # Create test user (if not exists)
    if not User.query.filter_by(username='testuser').first():
        test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('test123'),
            role='student',
            created_at=datetime.utcnow()
        )
        db.session.add(test_user)
        db.session.commit()
        print("Test user created")

    # Import and create course data
    from course_data import COURSES, LESSONS, EXERCISES, EXAMS, EXAM_QUESTIONS

    # Create courses
    course_map = {}
    for i, c in enumerate(COURSES, 1):
        course = Course(
            title=c['title'],
            description=c['description'],
            category=c['category'],
            level=c['level'],
            content=c.get('content', ''),
            order=c.get('order', 0),
            is_published=c.get('is_published', True)
        )
        db.session.add(course)
        db.session.flush()
        course_map[i] = course.id

    db.session.commit()
    print(f"Created {len(course_map)} courses")

    # Create lessons
    lesson_map = {}
    for i, l in enumerate(LESSONS, 1):
        lesson = Lesson(
            title=l['title'],
            content=l.get('content', ''),
            course_id=course_map.get(l.get('course', 1), 1),
            order=l.get('order', 1)
        )
        db.session.add(lesson)
        db.session.flush()
        lesson_map[i] = lesson.id

    db.session.commit()
    print(f"Created {len(lesson_map)} lessons")

    # Create exercises
    for e in EXERCISES:
        exercise = Exercise(
            title=e['title'],
            description=e.get('desc', e.get('description', '')),
            starter_code=e.get('starter', e.get('starter_code', '')),
            category=e.get('cat', e.get('category', '基础')),
            difficulty=e.get('diff', e.get('difficulty', 'easy')),
            hints=e.get('hints', '')
        )
        db.session.add(exercise)

    db.session.commit()
    print(f"Created {len(EXERCISES)} exercises")

    # Create exams
    exam_map = {}
    for i, e in enumerate(EXAMS, 1):
        exam = Exam(
            title=e['title'],
            description=e.get('desc', e.get('description', '')),
            duration_minutes=e.get('duration', 60),
            passing_score=e.get('passing', e.get('passing_score', 60.0)),
            level=e.get('level', 'beginner')
        )
        db.session.add(exam)
        db.session.flush()
        exam_map[i] = exam.id

    db.session.commit()
    print(f"Created {len(exam_map)} exams")

    # Create exam questions
    for q in EXAM_QUESTIONS:
        question = ExamQuestion(
            exam_id=exam_map.get(q.get('exam', q.get('exam_id', 1)), 1),
            question_type=q.get('type', q.get('question_type', 'multiple_choice')),
            question_text=q['text'],
            options=q.get('options', ''),
            correct_answer=q.get('answer', q.get('correct_answer', '')),
            points=q.get('points', 1),
            order=q.get('order', 1)
        )
        db.session.add(question)

    db.session.commit()
    print(f"Created {len(EXAM_QUESTIONS)} exam questions")

    print("\nDatabase initialization complete!")
