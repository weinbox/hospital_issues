import gspread
import sys
from oauth2client.service_account import ServiceAccountCredentials

# تعيين ترميز المخرجات إلى UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def test_connection():
    # تهيئة الاتصال
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)
    
    # فتح جدول البيانات
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1bn2fbuQeDATPiOSOhORkqi1cd6g7Ct_8CG32_66h3NI/edit?usp=sharing')
    
    # طباعة معلومات عن جدول البيانات
    print("Title:", spreadsheet.title)
    print("\nWorksheets:")
    for worksheet in spreadsheet.worksheets():
        print(f"- {worksheet.title}")
        # طباعة العناوين في كل ورقة
        headers = worksheet.row_values(1)
        if headers:  # إذا كان هناك بيانات في الصف الأول
            print(f"  Headers: {headers}\n")

if __name__ == '__main__':
    test_connection()
