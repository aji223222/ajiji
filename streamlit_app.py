import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# 多言語対応の辞書
TRANSLATIONS = {
    'ja': {
        'title': '日田市ナビゲーションアプリ',
        'mode': 'モード選択',
        'tourism': '観光モード',
        'disaster': '防災モード',
        'weather': '現在の天気',
        'language': '言語選択',
        'current_location': '現在地',
        'destination': '目的地',
        'transport': '交通手段',
        'walk': '徒歩',
        'bicycle': '自転車',
        'public': '公共交通機関',
        'car': '車',
        'route': 'ルート表示',
        'cost': '費用',
        'calendar': 'イベントカレンダー',
        'restaurants': 'おすすめ飲食店',
        'attractions': '観光地',
        'events': 'イベント',
        'evacuation': '避難所',
        'hazard_map': 'ハザードマップ',
        'budget': '予算',
        'plan_type': 'プランタイプ',
    },
    'en': {
        'title': 'Hita City Navigation App',
        'mode': 'Mode Selection',
        'tourism': 'Tourism Mode',
        'disaster': 'Disaster Prevention Mode',
        'weather': 'Current Weather',
        'language': 'Language',
        'current_location': 'Current Location',
        'destination': 'Destination',
        'transport': 'Transportation',
        'walk': 'Walk',
        'bicycle': 'Bicycle',
        'public': 'Public Transport',
        'car': 'Car',
        'route': 'Show Route',
        'cost': 'Cost',
        'calendar': 'Event Calendar',
        'restaurants': 'Recommended Restaurants',
        'attractions': 'Tourist Attractions',
        'events': 'Events',
        'evacuation': 'Evacuation Sites',
        'hazard_map': 'Hazard Map',
        'budget': 'Budget',
        'plan_type': 'Plan Type',
    },
    'zh': {
        'title': '日田市导航应用',
        'mode': '模式选择',
        'tourism': '旅游模式',
        'disaster': '防灾模式',
        'weather': '当前天气',
        'language': '语言',
        'current_location': '当前位置',
        'destination': '目的地',
        'transport': '交通方式',
        'walk': '步行',
        'bicycle': '自行车',
        'public': '公共交通',
        'car': '汽车',
        'route': '显示路线',
        'cost': '费用',
        'calendar': '活动日历',
        'restaurants': '推荐餐厅',
        'attractions': '旅游景点',
        'events': '活动',
        'evacuation': '避难所',
        'hazard_map': '灾害地图',
        'budget': '预算',
        'plan_type': '计划类型',
    },
    'ko': {
        'title': '히타시 내비게이션 앱',
        'mode': '모드 선택',
        'tourism': '관광 모드',
        'disaster': '방재 모드',
        'weather': '현재 날씨',
        'language': '언어',
        'current_location': '현재 위치',
        'destination': '목적지',
        'transport': '교통수단',
        'walk': '도보',
        'bicycle': '자전거',
        'public': '대중교통',
        'car': '자동차',
        'route': '경로 표시',
        'cost': '비용',
        'calendar': '이벤트 캘린더',
        'restaurants': '추천 레스토랑',
        'attractions': '관광지',
        'events': '이벤트',
        'evacuation': '대피소',
        'hazard_map': '재해 지도',
        'budget': '예산',
        'plan_type': '플랜 유형',
    }
}

# サンプルデータ（実際のアプリではAPIや데ータベースから取得）
HITA_CENTER = (33.3219, 130.9414)

SAMPLE_RESTAURANTS = [
    {'name': '日田焼きそば専門店', 'lat': 33.3219, 'lon': 130.9414, 'wait_time': '15分', 'crowded': '普通', 'hours': '11:00-20:00'},
    {'name': '鮎料理 かわせみ', 'lat': 33.3250, 'lon': 130.9450, 'wait_time': '30分', 'crowded': '混雑', 'hours': '11:30-21:00'},
    {'name': '豆田カフェ', 'lat': 33.3200, 'lon': 130.9380, 'wait_time': '5分', 'crowded': '空いている', 'hours': '9:00-18:00'},
]

SAMPLE_ATTRACTIONS = [
    {'name': '豆田町', 'lat': 33.3200, 'lon': 130.9380, 'stay_time': '2時間', 'category': '歴史'},
    {'name': '咸宜園', 'lat': 33.3280, 'lon': 130.9420, 'stay_time': '1.5時間', 'category': '歴史'},
    {'name': '日田温泉', 'lat': 33.3150, 'lon': 130.9350, 'stay_time': '3時間', 'category': '温泉'},
]

SAMPLE_EVENTS = [
    {'name': '日田天領まつり', 'month': 3, 'date': '3月中旬', 'poster': '🎌', 'info': '江戸時代の天領を再現したお祭り'},
    {'name': '日田川開き観光祭', 'month': 5, 'date': '5月下旬', 'poster': '🎆', 'info': '花火大会と水郷祭'},
    {'name': '日田祇園祭', 'month': 7, 'date': '7月', 'poster': '🏮', 'info': 'ユネスコ無形文化遺産'},
]

SAMPLE_EVACUATION = [
    {'name': '日田市役所', 'lat': 33.3219, 'lon': 130.9414, 'capacity': 500, 'current': 120},
    {'name': '三隈中学校', 'lat': 33.3180, 'lon': 130.9350, 'capacity': 800, 'current': 200},
    {'name': '豆田小学校', 'lat': 33.3200, 'lon': 130.9380, 'capacity': 600, 'current': 150},
]

def get_translation(lang, key):
    return TRANSLATIONS.get(lang, TRANSLATIONS['ja']).get(key, key)

def create_map(center, markers=None, evacuation_mode=False):
    m = folium.Map(location=center, zoom_start=14)
    
    if markers:
        for marker in markers:
            color = 'red' if evacuation_mode else 'blue'
            folium.Marker(
                [marker['lat'], marker['lon']],
                popup=marker.get('name', 'Location'),
                icon=folium.Icon(color=color)
            ).add_to(m)
    
    return m

def calculate_route(start, end, transport):
    # 実際のアプリではルーティングAPIを使用
    distance = geodesic(start, end).kilometers
    
    if transport == 'walk':
        time = distance * 12  # 徒歩：約5km/h
        cost = 0
    elif transport == 'bicycle':
        time = distance * 4  # 自転車：約15km/h
        cost = 0
    elif transport == 'public':
        time = distance * 3  # 公共交通
        cost = int(distance * 200)  # 概算
    else:  # car
        time = distance * 2  # 車：約30km/h（市内）
        cost = int(distance * 50)  # ガソリン代概算
    
    return {'distance': round(distance, 2), 'time': int(time), 'cost': cost}

def main():
    # セッション状態の初期化
    if 'language' not in st.session_state:
        st.session_state.language = 'ja'
    if 'mode' not in st.session_state:
        st.session_state.mode = 'tourism'
    
    lang = st.session_state.language
    
    # サイドバー
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # 言語選択
        language_options = {'日本語': 'ja', 'English': 'en', '中文': 'zh', '한국어': 'ko'}
        selected_lang = st.selectbox(
            get_translation(lang, 'language'),
            options=list(language_options.keys()),
            index=list(language_options.values()).index(lang)
        )
        st.session_state.language = language_options[selected_lang]
        lang = st.session_state.language
        
        # モード選択
        mode = st.radio(
            get_translation(lang, 'mode'),
            [get_translation(lang, 'tourism'), get_translation(lang, 'disaster')]
        )
        st.session_state.mode = 'tourism' if mode == get_translation(lang, 'tourism') else 'disaster'
    
    # メインタイトル
    st.title(get_translation(lang, 'title'))
    
    # 天気情報（サンプル）
    with st.expander(f"🌤️ {get_translation(lang, 'weather')}"):
        st.write("**日田市**")
        st.write("気温: 18°C | 天気: 晴れ | 湿度: 65%")
        st.write("予報: 本日は晴れ、明日は曇り時々雨")
    
    # 観光モード
    if st.session_state.mode == 'tourism':
        st.header(f"🏞️ {get_translation(lang, 'tourism')}")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            get_translation(lang, 'restaurants'),
            get_translation(lang, 'attractions'),
            get_translation(lang, 'events'),
            get_translation(lang, 'calendar')
        ])
        
        with tab1:
            st.subheader(get_translation(lang, 'restaurants'))
            for restaurant in SAMPLE_RESTAURANTS:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{restaurant['name']}**")
                        st.write(f"待ち時間: {restaurant['wait_time']} | 混雑: {restaurant['crowded']}")
                        st.write(f"営業時間: {restaurant['hours']}")
                    with col2:
                        if st.button('選択', key=f"rest_{restaurant['name']}"):
                            st.session_state.selected_destination = (restaurant['lat'], restaurant['lon'])
                    st.divider()
            
            # マップ表示
            m = create_map(HITA_CENTER, SAMPLE_RESTAURANTS)
            folium_static(m, width=700, height=400)
        
        with tab2:
            st.subheader(get_translation(lang, 'attractions'))
            
            # 月別人気ベスト3
            st.write("### 今月の人気ベスト3")
            for i, attr in enumerate(SAMPLE_ATTRACTIONS[:3], 1):
                st.write(f"{i}. **{attr['name']}** - 滞在時間: {attr['stay_time']}")
            
            st.divider()
            
            # プラン選択
            plan_type = st.selectbox(
                get_translation(lang, 'plan_type'),
                ['家族プラン', '一人旅プラン', '0-5,000円', '5,001-10,000円', '10,001-30,000円', '30,000円以上']
            )
            
            for attraction in SAMPLE_ATTRACTIONS:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{attraction['name']}**")
                        st.write(f"推奨滞在時間: {attraction['stay_time']} | カテゴリ: {attraction['category']}")
                    with col2:
                        if st.button('選択', key=f"attr_{attraction['name']}"):
                            st.session_state.selected_destination = (attraction['lat'], attraction['lon'])
                    st.divider()
            
            m = create_map(HITA_CENTER, SAMPLE_ATTRACTIONS)
            folium_static(m, width=700, height=400)
        
        with tab3:
            st.subheader(get_translation(lang, 'events'))
            
            # 月別フィルター
            selected_month = st.slider('月を選択', 1, 12, datetime.now().month)
            
            filtered_events = [e for e in SAMPLE_EVENTS if e['month'] == selected_month]
            
            if filtered_events:
                for event in filtered_events:
                    with st.expander(f"{event['poster']} {event['name']}"):
                        st.write(f"**開催時期:** {event['date']}")
                        st.write(f"**詳細:** {event['info']}")
            else:
                st.info("この月にはイベントがありません")
        
        with tab4:
            st.subheader(get_translation(lang, 'calendar'))
            
            # 年間イベントカレンダー
            for month in range(1, 13):
                month_events = [e for e in SAMPLE_EVENTS if e['month'] == month]
                if month_events:
                    st.write(f"### {month}月")
                    for event in month_events:
                        st.write(f"- {event['name']}: {event['date']}")
    
    # 防災モード
    else:
        st.header(f"🚨 {get_translation(lang, 'disaster')}")
        
        tab1, tab2, tab3 = st.tabs([
            get_translation(lang, 'evacuation'),
            get_translation(lang, 'hazard_map'),
            '防災グッズ'
        ])
        
        with tab1:
            st.subheader('避難所情報')
            
            for shelter in SAMPLE_EVACUATION:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{shelter['name']}**")
                    with col2:
                        remaining = shelter['capacity'] - shelter['current']
                        st.write(f"収容可能: {remaining}人")
                    with col3:
                        occupancy = (shelter['current'] / shelter['capacity']) * 100
                        st.progress(occupancy / 100)
                        st.write(f"{occupancy:.0f}%")
                    st.divider()
            
            # 避難所マップ
            m = create_map(HITA_CENTER, SAMPLE_EVACUATION, evacuation_mode=True)
            folium_static(m, width=700, height=400)
            
            st.info("🚰 自動販売機の位置も地図に表示されます")
        
        with tab2:
            st.subheader(get_translation(lang, 'hazard_map'))
            st.write("### 日田市ハザードマップ")
            
            hazard_type = st.selectbox(
                'ハザードマップの種類',
                ['洪水', '土砂災害', '地震', '津波']
            )
            
            # ハザードマップ表示（サンプル）
            m = create_map(HITA_CENTER)
            # 実際のアプリでは危険区域をポリゴンで表示
            folium_static(m, width=700, height=400)
            
            st.warning(f"⚠️ {hazard_type}の危険区域が赤色で表示されています")
        
        with tab3:
            st.subheader('防災グッズ提案')
            
            budget = st.select_slider(
                get_translation(lang, 'budget'),
                options=[5000, 10000, 20000, 30000, 50000],
                value=10000,
                format_func=lambda x: f"¥{x:,}"
            )
            
            st.write(f"### 予算 ¥{budget:,} でのおすすめ防災グッズ")
            
            if budget >= 5000:
                st.write("✅ 非常用飲料水（2L×6本）")
                st.write("✅ 非常食セット（3日分）")
                st.write("✅ 懐中電灯＋電池")
            if budget >= 10000:
                st.write("✅ 防災ラジオ")
                st.write("✅ 救急セット")
                st.write("✅ 携帯トイレ")
            if budget >= 20000:
                st.write("✅ 寝袋・毛布")
                st.write("✅ 発電機（小型）")
            if budget >= 30000:
                st.write("✅ 浄水器")
                st.write("✅ テント")
    
    # ナビゲーション機能
    st.header("🗺️ ナビゲーション")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**{get_translation(lang, 'current_location')}**")
        current_lat = st.number_input('緯度', value=HITA_CENTER[0], format="%.6f", key='curr_lat')
        current_lon = st.number_input('経度', value=HITA_CENTER[1], format="%.6f", key='curr_lon')
        
        if st.button('📍 GPS取得'):
            st.info('GPS機能を使用するにはブラウザの位置情報許可が必要です')
    
    with col2:
        st.write(f"**{get_translation(lang, 'destination')}**")
        dest_lat = st.number_input('緯度', value=33.3200, format="%.6f", key='dest_lat')
        dest_lon = st.number_input('経度', value=130.9380, format="%.6f", key='dest_lon')
    
    # 複数目的地選択
    num_destinations = st.number_input('目的地の数', min_value=1, max_value=5, value=1)
    
    # 交通手段選択
    transport = st.radio(
        get_translation(lang, 'transport'),
        [get_translation(lang, 'walk'), get_translation(lang, 'bicycle'), 
         get_translation(lang, 'public'), get_translation(lang, 'car')]
    )
    
    transport_map = {
        get_translation(lang, 'walk'): 'walk',
        get_translation(lang, 'bicycle'): 'bicycle',
        get_translation(lang, 'public'): 'public',
        get_translation(lang, 'car'): 'car'
    }
    
    if st.button(f"🚀 {get_translation(lang, 'route')}"):
        start = (current_lat, current_lon)
        end = (dest_lat, dest_lon)
        
        route_info = calculate_route(start, end, transport_map[transport])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("距離", f"{route_info['distance']} km")
        with col2:
            st.metric("所要時間", f"{route_info['time']} 分")
        with col3:
            st.metric(get_translation(lang, 'cost'), f"¥{route_info['cost']}")
        
        # ルートマップ
        m = folium.Map(location=start, zoom_start=13)
        folium.Marker(start, popup='出発地', icon=folium.Icon(color='green')).add_to(m)
        folium.Marker(end, popup='目的地', icon=folium.Icon(color='red')).add_to(m)
        folium.PolyLine([start, end], color='blue', weight=5, opacity=0.7).add_to(m)
        folium_static(m, width=700, height=400)

if __name__ == '__main__':
    main()