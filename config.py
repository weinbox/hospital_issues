import os

class Config:
    SECRET_KEY = 'your-secret-key-here'  # يجب تغييره في الإنتاج
    
    # إعدادات قاعدة البيانات
    if os.environ.get('PYTHONANYWHERE_DOMAIN'):
        # مسار قاعدة البيانات على PythonAnywhere
        SQLALCHEMY_DATABASE_URI = 'sqlite:////home/YOUR_USERNAME/hospital_issues/hospital.db'
    else:
        # مسار قاعدة البيانات المحلي
        SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
