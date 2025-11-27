import streamlit as st
import numpy as np
import time

# -------------------------------------------------------
# CSS（ボタンのフォントサイズ・色などを大きくする）
# -------------------------------------------------------
st.markdown("""
<style>
button[kind="primary"] {
    font-size: 28px !important;
    font-weight: bold !important;
}
div[data-testid="stButton"] > button {
    font-size: 28px !important;
    font-weight: bold !important;
    height: 60px !important;
    width: 60px !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# ゲーム初期化
# -------------------------------------------------------
def init_board():
    board = np.zeros((8, 8), dtype=int)
    board[3][3] = board[4][4] = -1  # 白
    board[3][4] = board[4][3] = 1   # 黒
    st.session_state.board = board
    st.session_state.current = 1   # 黒のターン
    st.session_state.ai_pending = False
    st.session_state.game_over = False


# 初回のみ初期化
if "board" not in st.session_state:
    init_board()


# -------------------------------------------------------
# Othello ルール
# -------------------------------------------------------
def is_valid_move(row, col, player):
    board = st.session_state.board
    if board[row][col] != 0:
        return False

    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    for dr, dc in dirs:
        r, c = row + dr, col + dc
        found = False
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == -player:
            found = True
            r += dr
            c += dc

        if found and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            return True
    return False


def get_valid_moves(player):
    return [(r,c) for r in range(8) for c in range(8) if is_valid_move(r,c,player)]


def make_move(row, col, player):
    if not is_valid_move(row, col, player):
        return False

    board = st.session_state.board
    board[row][col] = player

    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for dr, dc in dirs:
        r, c = row + dr, col + dc
        flips = []

        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == -player:
            flips.append((r, c))
            r += dr
            c += dc

        if flips and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for fr, fc in flips:
                board[fr][fc] = player

    return True


def evaluate_board():
    b = st.session_state.board
    return np.sum(b == -1) - np.sum(b == 1)


# -------------------------------------------------------
# minimax（AIの強さ調整）
# -------------------------------------------------------
def minimax(depth, maximizing, alpha=float('-inf'), beta=float('inf')):
    board = st.session_state.board

    if depth == 0:
        return evaluate_board(), None

    player = -1 if maximizing else 1
    moves = get_valid_moves(player)

    if not moves:
        return evaluate_board(), None

    if maximizing:
        best, best_move = float('-inf'), None
        for r, c in moves:
            backup = board.copy()
            make_move(r, c, -1)
            val, _ = minimax(depth-1, False, alpha, beta)
            board[:, :] = backup

            if val > best:
                best, best_move = val, (r, c)

            alpha = max(alpha, val)
            if beta <= alpha:
                break

        return best, best_move

    else:
        best, best_move = float('inf'), None
        for r, c in moves:
            backup = board.copy()
            make_move(r, c, 1)
            val, _ = minimax(depth-1, True, alpha, beta)
            board[:, :] = backup

            if val < best:
                best, best_move = val, (r, c)

            beta = min(beta, val)
            if beta <= alpha:
                break

        return best, best_move


def ai_move():
    difficulty = st.session_state.ai_level
    depth = {"弱い":1, "普通":3, "強い":5}[difficulty]

    _, move = minimax(depth, True)

    if move:
        make_move(move[0], move[1], -1)


# -------------------------------------------------------
# UI
# -------------------------------------------------------
st.title("🎮 Othello（黒：あなた vs 白：AI）")

st.markdown("""
### 📝 遊び方
- あなた（黒 ●）が先手  
- 打てる場所は **緑「✓」** で表示  
- 黒を置いたあと **5秒後にAIが白を置きます**  
- 「新しいゲーム」でリセット  
""")

# AIの強さ選択
ai_level = st.sidebar.selectbox("AIの強さ", ["弱い", "普通", "強い"])
st.session_state.ai_level = ai_level

if st.button("🔄 新しいゲーム"):
    init_board()
    st.rerun()


board = st.session_state.board
moves = get_valid_moves(1)


# -------------------------------------------------------
# AI の遅延処理（5秒）
# -------------------------------------------------------
if st.session_state.ai_pending:
    time.sleep(5)
    ai_move()
    st.session_state.ai_pending = False
    st.session_state.current = 1
    st.rerun()


# -------------------------------------------------------
# 盤の表示（gap="small"）
# -------------------------------------------------------
for r in range(8):
    cols = st.columns(8, gap="small")
    for c in range(8):
        val = board[r][c]

        # 黒
        if val == 1:
            cols[c].button("●", key=f"{r}{c}", disabled=True)

        # 白
        elif val == -1:
            cols[c].button("○", key=f"{r}{c}", disabled=True)

        # 置ける場所
        elif (r,c) in moves:
            press = cols[c].button("✓", key=f"{r}{c}")
            if press:
                make_move(r, c, 1)
                st.session_state.current = -1
                st.session_state.ai_pending = True
                st.rerun()

        else:
            cols[c].button("", key=f"{r}{c}", disabled=True)


# -------------------------------------------------------
# スコアと勝敗表示
# -------------------------------------------------------
black = np.sum(board == 1)
white = np.sum(board == -1)

st.subheader(f"● 黒: {black}    ○ 白(AI): {white}")

# 勝敗判定
if not get_valid_moves(1) and not get_valid_moves(-1):
    st.session_state.game_over = True

if st.session_state.game_over:
    st.markdown("---")
    if black > white:
        st.success("🎉 **あなたの勝ち！**")
    elif white > black:
        st.error("🤖 **AIの勝ち！**")
    else:
        st.info("🤝 **引き分け**")
