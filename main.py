#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 22:29:56 2025

@author: cglinmacbook
"""

import streamlit as st
from modules.HOHOgame import quiz
from modules.HOHOcard import card_page
from modules.HOpic import pic_page
from PIL import Image


# 頁面密碼設定
page_passwords = {
    "2025 HOHO's 20th birthday": "0",
    "2025 ???'s 20th birthday": "1"
}

# 頁面選單
pages = list(page_passwords.keys())
selected_page = st.sidebar.selectbox("請選擇主題頁面", pages)

# 驗證狀態的key
auth_key = f"auth_{selected_page}"

st.title("2025 HOHO's 20th birthday")




st.write(" Welcome ")

# 根據頁面選擇呼叫對應內容
if selected_page == "2025 HOHO's 20th birthday":


    subpage = st.radio("請選擇功能頁面", ["首頁", "take a quiz about HO and see how much you really know her","pictures", "卡片"])

    if subpage == "首頁":
        st.markdown("""
        
        - choose the page, there is nothing here.
        - Designer: CL
    
        """)
        img = Image.open("/Users/cglinmacbook/Desktop/python專案/birthday/荷/非答案資料夾/author.png")
        st.image(img, caption="Hallo", use_column_width=10)
        
    elif subpage == "take a quiz about HO and see how much you really know her":
        quiz()
        
    elif subpage == "pictures":
        pic_page()
    elif subpage == "卡片":
        # 密碼驗證區塊
        CARD_AUTH_KEY = "card_auth"
        CARD_PASSWORD = "0800"  # 請換成你要的密碼

        if not st.session_state.get(CARD_AUTH_KEY, False):
            pwd = st.text_input("請輸入密碼以進入卡片頁面：", type="password")
            if st.button("驗證"):
                if pwd == CARD_PASSWORD:
                    st.session_state[CARD_AUTH_KEY] = True
                    st.success("密碼正確，歡迎進入卡片頁面！")
                    st.experimental_rerun()
                else:
                    st.error("密碼錯誤，請再試一次！")
            st.stop()  # 密碼錯誤或還沒驗證就不顯示 card_page

        # 密碼正確才會執行這行
        card_page()

    
    
elif selected_page == "2025 ???'s 20th birthday":
    st.write("這是另一個生日頁面內容，請自行填寫。")








            