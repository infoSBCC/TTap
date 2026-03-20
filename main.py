import gspread
import json
import os
from google.oauth2.service_account import Credentials

# โหลด credentials จาก GitHub Secret
creds_json = os.environ["GOOGLE_CREDENTIALS_JSON"]
creds_dict = json.loads(creds_json)

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

# Google Sheet ID
SHEET_ID = "1jOsRV1Q8BbLM1p1HJAdvJ6liK9VlG3sUX1LalDcxSks"
sheet = client.open_by_key(SHEET_ID).worksheet("test")

# รายการที่ต้องการเพิ่ม
new_rows = [
    ["a003", "grape", 7],
    ["a004", "tomato", 5],
]

# เพิ่มแถวต่อท้ายตาราง
sheet.append_rows(new_rows)

print("===== เพิ่มข้อมูลสำเร็จ =====")
for row in new_rows:
    print(f"  ID: {row[0]}, Product: {row[1]}, Value: {row[2]}")

print()
print("===== ข้อมูลทั้งหมดใน sheet test =====")
import pandas as pd
data = sheet.get_all_records()
df = pd.DataFrame(data)
print(df)
