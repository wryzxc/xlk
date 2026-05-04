(function(){
  'use strict';

  var LOCALES = {
    'zh-CN': {
      '_langName': '中文',
      '_langFlag': '&#127464;&#127475;',

      // 导航栏
      'nav.home': '首页',
      'nav.courses': '课程',
      'nav.exercises': '练习',
      'nav.exams': '考试',
      'nav.community': '社区',
      'nav.resources': '资源',
      'nav.login': '登录',
      'nav.register': '免费注册',
      'nav.profile': '个人中心',
      'nav.progress': '学习进度',
      'nav.report': '学习报告',
      'nav.admin': '管理后台',
      'nav.logout': '退出登录',
      'nav.switchLang': '切换语言',

      // 跳过链接
      'skip.toMain': '跳转到主内容',

      // 品牌
      'brand.name': 'Python实训平台',

      // 页脚
      'footer.tagline': '一站式Python学习平台，提供课程学习、编码练习、考核评估等全方位服务。',
      'footer.quickLinks': '快速链接',
      'footer.courses': '课程中心',
      'footer.exercises': '练习题库',
      'footer.community': '学习社区',
      'footer.contact': '联系我们',
      'footer.copyright': 'Python编程实训平台. All rights reserved.',

      // 首页
      'home.hero.title': '掌握Python编程',
      'home.hero.subtitle': '从零基础到高级应用，系统化学习路径，交互式编码环境，助你成为专业的Python开发者',
      'home.hero.cta': '开始免费学习',
      'home.hero.explore': '浏览全部课程',
      'home.feature.courses': '系统课程',
      'home.feature.courses.desc': '从基础到高级，完整的Python知识体系，每个知识点都配有代码示例',
      'home.feature.code': '在线编程',
      'home.feature.code.desc': '交互式编码环境，实时运行代码，即时获得错误反馈和评分',
      'home.feature.assessment': '考核评估',
      'home.feature.assessment.desc': '自动评分系统，个性化学习报告，帮助你了解自己的学习进度',
      'home.path.title': '推荐学习路径',
      'home.path.step1': '基础入门',
      'home.path.step2': '数据结构',
      'home.path.step3': '面向对象',
      'home.path.step4': '高级特性',
      'home.path.step5': 'Web开发',
      'home.hotCourses': '热门课程',
      'home.viewAll': '查看全部',
      'home.stats.students': '学员',
      'home.stats.courses': '课程',
      'home.stats.exercises': '练习题',
      'home.stats.rate': '好评率',

      // ===== 课程页 =====
      'courses.title': '课程中心',
      'courses.subtitle': '从入门到高级，系统化Python学习路径',
      'courses.search': '搜索课程',
      'courses.searchPlaceholder': '输入课程名称或关键词...',
      'courses.filterCategory': '按分类筛选',
      'courses.filterLevel': '按难度筛选',
      'courses.all': '全部',
      'courses.allCategories': '全部分类',
      'courses.allLevels': '全部难度',
      'courses.count': '个课程',
      'courses.start': '开始学习',
      'courses.level.beginner': '入门',
      'courses.level.intermediate': '进阶',
      'courses.level.advanced': '高级',
      'courses.noResults': '未找到相关课程',
      'courses.noResultsHint': '请尝试其他关键词或筛选条件',
      'courses.viewAllCourses': '查看全部课程',
      'courses.students': '学员',
      'courses.lessons': '章节',

      // ===== 练习页 =====
      'exercises.title': '练习题库',
      'exercises.subtitle': '从基础语法到高级算法，多维度的Python编程练习，支持在线编码、实时运行与自动评分',
      'exercises.filterCategory': '分类',
      'exercises.filterDifficulty': '难度',
      'exercises.all': '全部分类',
      'exercises.allDifficulties': '全部难度',
      'exercises.difficulty.easy': '简单',
      'exercises.difficulty.medium': '中等',
      'exercises.difficulty.hard': '困难',
      'exercises.count': '道练习题',
      'exercises.start': '开始练习',
      'exercises.login': '登录练习',
      'exercises.noResults': '暂无匹配的练习题',
      'exercises.viewAll': '查看全部练习',

      // ===== 练习详情页 =====
      'exercise.runCode': '运行代码',
      'exercise.submit': '提交答案',
      'exercise.hint': '查看提示',
      'exercise.placeholder': '点击"运行代码"查看结果...',
      'exercise.loading': '执行中...',
      'exercise.success': '代码执行成功',
      'exercise.failed': '代码执行失败',
      'exercise.passed': '恭喜！练习通过，得分: ',
      'exercise.partial': '部分正确，得分: ',
      'exercise.notPassed': '未通过，请重试',
      'exercise.networkError': '网络错误',
      'exercise.emptyCode': '代码不能为空',
      'exercise.formError': '请修正表单中的错误',
      'exercise.keyboardHint': '提示: 按 Ctrl+Enter 快速运行代码',
      'exercise.submitting': '提交中...',
      'exercise.submitFailed': '提交失败',
      'exercise.category': '分类',

      // ===== 考试页 =====
      'exams.title': '在线考试',
      'exams.subtitle': '科学的分级考核体系，通过阶段性考试检验学习成果，获得学习认证',
      'exams.duration': '考试时长',
      'exams.minutes': '分钟',
      'exams.passingScore': '及格分数',
      'exams.questions': '题目数量',
      'exams.start': '开始考试',
      'exams.noExams': '暂无可用考试',

      // ===== 社区页 =====
      'community.title': '学习社区',
      'community.subtitle': '与学员交流编程经验、分享学习心得、讨论技术问题，共同成长进步',
      'community.newPost': '发布新帖',
      'community.noPosts': '暂无帖子，快来发布第一个帖子吧',
      'community.post': '帖子',
      'community.replies': '回复',
      'community.author': '作者',

      // ===== 资源页 =====
      'resources.title': '学习资源',
      'resources.subtitle': '精心整理的Python学习资料，包括课件、代码示例和参考文档，支持免费下载',
      'resources.filterCategory': '资源分类',
      'resources.all': '全部分类',
      'resources.courseware': '课件',
      'resources.code': '代码',
      'resources.doc': '文档',
      'resources.count': '个资源',
      'resources.download': '下载资源',
      'resources.noResults': '暂无匹配的资源',
      'resources.viewAll': '查看全部资源',

      // ===== 进度页 =====
      'progress.title': '学习进度',
      'progress.subtitle': '实时追踪你的学习进度，科学规划学习路径，确保每个知识点都扎实掌握',
      'progress.coursesLearned': '已学习课程',
      'progress.chaptersLearned': '学习章节数',
      'progress.chaptersCompleted': '已完成章节',
      'progress.detail': '课程进度详情',
      'progress.completed': '已完成',
      'progress.noData': '还没有开始学习，快去探索课程吧',
      'progress.browseCourses': '浏览课程',

      // ===== 学习报告页 =====
      'report.title': '学习报告',
      'report.subtitle': '多维度数据分析，帮助你了解学习状态、发现薄弱环节、优化学习策略',
      'report.totalSubmissions': '总提交数',
      'report.avgScore': '练习平均分',
      'report.avgExamScore': '考试平均分',
      'report.completionRate': '课程完成率',
      'report.categoryScores': '分类得分统计',
      'report.noData': '暂无可分析数据，完成一些练习后即可生成学习报告',
      'report.startPractice': '开始练习',

      // ===== 登录/注册页 =====
      'login.title': '用户登录',
      'login.username': '用户名',
      'login.password': '密码',
      'login.submit': '登录',
      'login.noAccount': '没有账号？',
      'login.toRegister': '立即注册',

      'register.title': '用户注册',
      'register.username': '用户名',
      'register.email': '邮箱',
      'register.password': '密码',
      'register.confirmPassword': '确认密码',
      'register.submit': '注册',
      'register.hasAccount': '已有账号？',
      'register.toLogin': '立即登录',
      'register.usernameHelp': '3-80个字符',
      'register.emailHelp': '我们将不会分享您的邮箱地址',
      'register.passwordHelp': '至少6个字符',

      // 表单验证
      'validation.required': '此字段为必填项',
      'validation.minLength': '至少需要',
      'validation.characters': '个字符',
      'validation.invalidEmail': '请输入有效的邮箱地址',
      'validation.passwordMismatch': '两次输入的密码不一致',

      // Toast通知
      'toast.success': '操作成功',
      'toast.error': '操作失败',
      'toast.warning': '请注意',
      'toast.info': '提示',
    },

    'en': {
      '_langName': 'English',
      '_langFlag': '&#127468;&#127463;',

      // Navigation
      'nav.home': 'Home',
      'nav.courses': 'Courses',
      'nav.exercises': 'Practice',
      'nav.exams': 'Exams',
      'nav.community': 'Community',
      'nav.resources': 'Resources',
      'nav.login': 'Login',
      'nav.register': 'Sign Up Free',
      'nav.profile': 'Profile',
      'nav.progress': 'Progress',
      'nav.report': 'Report',
      'nav.admin': 'Admin Panel',
      'nav.logout': 'Logout',
      'nav.switchLang': 'Switch Language',

      // Skip link
      'skip.toMain': 'Skip to main content',

      // Brand
      'brand.name': 'Python Academy',

      // Footer
      'footer.tagline': 'Your one-stop Python learning platform with courses, coding practice, and assessment.',
      'footer.quickLinks': 'Quick Links',
      'footer.courses': 'Courses',
      'footer.exercises': 'Exercises',
      'footer.community': 'Community',
      'footer.contact': 'Contact Us',
      'footer.copyright': 'Python Academy. All rights reserved.',

      // Homepage
      'home.hero.title': 'Master Python Programming',
      'home.hero.subtitle': 'From beginner to advanced, a systematic learning path with interactive coding environment to make you a professional Python developer',
      'home.hero.cta': 'Start Learning Free',
      'home.hero.explore': 'Browse All Courses',
      'home.feature.courses': 'Systematic Courses',
      'home.feature.courses.desc': 'Complete Python curriculum from basics to advanced, with code examples for every topic',
      'home.feature.code': 'Online Coding',
      'home.feature.code.desc': 'Interactive coding environment with real-time execution and instant error feedback',
      'home.feature.assessment': 'Assessment',
      'home.feature.assessment.desc': 'Auto-grading system with personalized learning reports to track your progress',
      'home.path.title': 'Recommended Learning Path',
      'home.path.step1': 'Basics',
      'home.path.step2': 'Data Structures',
      'home.path.step3': 'OOP',
      'home.path.step4': 'Advanced',
      'home.path.step5': 'Web Dev',
      'home.hotCourses': 'Popular Courses',
      'home.viewAll': 'View All',
      'home.stats.students': 'Students',
      'home.stats.courses': 'Courses',
      'home.stats.exercises': 'Exercises',
      'home.stats.rate': 'Satisfaction',

      // Courses
      'courses.title': 'Course Catalog',
      'courses.subtitle': 'A systematic Python learning path from beginner to advanced',
      'courses.search': 'Search Courses',
      'courses.searchPlaceholder': 'Enter course name or keywords...',
      'courses.filterCategory': 'Filter by Category',
      'courses.filterLevel': 'Filter by Level',
      'courses.all': 'All',
      'courses.allCategories': 'All Categories',
      'courses.allLevels': 'All Levels',
      'courses.count': 'courses',
      'courses.start': 'Start Learning',
      'courses.level.beginner': 'Beginner',
      'courses.level.intermediate': 'Intermediate',
      'courses.level.advanced': 'Advanced',
      'courses.noResults': 'No courses found',
      'courses.noResultsHint': 'Try different keywords or filters',
      'courses.viewAllCourses': 'View All Courses',
      'courses.students': 'students',
      'courses.lessons': 'lessons',

      // Exercises
      'exercises.title': 'Practice Exercises',
      'exercises.subtitle': 'Multi-dimensional Python coding exercises from basics to advanced algorithms, with online coding, real-time execution and auto-grading',
      'exercises.filterCategory': 'Category',
      'exercises.filterDifficulty': 'Difficulty',
      'exercises.all': 'All Categories',
      'exercises.allDifficulties': 'All Levels',
      'exercises.difficulty.easy': 'Easy',
      'exercises.difficulty.medium': 'Medium',
      'exercises.difficulty.hard': 'Hard',
      'exercises.count': 'exercises',
      'exercises.start': 'Start Practice',
      'exercises.login': 'Login to Practice',
      'exercises.noResults': 'No matching exercises',
      'exercises.viewAll': 'View All Exercises',

      // Exercise Detail
      'exercise.runCode': 'Run Code',
      'exercise.submit': 'Submit Answer',
      'exercise.hint': 'Show Hint',
      'exercise.placeholder': 'Click "Run Code" to see results...',
      'exercise.loading': 'Running...',
      'exercise.success': 'Code executed successfully',
      'exercise.failed': 'Code execution failed',
      'exercise.passed': 'Congratulations! Exercise passed, score: ',
      'exercise.partial': 'Partially correct, score: ',
      'exercise.notPassed': 'Not passed, please try again',
      'exercise.networkError': 'Network error',
      'exercise.emptyCode': 'Code cannot be empty',
      'exercise.formError': 'Please fix the form errors',
      'exercise.keyboardHint': 'Tip: Press Ctrl+Enter to run code quickly',
      'exercise.submitting': 'Submitting...',
      'exercise.submitFailed': 'Submission failed',
      'exercise.category': 'Category',

      // Exams
      'exams.title': 'Online Exams',
      'exams.subtitle': 'A scientific tiered assessment system to test your learning outcomes through staged exams and earn certifications',
      'exams.duration': 'Duration',
      'exams.minutes': 'min',
      'exams.passingScore': 'Passing Score',
      'exams.questions': 'Questions',
      'exams.start': 'Start Exam',
      'exams.noExams': 'No exams available',

      // Community
      'community.title': 'Community',
      'community.subtitle': 'Exchange coding tips, share learning experiences, discuss technical questions, and grow together',
      'community.newPost': 'New Post',
      'community.noPosts': 'No posts yet. Be the first to share!',
      'community.post': 'Post',
      'community.replies': 'replies',
      'community.author': 'Author',

      // Resources
      'resources.title': 'Learning Resources',
      'resources.subtitle': 'Carefully curated Python learning materials including slides, code samples and reference docs, all free to download',
      'resources.filterCategory': 'Resource Category',
      'resources.all': 'All Categories',
      'resources.courseware': 'Courseware',
      'resources.code': 'Code',
      'resources.doc': 'Documentation',
      'resources.count': 'resources',
      'resources.download': 'Download',
      'resources.noResults': 'No matching resources',
      'resources.viewAll': 'View All Resources',

      // Progress
      'progress.title': 'Learning Progress',
      'progress.subtitle': 'Track your learning progress in real-time with a scientific roadmap to master every concept thoroughly',
      'progress.coursesLearned': 'Courses Learned',
      'progress.chaptersLearned': 'Chapters Studied',
      'progress.chaptersCompleted': 'Chapters Completed',
      'progress.detail': 'Course Progress Details',
      'progress.completed': 'Completed',
      'progress.noData': 'You haven\'t started learning yet. Explore our courses!',
      'progress.browseCourses': 'Browse Courses',

      // Report
      'report.title': 'Learning Report',
      'report.subtitle': 'Multi-dimensional data analysis to help you understand your learning status, identify weaknesses, and optimize your strategy',
      'report.totalSubmissions': 'Total Submissions',
      'report.avgScore': 'Avg Exercise Score',
      'report.avgExamScore': 'Avg Exam Score',
      'report.completionRate': 'Completion Rate',
      'report.categoryScores': 'Category Score Breakdown',
      'report.noData': 'No data to analyze yet. Complete some exercises to generate your report.',
      'report.startPractice': 'Start Practice',

      // Login / Register
      'login.title': 'Login',
      'login.username': 'Username',
      'login.password': 'Password',
      'login.submit': 'Login',
      'login.noAccount': 'Don\'t have an account?',
      'login.toRegister': 'Register now',

      'register.title': 'Register',
      'register.username': 'Username',
      'register.email': 'Email',
      'register.password': 'Password',
      'register.confirmPassword': 'Confirm Password',
      'register.submit': 'Register',
      'register.hasAccount': 'Already have an account?',
      'register.toLogin': 'Log in',
      'register.usernameHelp': '3-80 characters',
      'register.emailHelp': 'We\'ll never share your email',
      'register.passwordHelp': 'At least 6 characters',

      // Form validation
      'validation.required': 'This field is required',
      'validation.minLength': 'At least ',
      'validation.characters': ' characters required',
      'validation.invalidEmail': 'Please enter a valid email address',
      'validation.passwordMismatch': 'Passwords do not match',

      // Toast
      'toast.success': 'Success',
      'toast.error': 'Error',
      'toast.warning': 'Warning',
      'toast.info': 'Info',
    }
  };

  function detectLanguage(){
    try{var stored=localStorage.getItem('lang');if(stored&&LOCALES[stored])return stored}catch(e){}
    var browserLang=(navigator.language||navigator.userLanguage||'').split('-')[0];
    if(browserLang==='zh')return'zh-CN';
    try{var stored2=localStorage.getItem('lang');if(stored2&&LOCALES[stored2])return stored2}catch(e){}
    return'zh-CN';
  }

  var currentLang=detectLanguage();

  function t(key){
    return(LOCALES[currentLang]&&LOCALES[currentLang][key])||(LOCALES['zh-CN']&&LOCALES['zh-CN'][key])||key;
  }

  function applyTranslations(root){
    root=root||document.documentElement;
    // html lang attribute
    document.documentElement.lang=currentLang;

    // data-i18n for text content
    var elements=root.querySelectorAll('[data-i18n]');
    for(var i=0;i<elements.length;i++){
      var el=elements[i];
      var key=el.getAttribute('data-i18n');
      if(key)el.textContent=t(key);
    }

    // data-i18n-placeholder
    var placeholders=root.querySelectorAll('[data-i18n-placeholder]');
    for(var j=0;j<placeholders.length;j++){
      var pel=placeholders[j];
      var pkey=pel.getAttribute('data-i18n-placeholder');
      if(pkey)pel.placeholder=t(pkey);
    }

    // data-i18n-title
    var titles=root.querySelectorAll('[data-i18n-title]');
    for(var k=0;k<titles.length;k++){
      var tel=titles[k];
      var tkey=tel.getAttribute('data-i18n-title');
      if(tkey)tel.title=t(tkey);
    }

    // data-i18n-aria-label
    var ariaLabels=root.querySelectorAll('[data-i18n-aria-label]');
    for(var l=0;l<ariaLabels.length;l++){
      var ael=ariaLabels[l];
      var akey=ael.getAttribute('data-i18n-aria-label');
      if(akey)ael.setAttribute('aria-label',t(akey));
    }

    // data-i18n-html (for elements containing HTML)
    var htmlEls=root.querySelectorAll('[data-i18n-html]');
    for(var m=0;m<htmlEls.length;m++){
      var hel=htmlEls[m];
      var hkey=hel.getAttribute('data-i18n-html');
      if(hkey)hel.innerHTML=t(hkey);
    }
  }

  function switchLanguage(lang,animate){
    if(!LOCALES[lang])return;
    if(lang===currentLang)return;

    // Transition animation
    if(animate!==false){
      var main=document.getElementById('main-content');
      if(main){
        main.style.transition='opacity .15s ease';
        main.style.opacity='0';
        setTimeout(function(){
          currentLang=lang;
          try{localStorage.setItem('lang',lang)}catch(e){}
          applyTranslations();
          updateLangSwitcherUI();
          main.style.opacity='1';
          setTimeout(function(){main.style.transition=''},200);
        },160);
        return;
      }
    }

    currentLang=lang;
    try{localStorage.setItem('lang',lang)}catch(e){}
    applyTranslations();
    updateLangSwitcherUI();
    if(window.showToast){
      var msg=lang==='zh-CN'?'已切换为中文':'Switched to English';
      showToast(msg,'success',2000);
    }
  }

  function updateLangSwitcherUI(){
    var langBtn=document.getElementById('langSwitcherBtn');
    if(langBtn){
      var currentLocale=LOCALES[currentLang];
      langBtn.innerHTML='<span class="lang-flag" aria-hidden="true">'+(currentLocale._langFlag||'')+'</span> <span class="lang-current-name">'+(currentLocale._langName||currentLang)+'</span>';
    }

    // Update the dropdown menu to show current language as active
    var langOptions=document.querySelectorAll('[data-lang-option]');
    for(var i=0;i<langOptions.length;i++){
      var opt=langOptions[i];
      var optLang=opt.getAttribute('data-lang-option');
      if(optLang===currentLang){
        opt.classList.add('lang-current-item');
      }else{
        opt.classList.remove('lang-current-item');
      }
    }
  }

  function init(){
    applyTranslations();
    updateLangSwitcherUI();

    // Set up language switch click handlers
    var langOptions=document.querySelectorAll('[data-lang-option]');
    for(var i=0;i<langOptions.length;i++){
      (function(opt){
        opt.addEventListener('click',function(e){
          e.preventDefault();
          var lang=opt.getAttribute('data-lang-option');
          if(lang)switchLanguage(lang);
        });
      })(langOptions[i]);
    }

    // Keyboard support for language switcher
    var langBtn=document.getElementById('langSwitcherBtn');
    var langDropdown=document.getElementById('langDropdown');
    if(langBtn&&langDropdown){
      (function(){
        var langOpts=langDropdown.querySelectorAll('[data-lang-option]');
        langBtn.addEventListener('keydown',function(e){
          if(e.key==='Enter'||e.key===' '){
            e.preventDefault();
            var ex=langBtn.getAttribute('aria-expanded')==='true';
            langBtn.setAttribute('aria-expanded',!ex);
          }
          if(e.key==='Escape'){
            langBtn.setAttribute('aria-expanded','false');
            langBtn.focus();
          }
        });
        langOpts.forEach(function(opt,idx){
          opt.addEventListener('keydown',function(e){
            if(e.key==='ArrowDown'){
              e.preventDefault();
              langOpts[(idx+1)%langOpts.length].focus();
            }
            if(e.key==='ArrowUp'){
              e.preventDefault();
              langOpts[(idx-1+langOpts.length)%langOpts.length].focus();
            }
            if(e.key==='Escape'){
              langBtn.setAttribute('aria-expanded','false');
              langBtn.focus();
            }
          });
        });
      })();
    }
  }

  // Expose globally
  window.i18n={
    t:t,
    currentLang:currentLang,
    switchLanguage:switchLanguage,
    applyTranslations:applyTranslations,
    LOCALES:LOCALES,
    getCurrentLang:function(){return currentLang}
  };

  // Initialize on DOM ready
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',init);
  }else{
    init();
  }
})();
