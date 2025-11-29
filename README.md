# 🎮 Othello（黒：あなた vs 白：AI） — Streamlit Reversi App

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

AI と対戦できるシンプルな **オセロ（リバーシ）ゲーム** です。  
黒がユーザー、白が AI（minimax アルゴリズム）です。

---

## 📺 デモ（動作版）

https://othello-ai.streamlit.app/

## 📌 主な特徴

- 🧠 **minimax + αβ法によるAI（3段階の強さ）**
- 🕒 **ユーザー着手後に5秒待ってから AI が着手**
- 🎨 **CSS で盤面の石ボタンを見やすく調整**
- ♟ **オセロの基本ルール（ひっくり返し処理）を実装**
- 🧩 **Streamlit の `session_state` による状態管理**
- 📝 **学習用・改造しやすいシンプルなコード構造**

---

## 📂 リポジトリ構成

├─ app.py # メインアプリ
├─ README.md # このドキュメント
└─ requirements.txt # 必要ライブラリ
---

## 🚀 実行方法

### 1. 仮想環境（任意）
```bash
python -m venv venv
source venv/bin/activate   # Windowsは venv\Scripts\activate

2. 必要ライブラリをインストール
pip install -r requirements.txt

3. アプリ実行
streamlit run app.py
ブラウザが自動で開きます。

🎮 遊び方
黒（あなた）が 先手
石を置ける場所は 緑の「✓」で表示
黒を置いたあと 5秒後に AI が白を置く
置ける場所が無くなるまで交互にプレイ
最終的に石の数で勝敗が決まる

🧠 AI（minimax アルゴリズム）
AI の強さは 3 段階です：
| 強さ | 読みの深さ |
| -- | ----- |
| 弱い | 1     |
| 普通 | 3     |
| 強い | 5     |

評価関数はシンプルに
白石 − 黒石
白に有利な盤ほど高得点となります。
アルファベータ法と再帰探索により効率化されています。

🧩 コード概要（理解しやすい解説）
1. CSS（ボタンを大きくする）
盤面ボタンが見やすいように CSS を注入しています。
2. ゲーム初期化
8×8 の盤を作り、初期配置の4石を置きます。
3. 置ける場所判定（is_valid_move）
「自分の石 → 相手の石 → 自分の石」がある方向を探します。
4. ひっくり返し処理（make_move）
8方向に向かって反転処理を行います。
5. AI（minimax）
先読みして最善手を選びます。
6. UI描画（ボタンで盤を表示）
● 黒
○ 白
✓ 置ける場所
を Streamlit のボタンで表示します。

例：
<img width="702" height="806" alt="image" src="https://github.com/user-attachments/assets/59d7c70c-264c-436e-911d-15e0a23749c7" />

🙌 著者

Created by 福田雅彦
GitHub: 
