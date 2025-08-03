#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 11:45:42 2025

@author: cglinmacbook
"""

import streamlit as st
import os

CARD_FILE = "/Users/cglinmacbook/Desktop/python專案/birthday/modules/HOHOcard.txt"  # 祝福文字檔案，請放在專案根目錄或指定路徑

def card_page():
    st.header("🎁")

    # 讀取卡片內容，每行一則
    if not os.path.exists(CARD_FILE):
        st.info("目前還沒有收到任何卡片，歡迎成為第一個留言的人！")
        return

    with open(CARD_FILE, "r", encoding="utf-8") as f:
        cards = [line.strip() for line in f if line.strip()]

    if not cards:
        st.info("目前還沒有收到任何卡片，歡迎成為第一個留言的人！")
        return

    # 自訂卡片樣式
    card_css = """
    <style>
    .cardwall {
        display: flex;
        flex-wrap: wrap;
        gap: 24px;
        margin-top: 20px;
    }
    .mycard {
        background: linear-gradient(135deg, #f7cac9 0%, #92a8d1 100%);
        border-radius: 20px;
        box-shadow: 0 6px 18px 4px rgba(100, 100, 100, 0.15);
        color: #222;
        padding: 28px 26px 22px 26px;
        min-width: 250px;
        max-width: 330px;
        font-size: 1.13rem;
        margin-bottom: 12px;
        word-break: break-all;
        white-space: pre-wrap;
    }
    </style>
    """
    st.markdown(card_css, unsafe_allow_html=True)

    # 用自訂HTML + CSS排版顯示所有卡片
    card_html = '<div class="cardwall">'
    for text in cards:
        card_html += f'<div class="mycard">{st.markdown(text, unsafe_allow_html=False)}</div>'
    card_html += '</div>'
    st.markdown(card_html, unsafe_allow_html=True)