import sys
import os

# تحديد مسار المشروع
path = '/home/YOUR_USERNAME/hospital_issues'
if path not in sys.path:
    sys.path.append(path)

# تفعيل البيئة الافتراضية
python_version = 'python3.9'  # تأكد من تغيير هذا حسب إصدار Python الخاص بك
activate_this = f'/home/YOUR_USERNAME/hospital_issues/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# استيراد التطبيق
from app import app as application
