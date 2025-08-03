#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 22:53:13 2025

@author: cglinmacbook
"""
import streamlit as st
import os
import random

# ======== 共用工具函式 ========
def get_image_files(folder):
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
    ]

# ======== 題目設定，每題指定答案/非答案資料夾 ========
QUESTIONS = [
    {
        "question": "which one are HO's eyes？",
        "answer_dir": "荷/答案資料夾/ho-eyes",      # 相對路徑
        "non_answer_dir": "荷/非答案資料夾/others-eyes",
        "explanation": "difficulty: 3/5"
    },
    {
        "question": "which one are HO's legs？",
        "answer_dir": "荷/答案資料夾/ho-legs",
        "non_answer_dir": "荷/非答案資料夾/others-legs",
        "explanation": "difficulty: 3.5/5"
    },
    {
        "question": "which one is HO's face？",
        "answer_dir": "荷/答案資料夾/ho-face",
        "non_answer_dir": "荷/非答案資料夾/others-face",
        "explanation": "difficulty: 1/5"
    },
    {
        "question": "which one is HO's mouth？",
        "answer_dir": "荷/答案資料夾/ho-mouth",
        "non_answer_dir": "荷/非答案資料夾/others-mouth",
        "explanation": "difficulty: 4/5"
    },
    {
        "question": "which one is HO？",
        "answer_dir": "荷/答案資料夾/ho-ponytails",
        "non_answer_dir": "荷/非答案資料夾/ponytails",
        "explanation": "difficulty: 4.5/5"
    },
    {
        "question": "which one is HO？",
        "answer_dir": "荷/答案資料夾/ho-face",
        "non_answer_dir": "荷/答案資料夾/ho-face",
        "explanation": "difficulty: 5/5 all of them are HOHO. really difficult . but 我沒時間改ㄌ"
    },
]

RANKING_PATH = "quiz_ranking.json"

def load_ranking():
    if os.path.exists(RANKING_PATH):
        import json
        with open(RANKING_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_ranking(ranking):
    import json
    with open(RANKING_PATH, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)

# ======== 單題圖片選擇邏輯 ========
def photo_choice_question(question_idx):
    q = QUESTIONS[question_idx]
    ans_key = f"q{question_idx}_options"
    correct_idx_key = f"q{question_idx}_correct_idx"
    result_key = f"q{question_idx}_answered"
    selected_key = f"q{question_idx}_selected"

    # 只在第一次進入該題時產生選項
    if ans_key not in st.session_state:
        answer_imgs = get_image_files(q["answer_dir"])
        if not answer_imgs:
            st.error("答案資料夾沒有圖片")
            st.stop()
        answer_img = random.choice(answer_imgs)

        non_answer_imgs = get_image_files(q["non_answer_dir"])
        if len(non_answer_imgs) < 3:
            st.error("非答案資料夾圖片不足三張")
            st.stop()
        non_answer_options = random.sample(non_answer_imgs, 3)
        options = [answer_img] + non_answer_options
        random.shuffle(options)
        st.session_state[ans_key] = options
        st.session_state[correct_idx_key] = options.index(answer_img)
        st.session_state[result_key] = False
        st.session_state[selected_key] = None

    options = st.session_state[ans_key]
    st.subheader(f"question {question_idx+1} 題")
    st.write(q["question"])
    cols = st.columns(4)
    selected = None
    for i, col in enumerate(cols):
        with col:
            st.image(options[i], width=120)
            if st.button(f"選擇 {i+1}", key=f"{ans_key}_opt{i}"):
                selected = i

    # 只允許作答一次
    if selected is not None and not st.session_state[result_key]:
        st.session_state[result_key] = True
        st.session_state[selected_key] = selected
        correct_idx = st.session_state[correct_idx_key]
        if selected == correct_idx:
            st.session_state["score"] += 1
            st.session_state["last_is_correct"] = True
        else:
            st.session_state["last_is_correct"] = False
        st.session_state["show_answer"] = True
        st.experimental_rerun()

    # 顯示答案與說明
    if st.session_state[result_key]:
        correct_idx = st.session_state[correct_idx_key]
        correct_img = options[correct_idx]
        user_selected = st.session_state[selected_key]
        if st.session_state["last_is_correct"]:
            st.success("good！")
        else:
            st.error("wrong囉～")
        st.info("correct如下：")
        st.image(correct_img, caption="正確答案", width=120)
        st.write(f"【說明】{q['explanation']}")
        if st.button("next", key=f"next_{question_idx}"):
            st.session_state.q_idx += 1
            st.session_state.show_answer = False
            # 清除本題狀態
            for key in [ans_key, correct_idx_key, result_key, selected_key, "last_is_correct"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()

# ======= 主流程 =======

def quiz():
    # 1. 先輸入名字
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""
    if not st.session_state.player_name:
        name = st.text_input("請輸入你的名字name")
        if st.button("enter"):
            if name:
                st.session_state.player_name = name
        st.stop()
    
    # 2. 遊戲進度/分數狀態
    if "q_idx" not in st.session_state:
        st.session_state.q_idx = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    
    # 3. 題目輪詢
    if st.session_state.q_idx < len(QUESTIONS):
        photo_choice_question(st.session_state.q_idx)
    else:
        # 4. 遊戲結束，顯示分數與排行榜
        st.header("遊戲結束！")
        st.write(f"你的得分：{st.session_state.score} / {len(QUESTIONS)}")
    
        # 排行榜處理
        ranking = load_ranking()
        ranking.append({"name": st.session_state.player_name, "score": st.session_state.score})
        ranking = sorted(ranking, key=lambda x: x['score'], reverse=True)[:20]
        save_ranking(ranking)
    
        st.subheader("ranking (only on the same device)")
        for i, entry in enumerate(ranking, 1):
            st.write(f"{i}. {entry['name']} - {entry['score']} 分")
    
        if st.button("重新開始遊戲 play again(the pictures are random 美燦看都不一一ㄤ)"):
            for key in list(st.session_state.keys()):
                if key not in {"player_name"}:
                    del st.session_state[key]
            st.session_state.score = 0
            st.session_state.q_idx = 0
            st.experimental_rerun()
            
            
            
            
            
            
            
            
            
            
            
            