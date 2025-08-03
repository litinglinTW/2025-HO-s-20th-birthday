#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 14:50:07 2025

@author: cglinmacbook
"""

import streamlit as st
from PIL import Image
import os

def pic_page():
    
    MEDIA_FOLDER = "/Users/cglinmacbook/Desktop/python專案/birthday/荷/group"
    image_exts = [".jpg", ".jpeg", ".png"]
    video_exts = [".mp4", ".webm", ".mov"]
    
    # 取得所有檔案
    media_files = os.listdir(MEDIA_FOLDER)
    
    # 過濾圖片與影片
    image_files = [f for f in media_files if os.path.splitext(f)[1].lower() in image_exts]
    video_files = [f for f in media_files if os.path.splitext(f)[1].lower() in video_exts]
    
    # 標題
    st.title("📸 Photo Gallery")
    st.write("以下是你收藏的圖片：pictures(age 13~15) 來自那個國中聚餐影片")
    
    # 設定每列顯示幾張圖片
    columns_per_row = 1
    rows = (len(image_files) + columns_per_row - 1) // columns_per_row
    
    # 動態建立網格顯示圖片
    for row in range(rows):
        cols = st.columns(columns_per_row)
        for col_idx in range(columns_per_row):
            img_idx = row * columns_per_row + col_idx
            if img_idx < len(image_files):
                image_path = os.path.join(MEDIA_FOLDER, image_files[img_idx])
                image = Image.open(image_path)
                with cols[col_idx]:
                    st.image(image, caption=image_files[img_idx], use_column_width=True)
                    
                    
                    
    # 顯示影片
    st.write("這個影片我自己都不敢看 但我幫你截了部分畫面 hehe")
    for video_file in video_files:
        video_path = os.path.join(MEDIA_FOLDER, video_file)
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        st.video(video_bytes, format="video/mp4")
