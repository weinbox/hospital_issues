import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz
from models import User

class SheetsDB:
    def __init__(self, credentials_path, spreadsheet_url):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(credentials)
        
        self.spreadsheet = client.open_by_url(spreadsheet_url)
        self.responses_sheet = self.spreadsheet.worksheet('Form Responses 1')
        self.issues_sheet = self.spreadsheet.worksheet('Sheet1')
        
        # إنشاء ورقة المستخدمين إذا لم تكن موجودة
        try:
            self.users_sheet = self.spreadsheet.worksheet('Users')
        except gspread.exceptions.WorksheetNotFound:
            self.users_sheet = self.spreadsheet.add_worksheet('Users', 1, 4)
            # إضافة رؤوس الأعمدة
            self.users_sheet.append_row(['id', 'username', 'password_hash', 'is_admin'])
            # إضافة مستخدم افتراضي
            from werkzeug.security import generate_password_hash
            self.users_sheet.append_row(['1', 'admin', generate_password_hash('admin123'), 'True'])
        
        # إنشاء أوراق التعليقات والإشعارات إذا لم تكن موجودة
        try:
            self.comments_sheet = self.spreadsheet.worksheet('Comments')
        except gspread.WorksheetNotFound:
            self.comments_sheet = self.spreadsheet.add_worksheet('Comments', 1000, 5)
            self.comments_sheet.append_row(['id', 'issue_id', 'user_id', 'content', 'created_at'])
            
        try:
            self.notifications_sheet = self.spreadsheet.worksheet('Notifications')
        except gspread.WorksheetNotFound:
            self.notifications_sheet = self.spreadsheet.add_worksheet('Notifications', 1000, 6)
            self.notifications_sheet.append_row(['id', 'user_id', 'message', 'issue_id', 'is_read', 'created_at'])

    def _get_next_id(self, worksheet):
        """الحصول على معرف جديد للصف التالي"""
        try:
            values = worksheet.col_values(1)[1:]  # تجاهل الصف الأول (العناوين)
            return max([int(x) for x in values if x.isdigit()]) + 1
        except:
            return 1

    def get_user_by_username(self, username):
        """البحث عن مستخدم باسم المستخدم"""
        users = self.users_sheet.get_all_records()
        user = next((user for user in users if user['username'] == username), None)
        if user:
            return User(user)
        return None
    
    def get_user_by_id(self, user_id):
        """البحث عن مستخدم بالمعرف"""
        users = self.users_sheet.get_all_records()
        user = next((user for user in users if str(user['id']) == str(user_id)), None)
        if user:
            return User(user)
        return None
        
    def get_all_issues(self):
        """الحصول على جميع المشكلات"""
        all_issues = self.issues_sheet.get_all_records()
        return all_issues

    def get_issue_by_id(self, row_number):
        """الحصول على مشكلة محددة حسب رقم الصف"""
        try:
            issue = self.issues_sheet.row_values(row_number)
            headers = self.issues_sheet.row_values(1)
            return dict(zip(headers, issue))
        except:
            return None

    def update_issue_status(self, row_number, status):
        """تحديث حالة المشكلة"""
        if status:
            self.issues_sheet.update_cell(row_number, 5, status)  # عمود حالة الصيانة

    def create_issue(self, data):
        """إضافة مشكلة جديدة إلى جدول البيانات"""
        # الحصول على التاريخ الحالي
        tz = pytz.timezone('Asia/Riyadh')
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        
        # تجهيز البيانات للإدخال
        row = [
            current_time,  # تاريخ التسجيل
            data['location'],  # المكان
            data['issue_details'],  # تفاصيل العطل
            data['reporter_name'],  # اسم المبلغ
            '',  # حالة الصيانة (الشركة)
            '',  # المتابعة (الهندسية)
        ]
        
        # إضافة الصف الجديد
        self.responses_sheet.append_row(row)
        
        # إرجاع رقم الصف المضاف
        return len(self.responses_sheet.get_all_values())

    def add_comment(self, issue_id, user_id, content):
        """إضافة تعليق جديد"""
        comment_id = self._get_next_id(self.comments_sheet)
        now = datetime.now(pytz.timezone('Asia/Riyadh')).strftime('%Y-%m-%d %H:%M:%S')
        self.comments_sheet.append_row([
            comment_id,
            issue_id,
            user_id,
            content,
            now
        ])
        return comment_id

    def get_comments(self, issue_id):
        """الحصول على تعليقات مشكلة محددة"""
        all_comments = self.comments_sheet.get_all_records()
        return [comment for comment in all_comments if str(comment['issue_id']) == str(issue_id)]

    def add_notification(self, user_id, message, issue_id):
        """إضافة إشعار جديد"""
        notification_id = self._get_next_id(self.notifications_sheet)
        now = datetime.now(pytz.timezone('Asia/Riyadh')).strftime('%Y-%m-%d %H:%M:%S')
        self.notifications_sheet.append_row([
            notification_id,
            user_id,
            message,
            issue_id,
            False,  # is_read
            now
        ])
        return notification_id

    def get_notifications(self, user_id):
        """الحصول على إشعارات مستخدم محدد"""
        all_notifications = self.notifications_sheet.get_all_records()
        return [n for n in all_notifications if str(n['user_id']) == str(user_id)]

    def mark_notification_read(self, notification_id):
        """تحديث حالة الإشعار إلى مقروء"""
        try:
            cell = self.notifications_sheet.find(str(notification_id))
            if cell and cell.col == 1:  # تأكد من أن الخلية في عمود المعرف
                self.notifications_sheet.update_cell(cell.row, 5, True)  # عمود is_read
                return True
        except:
            pass
        return False
