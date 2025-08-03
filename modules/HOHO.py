#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 22:53:13 2025

@author: cglinmacbook
"""
import streamlit as st
from PIL import Image
import random
import os
import re

# ====== 共用圖片抓取函式 ======
def get_image_files(folder):
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
    ]

# ====== 單選題範例：eyes ======
def question_1():
    st.subheader("eyes")
    st.header("Which one is HO's eyes?")
    st.write("請選出下列哪張圖片是 HO 的眼睛？")

    ANSWER_DIR = "/Users/cglinmacbook/Desktop/python專案/birthday/荷/答案資料夾/ho-eyes"
    NON_ANSWER_DIR = "/Users/cglinmacbook/Desktop/python專案/birthday/荷/非答案資料夾/others-eyes"

    if "q1_options" not in st.session_state:
        answer_imgs = get_image_files(ANSWER_DIR)
        if not answer_imgs:
            st.error("答案資料夾沒有圖片")
            st.stop()
        answer_img = random.choice(answer_imgs)
        non_answer_imgs = get_image_files(NON_ANSWER_DIR)
        if len(non_answer_imgs) < 3:
            st.error("非答案資料夎圖片不足三張")
            st.stop()
        non_answer_options = random.sample(non_answer_imgs, 3)
        options = [answer_img] + non_answer_options
        random.shuffle(options)
        st.session_state.q1_options = options
        st.session_state.q1_correct_idx = options.index(answer_img)
    else:
        options = st.session_state.q1_options
        correct_idx = st.session_state.q1_correct_idx

    cols = st.columns(4)
    selected = None
    for i, col in enumerate(cols):
        with col:
            st.image(options[i], width=120)
            if st.button(f"選擇 {i+1}", key=f"q1_opt{i}"):
                selected = i

    if selected is not None:
        st.session_state.show_answer = True
        if selected == st.session_state.q1_correct_idx:
            st.success("correct!")
        else:
            st.error("wrong ans XXX")

# ====== 單選題範例：legs ======
def question_2():
    st.subheader("legs")
    st.header("Which one is HO's legs?")
    st.write("請選出下列哪張圖片是 HO 的腿？")

    ANSWER_DIR = "/Users/cglinmacbook/Desktop/python專案/birthday/荷/答案資料夾/ho-legs"
    NON_ANSWER_DIR = "/Users/cglinmacbook/Desktop/python專案/birthday/荷/非答案資料夾/others-legs"

    if "q2_options" not in st.session_state:
        answer_imgs = get_image_files(ANSWER_DIR)
        if not answer_imgs:
            st.error("答案資料夾沒有圖片")
            st.stop()
        answer_img = random.choice(answer_imgs)
        non_answer_imgs = get_image_files(NON_ANSWER_DIR)
        if len(non_answer_imgs) < 3:
            st.error("非答案資料夎圖片不足三張")
            st.stop()
        non_answer_options = random.sample(non_answer_imgs, 3)
        options = [answer_img] + non_answer_options
        random.shuffle(options)
        st.session_state.q2_options = options
        st.session_state.q2_correct_idx = options.index(answer_img)
    else:
        options = st.session_state.q2_options
        correct_idx = st.session_state.q2_correct_idx

    cols = st.columns(4)
    selected = None
    for i, col in enumerate(cols):
        with col:
            st.image(options[i], width=120)
            if st.button(f"選擇 {i+1}", key=f"q2_opt{i}"):
                selected = i

    if selected is not None:
        st.session_state.show_answer = True
        if selected == st.session_state.q2_correct_idx:
            st.success("correct!")
        else:
            st.error("wrong ans XXX")

# ====== 圖片排序題範例 ======
def question_3():
    PHOTO_DIR = "/Users/cglinmacbook/Desktop/python專案/birthday/荷/答案資料夾/"

    # 只抓檔名為「檔案1」、「檔案2」…的圖片
    pattern = re.compile(r'^檔案\d+\.(png|jpg|jpeg|bmp|gif)$', re.IGNORECASE)
    photo_files = [
        f for f in os.listdir(PHOTO_DIR)
        if pattern.match(f)
    ]

    # 依檔案建立時間排序正確順序
    photo_files_with_ctime = [
        (f, os.path.getctime(os.path.join(PHOTO_DIR, f)))
        for f in photo_files
    ]
    correct_order = [
        f for f, _ in sorted(photo_files_with_ctime, key=lambda x: x[1])
    ]

    # ========== 初始化亂序 ==========
    if 'shuffled_photos' not in st.session_state:
        st.session_state.shuffled_photos = correct_order.copy()
        random.shuffle(st.session_state.shuffled_photos)

    if 'selected_photo' not in st.session_state:
        st.session_state.selected_photo = None

    st.header("圖片排序題")
    st.write("請將下列圖片按照正確順序排列。")

    cols = st.columns(len(st.session_state.shuffled_photos))
    for idx, col in enumerate(cols):
        with col:
            img_path = os.path.join(PHOTO_DIR, st.session_state.shuffled_photos[idx])
            st.image(img_path, width=120, caption=f"{idx+1}")

    st.write("請依序點選兩張圖片以互換位置。")
    col2s = st.columns(len(st.session_state.shuffled_photos))
    for idx, col in enumerate(col2s):
        with col:
            if st.button(f"選擇第{idx+1}張", key=f"pick_{idx}"):
                if st.session_state.selected_photo is None:
                    st.session_state.selected_photo = idx
                else:
                    i, j = st.session_state.selected_photo, idx
                    photos = st.session_state.shuffled_photos
                    photos[i], photos[j] = photos[j], photos[i]
                    st.session_state.shuffled_photos = photos
                    st.session_state.selected_photo = None
                    st.experimental_rerun()

    if st.button("送出答案"):
        if st.session_state.shuffled_photos == correct_order:
            st.success("答對了！排序正確。")
            st.session_state.show_answer = True
        else:
            st.error("答案錯誤，請再試一次。")
            st.session_state.show_answer = False

    if st.button("重新亂序"):
        st.session_state.shuffled_photos = correct_order.copy()
        random.shuffle(st.session_state.shuffled_photos)
        st.session_state.selected_photo = None
        st.experimental_rerun()

# ====== 主程式 ======
def quiz():
    st.header("圖片選擇與排序測驗")
    if "q_idx" not in st.session_state:
        st.session_state.q_idx = 0
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False

    questions = [question_1, question_2, question_3]
    q_idx = st.session_state.q_idx

    if q_idx < len(questions):
        questions[q_idx]()
        if st.session_state.show_answer:
            if st.button("下一題"):
                st.session_state.q_idx += 1
                st.session_state.show_answer = False
                st.experimental_rerun()
    else:
        st.success("測驗結束！")
        if st.button("重新開始"):
            st.session_state.q_idx = 0
            st.session_state.show_answer = False
            # 清除所有 session_state 的題目選項
            for key in list(st.session_state.keys()):
                if key.startswith("q") or key.startswith("shuffled") or key.startswith("selected"):
                    del st.session_state[key]
            st.experimental_rerun()

if __name__ == "__main__":
    quiz()