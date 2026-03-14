from datetime import datetime

now = datetime.utcnow()

print('==============================')
print('   Hello from GitHub Actions!')
print('==============================')
print(f'รันเมื่อ (UTC): {now.strftime("%Y-%m-%d %H:%M:%S")}')
print('สคริปต์ทำงานเสร็จเรียบร้อย!')
