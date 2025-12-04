import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ページ設定
st.set_page_config(
    page_title="経済指標チェック",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# タイトル
st.title("📊 経済指標チェック")

# しきい値設定（23指標）
THRESHOLDS = {
    'バフェット指数': {
        'levels': [150, 180, 220],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%'
    },
    'シラーPER': {
        'levels': [25, 30, 35],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '倍'
    },
    '恐怖指数 VIX': {
        'levels': [15, 20, 30],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': ''
    },
    'バークシャー手元資金': {
        'levels': [10, 20, 30],  # 前年比増加率%
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%'
    },
    '逆イールドカーブ': {
        'levels': [0, -0.2, -0.5],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%',
        'reverse': True  # 値が小さい方が危険
    },
    'クレジットスプレッド': {
        'levels': [150, 180, 200],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': 'bp'
    },
    '信用買い残高統計': {
        'levels': [10, 30, 50],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%'
    },
    '高利回り社債スプレッド': {
        'levels': [300, 400, 500],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': 'bp'
    },
    'S&P500 PER': {
        'levels': [20, 25, 30],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '倍'
    },
    '米ドル指数DXY': {
        'levels': [3, 4, 5],  # 直近30日変動率%
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%'
    },
    'SOFR-Treasury Spread': {
        'levels': [50, 100, 200],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': 'bp'
    },
    'Case-Shiller住宅価格指数': {
        'levels': [5, 10, 20],  # 前年比%
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%'
    },
    'ADS景気指数': {
        'levels': [-0.5, -1.0, -2.0],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '',
        'reverse': True
    },
    '雇用の質指標': {
        'levels': [0.5, 1.0, 1.5],  # 前年差%
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%'
    },
    'FTSE NAREIT REITs': {
        'levels': [5, 15, 25],  # 前年比%
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%'
    },
    'レポ市場スプレッド': {
        'levels': [25, 50, 100],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': 'bp'
    },
    '企業債務GDP比率': {
        'levels': [100, 200, 300],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%'
    },
    'JPMorgan CDS 5年': {
        'levels': [50, 100, 200],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': 'bp'
    },
    'ISM製造業指数': {
        'levels': [50, 48, 45],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '',
        'reverse': True
    },
    'LEI先行経済指標': {
        'levels': [2, 0, -2],  # 前年比%
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%',
        'reverse': True
    },
    '個人消費支出（実質PCE）': {
        'levels': [3, 1, 0],  # 前年比%
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%',
        'reverse': True
    },
    ' 企業利益成長率': {
        'levels': [10, 0, -10],
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%',
        'reverse': True
    },
    '銅価格': {
        'levels': [10, 20, 30],  # 前年比変動率（絶対値）%
        'labels': ['正常', '注意', '警戒', '危険'],
        'colors': ['green', 'yellow', 'orange', 'red'],
        'unit': '%'
    }
}

def get_status(value, indicator_name):
    """指標値に基づいてステータスを判定"""
    if pd.isna(value) or indicator_name not in THRESHOLDS:
        return None, None, None
    
    config = THRESHOLDS[indicator_name]
    levels = config['levels']
    labels = config['labels']
    colors = config['colors']
    reverse = config.get('reverse', False)
    
    if reverse:
        # 逆転指標（値が小さい方が危険）
        if value > levels[0]:
            return labels[0], colors[0], '🟢'
        elif value > levels[1]:
            return labels[1], colors[1], '🟡'
        elif value > levels[2]:
            return labels[2], colors[2], '🟠'
        else:
            return labels[3], colors[3], '🔴'
    else:
        # 通常指標（値が大きい方が危険）
        if value < levels[0]:
            return labels[0], colors[0], '🟢'
        elif value < levels[1]:
            return labels[1], colors[1], '🟡'
        elif value < levels[2]:
            return labels[2], colors[2], '🟠'
        else:
            return labels[3], colors[3], '🔴'

def add_threshold_lines(fig, indicator_name, y_range=None):
    """グラフにしきい値線を追加"""
    if indicator_name not in THRESHOLDS:
        return
    
    config = THRESHOLDS[indicator_name]
    levels = config['levels']
    labels = config['labels']
    colors = config['colors']
    
    # しきい値線を追加（labels[1]以降：注意、警戒、危険の境界線）
    line_styles = ['dot', 'dash', 'solid']
    for i, level in enumerate(levels):
        fig.add_hline(
            y=level,
            line_dash=line_styles[i],
            line_color=colors[i+1],
            line_width=1.5,
            annotation_text=f"{labels[i+1]} ({level}{config['unit']})",
            annotation_position="right"
        )

# キャッシュを使用してデータを読み込み
@st.cache_data
def load_data(file_path):
    """Excelファイルからデータを読み込み"""
    df = pd.read_excel(file_path, sheet_name='時系列データ', header=1)
    
    # 日付列を日付型に変換
    df['日付'] = pd.to_datetime(df['日付'])
    
    # 数値データの列を特定（.1がついている列）
    numeric_columns = [col for col in df.columns if '.1' in str(col)]
    
    # '景気動向系.1'は数値ではないので除外
    numeric_columns = [col for col in numeric_columns if col != '景気動向系.1']
    
    # 列名から.1を削除してクリーンな名前に
    clean_data = df[['日付']].copy()
    for col in numeric_columns:
        clean_name = col.replace('.1', '').strip()
        # '-'を NaN に変換してから数値型に
        clean_data[clean_name] = pd.to_numeric(df[col], errors='coerce')
    
    return clean_data

# セッション状態の初期化
if 'detail_view' not in st.session_state:
    st.session_state.detail_view = False
    st.session_state.selected_indicator = None

# データ読み込み
try:
    data = load_data('暴落指標.xlsx')
    
    # サイドバー
    with st.sidebar:
        st.header("⚙️ 設定")
        
        # 期間選択
        st.subheader("期間選択")
        period_options = {
            "1ヶ月": 30,
            "3ヶ月": 90,
            "6ヶ月": 180,
            "1年": 365,
            "全期間": None
        }
        selected_period = st.radio(
            "表示期間",
            list(period_options.keys()),
            index=4  # デフォルトは全期間
        )
        
        # データをフィルタリング
        if period_options[selected_period] is not None:
            cutoff_date = data['日付'].max() - pd.Timedelta(days=period_options[selected_period])
            filtered_data = data[data['日付'] >= cutoff_date]
        else:
            filtered_data = data
        
        st.divider()
        
        # 指標選択
        st.subheader("指標選択")
        all_indicators = [col for col in data.columns if col != '日付']
        
        # デフォルトで主要な指標を選択
        default_indicators = [
            'バフェット指数', 'シラーPER',  '信用買い残高統計',
            'クレジットスプレッド', '企業債務GDP比率', '恐怖指数 VIX',
            '逆イールドカーブ', 'ISM製造業指数', 'LEI先行経済指標'
        ]
        default_selection = [ind for ind in default_indicators if ind in all_indicators]
        
        # 初期値の設定（セッション状態）
        if 'selected_indicators' not in st.session_state:
            st.session_state.selected_indicators = default_selection if default_selection else all_indicators[:6]
        
        # クイック選択ボタン
        col1, col2 = st.columns(2)
        with col1:
            if st.button("基本9指標", use_container_width=True):
                st.session_state.selected_indicators = default_selection
                st.rerun()
        with col2:
            if st.button("全指標", use_container_width=True):
                st.session_state.selected_indicators = all_indicators
                st.rerun()
        
        selected_indicators = st.multiselect(
            "表示する指標を選択",
            all_indicators,
            default=st.session_state.selected_indicators
        )
        
        # 選択が変更されたらセッション状態を更新
        st.session_state.selected_indicators = selected_indicators
        
        st.divider()
        
        # 表示オプション
        st.subheader("表示オプション")
        normalize = st.checkbox("正規化表示（初期値=100）", value=False)
        show_thresholds = st.checkbox("しきい値を表示", value=True)
        
        st.divider()
        
        # データ情報
        st.subheader("📈 データ情報")
        st.metric("データ期間", f"{len(filtered_data)}週")
        st.metric("最新データ", filtered_data['日付'].max().strftime('%Y-%m-%d'))
        
        # ステータスサマリー
        if show_thresholds:
            st.divider()
            st.subheader("⚠️ ステータスサマリー")
            
            # 最新値のステータスをカウント
            status_counts = {'🔴': 0, '🟠': 0, '🟡': 0, '🟢': 0}
            for indicator in selected_indicators:
                if indicator in filtered_data.columns:
                    latest_value = filtered_data[indicator].dropna().iloc[-1] if len(filtered_data[indicator].dropna()) > 0 else None
                    if latest_value is not None:
                        _, _, icon = get_status(latest_value, indicator)
                        if icon:
                            status_counts[icon] += 1
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🔴 危険", status_counts['🔴'])
                st.metric("🟠 警戒", status_counts['🟠'])
            with col2:
                st.metric("🟡 注意", status_counts['🟡'])
                st.metric("🟢 正常", status_counts['🟢'])
        
        # 詳細ビューの場合は戻るボタン
        if st.session_state.detail_view:
            st.divider()
            if st.button("⬅️ グリッド表示に戻る", use_container_width=True):
                st.session_state.detail_view = False
                st.session_state.selected_indicator = None
                st.rerun()
    
    # メインエリア
    if not selected_indicators:
        st.warning("⚠️ 少なくとも1つの指標を選択してください")
    else:
        if st.session_state.detail_view and st.session_state.selected_indicator:
            # 詳細ビュー
            indicator = st.session_state.selected_indicator
            
            indicator_data = filtered_data[indicator].dropna()
            latest_value = indicator_data.iloc[-1] if len(indicator_data) > 0 else None
            
            # ステータスを取得
            status_label, status_color, status_icon = get_status(latest_value, indicator)
            
            # ヘッダー
            if status_icon:
                st.subheader(f"📊 {indicator} {status_icon} {status_label}")
            else:
                st.subheader(f"📊 {indicator} - 詳細表示")
            
            # 統計情報を表示
            col1, col2, col3, col4 = st.columns(4)
            
            if len(indicator_data) > 0:
                with col1:
                    if status_icon:
                        st.metric("最新値", f"{latest_value:.2f}", delta=status_label)
                    else:
                        st.metric("最新値", f"{latest_value:.2f}")
                with col2:
                    st.metric("平均値", f"{indicator_data.mean():.2f}")
                with col3:
                    st.metric("最大値", f"{indicator_data.max():.2f}")
                with col4:
                    st.metric("最小値", f"{indicator_data.min():.2f}")
            
            # 大きなチャートを表示
            fig = go.Figure()
            
            y_data = filtered_data[indicator]
            if normalize:
                # 正規化：最初の有効値を100とする
                first_valid = y_data.dropna().iloc[0] if len(y_data.dropna()) > 0 else 1
                y_data = (y_data / first_valid) * 100
            
            # メインの折れ線グラフ
            fig.add_trace(go.Scatter(
                x=filtered_data['日付'],
                y=y_data,
                mode='lines',
                name=indicator,
                line=dict(width=3, color='#1f77b4'),
                connectgaps=False
            ))
            
            # しきい値線を追加
            if show_thresholds and not normalize:
                add_threshold_lines(fig, indicator)
            
            fig.update_layout(
                height=500,
                hovermode='x unified',
                xaxis_title="日付",
                yaxis_title="正規化値（初期値=100）" if normalize else "値",
                template="plotly_white",
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # しきい値情報を表示
            if show_thresholds and indicator in THRESHOLDS:
                st.info(f"📌 しきい値設定: {THRESHOLDS[indicator]['labels'][0]}(<{THRESHOLDS[indicator]['levels'][0]}{THRESHOLDS[indicator]['unit']}) / "
                       f"{THRESHOLDS[indicator]['labels'][1]}({THRESHOLDS[indicator]['levels'][0]}-{THRESHOLDS[indicator]['levels'][1]}{THRESHOLDS[indicator]['unit']}) / "
                       f"{THRESHOLDS[indicator]['labels'][2]}({THRESHOLDS[indicator]['levels'][1]}-{THRESHOLDS[indicator]['levels'][2]}{THRESHOLDS[indicator]['unit']}) / "
                       f"{THRESHOLDS[indicator]['labels'][3]}({THRESHOLDS[indicator]['levels'][2]}{THRESHOLDS[indicator]['unit']}超)")
            
            # データテーブル
            st.subheader("📋 データテーブル")
            display_data = filtered_data[['日付', indicator]].copy()
            display_data['日付'] = display_data['日付'].dt.strftime('%Y-%m-%d')
            
            # ステータス列を追加
            if show_thresholds:
                display_data['ステータス'] = display_data[indicator].apply(
                    lambda x: f"{get_status(x, indicator)[2]} {get_status(x, indicator)[0]}" if get_status(x, indicator)[0] else ""
                )
            
            st.dataframe(
                display_data.sort_values('日付', ascending=False),
                hide_index=True,
                use_container_width=True
            )
            
        else:
            # グリッドビュー
            st.subheader("複数指標を比較")
            st.caption("グラフをクリックして詳細を表示")
            
            # グリッドレイアウト（3列）
            num_cols = 3
            num_indicators = len(selected_indicators)
            num_rows = (num_indicators + num_cols - 1) // num_cols
            
            for row in range(num_rows):
                cols = st.columns(num_cols)
                for col_idx in range(num_cols):
                    indicator_idx = row * num_cols + col_idx
                    if indicator_idx < num_indicators:
                        indicator = selected_indicators[indicator_idx]
                        
                        with cols[col_idx]:
                            # 指標名と最新値、ステータスを表示
                            indicator_data = filtered_data[indicator].dropna()
                            if len(indicator_data) > 0:
                                latest_value = indicator_data.iloc[-1]
                                status_label, status_color, status_icon = get_status(latest_value, indicator)
                                
                                if status_icon:
                                    st.markdown(f"**{indicator}** {status_icon}")
                                    st.caption(f"最新値: {latest_value:.2f} ({status_label})")
                                else:
                                    st.markdown(f"**{indicator}**")
                                    st.caption(f"最新値: {latest_value:.2f}")
                            else:
                                st.markdown(f"**{indicator}**")
                                st.caption("データなし")
                            
                            # チャートを作成
                            fig = go.Figure()
                            
                            y_data = filtered_data[indicator]
                            if normalize:
                                # 正規化：最初の有効値を100とする
                                first_valid = y_data.dropna().iloc[0] if len(y_data.dropna()) > 0 else 1
                                y_data = (y_data / first_valid) * 100
                            
                            fig.add_trace(go.Scatter(
                                x=filtered_data['日付'],
                                y=y_data,
                                mode='lines',
                                name=indicator,
                                line=dict(width=2),
                                connectgaps=False
                            ))
                            
                            # しきい値線を追加（小さめ）
                            if show_thresholds and not normalize and indicator in THRESHOLDS:
                                config = THRESHOLDS[indicator]
                                levels = config['levels']
                                colors = config['colors']
                                
                                for i, level in enumerate(levels):
                                    fig.add_hline(
                                        y=level,
                                        line_dash='dot',
                                        line_color=colors[i+1],
                                        line_width=1,
                                        opacity=0.5
                                    )
                            
                            fig.update_layout(
                                height=250,
                                margin=dict(l=10, r=10, t=10, b=10),
                                xaxis=dict(showticklabels=True, showgrid=True),
                                yaxis=dict(showticklabels=True, showgrid=True),
                                hovermode='x unified',
                                template="plotly_white",
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig, use_container_width=True, key=f"chart_{indicator}")
                            
                            # 詳細表示ボタン
                            if st.button(f"詳細を見る", key=f"btn_{indicator}", use_container_width=True):
                                st.session_state.detail_view = True
                                st.session_state.selected_indicator = indicator
                                st.rerun()

except Exception as e:
    st.error(f"エラーが発生しました: {str(e)}")
    st.info("Excelファイルが正しく配置されているか確認してください。")
    st.exception(e)
