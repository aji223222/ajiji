import streamlit as st
import pandas as pd
import datetime

# 実際のPlayStationソフトのダミーデータ（大規模版）
data = {
    'タイトル': [
        'FINAL FANTASY VII REBIRTH', 'ELDEN RING', 'God of War Ragnarök',
        'Marvel\'s Spider-Man 2', 'Ghost of Tsushima', 'Hogwarts Legacy',
        'Demon\'s Souls', 'Persona 5 Royal', 'The Last of Us Part I',
        'Horizon Forbidden West', 'Red Dead Redemption 2', 'Cyberpunk 2077',
        'Grand Theft Auto V', 'The Witcher 3: Wild Hunt', 'Uncharted 4: A Thief\'s End',
        'Bloodborne', 'Sekiro: Shadows Die Twice', 'Resident Evil 4',
        'Nioh 2', 'Yakuza: Like a Dragon', 'Dragon Quest XI S',
        'Tales of Arise', 'Genshin Impact', 'Stellar Blade',
        'Helldivers 2', 'Baldur\'s Gate 3', 'NieR:Automata',
        'Death Stranding', 'Returnal', 'Ratchet & Clank: Rift Apart'
    ],
    'ジャンル': [
        'RPG', 'アクションRPG', 'アクションアドベンチャー',
        'アクションアドベンチャー', 'アクションアドベンチャー', 'アクションRPG',
        'アクションRPG', 'RPG', 'アクションアドベンチャー',
        'アクションRPG', 'アクションアドベンチャー', 'アクションRPG',
        'アクションアドベンチャー', 'RPG', 'アクションアドベンチャー',
        'アクションRPG', 'アクションアドベンチャー', 'ホラー',
        'アクションRPG', 'RPG', 'RPG',
        'RPG', 'アクションRPG', 'アクションアドベンチャー',
        'アクションシューター', 'RPG', 'アクションRPG',
        'アクションアドベンチャー', 'アクションシューター', 'アクションアドベンチャー'
    ],
    '評価(Metacritic)': [
        92, 96, 94,
        90, 83, 84,
        92, 95, 88,
        88, 97, 86,
        97, 92, 93,
        92, 91, 93,
        85, 84, 91,
        87, 81, 80,
        83, 96, 88,
        82, 87, 88
    ],
    'プレイ時間(h)': [
        40, 60, 25,
        15, 45, 30,
        20, 100, 15,
        30, 50, 60,
        30, 50, 15,
        30, 25, 18,
        35, 45, 60,
        30, 200, 25,
        40, 100, 25,
        40, 20, 15
    ],
    '発売年': [
        2024, 2022, 2022,
        2023, 2020, 2023,
        2020, 2020, 2022,
        2022, 2018, 2020,
        2013, 2015, 2016,
        2015, 2019, 2023,
        2020, 2020, 2019,
        2021, 2020, 2024,
        2024, 2023, 2017,
        2019, 2021, 2021
    ],
    '対応機種': [
        'PS5', 'PS4/PS5', 'PS4/PS5',
        'PS5', 'PS4/PS5', 'PS4/PS5',
        'PS5', 'PS4', 'PS5',
        'PS4/PS5', 'PS4', 'PS4/PS5',
        'PS4', 'PS4/PS5', 'PS4',
        'PS4', 'PS4/PS5', 'PS5',
        'PS4/PS5', 'PS4', 'PS4/PS5',
        'PS4/PS5', 'PS4/PS5', 'PS5',
        'PS5', 'PS5', 'PS4',
        'PS4', 'PS5', 'PS5'
    ]
}
df = pd.DataFrame(data)

st.title('🎮 PlayStationゲームおすすめアプリ')
st.write('あなたの好みに合わせて、おすすめのPlayStationソフトを提案します。')
st.divider()

st.header('1. ゲームの好みを教えてください')

# ジャンルの選択
genre_list = ['全て'] + sorted(df['ジャンル'].unique().tolist())
selected_genre = st.selectbox('好きなジャンルを選んでください', genre_list)

# 評価の選択
min_rating = st.slider('最低評価（Metacriticスコア）', 70, 100, 85)

# プレイ時間の選択
max_playtime = st.slider('最大プレイ時間（時間）', 10, 250, 50)

# 発売年の選択
current_year = datetime.datetime.now().year
min_year = st.slider('最低発売年', 2010, current_year, 2020)

# おすすめを提案するボタン
if st.button('おすすめのゲームを提案する', use_container_width=True):
    st.divider()
    st.header('2. あなたへのおすすめ')
    
    # ユーザーの選択に基づいてフィルタリング
    filtered_df = df[
        (df['評価(Metacritic)'] >= min_rating) &
        (df['プレイ時間(h)'] <= max_playtime) &
        (df['発売年'] >= min_year)
    ]

    # ジャンルでフィルタリング（'全て'が選択された場合はフィルタリングしない）
    if selected_genre != '全て':
        filtered_df = filtered_df[filtered_df['ジャンル'] == selected_genre]

    # 結果の表示
    if not filtered_df.empty:
        st.write('以下のゲームがおすすめです。')
        # インデックスを非表示にして表示
        st.dataframe(filtered_df.reset_index(drop=True))
    else:
        st.warning('条件に合うゲームが見つかりませんでした。別の条件を試してください。')

st.divider()
st.sidebar.info('このアプリはPythonとStreamlitで作成されています。データの出典は架空のものです。')