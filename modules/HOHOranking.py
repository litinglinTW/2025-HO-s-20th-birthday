#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 11:51:36 2025

@author: cglinmacbook
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import os

# 設定 Google Sheet 相關資訊
SHEET_NAME = "HOHO_Quiz_Ranking"   # 你的 Google Sheet 名稱
WORKSHEET_NAME = "排行榜"           # 工作表名稱（可自訂）
CREDENTIALS_FILE = "/Users/cglinmacbook/Desktop/python專案/birthday/modules/荷金鑰/dazzling-kite-467903-j8-458957fcfd0c.json"  # 你的金鑰檔案路徑

# 權限範圍
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 取得 Google Sheet 服務
def get_gsheet():
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPE)
    gc = gspread.authorize(creds)
    sh = gc.open(SHEET_NAME)
    ws = sh.worksheet(WORKSHEET_NAME)
    return ws

# 新增一筆紀錄
def add_record(name, score, total, ts=None):
    ws = get_gsheet()
    if ts is None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([name, str(score), str(total), ts])

# 取得所有紀錄，回傳 pandas DataFrame
def get_ranking():
    ws = get_gsheet()
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    # 排序，高分在前，若同分則較早時間在前
    if not df.empty and "分數" in df.columns and "時間" in df.columns:
        df = df.sort_values(by=["分數", "時間"], ascending=[False, True])
    return df

# 排行榜顯示區塊
def show_ranking(top_n=20):
    st.subheader("🏆 排行榜")
    df = get_ranking()
    if df.empty:
        st.info("目前尚無任何紀錄，快來挑戰第一名吧！")
        return
    # 只顯示前 top_n 名
    df = df.head(top_n)
    # 美化欄位名稱
    df = df.rename(columns={
        "姓名": "姓名",
        "分數": "分數",
        "總題數": "總題數",
        "時間": "作答時間"
    })
    st.table(df[["姓名", "分數", "總題數", "作答時間"]])

# 範例：在答題結束時呼叫這個函式寫入
def save_score(name, score, total):
    add_record(name, score, total)