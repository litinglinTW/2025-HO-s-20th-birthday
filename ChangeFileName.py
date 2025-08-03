#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 10:42:32 2025

@author: cglinmacbook
"""

import os

def rename_files_in_folder(folder_path, prefix="file", exts=None):
    """
    統一更名資料夾內檔案
    :param folder_path: 資料夾路徑
    :param prefix: 檔名開頭
    :param exts: 限定副檔名，如 ['.jpg', '.png']
    """
    
    try:
        files = [f for f in os.listdir(folder_path)
                 if os.path.isfile(os.path.join(folder_path, f))]
    except FileNotFoundError:
        print(f"\033[91m[錯誤] 找不到資料夾：{folder_path}\033[0m")
        return

    # 過濾副檔名
    if exts:
        exts = [e.lower() for e in exts]
        files = [f for f in files if os.path.splitext(f)[1].lower() in exts]
    if not files:
        print("\033[93m[提示] 沒有符合的檔案\033[0m")
        return

    files.sort()  # 按檔名排序
    for idx, filename in enumerate(files, start=1):
        ext = os.path.splitext(filename)[1]
        new_name = f"{prefix}_{idx:03d}{ext}"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        # 處理新檔名若已存在
        counter = idx
        while os.path.exists(new_path) and filename != new_name:
            counter += 1
            new_name = f"{prefix}_{counter:03d}{ext}"
            new_path = os.path.join(folder_path, new_name)

        if filename == new_name:
            print(f"\033[96m[略過] {repr(filename)} 已是目標名稱\033[0m")
            continue

        try:
            os.rename(old_path, new_path)
            print(f"\033[92m[成功] {repr(filename)} → {repr(new_name)}\033[0m")
        except Exception as e:
            print(f"\033[91m[失敗] {repr(filename)} 無法改名：{e}\033[0m")

if __name__ == "__main__":
    folder = input("請輸入資料夾路徑：").strip()
    prefix = input("請輸入檔名前綴字 (預設 file)：").strip() or "file"
    ext_input = input("只針對哪些副檔名更名？(用逗號分隔, 留空全檔案)：").strip()
    exts = [e if e.startswith('.') else '.' + e for e in ext_input.split(',') if e] if ext_input else None

    rename_files_in_folder(folder, prefix, exts)
    
    
    
    
    