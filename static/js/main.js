// تأكيد حذف العناصر
function confirmDelete(event) {
    if (!confirm('هل أنت متأكد من حذف هذا العنصر؟')) {
        event.preventDefault();
    }
}

// إخفاء رسائل التنبيه تلقائياً
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        });
    }, 3000);
});

// تحديث حالة البلاغ
function updateIssueStatus(issueId, status) {
    fetch(`/issue/${issueId}/update`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}

// تحقق من صحة رقم الهاتف
document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.getElementById('reporter_phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let phone = e.target.value.replace(/\D/g, '');
            if (phone.length > 10) {
                phone = phone.substr(0, 10);
            }
            e.target.value = phone;
        });
    }
});
