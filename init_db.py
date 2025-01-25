from app import app, db
from models import User

def init_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create tables
        db.create_all()
        
        # Create admin account
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully")
