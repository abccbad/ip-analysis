import streamlit as st
import pandas as pd
from io import BytesIO
import json
import plotly.graph_objects as go
import plotly.express as px
import time, re
from datetime import datetime
from streamlit_modal import Modal
# 页面基础配置
st.set_page_config(
    page_title="IP投资智能分析平台",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 全局样式
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700;900&display=swap');
*, html, body, [class*="css"] { font-family: 'Noto Sans SC', sans-serif !important; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }
.stTabs [data-baseweb="tab-list"] { gap:0!important; background:#fff!important; border-bottom:1.5px solid #e8eaf0!important; padding:0 24px!important; }
.stTabs [data-baseweb="tab"] { height:44px!important; padding:0 18px!important; font-size:13px!important; font-weight:500!important; color:#64748b!important; border-bottom:2.5px solid transparent!important; margin-bottom:-1px!important; background:transparent!important; }
.stTabs [aria-selected="true"] { color:#e5392e!important; border-bottom:2.5px solid #e5392e!important; }
.nav-dot { width:7px; height:7px; border-radius:50%; background:#22c55e; box-shadow:0 0 0 3px #dcfce7; display:inline-block; }
.sb-bot { display:flex; align-items:center; gap:9px; padding:10px 14px; background:linear-gradient(135deg,#667eea,#764ba2); border-radius:10px; color:#fff; margin-bottom:12px; }
.sb-sec { font-size:10.5px; font-weight:700; color:#9ca3af; padding:8px 0 4px; letter-spacing:.06em; }
.sb-item { display:flex; align-items:center; gap:8px; padding:8px 10px; font-size:12.5px; color:#374151; border-left:3px solid transparent; border-radius:0 7px 7px 0; margin-bottom:2px; }
.sb-item.on { background:#fff5f5; color:#e5392e; border-left-color:#e5392e; font-weight:600; }
div.stButton > button[kind="secondary"] { 
    font-size: 11px !important; 
    padding: 4px 8px !important; 
    height: auto !important; 
    min-height: 28px !important;
    line-height: 1.4 !important;
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    color: #475569 !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    text-align: left !important;
    justify-content: flex-start !important;
}
div.stButton > button[kind="secondary"]:hover {
    background: #f1f5f9 !important;
    border-color: #cbd5e1 !important;
}
.proc-item { font-size:11px; color:#64748b; line-height:2.1; }
.u-msg { display:flex; justify-content:flex-end; margin:10px 0; }
.u-bub { background:#e5392e; color:#fff; border-radius:14px 14px 3px 14px; padding:10px 15px; max-width:66%; font-size:13px; line-height:1.65; }
.a-msg { display:flex; gap:9px; margin:10px 0; }
.a-av { width:30px; height:30px; border-radius:50%; flex-shrink:0; background:linear-gradient(135deg,#667eea,#764ba2); display:flex; align-items:center; justify-content:center; font-size:13px; }
.a-bub { background:#f3f4f8; border-radius:3px 14px 14px 14px; padding:11px 15px; max-width:84%; font-size:12.5px; line-height:1.85; color:#1e293b; }
.flow-bar { display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:6px; background:#f8faff; border:1px solid #dde5ff; border-radius:10px; padding:11px 18px; margin-bottom:14px; }
.fn { display:inline-flex; align-items:center; gap:4px; background:#fff; border:1px solid #c7d2fe; border-radius:6px; padding:4px 11px; font-size:11.5px; color:#4338ca; font-weight:500; }
.fa { color:#a5b4fc; font-size:13px; }
div.stButton > button { border-radius:7px!important; font-size:12px!important; padding:5px 10px!important; }
div.stButton > button[kind="primary"] { background:#e5392e!important; border-color:#e5392e!important; color:#fff!important; }
div.stTextInput > div > div > input { border-radius:8px!important; font-size:12.5px!important; border:1.5px solid #e2e8f0!important; padding:9px 13px!important; }
div.stTextInput > div > div > input:focus { border-color:#e5392e!important; }
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-thumb { background:#cbd5e1; border-radius:3px; }

/* IP推荐榜单样式 */
/* IP推荐榜单样式 - 仅保留实际使用的样式 */
.stApp {
    background-color: #f5f7fa;
}
.block-container {
    padding: 20px 30px !important;
    max-width: 1200px !important;
}
.ip-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    margin-bottom: 12px;
    overflow: hidden;
}
.ip-card.active {
    border-left: 4px solid #2563eb;
    background: #f8fafc;
}
.ip-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 15px;
    border-bottom: 1px solid #e5e7eb;
}
.ip-title {
    font-size: 15px;
    font-weight: 600;
    color: #111827;
    margin: 0;
}
.ip-tags {
    display: flex;
    gap: 6px;
    align-items: center;
}
.ip-tag {
    font-size: 11px;
    padding: 2px 6px;
    border-radius: 3px;
    background: #e0f2fe;
    color: #0369a1;
    margin: 0;
}
.ip-tag.a {
    background: #dcfce7;
    color: #166534;
}
.score-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    padding: 10px 15px;
    gap: 10px;
}
.score-item {
    text-align: center;
    margin: 0;
}
.score-label {
    font-size: 11px;
    color: #6b7280;
    margin-bottom: 4px;
    margin: 0;
}
.score-value {
    font-size: 13px;
    font-weight: 500;
    color: #111827;
    margin: 0;
}
.core-driver {
    padding: 8px 15px;
    font-size: 12px;
    color: #4b5563;
    background: #f9fafb;
    border-top: 1px solid #e5e7eb;
    margin: 0;
}
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin-top: 20px;
}
.page-btn {
    width: 28px;
    height: 28px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    border: 1px solid #d1d5db;
    background: #ffffff;
    color: #374151;
    cursor: default;
}
.page-btn.active {
    background: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
}
.stDownloadButton {
    margin-right: 0 !important;
}
.modal-content {
    background: #ffffff;
    border-radius: 8px;
    width: 90%;
    max-width: 1200px;
    max-height: 90vh;
    overflow-y: auto;
    padding: 20px;
    position: relative;
    z-index: 99998;
}
.modal-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

/* 关闭按钮样式 */
button[key="close_modal_top"] {
    background: transparent !important;
    border: none !important;
    font-size: 20px !important;
    color: #666 !important;
    padding: 0 !important;
    margin: 0 !important;
    width: 30px !important;
    height: 30px !important;
    min-width: 30px !important;
    line-height: 1 !important;
    cursor: pointer !important;
    float: right;
}
button[key="close_modal_top"]:hover {
    color: #e5392e !important;
    background: transparent !important;
}
button[key="close_modal_bottom"] {
    background: #f3f4f6 !important;
    border: 1px solid #d1d5db !important;
    color: #374151 !important;
    padding: 4px 12px !important;
    border-radius: 4px !important;
    font-size: 13px !important;
}
button[key="close_modal_bottom"]:hover {
    background: #e5e7eb !important;
}

.report-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}
.report-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 15px;
}
.report-card h4 {
    font-size: 14px;
    color: #4b5563;
    margin: 0 0 12px 0;
    display: flex;
    align-items: center;
    gap: 6px;
}
.advantage-item {
    font-size: 13px;
    color: #333;
    margin: 6px 0;
    display: flex;
    align-items: flex-start;
    gap: 6px;
}
.advantage-item::before {
    content: "✓";
    color: #00cc66;
    font-weight: bold;
}
.note-item {
    font-size: 13px;
    color: #333;
    margin: 6px 0;
    display: flex;
    align-items: flex-start;
    gap: 6px;
}
.note-item::before {
    content: "⚠️";
    color: #ff9900;
}
.performance-row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px dotted #e5e7eb;
}
.performance-label {
    font-size: 13px;
    color: #4b5563;
}
.performance-value {
    font-size: 13px;
    font-weight: 500;
    color: #2563eb;
}
.report-pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin-top: 20px;
}
.report-page-btn {
    width: 28px;
    height: 28px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    border: 1px solid #d1d5db;
    background: #ffffff;
    color: #374151;
    cursor: default;
}
.report-page-btn.active {
    background: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
}

div[data-testid="stButton"][key^="detail_"] > button::after {
    content: "➡️";
}

/* 合并后的modal-overlay样式 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.stPlotlyChart{
    position: relative;
    z-index: 1001;
}
</style>
""", unsafe_allow_html=True)

# 数据定义（智能问答部分）
def mk(name,tp,tk,budget,scores,core,adv,warn,fc,aud,trend,tc,wc,risks,comm,alts):
    return dict(name=name,type=tp,tk=tk,budget=budget,scores=scores,core=core,
                advantages=adv,warnings=warn,forecast=fc,audience=aud,trend=trend,
                tags_core=tc,wordcloud=wc,risks=risks,commercial=comm,alts=alts)

P1 = [
    mk("好好的时光","影视IP","film","60-85万",
       [("IP综合表现",19,20),("传播塑造力",78,80),("风险指数",2,10),("话题引力",9,10),
        ("品牌适配度",9,10),("情绪感染力",72,75),("圈层穿透力",14,15),
        ("热度",24,25),("热度趋势",23,25),("商业价值",9,10)],
       "2026年3月播映+25-35岁女性占比85%｜预期回报210%｜10维评分均TOP1",
       ["IP综合表现19/20，行业顶尖，口碑积累稳定","品牌适配度9/10，亲子家庭乳品高度契合",
        "风险指数2/10，极低风险，适合保守型投资","传播塑造力78/80，社交传播渠道极为丰富",
        "25-35岁女性占比85%，精准触达目标受众"],
       ["竞品抢投概率12%，建议48小时内锁定","预算区间60-85万，需充足资金规划",
        "热度峰值在D+4，把握宣传节点","需配合付费流量最大化价值"],
       [("预估ROI","210%"),("回本周期","45天"),("声量提升","180%"),("转化率提升","25%")],
       [("25-35岁女性",85),("亲子家庭",89),("下沉市场",68),("高消费力",76)],
       "播出初期热度25/25，传播塑造力79/80。热度峰值D+4，后续回暖节点D+6预计反弹。",
       ["治愈家庭","女性向","都市","情感","亲子","孙莉主演","视频剧","金牌导演"],
       [("好好的时光",46,"#e5392e"),("亲子",50,"#1d4ed8"),("治愈家庭",42,"#065f46"),
        ("孙莉主演",38,"#b45309"),("女性向",30,"#7c3aed"),("情感",36,"#dc2626"),
        ("都市",26,"#374151"),("腾讯视频",28,"#1d4ed8"),("国民IP",34,"#b45309")],
       [("竞品抢投","2/10","m","中12%","48小时内签定合作协议，支付全额预定金"),
        ("舆情波动","2/10","l","低8%","7x24小时舆情监测，备用舆控应急素材"),
        ("热度不及预期","2/10","l","低10%","预定2个备选IP分散风险")],
       [("合作形式","冠名/内容植入、主演官方、品牌定制、衍生联名"),
        ("预算区间","标准投入20-25万，实惠套餐5-10万，约60-85万"),
        ("商业价值","预估回报210%，声量提升180%，转化提升25%"),
        ("IP标签适配","乳品、孕婴产品、亲子家庭食品、母婴产品")],
       [("巧虎","动漫IP","75/80","22/25","8/10","2/10","55-70万"),
        ("2026中国亲子运动会","体育赛事IP","70/80","21/25","7/10","4/10","70-90万"),
        ("小欢喜3","影视IP","73/80","22/25","8/10","3/10","55-75万"),
        ("年糕妈妈","KOL IP","72/80","21/25","9/10","2/10","40-60万")]),
    mk("巧虎","动漫IP","anime","55-70万",
       [("IP综合表现",18,20),("传播塑造力",75,80),("风险指数",2,10),("话题引力",8,10),
        ("品牌适配度",9,10),("情绪感染力",70,75),("圈层穿透力",13,15),
        ("热度",22,25),("热度趋势",21,25),("商业价值",8,10)],
       "亲子教育头部IP+亲子家庭占比95%｜预期回报190%｜经典IP品牌认知度极高",
       ["亲子教育品类头部IP，品牌认知度极高","亲子家庭用户占比95%，精准覆盖目标受众",
        "风险极低2/10，适合首次IP投资布局","内容生态完整，支持多场景植入",
        "日本经典IP背书，信任度持续高位"],
       ["热度相对低于好好的时光，需补充话题引爆","季节性影响明显，3-6月亲子旺季效果最佳",
        "竞品抢投率略高，建议及时锁定","单一年龄段集中，需匹配对应品类"],
       [("预估ROI","190%"),("回本周期","52天"),("声量提升","165%"),("转化率提升","22%")],
       [("25-35岁女性",78),("亲子家庭",95),("下沉市场",72),("高消费力",68)],
       "全年稳定高热度，无明显波动。3-6月亲子旺季为最佳投放窗口，品牌认知度全年保持高位。",
       ["亲子教育","早教","成长","卡通","家庭","0-6岁","动漫","日本IP"],
       [("巧虎",46,"#065f46"),("早教",40,"#b45309"),("亲子成长",34,"#7c3aed"),
        ("卡通",28,"#e5392e"),("0-6岁",26,"#374151"),("家庭",36,"#1d4ed8"),
        ("科学育儿",28,"#b45309"),("日本IP",30,"#065f46")],
       [("版权合规风险","1/10","l","低5%","提前做好授权协议，避免使用未授权素材"),
        ("热度峰值较低","3/10","m","中15%","搭配社交媒体投放放大传播效果"),
        ("受众年龄集中","2/10","l","低8%","适合0-6岁家长品类，需精准匹配产品线")],
       [("合作形式","内容植入、冠名早教栏目、品牌定制套装"),
        ("预算区间","标准投入25-35万，衍生品联名15-20万"),
        ("商业价值","预估回报190%，声量提升165%，转化提升22%"),
        ("IP标签适配","婴幼儿食品、玩具、早教产品、母婴用品")],
       [("好好的时光","影视IP","78/80","23/25","9/10","2/10","60-85万"),
        ("小欢喜3","影视IP","73/80","22/25","8/10","3/10","55-75万"),
        ("2026中国亲子运动会","体育赛事IP","70/80","21/25","7/10","4/10","70-90万"),
        ("年糕妈妈","KOL IP","72/80","21/25","9/10","2/10","40-60万")]),
    mk("2026中国亲子运动会","体育赛事IP","sport","70-90万",
       [("IP综合表现",17,20),("传播塑造力",70,80),("风险指数",4,10),("话题引力",8,10),
        ("品牌适配度",9,10),("情绪感染力",68,75),("圈层穿透力",11,15),
        ("热度",21,25),("热度趋势",22,25),("商业价值",7,10)],
       "全国性赛事曝光+10城巡回覆盖｜预期回报165%｜线下触达50万+家庭",
       ["全国性赛事，线下触达真实家庭消费场景","现场曝光+线上直播双渠道放大品牌声量",
        "赛事权威背书，品牌形象提升显著","亲子运动赛道蓝海，差异化竞争优势",
        "10城巡回赛，地域覆盖广泛"],
       ["风险指数4/10，赛事举办存在不确定因素","预算70-90万，投入相对较高",
        "线下执行难度大，需本地合作资源支持","受天气场馆等不可控因素影响"],
       [("预估ROI","165%"),("回本周期","65天"),("声量提升","140%"),("转化率提升","18%")],
       [("25-35岁女性",65),("亲子家庭",90),("下沉市场",55),("高消费力",70)],
       "赛事期间热度集中爆发，赛前2周预热期为最佳投放窗口，赛后长尾效应持续约30天。",
       ["亲子运动","健康家庭","体育赛事","全国巡回","线下活动","品牌冠名"],
       [("亲子运动",42,"#9d174d"),("健康家庭",36,"#065f46"),("全国巡回",28,"#b45309"),
        ("体育赛事",32,"#7c3aed"),("线下活动",26,"#374151"),("品牌冠名",30,"#e5392e"),
        ("10城",24,"#5b21b6")],
       [("赛事取消或延期","4/10","m","中12%","合同中明确不可抗力条款，要求赛事方提供保险"),
        ("线下执行风险","3/10","m","中10%","提前派驻专人跟进，建立应急预案"),
        ("热度分散","3/10","l","低8%","集中资源在TOP3城市，确保核心市场效果")],
       [("合作形式","赛事冠名、场地广告、活动定制套装、直播植入"),
        ("预算区间","冠名赞助40-60万，活动执行20-30万"),
        ("商业价值","预估回报165%，线下触达50万家庭，声量提升140%"),
        ("IP标签适配","运动食品、健康营养品、家庭户外装备")],
       [("好好的时光","影视IP","78/80","23/25","9/10","2/10","60-85万"),
        ("巧虎","动漫IP","75/80","22/25","8/10","2/10","55-70万"),
        ("小欢喜3","影视IP","73/80","22/25","8/10","3/10","55-75万"),
        ("年糕妈妈","KOL IP","72/80","21/25","9/10","2/10","40-60万")]),
    mk("小欢喜3","影视IP","film","55-75万",
       [("IP综合表现",18,20),("传播塑造力",73,80),("风险指数",3,10),("话题引力",8,10),
        ("品牌适配度",9,10),("情绪感染力",71,75),("圈层穿透力",11,15),
        ("热度",22,25),("热度趋势",20,25),("商业价值",8,10)],
       "系列IP续集+品牌影响力持续覆盖｜预期回报170%｜家庭情感共鸣感极高",
       ["系列IP第三部，忠实粉丝基础庞大稳固","家庭情感主题，品牌情感植入自然融合",
        "系列积累的媒体资源和传播渠道成熟","高中考家庭共鸣强，暑期档期精准覆盖",
        "续集热度有保障，风险相对可控"],
       ["续集质量存在不确定性，需提前评估剧本","竞品同期影视IP较多，需差异化投放策略",
        "目标受众年龄跨度大（35-50岁家长为主）","暑期档竞争激烈，需提前锁定资源"],
       [("预估ROI","170%"),("回本周期","55天"),("声量提升","155%"),("转化率提升","20%")],
       [("25-35岁女性",62),("亲子家庭",85),("下沉市场",60),("高消费力",72)],
       "开播初期热度22/25，传播塑造力随剧情发展稳步提升。暑期档竞争激烈，D+7至D+14为关键窗口期。",
       ["家庭情感","高考","成长","亲子","教育焦虑","影视剧","暑期档"],
       [("小欢喜",42,"#1d4ed8"),("家庭情感",38,"#374151"),("教育焦虑",32,"#b45309"),
        ("暑期档",28,"#7c3aed"),("成长",30,"#065f46"),("亲子",34,"#e5392e")],
       [("续集质量风险","4/10","m","中15%","提前获取剧本摘要，评估与品牌调性匹配度"),
        ("竞品干扰","3/10","m","中12%","锁定独家植入位，避免竞品同期曝光"),
        ("受众偏移","2/10","l","低8%","结合数据平台实时监控受众画像变化")],
       [("合作形式","内容植入、主角同款、品牌贴片广告、社媒联动"),
        ("预算区间","深度植入35-50万，贴片广告15-25万"),
        ("商业价值","预估回报170%，家长群体高触达，声量提升155%"),
        ("IP标签适配","教育产品、家庭食品、文具用品、健康营养品")],
       [("好好的时光","影视IP","78/80","23/25","9/10","2/10","60-85万"),
        ("巧虎","动漫IP","75/80","22/25","8/10","2/10","55-70万"),
        ("2026中国亲子运动会","体育赛事IP","70/80","21/25","7/10","4/10","70-90万"),
        ("年糕妈妈","KOL IP","72/80","21/25","9/10","2/10","40-60万")]),
    mk("年糕妈妈","KOL IP","kol","40-60万",
       [("IP综合表现",17,20),("传播塑造力",72,80),("风险指数",2,10),("话题引力",9,10),
        ("品牌适配度",10,10),("情绪感染力",70,75),("圈层穿透力",15,15),
        ("热度",20,25),("热度趋势",21,25),("商业价值",9,10)],
       "垂直头部KOL+带货转化率极强｜预期回报175%｜性价比最高的IP投资选项",
       ["母婴垂直领域头部KOL，粉丝精准高质量","品牌适配度10/10满分，完美契合母婴赛道",
        "圈层穿透力15/15满分，精准深度覆盖","带货转化率行业顶尖，ROI可量化",
        "投入门槛最低（40-60万），性价比最优"],
       ["单一渠道依赖风险，需配合多平台投放","KOL个人因素风险，需评估账号健康状态",
        "热度上限相比影视IP略低","内容形式相对固定，创意空间有限"],
       [("预估ROI","175%"),("回本周期","40天"),("声量提升","145%"),("转化率提升","35%")],
       [("25-35岁女性",88),("亲子家庭",92),("下沉市场",75),("高消费力",65)],
       "内容发布后72小时内转化率最高，长期粉丝基础保持稳定种草效果。月均合作形成持续品牌露出。",
       ["母婴","科学育儿","辅食","婴儿护理","好物推荐","KOL","带货","垂直达人"],
       [("年糕妈妈",46,"#5b21b6"),("科学育儿",40,"#065f46"),("带货",36,"#b45309"),
        ("辅食",32,"#e5392e"),("婴儿护理",28,"#374151"),("垂直达人",30,"#7c3aed"),
        ("好物推荐",34,"#1d4ed8")],
       [("KOL个人风险","3/10","l","低10%","签订完整合同，明确违约条款和赔偿机制"),
        ("平台政策变化","2/10","l","低8%","分散平台合作（小红书+抖音+微信），降低依赖"),
        ("数据造假风险","1/10","l","低5%","要求第三方数据监测报告，核验真实互动数据")],
       [("合作形式","内容种草、产品测评、直播带货、IP联名"),
        ("预算区间","单次合作15-20万，年度合作40-60万"),
        ("商业价值","预估回报175%，带货转化率35%，声量提升145%"),
        ("IP标签适配","婴幼儿食品、母婴护理、儿童营养品、亲子教育")],
       [("好好的时光","影视IP","78/80","23/25","9/10","2/10","60-85万"),
        ("巧虎","动漫IP","75/80","22/25","8/10","2/10","55-70万"),
        ("小欢喜3","影视IP","73/80","22/25","8/10","3/10","55-75万"),
        ("2026中国亲子运动会","体育赛事IP","70/80","21/25","7/10","4/10","70-90万")]),
]

ALL_IPS = {ip['name']: ip for ip in P1}
BDGC = {'film': '#1d4ed8', 'anime': '#065f46', 'sport': '#9d174d', 'kol': '#5b21b6'}
BDGB = {'film': '#dbeafe', 'anime': '#d1fae5', 'sport': '#fce7f3', 'kol': '#ede9fe'}

# Mock AI函数
def mock_ai(q):
    ql = q.lower()
    if any(k in ql for k in ['推荐','投资','热门','未来','7天','top','哪些']):
        return '未来7天热门乳品赛道 **TOP5值得投资的IP**：\n\n1. **好好的时光**（影视IP）综合19/20，传播78/80，风险2/10；预期回报 **210%**，预算 **60-85万**。\n2. **巧虎**（动漫IP）综合18/20；预期回报 **190%**，预算 **55-70万**。\n3. **2026中国亲子运动会**（体育赛事IP）预期回报 **165%**，预算 **70-90万**。\n4. **小欢喜3**（影视IP）预期回报 **170%**，预算 **55-75万**。\n5. **年糕妈妈**（KOL IP）品牌适配 **10/10满分**；预期回报 **175%**，预算 **40-60万**，性价比最优。\n\n> 优先推荐好好的时光，10大维度全线TOP1，建议48小时内锁定资源。'
    elif any(k in ql for k in ['风险','安全','稳健']):
        return '**低风险稳健型IP投资推荐**\n\n风险极低（2/10）：好好的时光、巧虎、年糕妈妈\n风险中等（3-4/10）：小欢喜3、2026亲子运动会\n\n稳健组合：好好的时光70% + 年糕妈妈30%，整体风险不超过2/10。'
    elif any(k in ql for k in ['预算','费用','多少钱']):
        return '**各IP预算区间对比**\n\n年糕妈妈：40-60万，ROI 175%（最低预算）\n巧虎：55-70万，ROI 190%\n小欢喜3：55-75万，ROI 170%\n好好的时光：60-85万，ROI 210%（最高回报）\n2026亲子运动会：70-90万，ROI 165%'
    elif any(k in ql for k in ['好好的时光','巧虎','2026中国亲子运动会','小欢喜3','年糕妈妈']):
        ip_name = next((n for n in ['好好的时光','巧虎','2026中国亲子运动会','小欢喜3','年糕妈妈'] if n in ql), None)
        if ip_name:
            return f'**《{ip_name}》详细分析**\n\n{ALL_IPS[ip_name]["core"]}\n\n优势：' + '；'.join(ALL_IPS[ip_name]['advantages'][:3]) + '\n\n注意事项：' + '；'.join(ALL_IPS[ip_name]['warnings'][:2]) + '\n\n点击右侧「详细报告」按钮可查看完整分析。'
    else:
        return '感谢您的提问！\n\n🏆 TOP推荐：好好的时光，综合19/20，预期回报210%，风险极低\n📊 性价比最优：年糕妈妈，40-60万，转化率35%，40天回本\n\n可进一步询问：具体IP详细分析、预算方案、风险评估策略。'

# 数据定义（IP推荐榜单部分）
ip_data = [
    {
        "id": 1,
        "name": "《好好的时光》",
        "type": "影视IP",
        "level": "S级推荐",
        "scores": {
            "IP综合素质": "19/20",
            "传播裂变力": "78/80",
            "风险指数": "2/10",
            "话题吸引力": "9/10",
            "品牌适配度": "10/10",
            "情绪感染力": "75/75",
            "圈层穿透力": "14/15",
            "热度": "24/25",
            "热度趋势": "23/25",
            "商业价值": "9/10"
        },
        "driver": "核心驱动：2026年3月热播+25-35岁女性受众占比85% | 投资回报率：210% | 10维评分均列TOP1",
        "active": True
    },
    {
        "id": 2,
        "name": "巧虎",
        "type": "动漫IP",
        "level": "A级推荐",
        "scores": {
            "IP综合素质": "18/20",
            "传播裂变力": "75/80",
            "风险指数": "3/10",
            "话题吸引力": "8/10",
            "品牌适配度": "9/10",
            "情绪感染力": "70/75",
            "圈层穿透力": "13/15",
            "热度": "22/25",
            "热度趋势": "21/25",
            "商业价值": "8/10"
        },
        "driver": "核心驱动：新早教课程上线+亲子家庭占比95% | 投资回报率：180% | 亲子场景适配度极高",
        "active": False
    },
    {
        "id": 3,
        "name": "2026中国亲子运动会",
        "type": "赛事IP",
        "level": "A级推荐",
        "scores": {
            "IP综合素质": "17/20",
            "传播裂变力": "70/80",
            "风险指数": "4/10",
            "话题吸引力": "8/10",
            "品牌适配度": "9/10",
            "情绪感染力": "68/75",
            "圈层穿透力": "12/15",
            "热度": "21/25",
            "热度趋势": "22/25",
            "商业价值": "7/10"
        },
        "driver": "核心驱动：全国性赛事预热+母婴适配度98% | 投资回报率：165% | 曝光覆盖面广",
        "active": False
    },
    {
        "id": 4,
        "name": "《小欢喜3》",
        "type": "影视IP",
        "level": "A级推荐",
        "scores": {
            "IP综合素质": "18/20",
            "传播裂变力": "73/80",
            "风险指数": "3/10",
            "话题吸引力": "8/10",
            "品牌适配度": "9/10",
            "情绪感染力": "71/75",
            "圈层穿透力": "13/15",
            "热度": "22/25",
            "热度趋势": "20/25",
            "商业价值": "8/10"
        },
        "driver": "核心驱动：系列IP口碑+家庭场景强关联 | 投资回报率：170% | 受众基础牢固",
        "active": False
    },
    {
        "id": 5,
        "name": "年糕妈妈",
        "type": "KOL IP",
        "level": "A级推荐",
        "scores": {
            "IP综合素质": "17/20",
            "传播裂变力": "72/80",
            "风险指数": "2/10",
            "话题吸引力": "9/10",
            "品牌适配度": "9/10",
            "情绪感染力": "70/75",
            "圈层穿透力": "12/15",
            "热度": "20/25",
            "热度趋势": "21/25",
            "商业价值": "9/10"
        },
        "driver": "核心驱动：母婴垂类头部流量+带货转化能力强 | 投资回报率：175% | 性价比高",
        "active": False
    },
    {
        "id": 6,
        "name": "《妈妈是超人6》",
        "type": "综艺IP",
        "level": "A级推荐",
        "scores": {
            "IP综合素质": "16/20",
            "传播裂变力": "71/80",
            "风险指数": "5/10",
            "话题吸引力": "8/10",
            "品牌适配度": "9/10",
            "情绪感染力": "70/75",
            "圈层穿透力": "12/15",
            "热度": "21/25",
            "热度趋势": "20/25",
            "商业价值": "8/10"
        },
        "driver": "核心驱动：经典综艺IP+明星宝妈阵容 | 投资回报率：160% | 明星流量加持",
        "active": False
    }
]

ip_detail_data = {
    "《好好的时光》": {
        "radar_labels": [
            "IP综合素质", "传播裂变力", "风险指数(反向)", "话题吸引力", 
            "品牌适配度", "情绪感染力", "圈层穿透力", "热度", "热度趋势", "商业价值"
        ],
        "radar_values": [19, 78, 8, 9, 10, 75, 14, 24, 23, 9],
        "radar_max": [20, 80, 10, 10, 10, 75, 15, 25, 25, 10],
        "advantages": [
            "IP综合素质评分19/20，行业顶尖水平",
            "品牌适配度满分，与乳品品牌高度契合",
            "风险指数仅2/10，投资风险极低",
            "传播裂变力78/80，社交传播能力强",
            "25-35岁女性受众占比85%，精准匹配目标人群"
        ],
        "notes": [
            "竞品抢投概率12%，建议48小时内锁定合作",
            "预算区间60-85万，需提前做好资金规划",
            "热度峰值出现在D+4，需把握营销节点",
            "需配合宣发资源，最大化IP价值"
        ],
        "performance": {
            "预估投资回报率": "210%",
            "回本周期": "45天",
            "品牌声量提升": "180%",
            "产品转化率提升": "25%",
            "热度峰值": "24.5/25 (D+4)"
        },
        "audience": {
            "labels": ["25-35岁女性", "亲子家庭", "下沉市场用户", "高消费能力"],
            "values": [85, 89, 68, 76],
            "colors": ["#3388ff", "#00cc66", "#ff9900", "#9966ff"]
        }
    },
    "巧虎": {
        "radar_labels": [
            "IP综合素质", "传播裂变力", "风险指数(反向)", "话题吸引力", 
            "品牌适配度", "情绪感染力", "圈层穿透力", "热度", "热度趋势", "商业价值"
        ],
        "radar_values": [18, 75, 7, 8, 9, 70, 13, 22, 21, 8],
        "radar_max": [20, 80, 10, 10, 10, 75, 15, 25, 25, 10],
        "advantages": [
            "IP综合素质评分18/20，行业优秀水平",
            "品牌适配度9/10，与母婴乳品高度契合",
            "亲子家庭受众占比95%，精准覆盖目标人群",
            "内容安全合规，风险指数低",
            "用户信任度高，复购率表现优异"
        ],
        "notes": [
            "内容合规风险5%，需审核早教内容适配性",
            "预算区间50-70万，性价比突出",
            "新早教课程上线期，营销节点关键",
            "建议深度绑定课程做联合营销"
        ],
        "performance": {
            "预估投资回报率": "180%",
            "回本周期": "60天",
            "品牌声量提升": "150%",
            "产品转化率提升": "20%",
            "热度峰值": "22.5/25 (D+5)"
        },
        "audience": {
            "labels": ["3-6岁儿童", "宝妈群体", "一二线城市家庭", "高消费能力"],
            "values": [90, 98, 75, 80],
            "colors": ["#ff6666", "#66ccff", "#ffcc66", "#cc99ff"]
        }
    },
    "2026中国亲子运动会": {
        "radar_labels": [
            "IP综合素质", "传播裂变力", "风险指数(反向)", "话题吸引力", 
            "品牌适配度", "情绪感染力", "圈层穿透力", "热度", "热度趋势", "商业价值"
        ],
        "radar_values": [17, 70, 6, 8, 9, 68, 12, 21, 22, 7],
        "radar_max": [20, 80, 10, 10, 10, 75, 15, 25, 25, 10],
        "advantages": [
            "国家级体育赛事IP，官方背书公信力强",
            "亲子运动场景天然适配健康品类",
            "亲子家庭占比92%，目标人群集中",
            "线下体验+线上传播双渠道覆盖",
            "一二线城市用户占比80%，消费潜力大"
        ],
        "notes": [
            "执行风险10%，需提前确认赛事落地细节",
            "预算区间70-90万，需合理分配线下资源",
            "赛事预热期投放，效果最佳",
            "建议重点布局线下亲子互动区"
        ],
        "performance": {
            "预估投资回报率": "170%",
            "回本周期": "75天",
            "品牌声量提升": "160%",
            "产品转化率提升": "18%",
            "热度峰值": "21/25 (D+3)"
        },
        "audience": {
            "labels": ["亲子家庭", "体育爱好者", "一二线城市用户", "高消费能力"],
            "values": [92, 65, 80, 78],
            "colors": ["#00cc99", "#ff6699", "#6699ff", "#ff9966"]
        }
    },
    "《小欢喜3》": {
        "radar_labels": [
            "IP综合素质", "传播裂变力", "风险指数(反向)", "话题吸引力", 
            "品牌适配度", "情绪感染力", "圈层穿透力", "热度", "热度趋势", "商业价值"
        ],
        "radar_values": [18, 73, 7, 8, 9, 71, 13, 22, 20, 8],
        "radar_max": [20, 80, 10, 10, 10, 75, 15, 25, 25, 10],
        "advantages": [
            "经典家庭剧续作，受众基础稳固",
            "30-45岁成熟女性占比88%，决策人群集中",
            "家庭场景密集，品牌植入自然",
            "口碑风险低，内容质量有保障",
            "下沉市场用户占比70%，覆盖广泛"
        ],
        "notes": [
            "口碑风险8%，需关注剧集播出口碑",
            "预算区间65-75万，投资稳定",
            "温情节点营销效果最佳",
            "建议突出'家'的情感共鸣"
        ],
        "performance": {
            "预估投资回报率": "175%",
            "回本周期": "65天",
            "品牌声量提升": "155%",
            "产品转化率提升": "19%",
            "热度峰值": "22/25 (D+4)"
        },
        "audience": {
            "labels": ["30-45岁女性", "家庭用户", "下沉市场用户", "高消费能力"],
            "values": [88, 90, 70, 75],
            "colors": ["#9966ff", "#ff6699", "#66cc99", "#ffcc66"]
        }
    },
    "年糕妈妈": {
        "radar_labels": [
            "IP综合素质", "传播裂变力", "风险指数(反向)", "话题吸引力", 
            "品牌适配度", "情绪感染力", "圈层穿透力", "热度", "热度趋势", "商业价值"
        ],
        "radar_values": [17, 72, 8, 9, 9, 70, 12, 20, 21, 9],
        "radar_max": [20, 80, 10, 10, 10, 75, 15, 25, 25, 10],
        "advantages": [
            "母婴垂类头部KOL，专业信任度高",
            "带货能力强，ROI兑现度高",
            "25-40岁宝妈占比95%，精准触达",
            "新手父母渗透率92%，增量市场明显",
            "高线城市用户占比85%，消费能力强"
        ],
        "notes": [
            "合作风险6%，建议锁定独家合作权益",
            "预算区间40-60万，性价比极高",
            "直播带货转化效果最佳",
            "配合专业测评内容，提升信任度"
        ],
        "performance": {
            "预估投资回报率": "175%",
            "回本周期": "50天",
            "品牌声量提升": "140%",
            "产品转化率提升": "22%",
            "热度峰值": "20/25 (D+2)"
        },
        "audience": {
            "labels": ["25-40岁宝妈", "新手父母", "高线城市用户", "高消费能力"],
            "values": [95, 92, 85, 82],
            "colors": ["#ff99cc", "#66ff99", "#99ccff", "#ffcc99"]
        }
    },
    "《妈妈是超人6》": {
        "radar_labels": [
            "IP综合素质", "传播裂变力", "风险指数(反向)", "话题吸引力", 
            "品牌适配度", "情绪感染力", "圈层穿透力", "热度", "热度趋势", "商业价值"
        ],
        "radar_values": [16, 71, 5, 8, 9, 70, 12, 21, 20, 8],
        "radar_max": [20, 80, 10, 10, 10, 75, 15, 25, 25, 10],
        "advantages": [
            "经典亲子综艺IP，口碑保障",
            "明星宝妈阵容自带流量，曝光度高",
            "亲子互动场景丰富，植入机会多",
            "25-40岁女性占比85%，目标人群精准",
            "娱乐爱好者渗透率75%，传播潜力大"
        ],
        "notes": [
            "收视率风险10%，需关注首播数据",
            "预算区间65-80万，合理分配明星资源",
            "明星带娃场景植入效果最佳",
            "建议灵活调整投放策略"
        ],
        "performance": {
            "预估投资回报率": "160%",
            "回本周期": "70天",
            "品牌声量提升": "150%",
            "产品转化率提升": "17%",
            "热度峰值": "21/25 (D+3)"
        },
        "audience": {
            "labels": ["25-40岁女性", "亲子家庭", "娱乐爱好者", "高消费能力"],
            "values": [85, 88, 75, 72],
            "colors": ["#cc99ff", "#ff66cc", "#66ccff", "#ff9966"]
        }
    }
}

# 初始化会话状态
for k, v in [('chat_history', []), ('selected_ip', None), ('filter_open', False), 
             ('selected_type', '全部IP'), ('selected_level', '全部等级'), 
             ('show_detail', False), ('current_ip', '')]:
    if k not in st.session_state:
        st.session_state[k] = v

# 顶部导航
st.markdown('<div style="display:flex;align-items:center;gap:10px;padding:0 24px;height:50px;background:#fff;border-bottom:1.5px solid #e8eaf0;position:sticky;top:0;z-index:200;">'
    '<span style="font-size:20px;">🎬</span>'
    '<span style="font-size:15px;font-weight:800;color:#0f172a;">IP投资智能分析平台</span>'
    '<span style="font-size:11px;color:#94a3b8;margin-left:2px;">基于AI多维度评分模型 · 数据实时更新</span>'
    '<div style="flex:1;"></div>'
    '<span class="nav-dot"></span>'
    '<span style="font-size:11px;color:#64748b;">系统运行正常</span>'
    '</div>', unsafe_allow_html=True)


# 创建两个tab页
tab1, tab2 = st.tabs(['📊 每日爆款IP推荐','💬 智能问答'])

# ═══════ TAB 1: IP推荐榜单 ═══════════════════════════════════════════════════════════════
with tab1:
    
    # 主标题
    st.markdown("### IP推荐榜单：未来7天热门投资IP")

    # 筛选栏
    st.markdown("""
    <style>
        .filter-toggle-btn {
            background: none;
            border: none;
            padding: 0;
            margin: 0;
            font-size: 14px;
            color: #4b5563;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .filter-toggle-btn:hover {
            color: #2563eb;
        }
        .filter-toggle-btn:focus {
            outline: none;
        }
    </style>
    """, unsafe_allow_html=True)

    arrow = "▲" if st.session_state.filter_open else "▼"
    if st.button(f"{arrow} 评估对象筛选（可筛选IP类型/价格/10大维度评分等）", key="filter_toggle", help="点击展开/收起筛选选项"):
        st.session_state.filter_open = not st.session_state.filter_open
        st.rerun()

    # 筛选项面板
    if st.session_state.filter_open:
        # 第一组：IP类型筛选
        type_options = ["全部IP", "影视IP", "动漫IP", "赛事IP", "KOL IP", "综艺IP"]
        cols = st.columns([1, 1, 1, 1, 1, 1, 4], gap="small")
        for i, opt in enumerate(type_options):
            with cols[i]:
                is_active = (opt == st.session_state.selected_type)
                if st.button(opt, key=f"type_{opt}", help=f"选择{opt}", use_container_width=True):
                    st.session_state.selected_type = opt
                    st.rerun()
        
        # 第二组：推荐等级筛选
        level_options = ["全部等级", "S级推荐", "A级推荐"]
        cols2 = st.columns([1, 1, 1, 6], gap="small")
        for i, opt in enumerate(level_options):
            with cols2[i]:
                is_active = (opt == st.session_state.selected_level)
                if st.button(opt, key=f"level_{opt}", help=f"选择{opt}", use_container_width=True):
                    st.session_state.selected_level = opt
                    st.rerun()
    
    # 筛选逻辑处理
    filtered_ips = []
    if st.session_state.selected_type == "全部IP" and st.session_state.selected_level == "全部等级":
        filtered_ips = ip_data
    elif st.session_state.selected_type == "全部IP":
        filtered_ips = [ip for ip in ip_data if ip["level"] == st.session_state.selected_level]
    elif st.session_state.selected_level == "全部等级":
        filtered_ips = [ip for ip in ip_data if ip["type"] == st.session_state.selected_type]
    else:
        filtered_ips = [ip for ip in ip_data if ip["type"] == st.session_state.selected_type and ip["level"] == st.session_state.selected_level]

    # 操作按钮
    col1, col2, col3, col4 = st.columns([8, 2.5, 3, 3])

    with col2:
        # 按钮1：下载推荐榜单
        list_content = "\n".join([f"{ip['id']}. {ip['name']} ({ip['type']} | {ip['level']})\n核心驱动：{ip['driver']}" for ip in filtered_ips])
        st.download_button(
            label="⬇️ 下载推荐榜单",
            data=list_content,
            file_name="IP推荐榜单.txt",
            mime="text/plain",
            use_container_width=False
        )

    with col3:
        # 按钮2：导出10维评分Excel
        # 在每次页面运行时重新生成Excel文件
        rows = []
        for ip in filtered_ips:
            row = {
                "序号": ip['id'],
                "IP名称": ip['name'],
                "IP类型": ip['type'],
                "推荐等级": ip['level']
            }
            row.update(ip['scores'])
            rows.append(row)
        df = pd.DataFrame(rows)
        
        # 使用BytesIO和ExcelWriter生成Excel文件
        output = BytesIO()
        # 将指针移动到开始位置
        output.seek(0)
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="IP10维评分")
        
        # 获取BytesIO的值
        excel_data = output.getvalue()
        
        st.download_button(
            label="📊 导出10维评分Excel",
            data=excel_data,
            file_name="IP10维评分数据.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=False
        )


    # IP卡片列表
    if filtered_ips:
        for idx, ip in enumerate(filtered_ips):
            card_class = "ip-card active" if (idx == 0 and st.session_state.selected_type == "全部IP" and st.session_state.selected_level == "全部等级") else "ip-card"
            tag_class = "ip-tag" if ip["level"] == "S级推荐" else "ip-tag a"
            
            ip_id = ip["id"]
            ip_name = ip["name"]
            ip_type = ip["type"]
            ip_level = ip["level"]
            ip_driver = ip["driver"]
            ip_scores = ip["scores"]
            
            # 计算综合评分（基于多个关键维度）
            # 提取数值进行加权计算
            def extract_score(score_str):
                if '/' in score_str:
                    return float(score_str.split('/')[0])
                return 0
            
            # 获取各维度分数
            comprehensive = extract_score(ip_scores["IP综合素质"])  # 满分20
            communication = extract_score(ip_scores["传播裂变力"])  # 满分80
            risk = extract_score(ip_scores["风险指数"])  # 满分10（反向指标，越低越好）
            topic = extract_score(ip_scores["话题吸引力"])  # 满分10
            brand = extract_score(ip_scores["品牌适配度"])  # 满分10
            emotion = extract_score(ip_scores["情绪感染力"])  # 满分75
            circle = extract_score(ip_scores["圈层穿透力"])  # 满分15
            heat = extract_score(ip_scores["热度"])  # 满分25
            trend = extract_score(ip_scores["热度趋势"])  # 满分25
            commercial = extract_score(ip_scores["商业价值"])  # 满分10
            
            # 加权计算综合得分（转换为百分制）
            # 权重分配：综合素质20%，传播裂变15%，风险(反向)10%，话题10%，品牌适配15%，情绪10%，圈层5%，热度5%，趋势5%，商业价值5%
            weighted_score = (
                (comprehensive / 20 * 20) +  # 综合素质 20分
                (communication / 80 * 15) +   # 传播裂变 15分
                ((10 - risk) / 10 * 10) +      # 风险(反向) 10分（风险越低得分越高）
                (topic / 10 * 10) +             # 话题吸引力 10分
                (brand / 10 * 15) +              # 品牌适配 15分
                (emotion / 75 * 10) +             # 情绪感染力 10分
                (circle / 15 * 5) +                # 圈层穿透力 5分
                (heat / 25 * 5) +                   # 热度 5分
                (trend / 25 * 5) +                    # 热度趋势 5分
                (commercial / 10 * 5)                  # 商业价值 5分
            )
            
            # 四舍五入保留整数，并确保不超过100
            composite_score = min(round(weighted_score), 100)
            
            card_class_str = card_class
            tag_class_str = tag_class

            col_title, col_arrow = st.columns([4, 1])
            with col_title:
                st.markdown(f"""
                <div class="{card_class_str}">
                    <div class="ip-header">
                        <div class="ip-title">{ip_id}. {ip_name}</div>
                        <div class="ip-tags">
                            <span class="ip-tag" style="background:#fee2e2; color:#dc2626; font-weight:700; border:1px solid #fecaca;">综合 {composite_score}</span>
                            <span class="ip-tag">{ip_type}</span>
                            <span class="{tag_class_str}">{ip_level}</span>
                        </div>
                    </div>
                    <div class="score-grid">
                        <div class="score-item">
                            <div class="score-label">IP综合素质(20)</div>
                            <div class="score-value">{ip_scores["IP综合素质"]}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-label">传播裂变力(80)</div>
                            <div class="score-value">{ip_scores["传播裂变力"]}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-label">风险指数(10)</div>
                            <div class="score-value">{ip_scores["风险指数"]}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-label">话题吸引力(10)</div>
                            <div class="score-value">{ip_scores["话题吸引力"]}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-label">品牌适配度(10)</div>
                            <div class="score-value">{ip_scores["品牌适配度"]}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-label">情绪感染力(75)</div>
                            <div class="score-value">{ip_scores["情绪感染力"]}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-label">圈层穿透力(15)</div>
                            <div class="score-value">{ip_scores["圈层穿透力"]}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-label">热度(25)</div>
                            <div class="score-value">{ip_scores["热度"]}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-label">热度趋势(25)</div>
                            <div class="score-value">{ip_scores["热度趋势"]}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-label">商业价值(10)</div>
                            <div class="score-value">{ip_scores["商业价值"]}</div>
                        </div>
                    </div>
                    <div class="core-driver">{ip_driver}</div>
                </div>
                """, unsafe_allow_html=True)

            
            with col_arrow:
                # 添加箭头按钮
                if st.button("➡️", key=f"detail_{ip['name']}", help=f"查看{ip['name']}详情"):
                    st.session_state.current_ip = ip['name']
                    st.session_state.show_detail = True

    else:
        st.markdown('<div style="text-align:center; padding:20px; color:#6b7280;">暂无符合条件的IP数据</div>', unsafe_allow_html=True)

    # 分页
    st.markdown("""
    <div class="pagination">
        <div class="page-btn">◀</div>
        <div class="page-btn active">1</div>
        <div class="page-btn">2</div>
        <div class="page-btn">3</div>
        <div class="page-btn">4</div>
        <div class="page-btn">5</div>
        <div class="page-btn">▶</div>
    </div>
    """, unsafe_allow_html=True)
    
    @st.dialog(f"{st.session_state.current_ip} IP详细分析报告", width="large")
    def show_ip_detail():
        detail = ip_detail_data[st.session_state.current_ip]
        
        # 第一行：雷达图 + 优势因子
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            # 左侧：雷达图
            st.markdown('<h4>📊 10维评分雷达图</h4>', unsafe_allow_html=True)
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=detail["radar_values"],
                theta=detail["radar_labels"],
                fill='toself',
                name=st.session_state.current_ip
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(detail["radar_max"])],
                        tickfont=dict(size=8)  # 设置坐标轴刻度字体大小
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=8)   # 设置角度轴标签字体大小
                    )
                ),
                showlegend=False,
                height=200,
                margin=dict(l=40, r=40, t=20, b=20),
                font=dict(size=8)  # 全局字体设置
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with row1_col2:
            # 右侧：优势因子
            st.markdown("""
            <div class="report-card">
                <h4>✅ 优势因子</h4>
                {advantages}
            </div>
            """.format(
                advantages=''.join([f'<div class="advantage-item">{item}</div>' for item in detail["advantages"]])
            ), unsafe_allow_html=True)
        
        # 第二行：注意事项 + 预计表现
        row2_col1, row2_col2 = st.columns(2, gap="small")

        with row2_col1:
            # 左侧：注意事项
            with st.container():
                st.markdown("""
                <div class="report-card" style="height: 220px; overflow-y: auto;">
                    <h4 style="margin-top: 0; margin-bottom: 10px;">⚠️ 注意事项</h4>
                    {notes}
                </div>
                """.format(
                    notes=''.join([f'<div class="note-item" style="margin: 8px 0;">{item}</div>' for item in detail["notes"]])
                ), unsafe_allow_html=True)

        with row2_col2:
            # 右侧：预计表现
            with st.container():
                st.markdown("""
                <div class="report-card" style="height: 220px; overflow-y: auto;">
                    <h4 style="margin-top: 0; margin-bottom: 10px;">📈 预计表现</h4>
                    {performance}
                </div>
                """.format(
                    performance=''.join([f'<div class="performance-row" style="padding: 8px 0;"><span class="performance-label">{k}</span><span class="performance-value" style="float: right;">{v}</span></div>' for k, v in detail["performance"].items()])
                ), unsafe_allow_html=True)
        
        # 第三行：受众画像 + 词云图
        st.markdown('<h4 style="margin-top: 20px;">👥 受众画像 & 关键词云</h4>', unsafe_allow_html=True)

        # 创建两列布局
        aud_col1, aud_col2 = st.columns(2)

        with aud_col1:
            # 左侧：原有的受众画像（包含统计数据和饼图）
            # 在左侧内部再创建两列布局，让统计数据和饼图并排
            inner_col1, inner_col2 = st.columns([1,2])
            
            with inner_col1:
                # 受众统计数据
                for label, value in zip(detail["audience"]["labels"], detail["audience"]["values"]):
                    st.markdown(f"""
                    <div style="margin-bottom:15px;">
                        <div style="font-size:13px; color:#4b5563; margin-bottom:2px;">{label}</div>
                        <div style="font-size:18px; font-weight:600; color:#2563eb;">{value} TGI</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with inner_col2:
                # 饼图
                fig_donut = go.Figure(data=[go.Pie(
                    labels=detail["audience"]["labels"],
                    values=detail["audience"]["values"],
                    hole=0.6,
                    marker_colors=detail["audience"]["colors"],
                    textinfo='label+percent',  # 显示标签和百分比
                    hoverinfo='label+percent',
                    textposition='auto',  # 自动调整文字位置
                    insidetextorientation='radial'  # 文字方向
                )])
                
                fig_donut.update_layout(
                    height=300,
                    showlegend=False,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                
                st.plotly_chart(fig_donut, use_container_width=True)

        with aud_col2:
            
            # 获取词云数据
            ip_name = st.session_state.current_ip
            if "好好的时光" in ip_name:
                words = [
                    ("亲子", 28, "#e5392e"), ("治愈家庭", 26, "#1d4ed8"), ("女性向", 22, "#7c3aed"),
                    ("情感", 24, "#dc2626"), ("都市", 20, "#374151"), ("孙莉主演", 23, "#b45309"),
                    ("口碑", 25, "#065f46"), ("金牌导演", 21, "#b45309"), ("腾讯视频", 19, "#1d4ed8"),
                    ("温情", 24, "#9d174d")
                ]
            elif "巧虎" in ip_name:
                words = [
                    ("早教", 28, "#065f46"), ("亲子成长", 25, "#b45309"), ("卡通", 23, "#e5392e"),
                    ("0-6岁", 22, "#374151"), ("家庭", 24, "#1d4ed8"), ("科学育儿", 21, "#b45309"),
                    ("日本IP", 20, "#065f46"), ("启蒙", 26, "#7c3aed"), ("玩具", 19, "#9d174d")
                ]
            elif "亲子运动会" in ip_name:
                words = [
                    ("亲子运动", 28, "#9d174d"), ("健康家庭", 25, "#065f46"), ("全国巡回", 22, "#b45309"),
                    ("体育赛事", 24, "#7c3aed"), ("线下活动", 21, "#374151"), ("品牌冠名", 23, "#e5392e"),
                    ("10城", 20, "#5b21b6"), ("户外", 19, "#0369a1"), ("活力", 26, "#b91c1c")
                ]
            elif "小欢喜" in ip_name:
                words = [
                    ("家庭情感", 27, "#1d4ed8"), ("教育焦虑", 24, "#b45309"), ("暑期档", 22, "#7c3aed"),
                    ("成长", 23, "#065f46"), ("亲子关系", 26, "#e5392e"), ("高考", 25, "#9d174d"),
                    ("家庭教育", 28, "#b91c1c"), ("黄磊", 21, "#0369a1"), ("海清", 20, "#5b21b6")
                ]
            elif "年糕妈妈" in ip_name:
                words = [
                    ("科学育儿", 28, "#5b21b6"), ("带货", 26, "#065f46"), ("辅食", 24, "#b45309"),
                    ("婴儿护理", 23, "#e5392e"), ("垂直达人", 22, "#374151"), ("好物推荐", 25, "#7c3aed"),
                    ("母婴", 27, "#1d4ed8"), ("测评", 21, "#9d174d"), ("宝妈", 26, "#b91c1c")
                ]
            else:
                words = [
                    ("亲子", 28, "#1d4ed8"), ("家庭", 26, "#065f46"), ("教育", 24, "#b45309"),
                    ("成长", 25, "#7c3aed"), ("健康", 23, "#e5392e"), ("情感", 22, "#9d174d"),
                    ("娱乐", 21, "#0369a1"), ("消费", 20, "#5b21b6"), ("品质", 22, "#b91c1c")
                ]
            
            # 创建词云图（使用散点图模拟）
            import random
            random.seed(42)
            
            fig_wordcloud = go.Figure()
            
            for word, size, color in words:
                # 生成随机位置
                x = random.uniform(10, 90)
                y = random.uniform(10, 90)
                
                fig_wordcloud.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='text',
                    text=[word],
                    textfont=dict(
                        size=size,
                        color=color,
                        family='Noto Sans SC, sans-serif',
                        weight='bold' if size > 24 else 'normal'
                    ),
                    hoverinfo='text',
                    hovertext=f'{word} ({size})',
                    showlegend=False
                ))
            
            fig_wordcloud.update_layout(
                xaxis=dict(
                    showgrid=False,
                    showticklabels=False,
                    zeroline=False,
                    range=[0, 100]
                ),
                yaxis=dict(
                    showgrid=False,
                    showticklabels=False,
                    zeroline=False,
                    range=[0, 100]
                ),
                height=250,
                margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='#f8fafc',  # 浅灰色背景
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='closest'
            )
            
            st.plotly_chart(fig_wordcloud, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        # 底部分页
        st.markdown("""
        <div style="display:flex; justify-content:center; gap:8px; margin-top:20px;">
            <div class="report-page-btn">◀</div>
            <div class="report-page-btn active">1</div>
            <div class="report-page-btn">2</div>
            <div class="report-page-btn">3</div>
            <div class="report-page-btn">4</div>
            <div class="report-page-btn">5</div>
            <div class="report-page-btn">▶</div>
        </div>
        """, unsafe_allow_html=True)

    # 调用 dialog
    if st.session_state.get("show_detail"):
        show_ip_detail()

# ═══════ TAB 2: 智能问答 ═══════════════════════════════════════════════════════════════
with tab2:

    
    sb_col, chat_col = st.columns([1, 3.5])
    with sb_col:
        st.markdown('<div class="sb-bot"><span style="font-size:20px;">🤖</span><div><div style="font-size:13px;font-weight:700;">IP投资顾问</div><div style="font-size:10.5px;opacity:.8;">智能分析 · 实时推荐</div></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-sec">功能入口</div><div class="sb-item on">💬 智能问答</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:1px;background:#e8eaf0;margin:8px 0;"></div><div class="sb-sec">历史记录</div>', unsafe_allow_html=True)
        for hist in st.session_state.chat_history[-3:]:
            if hist['role'] == 'user':
                st.markdown(f'<div class="sb-item">🕐 {hist["content"][:15]}...</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:1px;background:#e8eaf0;margin:8px 0;"></div><div class="sb-sec">💡 推荐问题</div>', unsafe_allow_html=True)
        for sq in ['未来7天热门IP推荐','好好的时光详细分析','低风险稳健投资推荐','各IP预算对比','年糕妈妈性价比分析']:
            st.button(sq, key='sq_'+sq, use_container_width=True, type="secondary")
        st.markdown('<div style="height:1px;background:#e8eaf0;margin:10px 0 6px;"></div><div class="sb-sec">⚙️ 处理流程</div>', unsafe_allow_html=True)
        st.markdown('<div class="proc-item">✅ 调取IP热度知识库<br>✅ 调取热度预测模型<br>✅ 整合数据生成交付物</div>', unsafe_allow_html=True)
    
    with chat_col:
        st.markdown('<div class="flow-bar"><span class="fn">① 用户提问</span><span class="fa">→</span><span class="fn">② 智能体调取IP热度知识库/预测模型</span><span class="fa">→</span><span class="fn">③ 输出IP推荐 + 多维度分析</span><span class="fa">→</span><span class="fn">④ 标准化专业报告</span></div>', unsafe_allow_html=True)
        
        if not st.session_state.chat_history:
            st.markdown('<div style="background:#fff;border:1.5px solid #e8eaf0;border-radius:12px;padding:18px 22px;min-height:320px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#94a3b8;"><div style="font-size:44px;margin-bottom:12px;">🤖</div><div style="font-size:15px;font-weight:600;color:#475569;margin-bottom:6px;">智能IP投资顾问</div><div style="font-size:12.5px;">请输入您的投资需求，例如「未来7天有哪些值得投资的IP？」</div></div>', unsafe_allow_html=True)
        else:
            chat_html = '<div style="background:#fff;border:1.5px solid #e8eaf0;border-radius:12px;padding:18px 22px;min-height:320px;">'
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    chat_html += '<div class="u-msg"><div class="u-bub">' + msg['content'] + '</div></div>'
                else:
                    c = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', msg['content'])
                    c = c.replace('\n\n','<br><br>').replace('\n','<br>')
                    chat_html += '<div class="a-msg"><div class="a-av">🤖</div><div class="a-bub">' + c + '</div></div>'
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)
        
        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([6, 1, 1])
        with c1:
            user_in = st.text_input('i', placeholder='请输入您的IP投资需求...', label_visibility='collapsed', key='ci')
        with c2:
            send_btn = st.button('发送 →', type='primary', use_container_width=True)
        with c3:
            if st.button('清空', use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        def do_send(q):
            st.session_state.chat_history.append({'role': 'user', 'content': q})
            with st.spinner('AI分析中...'): 
                time.sleep(0.4)
            st.session_state.chat_history.append({'role': 'assistant', 'content': mock_ai(q)})
            st.rerun()
        
        if '_pq' in st.session_state:
            do_send(st.session_state.pop('_pq'))
        
        if send_btn and user_in.strip():
            do_send(user_in.strip())

