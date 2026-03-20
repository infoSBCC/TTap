# ===== sheets.py =====
# จัดการ Google Sheets ทุก sheet

import gspread
import json
import os
from google.oauth2.service_account import Credentials
from config import (
    SCOPES,
    KEYWORD_SHEET_ID, KEYWORD_SHEET_NAME,
    KEYWORD_COL, KEYWORD_GROUP_COL, KEYWORD_DESC_COL,
    UNIQUE_POST_SHEET_ID, UNIQUE_POST_SHEET_NAME,
)


def get_client():
        """สร้าง gspread client จาก GitHub Secret"""
        creds_json = os.environ["GOOGLE_CREDENTIALS_JSON"]
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        return gspread.authorize(creds)


def get_sheet(spreadsheet_id, sheet_name):
        """เปิด worksheet จาก spreadsheet_id และ sheet_name"""
        client = get_client()
        return client.open_by_key(spreadsheet_id).worksheet(sheet_name)


# ─────────────────────────────────────────────
# ส่วนที่ 1: Keyword Sheet
# ─────────────────────────────────────────────

def get_keywords():
        """
            ดึง keyword + keyword_group + keyword_description จาก Keyword Sheet
                คืนค่าเป็น list of dict: [{"keyword": ..., "group": ..., "description": ...}, ...]
                    """
        sheet = get_sheet(KEYWORD_SHEET_ID, KEYWORD_SHEET_NAME)
        records = sheet.get_all_records()
        result = []
        for row in records:
                    kw = str(row.get(KEYWORD_COL, "")).strip()
                    grp = str(row.get(KEYWORD_GROUP_COL, "")).strip()
                    desc = str(row.get(KEYWORD_DESC_COL, "")).strip()
                    if kw:
                                    result.append({"keyword": kw, "group": grp, "description": desc})
                            return result


# ─────────────────────────────────────────────
# ส่วนที่ 2: UniquePost Sheet
# ─────────────────────────────────────────────

def get_existing_links():
        """
            ดึง link ที่มีอยู่แล้วใน sheet UniquePost (column "link")
                คืนค่าเป็น set ของ link
                    """
        sheet = get_sheet(UNIQUE_POST_SHEET_ID, UNIQUE_POST_SHEET_NAME)
        records = sheet.get_all_records()
        existing = set()
        for row in records:
                    link = str(row.get("link", "")).strip()
                    if link:
                                    existing.add(link)
                            return existing


def append_unique_posts(new_rows):
        """
            append แถวใหม่ลง sheet UniquePost
                new_rows: list of list [[keyword_group, keyword, link, transcript], ...]
                    """
        sheet = get_sheet(UNIQUE_POST_SHEET_ID, UNIQUE_POST_SHEET_NAME)

    # ตรวจสอบ header ถ้ายังไม่มีให้สร้าง
        header = sheet.row_values(1)
        if not header:
                    sheet.append_row(["keyword_group", "keyword", "link", "transcript"])
                    print("สร้าง header ใน UniquePost แล้ว")

        if new_rows:
                    sheet.append_rows(new_rows)
                    print(f"append {len(new_rows)} แถวลง UniquePost สำเร็จ")
else:
        print("ไม่มีแถวใหม่ให้ append")
