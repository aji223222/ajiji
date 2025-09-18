import streamlit as st
import pandas as pd

# データの準備（今回はダミーデータを使用）
data = {
    'タイトル': ['The Last of Us Part I', 'God of War Ragnarök', 'ELDEN RING', 'Marvel\'s Spider-Man 2', 'FINAL FANTASY VII REBIRTH'],
    'ジャンル': ['アクション', 'アクションRPG', 'アクションRPG', 'アクションアドベンチャー', 'RPG'],
    '評価': [96, 94, 95, 90, 92],
    'プレイ時間(h)': [15, 25, 60, 15, 40]
}
df = pd.DataFrame(data)

st.title('🎮 PlayStationゲームおすすめアプリ')
st.write('あなたの好みに合わせて、おすすめのPlayStationソフトを提案します。')

st.header('1. ゲームの好みを教えてください')

# ジャンルの選択
genre_list = df['ジャンル'].unique()
selected_genre = st.selectbox('好きなジャンルを選んでください', genre_list)

# 評価の選択
min_rating = st.slider('最低評価（メタスコア）', 80, 100, 90)

# プレイ時間の選択
max_playtime = st.slider('最大プレイ時間（時間）', 10, 100, 30)

# おすすめを提案するボタン
if st.button('おすすめのゲームを提案する'):
    st.header('2. あなたへのおすすめ')
    
    # ユーザーの選択に基づいてフィルタリング
    filtered_df = df[
        (df['ジャンル'] == selected_genre) &
        (df['評価'] >= min_rating) &
        (df['プレイ時間(h)'] <= max_playtime)
    ]

    # 結果の表示
    if not filtered_df.empty:
        st.write('以下のゲームがおすすめです。')
        st.table(filtered_df)
    else:
        st.write('条件に合うゲームが見つかりませんでした。別の条件を試してください。')

st.sidebar.markdown("""
---
### アプリについて
このアプリはStreamlitとPythonを使って作成されています。
データは架空のものです。
""")