from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Issue
from config import Config
import os
from datetime import datetime, timedelta
from sqlalchemy import inspect

app = Flask(__name__)
app.config.from_object(Config)

# تهيئة نظام تسجيل الدخول
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# تهيئة قاعدة البيانات
db.init_app(app)

# إنشاء قاعدة البيانات إذا لم تكن موجودة
def init_db():
    with app.app_context():
        # إنشاء الجداول إذا لم تكن موجودة
        db.create_all()
        
        # طباعة هيكل الجداول
        inspector = inspect(db.engine)
        for table_name in inspector.get_table_names():
            print(f"\nTable: {table_name}")
            for column in inspector.get_columns(table_name):
                print(f"Column: {column['name']}, Type: {column['type']}, Nullable: {column.get('nullable', True)}")
        
        # إنشاء حساب المشرف إذا لم يكن موجوداً
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

# تشغيل دالة تهيئة قاعدة البيانات
if not os.path.exists('hospital.db'):
    init_db()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    issues = Issue.query.order_by(Issue.created_at.desc()).all()
    return render_template('dashboard/issues.html', issues=issues)

@app.route('/issue/<int:id>')
@login_required
def view_issue(id):
    issue = Issue.query.get_or_404(id)
    return render_template('dashboard/issue_details.html', issue=issue)

@app.route('/issue/<int:id>/update_status', methods=['POST'])
@login_required
def update_status(id):
    issue = Issue.query.get_or_404(id)
    issue.status = request.form['status']
    db.session.commit()
    flash('تم تحديث حالة العطل بنجاح', 'success')
    return redirect(url_for('view_issue', id=id))

@app.route('/new_issue', methods=['POST'])
def new_issue():
    try:
        department = request.form['department']
        room = request.form['room']
        description = request.form['issue_details']
        reporter_name = request.form['reporter_name']
        
        location = f"{department} - {room}"
        
        issue = Issue(
            location=location,
            description=description,
            reporter_name=reporter_name,
            status='جديد'
        )
        
        db.session.add(issue)
        db.session.commit()
        
        flash('تم إضافة العطل بنجاح', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {str(e)}")
        db.session.rollback()
        flash('حدث خطأ أثناء إضافة العطل', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
