# ===== sheets.py =====
# Google Sheets helper functions

import gspread
import json
import os
from google.oauth2.service_account import Credentials
from config import (
    SCOPES,
    KEYWORD_SHEET_ID,
    KEYWORD_SHEET_NAME,
    KEYWORD_COL,
    KEYWORD_GROUP_COL,
    KEYWORD_DESC_COL,
    UNIQUE_POST_SHEET_ID,
    UNIQUE_POST_SHEET_NAME,
)


def get_client():
    creds_json = os.environ["GOOGLE_CREDENTIALS_JSON"]
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


def get_sheet(spreadsheet_id, sheet_name):
    client = get_client()
    return client.open_by_key(spreadsheet_id).worksheet(sheet_name)


# --- Keyword Sheet ---

def get_keywords():
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


# --- UniquePost Sheet ---

def get_existing_links():
    sheet = get_sheet(UNIQUE_POST_SHEET_ID, UNIQUE_POST_SHEET_NAME)
    records = sheet.get_all_records()
    existing = set()
    for row in records:
        link = str(row.get("link", "")).strip()
        if link:
            existing.add(link)
    return existing


def append_unique_posts(new_rows):
    sheet = get_sheet(UNIQUE_POST_SHEET_ID, UNIQUE_POST_SHEET_NAME)
    header = sheet.row_values(1)
    if not header:
        sheet.append_row(["keyword_group", "keyword", "link", "transcript"])
        print("created header in UniquePost")
    if new_rows:
        sheet.append_rows(new_rows)
        print(f"appended {len(new_rows)} rows to UniquePost")
    else:
        print("no new rows to append")
