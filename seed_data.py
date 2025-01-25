from app import app, db
from models import User, Issue, Comment, Notification
from datetime import datetime, timedelta

def create_seed_data():
    with app.app_context():
        # حذف البيانات الموجودة
        db.session.query(Notification).delete()
        db.session.query(Comment).delete()
        db.session.query(Issue).delete()
        db.session.query(User).delete()
        db.session.commit()

        # إنشاء المستخدمين
        admin = User(username='admin', email='admin@hospital.com', is_admin=True)
        admin.set_password('admin123')
        
        tech1 = User(username='فني_صيانة1', email='tech1@hospital.com')
        tech1.set_password('tech123')
        
        tech2 = User(username='فني_صيانة2', email='tech2@hospital.com')
        tech2.set_password('tech123')
        
        db.session.add_all([admin, tech1, tech2])
        db.session.commit()

        # إنشاء المشكلات
        issues = [
            Issue(
                title='عطل في جهاز الأشعة',
                description='جهاز الأشعة في قسم الطوارئ لا يعمل',
                location='قسم الطوارئ - الطابق الأول',
                status='قيد المعالجة',
                priority='عاجل',
                reporter_name='د. أحمد محمد',
                phone='0501234567',
                assigned_to=tech1.id,
                created_at=datetime.utcnow() + timedelta(hours=3) - timedelta(days=2)
            ),
            Issue(
                title='مشكلة في نظام التكييف',
                description='درجة الحرارة مرتفعة في غرف المرضى',
                location='جناح المرضى - الطابق الثالث',
                status='جديد',
                priority='مرتفع',
                reporter_name='م. سارة خالد',
                phone='0507654321',
                created_at=datetime.utcnow() + timedelta(hours=3) - timedelta(days=1)
            ),
            Issue(
                title='عطل في المصعد',
                description='المصعد رقم 2 متوقف عن العمل',
                location='المبنى الرئيسي',
                status='مكتمل',
                priority='متوسط',
                reporter_name='م. فهد العمري',
                phone='0503456789',
                assigned_to=tech2.id,
                created_at=datetime.utcnow() + timedelta(hours=3) - timedelta(days=5)
            )
        ]
        db.session.add_all(issues)
        db.session.commit()

        # إضافة تعليقات
        comments = [
            Comment(
                content='تم فحص الجهاز، يحتاج إلى قطعة غيار جديدة',
                issue_id=issues[0].id,
                user_id=tech1.id,
                created_at=datetime.utcnow() + timedelta(hours=3) - timedelta(days=1)
            ),
            Comment(
                content='تم طلب قطعة الغيار، ستصل خلال يومين',
                issue_id=issues[0].id,
                user_id=admin.id,
                created_at=datetime.utcnow() + timedelta(hours=3) - timedelta(hours=12)
            ),
            Comment(
                content='سيتم معاينة المشكلة اليوم',
                issue_id=issues[1].id,
                user_id=tech2.id,
                created_at=datetime.utcnow() + timedelta(hours=3) - timedelta(hours=2)
            )
        ]
        db.session.add_all(comments)
        db.session.commit()

        # إضافة إشعارات
        notifications = [
            Notification(
                message='تم تعيينك لمعالجة مشكلة جهاز الأشعة',
                user_id=tech1.id,
                issue_id=issues[0].id,
                created_at=datetime.utcnow() + timedelta(hours=3) - timedelta(days=2)
            ),
            Notification(
                message='تم إضافة تعليق جديد على المشكلة المسندة إليك',
                user_id=tech1.id,
                issue_id=issues[0].id,
                created_at=datetime.utcnow() + timedelta(hours=3) - timedelta(days=1)
            ),
            Notification(
                message='تم تعيينك لمعالجة مشكلة المصعد',
                user_id=tech2.id,
                issue_id=issues[2].id,
                created_at=datetime.utcnow() + timedelta(hours=3) - timedelta(days=5)
            )
        ]
        db.session.add_all(notifications)
        db.session.commit()

if __name__ == '__main__':
    create_seed_data()
    print("Data seeded successfully!")
