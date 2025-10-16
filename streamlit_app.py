import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import json
from geopy.distance import geodesic
import io

# ページ設定
st.set_page_config(
    page_title="日田ナビ - Hita Navi",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 多言語翻訳データ
TRANSLATIONS = {
    'ja': {
        'app_name': '日田ナビ',
        'mode_selection': 'モード選択',
        'tourism_mode': '観光モード',
        'disaster_mode': '防災モード',
        'weather_info': '天気情報',
        'language': '言語',
        'current_location': '現在地',
        'destination': '目的地',
        'navigation': 'ナビゲーション',
        'route': 'ルート案内',
        'distance': '距離',
        'time': '所要時間',
        'transport': '交通手段',
        'walk': '徒歩',
        'bicycle': '自転車',
        'public_transport': '公共交通',
        'car': '車',
        'cost': '費用',
        'attractions': '観光地',
        'restaurants': '飲食店',
        'events': 'イベント',
        'calendar': 'イベントカレンダー',
        'ranking': '人気ランキング',
        'plan': 'おすすめプラン',
        'evacuation': '避難所',
        'hazard_map': 'ハザードマップ',
        'disaster_goods': '防災グッズ',
        'upload_data': 'データアップロード',
        'select_spot': 'スポットを選択',
        'show_route': 'ルートを表示',
        'get_gps': 'GPS取得',
        'traffic_info': '交通状況',
        'wait_time': '待ち時間',
        'crowded': '混雑状況',
        'hours': '営業時間',
        'capacity': '収容可能人数',
        'occupancy': '収容率',
        'open_stores': '営業中の店舗',
        'vending_machines': '自動販売機',
        'budget': '予算',
        'family_plan': '家族向けプラン',
        'solo_plan': '一人旅プラン',
    },
    'en': {
        'app_name': 'Hita Navi',
        'mode_selection': 'Mode Selection',
        'tourism_mode': 'Tourism Mode',
        'disaster_mode': 'Disaster Prevention Mode',
        'weather_info': 'Weather Information',
        'language': 'Language',
        'current_location': 'Current Location',
        'destination': 'Destination',
        'navigation': 'Navigation',
        'route': 'Route Guide',
        'distance': 'Distance',
        'time': 'Duration',
        'transport': 'Transportation',
        'walk': 'Walk',
        'bicycle': 'Bicycle',
        'public_transport': 'Public Transport',
        'car': 'Car',
        'cost': 'Cost',
        'attractions': 'Attractions',
        'restaurants': 'Restaurants',
        'events': 'Events',
        'calendar': 'Event Calendar',
        'ranking': 'Popular Ranking',
        'plan': 'Recommended Plans',
        'evacuation': 'Evacuation Sites',
        'hazard_map': 'Hazard Map',
        'disaster_goods': 'Emergency Supplies',
        'upload_data': 'Upload Data',
        'select_spot': 'Select Spot',
        'show_route': 'Show Route',
        'get_gps': 'Get GPS',
        'traffic_info': 'Traffic Information',
        'wait_time': 'Wait Time',
        'crowded': 'Crowdedness',
        'hours': 'Business Hours',
        'capacity': 'Capacity',
        'occupancy': 'Occupancy Rate',
        'open_stores': 'Open Stores',
        'vending_machines': 'Vending Machines',
        'budget': 'Budget',
        'family_plan': 'Family Plan',
        'solo_plan': 'Solo Travel Plan',
    },
    'zh': {
        'app_name': '日田导航',
        'mode_selection': '模式选择',
        'tourism_mode': '旅游模式',
        'disaster_mode': '防灾模式',
        'weather_info': '天气信息',
        'language': '语言',
        'current_location': '当前位置',
        'destination': '目的地',
        'navigation': '导航',
        'route': '路线指南',
        'distance': '距离',
        'time': '所需时间',
        'transport': '交通方式',
        'walk': '步行',
        'bicycle': '自行车',
        'public_transport': '公共交通',
        'car': '汽车',
        'cost': '费用',
        'attractions': '景点',
        'restaurants': '餐厅',
        'events': '活动',
        'calendar': '活动日历',
        'ranking': '人气排行',
        'plan': '推荐计划',
        'evacuation': '避难所',
        'hazard_map': '灾害地图',
        'disaster_goods': '防灾用品',
        'upload_data': '上传数据',
        'select_spot': '选择地点',
        'show_route': '显示路线',
        'get_gps': '获取GPS',
        'traffic_info': '交通状况',
        'wait_time': '等待时间',
        'crowded': '拥挤程度',
        'hours': '营业时间',
        'capacity': '容量',
        'occupancy': '占用率',
        'open_stores': '营业店铺',
        'vending_machines': '自动售货机',
        'budget': '预算',
        'family_plan': '家庭计划',
        'solo_plan': '独行计划',
    },
    'ko': {
        'app_name': '히타 내비',
        'mode_selection': '모드 선택',
        'tourism_mode': '관광 모드',
        'disaster_mode': '방재 모드',
        'weather_info': '날씨 정보',
        'language': '언어',
        'current_location': '현재 위치',
        'destination': '목적지',
        'navigation': '내비게이션',
        'route': '경로 안내',
        'distance': '거리',
        'time': '소요 시간',
        'transport': '교통수단',
        'walk': '도보',
        'bicycle': '자전거',
        'public_transport': '대중교통',
        'car': '자동차',
        'cost': '비용',
        'attractions': '관광지',
        'restaurants': '음식점',
        'events': '이벤트',
        'calendar': '이벤트 캘린더',
        'ranking': '인기 순위',
        'plan': '추천 플랜',
        'evacuation': '대피소',
        'hazard_map': '재해 지도',
        'disaster_goods': '방재용품',
        'upload_data': '데이터 업로드',
        'select_spot': '장소 선택',
        'show_route': '경로 표시',
        'get_gps': 'GPS 획득',
        'traffic_info': '교통 상황',
        'wait_time': '대기 시간',
        'crowded': '혼잡도',
        'hours': '영업 시간',
        'capacity': '수용 인원',
        'occupancy': '수용률',
        'open_stores': '영업중인 매장',
        'vending_machines': '자동판매기',
        'budget': '예산',
        'family_plan': '가족 플랜',
        'solo_plan': '혼자 여행 플랜',
    }
}

# 日田市の中心座標
HITA_CENTER = (33.3219, 130.9414)

# サンプルデータ（Excel未アップロード時のデフォルト）
DEFAULT_TOURISM_DATA = {
    '番号': [1, 2, 3, 4, 5],
    'スポット名': ['豆田町', '咸宜園', '日田温泉', '大山ダム', '小鹿田焼の里'],
    '緯度': [33.3200, 33.3280, 33.3150, 33.3800, 33.3500],
    '経度': [130.9380, 130.9420, 130.9350, 130.9500, 130.9600],
    '説明': [
        '江戸時代の面影を残す歴史的な町並み',
        'ユネスコ世界遺産の私塾跡',
        '三隈川沿いの温泉郷',
        '筑後川の上流にある美しいダム',
        '伝統的な焼き物の産地'
    ]
}

DEFAULT_DISASTER_DATA = {
    '番号': [1, 2, 3, 4],
    'スポット名': ['日田市役所', '三隈中学校', '豆田小学校', '日田市総合体育館'],
    '緯度': [33.3219, 33.3180, 33.3200, 33.3250],
    '経度': [130.9414, 130.9350, 130.9380, 130.9450],
    '説明': [
        '収容人数: 500名',
        '収容人数: 800名',
        '収容人数: 600名',
        '収容人数: 1000名'
    ]
}

# セッション状態の初期化
def init_session_state():
    if 'language' not in st.session_state:
        st.session_state.language = 'ja'
    if 'mode' not in st.session_state:
        st.session_state.mode = 'tourism'
    if 'tourism_data' not in st.session_state:
        st.session_state.tourism_data = pd.DataFrame(DEFAULT_TOURISM_DATA)
    if 'disaster_data' not in st.session_state:
        st.session_state.disaster_data = pd.DataFrame(DEFAULT_DISASTER_DATA)
    if 'selected_spot' not in st.session_state:
        st.session_state.selected_spot = None
    if 'current_location' not in st.session_state:
        st.session_state.current_location = HITA_CENTER

def t(key):
    """翻訳関数"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

def load_excel_data(uploaded_file):
    """Excelファイルからデータを読み込む"""
    try:
        # 観光シート
        tourism_df = pd.read_excel(uploaded_file, sheet_name='観光')
        required_cols = ['番号', 'スポット名', '緯度', '経度', '説明']
        if all(col in tourism_df.columns for col in required_cols):
            st.session_state.tourism_data = tourism_df
            
        # 防災シート
        disaster_df = pd.read_excel(uploaded_file, sheet_name='防災')
        if all(col in disaster_df.columns for col in required_cols):
            st.session_state.disaster_data = disaster_df
            
        return True
    except Exception as e:
        st.error(f"エラー: {str(e)}")
        return False

def create_map(center, spots_df=None, show_all=True, selected_spot=None):
    """地図を作成"""
    m = folium.Map(location=center, zoom_start=13)
    
    # 現在地マーカー
    folium.Marker(
        center,
        popup="現在地 / Current Location",
        icon=folium.Icon(color='green', icon='home', prefix='fa')
    ).add_to(m)
    
    # スポットマーカー
    if spots_df is not None and show_all:
        for idx, row in spots_df.iterrows():
            color = 'red' if st.session_state.mode == 'disaster' else 'blue'
            if selected_spot and row['スポット名'] == selected_spot:
                color = 'orange'
                
            folium.Marker(
                [row['緯度'], row['経度']],
                popup=f"{row['スポット名']}<br>{row['説明']}",
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(m)
    
    # 選択されたスポットへのルート
    if selected_spot and spots_df is not None:
        spot_row = spots_df[spots_df['スポット名'] == selected_spot].iloc[0]
        dest = (spot_row['緯度'], spot_row['経度'])
        folium.PolyLine(
            [center, dest],
            color='purple',
            weight=4,
            opacity=0.7
        ).add_to(m)
    
    return m

def calculate_route_info(start, end, transport):
    """ルート情報を計算"""
    distance = geodesic(start, end).kilometers
    
    speeds = {
        'walk': 5,
        'bicycle': 15,
        'public_transport': 25,
        'car': 30
    }
    
    costs = {
        'walk': 0,
        'bicycle': 0,
        'public_transport': int(distance * 200),
        'car': int(distance * 50)
    }
    
    speed = speeds.get(transport, 5)
    time = (distance / speed) * 60  # 分単位
    cost = costs.get(transport, 0)
    
    return {
        'distance': round(distance, 2),
        'time': int(time),
        'cost': cost
    }

def show_weather_info():
    """天気情報を表示"""
    with st.expander(f"🌤️ {t('weather_info')}", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("気温 / Temperature", "18°C")
        with col2:
            st.metric("天気 / Weather", "☀️ 晴れ")
        with col3:
            st.metric("湿度 / Humidity", "65%")
        st.caption("※ 実際のアプリでは気象APIと連携します")

def tourism_mode():
    """観光モード"""
    st.header(f"🏞️ {t('tourism_mode')}")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        t('attractions'),
        t('restaurants'),
        t('events'),
        t('ranking')
    ])
    
    with tab1:
        st.subheader(t('attractions'))
        
        tourism_df = st.session_state.tourism_data
        
        # スポット一覧
        for idx, row in tourism_df.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{row['スポット名']}**")
                    st.caption(row['説明'])
                with col2:
                    if st.button('選択', key=f"tour_{idx}"):
                        st.session_state.selected_spot = row['スポット名']
                        st.rerun()
                st.divider()
        
        # 地図表示
        m = create_map(
            st.session_state.current_location,
            tourism_df,
            show_all=True,
            selected_spot=st.session_state.selected_spot
        )
        folium_static(m, width=1000, height=500)
    
    with tab2:
        st.subheader(t('restaurants'))
        
        # サンプル飲食店データ
        restaurants = [
            {'名前': '日田焼きそば専門店', '待ち時間': '15分', '混雑': '普通', '営業': '11:00-20:00'},
            {'名前': '鮎料理 かわせみ', '待ち時間': '30分', '混雑': '混雑', '営業': '11:30-21:00'},
            {'名前': '豆田カフェ', '待ち時間': '5分', '混雑': '空いている', '営業': '9:00-18:00'},
        ]
        
        for rest in restaurants:
            with st.container():
                st.markdown(f"**{rest['名前']}**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"{t('wait_time')}: {rest['待ち時間']}")
                with col2:
                    st.caption(f"{t('crowded')}: {rest['混雑']}")
                with col3:
                    st.caption(f"{t('hours')}: {rest['営業']}")
                st.divider()
    
    with tab3:
        st.subheader(t('events'))
        
        # 月選択
        selected_month = st.slider('月を選択', 1, 12, datetime.now().month)
        
        # サンプルイベント
        events = [
            {'名前': '日田天領まつり', '月': 3, '日程': '3月中旬', 'アイコン': '🎌', '説明': '江戸時代の天領を再現'},
            {'名前': '日田川開き観光祭', '月': 5, '日程': '5月下旬', 'アイコン': '🎆', '説明': '花火大会と水郷祭'},
            {'名前': '日田祇園祭', '月': 7, '日程': '7月', 'アイコン': '🏮', '説明': 'ユネスコ無形文化遺産'},
        ]
        
        filtered_events = [e for e in events if e['月'] == selected_month]
        
        if filtered_events:
            for event in filtered_events:
                with st.expander(f"{event['アイコン']} {event['名前']}"):
                    st.write(f"**開催時期:** {event['日程']}")
                    st.write(f"**詳細:** {event['説明']}")
        else:
            st.info("この月にはイベントがありません")
    
    with tab4:
        st.subheader(f"{t('ranking')} - 今月のベスト3")
        
        top3 = st.session_state.tourism_data.head(3)
        for idx, (i, row) in enumerate(top3.iterrows(), 1):
            medal = ['🥇', '🥈', '🥉'][idx-1]
            st.markdown(f"{medal} **{idx}位: {row['スポット名']}**")
            st.caption(row['説明'])
            st.divider()
        
        # プラン提案
        st.subheader(t('plan'))
        plan_type = st.radio(
            'プランタイプ',
            ['家族向けプラン', '一人旅プラン'],
            horizontal=True
        )
        
        budget_range = st.select_slider(
            t('budget'),
            options=['0-5,000円', '5,001-10,000円', '10,001-30,000円', '30,000円以上']
        )
        
        st.info(f"**{plan_type}** × **{budget_range}** に基づくおすすめルートを作成します")

def disaster_mode():
    """防災モード"""
    st.header(f"🚨 {t('disaster_mode')}")
    
    tab1, tab2, tab3 = st.tabs([
        t('evacuation'),
        t('hazard_map'),
        t('disaster_goods')
    ])
    
    with tab1:
        st.subheader(t('evacuation'))
        
        disaster_df = st.session_state.disaster_data
        
        # 避難所リスト
        for idx, row in disaster_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{row['スポット名']}**")
                    st.caption(row['説明'])
                with col2:
                    # 仮の収容率
                    occupancy = 40 + (idx * 10)
                    st.metric(t('occupancy'), f"{occupancy}%")
                with col3:
                    if st.button('ルート', key=f"evac_{idx}"):
                        st.session_state.selected_spot = row['スポット名']
                        st.rerun()
                st.progress(occupancy / 100)
                st.divider()
        
        # 地図表示
        m = create_map(
            st.session_state.current_location,
            disaster_df,
            show_all=True,
            selected_spot=st.session_state.selected_spot
        )
        folium_static(m, width=1000, height=500)
        
        # 追加情報
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🏪 {t('open_stores')}: 営業中の店舗情報")
        with col2:
            st.info(f"🥤 {t('vending_machines')}: 自動販売機の位置")
    
    with tab2:
        st.subheader(t('hazard_map'))
        
        hazard_type = st.selectbox(
            'ハザードマップの種類',
            ['洪水', '土砂災害', '地震']
        )
        
        st.warning(f"⚠️ {hazard_type}のハザードマップ")
        
        m = create_map(st.session_state.current_location)
        folium_static(m, width=1000, height=500)
        
        st.caption("※ 実際のアプリでは日田市の公式ハザードマップデータを表示します")
    
    with tab3:
        st.subheader(t('disaster_goods'))
        
        budget = st.select_slider(
            t('budget'),
            options=[5000, 10000, 20000, 30000, 50000],
            value=10000,
            format_func=lambda x: f"¥{x:,}"
        )
        
        st.markdown(f"### 予算 ¥{budget:,} でのおすすめ防災グッズ")
        
        goods = []
        if budget >= 5000:
            goods.extend(['✅ 非常用飲料水（2L×6本）', '✅ 非常食セット（3日分）', '✅ 懐中電灯＋電池'])
        if budget >= 10000:
            goods.extend(['✅ 防災ラジオ', '✅ 救急セット', '✅ 携帯トイレ'])
        if budget >= 20000:
            goods.extend(['✅ 寝袋・毛布', '✅ 発電機（小型）'])
        if budget >= 30000:
            goods.extend(['✅ 浄水器', '✅ テント'])
        if budget >= 50000:
            goods.extend(['✅ ポータブル電源', '✅ 簡易トイレセット'])
        
        for good in goods:
            st.write(good)

def navigation_section():
    """ナビゲーションセクション"""
    st.header(f"🗺️ {t('navigation')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(t('current_location'))
        curr_lat = st.number_input('緯度', value=st.session_state.current_location[0], format="%.6f", key='curr_lat')
        curr_lon = st.number_input('経度', value=st.session_state.current_location[1], format="%.6f", key='curr_lon')
        
        if st.button(f"📍 {t('get_gps')}"):
            st.info('GPS機能を使用するにはブラウザの位置情報許可が必要です')
            st.session_state.current_location = (curr_lat, curr_lon)
    
    with col2:
        st.subheader(t('destination'))
        
        # 選択されたスポット情報
        if st.session_state.selected_spot:
            st.success(f"選択中: {st.session_state.selected_spot}")
            
            # データフレームから選択
            df = st.session_state.tourism_data if st.session_state.mode == 'tourism' else st.session_state.disaster_data
            spot_data = df[df['スポット名'] == st.session_state.selected_spot].iloc[0]
            
            dest_lat = spot_data['緯度']
            dest_lon = spot_data['経度']
            
            st.write(f"緯度: {dest_lat}")
            st.write(f"経度: {dest_lon}")
        else:
            st.info("スポットを選択してください")
            dest_lat = HITA_CENTER[0]
            dest_lon = HITA_CENTER[1]
    
    # 交通手段選択
    transport_options = {
        t('walk'): 'walk',
        t('bicycle'): 'bicycle',
        t('public_transport'): 'public_transport',
        t('car'): 'car'
    }
    
    selected_transport = st.radio(
        t('transport'),
        list(transport_options.keys()),
        horizontal=True
    )
    
    transport = transport_options[selected_transport]
    
    # ルート表示
    if st.button(f"🚀 {t('show_route')}", type="primary"):
        if st.session_state.selected_spot:
            start = (curr_lat, curr_lon)
            end = (dest_lat, dest_lon)
            
            route_info = calculate_route_info(start, end, transport)
            
            # メトリクス表示
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t('distance'), f"{route_info['distance']} km")
            with col2:
                st.metric(t('time'), f"{route_info['time']} 分")
            with col3:
                st.metric(t('cost'), f"¥{route_info['cost']:,}")
            
            st.success(f"{t('route')} を表示しました！")
        else:
            st.warning("目的地を選択してください")

def main():
    init_session_state()
    
    # サイドバー
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # 言語選択
        lang_options = {'日本語': 'ja', 'English': 'en', '中文': 'zh', '한국어': 'ko'}
        selected_lang = st.selectbox(
            '🌐 ' + t('language'),
            list(lang_options.keys()),
            index=list(lang_options.values()).index(st.session_state.language)
        )
        st.session_state.language = lang_options[selected_lang]
        
        st.divider()
        
        # モード選択
        mode_selection = st.radio(
            t('mode_selection'),
            [t('tourism_mode'), t('disaster_mode')],
            index=0 if st.session_state.mode == 'tourism' else 1
        )
        st.session_state.mode = 'tourism' if mode_selection == t('tourism_mode') else 'disaster'
        
        st.divider()
        
        # Excelアップロード
        st.subheader(t('upload_data'))
        uploaded_file = st.file_uploader(
            "spots.xlsx をアップロード",
            type=['xlsx'],
            help="シート名: 「観光」「防災」\nカラム: 番号、スポット名、緯度、経度、説明"
        )
        
        if uploaded_file is not None:
            if st.button("データ読み込み"):
                if load_excel_data(uploaded_file):
                    st.success("✅ データ読み込み成功！")
                    st.rerun()
    
    # メインコンテンツ
    st.title(f"🗺️ {t('app_name')}")
    st.caption("日田市における観光と防災のタイムパフォーマンス向上アプリ")
    
    # 天気情報
    show_weather_info()
    
    st.divider()
    
    # モード別表示
    if st.session_state.mode == 'tourism':
        tourism_mode()
    else:
        disaster_mode()
    
    st.divider()
    
    # ナビゲーション
    navigation_section()
    
    # フッター
    st.divider()
    st.caption("© 2025 日田ナビ (Hita Navi) - Developed for Hita City")
    
    # デバッグ情報（開発用）
    with st.expander("🔧 デバッグ情報（開発者用）"):
        st.write("**セッション状態:**")
        st.json({
            "言語": st.session_state.language,
            "モード": st.session_state.mode,
            "選択スポット": st.session_state.selected_spot,
            "現在地": st.session_state.current_location,
            "観光データ件数": len(st.session_state.tourism_data),
            "防災データ件数": len(st.session_state.disaster_data)
        })

if __name__ == '__main__':
    main()