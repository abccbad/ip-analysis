import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import tempfile
import os
import platform
import time
import shutil

# ===================== 页面基础配置 =====================
st.set_page_config(
    page_title="营销资源智推Agent示例_智能问答",
    page_icon="📊",
    layout="wide"
)

# ===================== 全局样式 =====================
st.markdown("""
<style>
.stApp { background-color: #f8fafc; font-family: "Microsoft YaHei", sans-serif; }
.stTabs [data-baseweb="tab-list"] { gap: 0px; border-bottom: 1px solid #e2e8f0; }
.stTabs [data-baseweb="tab"] { padding: 0.6rem 1.5rem; font-size: 14px; font-weight: 500; color: #475569; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { color: #2563eb; border-bottom: 2px solid #2563eb; }
.module-box { border: 1px solid #e2e8f0; border-radius: 6px; padding: 1.2rem; margin-bottom: 1rem; background-color: #fff; }
.title-main { font-size: 20px; font-weight: 600; color: #1e293b; margin-bottom: 1rem; }
.title-sub { font-size: 16px; font-weight: 600; color: #334155; margin-bottom: 0.8rem; }
.step-tag { display: inline-flex; align-items: center; justify-content: center; width:24px; height:24px; 
           border-radius:50%; background:#2563eb; color:white; font-size:12px; margin-right:0.5rem; }
.ip-card { border:1px solid #e2e8f0; border-radius:6px; padding:1.2rem; margin-bottom:1.2rem; background:#fff; }
.loader { border:4px solid #f3f4f6; border-top:4px solid #2563eb; border-radius:50%; width:20px; height:20px; 
         animation:spin 1s linear infinite; display:inline-block; margin-right:8px; }
@keyframes spin { 0%{transform:rotate(0deg);} 100%{transform:rotate(360deg);} }
</style>
""", unsafe_allow_html=True)

# ===================== 字体加载 =====================
def load_chinese_font():
    """适配Streamlit 3.10 + 云端Linux环境的中文字体加载"""
    try:
        # Streamlit Cloud(Linux)优先加载开源中文字体，兼容本地Windows/Mac
        font_candidates = [
            # Streamlit Cloud 内置中文字体
            ("WenQuanYi Micro Hei", "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
            # Linux通用字体（备用）
            ("DejaVu Sans", None),
            # 本地Windows兼容
            ("SimHei", "C:/Windows/Fonts/simhei.ttf"),
            ("Microsoft YaHei", "C:/Windows/Fonts/msyh.ttc"),
            # Mac兼容
            ("PingFangSC", "/System/Library/Fonts/PingFang.ttc"),
            # 兜底
            ("Arial", None)
        ]
        
        for font_name, font_path in font_candidates:
            try:
                if font_path and os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    return font_name
                elif font_path is None:
                    # 系统内置字体无需路径
                    return font_name
            except Exception as e:
                continue
        return "Arial"
    except Exception as e:
        st.warning(f"字体加载降级为默认：{e}")
        return "Arial"

CHINESE_FONT = load_chinese_font()

# ===================== 数据定义 =====================
all_ip_data = [
    {
        "id": 1,
        "name": "《好好的时光》",
        "type": "影视IP",
        "comprehensive": 89,
        "communication": 78,
        "risk": {"type": "竞品抢投", "level": "中（12%）", "suggestion": "建议48小时内锁定合作"},
        "topic": 79,
        "brand_fit": 75,
        "emotion": 72,
        "circle": 56,
        "popularity": 74,
        "trend": 73,
        "commercial": 79,
        "roi": "210%",
        "driver": "2026年3月热播+25-35岁女性受众占比85%",
        "budget": "60–85万元",
        "audience": {"25-35岁女性": 85, "亲子家庭": 89, "下沉市场用户": 68, "高消费能力": 76},
        "advantage": ["IP综合素质评分89，行业顶尖水平", "品牌适配度评分75，与乳品品牌高度契合"],
        "performance": {"roi": "210%", "payback": "45天", "brand_voice": "180%", "conversion": "25%", "heat_peak": "24.5/25 (D+4)"},
        "analysis": {
            "value": "都市情感剧，精准覆盖25-35岁核心消费女性，情感共鸣强，品牌植入场景自然，是乳品/母婴品类的黄金载体",
            "audience": "25-35岁女性占比85%，亲子家庭渗透率89%，高消费能力用户76%，是典型的“高价值妈妈人群”，消费意愿强、决策链路短",
            "strategy": "竞品抢投风险中等，建议优先锁定剧集前3集黄金广告位，配合剧情节点做情感向营销，最大化曝光转化",
            "roi": "预计45天回本，ROI达210%，核心驱动是高精准人群触达+强情感共鸣带来的高转化，品牌声量可提升180%"
        }
    },
    {
        "id": 2,
        "name": "巧虎",
        "type": "动漫IP",
        "comprehensive": 78,
        "communication": 75,
        "risk": {"type": "内容合规", "level": "低（5%）", "suggestion": "需审核早教内容适配性"},
        "topic": 78,
        "brand_fit": 70,
        "emotion": 70,
        "circle": 73,
        "popularity":72,
        "trend": 71,
        "commercial": 78,
        "roi": "180%",
        "driver": "新早教课程上线+亲子家庭占比95%",
        "budget": "50-70万元",
        "audience": {"3-6岁儿童": 90, "宝妈群体": 98, "一二线城市家庭": 75, "高消费能力": 80},
        "advantage": ["IP综合素质评分75，行业优秀水平", "品牌适配度70，与母婴乳品高度契合"],
        "performance": {"roi": "180%", "payback": "60天", "brand_voice": "150%", "conversion": "20%", "heat_peak": "22.5/25 (D+5)"},
        "analysis": {
            "value": "经典早教IP，用户信任度高，3-6岁儿童核心受众明确，内容安全合规，是母婴品类的安全选择",
            "audience": "宝妈群体渗透率98%，一二线城市家庭占比75%，高消费能力用户80%，是典型的“精致育儿”人群，对品质要求高、价格敏感度低",
            "strategy": "内容合规风险低，可深度绑定早教课程做联合营销，推出IP定制款产品，提升用户粘性",
            "roi": "预计60天回本，ROI达180%，核心驱动是高信任度带来的复购率，品牌声量可提升150%"
        }
    },
    {
        "id": 3,
        "name": "2026中国亲子运动会",
        "type": "体育赛事IP",
        "comprehensive": 60,
        "communication": 73,
        "risk": {"type": "执行风险", "level": "中（10%）", "suggestion": "提前确认赛事落地细节"},
        "topic": 78,
        "brand_fit": 60,
        "emotion": 68,
        "circle": 72,
        "popularity": 71,
        "trend":70,
        "commercial": 77,
        "roi": "170%",
        "driver": "国家级赛事曝光+亲子家庭强关联",
        "budget": "70-90万元",
        "audience": {"亲子家庭": 92, "体育爱好者": 65, "一二线城市用户": 80, "高消费能力": 78},
        "advantage": ["IP综合素质评分60，官方背书公信力强", "品牌适配度60，亲子场景高度契合"],
        "performance": {"roi": "170%", "payback": "75天", "brand_voice": "160%", "conversion": "18%", "heat_peak": "21/25 (D+3)"},
        "analysis": {
            "value": "国家级体育赛事IP，官方背书公信力强，亲子运动场景天然适配健康品类，适合做线下体验+线上传播",
            "audience": "亲子家庭占比92%，体育爱好者65%，一二线城市用户80%，是典型的“健康生活”人群，注重运动与家庭陪伴",
            "strategy": "执行风险中等，建议提前确认赛事流程与赞助权益，重点布局线下亲子互动区，结合赛事做直播带货",
            "roi": "预计75天回本，ROI达170%，核心驱动是线下体验带来的高转化，品牌声量可提升160%"
        }
    },
    {
        "id": 4,
        "name": "《小敏家2》",
        "type": "影视IP",
        "comprehensive": 58,
        "communication": 73,
        "risk": {"type": "口碑风险", "level": "低（8%）", "suggestion": "关注剧集播出口碑"},
        "topic": 79,
        "brand_fit": 68,
        "emotion": 71,
        "circle": 63,
        "popularity": 62,
        "trend": 60,
        "commercial": 68,
        "roi": "175%",
        "driver": "经典IP续作+家庭场景强关联",
        "budget": "65-75万元",
        "audience": {"30-45岁女性": 88, "家庭用户": 90, "下沉市场用户": 70, "高消费能力": 75},
        "advantage": ["IP综合素质评分58，经典IP受众基础好", "家庭场景适配度高，品牌植入自然"],
        "performance": {"roi": "175%", "payback": "65天", "brand_voice": "155%", "conversion": "19%", "heat_peak": "22/25 (D+4)"},
        "analysis": {
            "value": "经典家庭剧续作，受众基础稳固，30-45岁成熟女性占比高，家庭场景密集，适合家居/家电/乳品等品类植入",
            "audience": "30-45岁女性占比88%，家庭用户90%，高消费能力用户75%，是典型的“家庭决策者”人群，消费决策理性、注重品质",
            "strategy": "口碑风险低，可结合剧集温情节点做品牌故事营销，突出“家”的情感共鸣，提升品牌温度",
            "roi": "预计65天回本，ROI达175%，核心驱动是经典IP带来的高关注度，品牌声量可提升155%"
        }
    },
    {
        "id": 5,
        "name": "年糕妈妈",
        "type": "KOL IP",
        "comprehensive": 55,
        "communication": 72,
        "risk": {"type": "合作风险", "level": "低（6%）", "suggestion": "锁定独家合作权益"},
        "topic": 67,
        "brand_fit": 69,
        "emotion": 70,
        "circle": 62,
        "popularity": 60,
        "trend": 61,
        "commercial": 69,
        "roi": "175%",
        "driver": "母婴垂类头部博主+带货能力强",
        "budget": "40-60万元",
        "audience": {"25-40岁宝妈": 95, "新手父母": 92, "高线城市用户": 85, "高消费能力": 82},
        "advantage": ["IP综合素质评分55，垂类影响力顶尖", "商业转化能力强，ROI兑现度高"],
        "performance": {"roi": "175%", "payback": "50天", "brand_voice": "140%", "conversion": "22%", "heat_peak": "20/25 (D+2)"},
        "analysis": {
            "value": "母婴垂类头部KOL，专业信任度高，带货能力强，是母婴品类的高效转化渠道",
            "audience": "25-40岁宝妈占比95%，新手父母92%，高线城市用户85%，高消费能力用户82%，是典型的“新手妈妈”人群，对专业推荐信任度高、转化意愿强",
            "strategy": "合作风险低，建议锁定独家直播带货权益，配合KOL专业测评内容，快速提升产品销量",
            "roi": "预计50天回本，ROI达175%，核心驱动是高信任度带来的高转化，品牌声量可提升140%"
        }
    },
    {
        "id": 6,
        "name": "《妈妈是超人6》",
        "type": "综艺IP",
        "comprehensive": 54,
        "communication": 71,
        "risk": {"type": "收视率风险", "level": "中（10%）", "suggestion": "需关注首播数据"},
        "topic": 68,
        "brand_fit": 69,
        "emotion": 70,
        "circle": 62,
        "popularity": 61,
        "trend": 60,
        "commercial": 68,
        "roi": "160%",
        "driver": "经典综艺IP+明星宝妈阵容",
        "budget": "65-80万元",
        "audience": {"25-40岁女性": 85, "亲子家庭": 88, "娱乐爱好者": 75, "高消费能力": 72},
        "advantage": ["IP综合素质评分54，经典IP口碑保障", "品牌适配度69，母婴乳品适配性高"],
        "performance": {"roi": "160%", "payback": "70天", "brand_voice": "150%", "conversion": "17%", "heat_peak": "21/25 (D+3)"},
        "analysis": {
            "value": "经典亲子综艺，明星宝妈阵容自带流量，亲子互动场景丰富，适合母婴/乳品/玩具等品类植入",
            "audience": "25-40岁女性占比85%，亲子家庭88%，高消费能力用户72%，是典型的“追星妈妈”人群，对明星同款敏感度高、消费意愿强",
            "strategy": "收视率风险中等，建议关注首播数据，灵活调整投放策略，重点布局明星带娃场景的植入",
            "roi": "预计70天回本，ROI达160%，核心驱动是明星流量带来的高曝光，品牌声量可提升150%"
        }
    }
]

# ===================== 会话状态初始化 =====================
if "selected_ip_id" not in st.session_state:
    st.session_state.selected_ip_id = None
if "chart_cache" not in st.session_state:
    st.session_state.chart_cache = {}
if "temp_files" not in st.session_state:
    st.session_state.temp_files = []

# ===================== 工具函数 =====================
def cleanup_temp_files():
    """兼容Streamlit 3.10 + 云端的临时文件清理（容错处理）"""
    try:
        for fp in st.session_state.get("temp_files", []):
            if fp and isinstance(fp, str) and os.path.exists(fp):
                try:
                    os.remove(fp)
                except Exception as e:
                    st.warning(f"清理临时文件 {fp} 失败：{e}")
        st.session_state["temp_files"] = []
        st.session_state["chart_cache"] = {}
    except Exception as e:
        st.warning(f"临时文件清理失败：{e}")

def generate_chart_images(ip_data, use_cache=True):
    """适配Streamlit 3.10：保留本地文件生成逻辑（兼容云端临时目录）"""
    cache_key = f"{ip_data['id']}_charts"
    if use_cache and cache_key in st.session_state.chart_cache:
        return st.session_state.chart_cache[cache_key]
    
    try:
        # 雷达图
        radar_labels = ["综合评分", "传播裂变", "风险指数", "话题热度", "品牌适配"]
        radar_values = [ip_data['comprehensive']/2, ip_data['communication']/8, list(ip_data['risk'].values()).index(ip_data['risk']['level'])+1, ip_data['topic'], ip_data['brand_fit']]
        fig_radar = go.Figure(go.Scatterpolar(r=radar_values, theta=radar_labels, fill='toself', line=dict(color='#2563eb', width=3), fillcolor='rgba(37, 99, 235, 0.3)', marker=dict(size=10, color='#2563eb')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10], tickvals=[0,2,4,6,8,10]), angularaxis=dict(tickfont=dict(size=12))), showlegend=False, width=500, height=500, margin=dict(l=40, r=60, t=40, b=40), font=dict(family=CHINESE_FONT))
        # 柱状图
        df_aud = pd.DataFrame(list(ip_data['audience'].items()), columns=["受众类型", "占比(%)"])
        fig_aud = px.bar(df_aud, x="受众类型", y="占比(%)", color_discrete_sequence=["#2563eb", "#3b82f6", "#60a5fa", "#93c5fd"])
        fig_aud.update_layout(width=800, height=450, margin=dict(l=40, r=40, t=40, b=60), showlegend=False, font=dict(family=CHINESE_FONT))
        
        # 使用云端可写的临时目录（关键适配）
        radar_path = tempfile.mkstemp(suffix='.png', dir=tempfile.gettempdir())[1]
        aud_path = tempfile.mkstemp(suffix='.png', dir=tempfile.gettempdir())[1]
        
        # 生成图片（适配Plotly在Streamlit 3.10的调用方式）
        fig_radar.write_image(radar_path, scale=3)
        fig_aud.write_image(aud_path, scale=3)
        
        st.session_state.temp_files.extend([radar_path, aud_path])
        st.session_state.chart_cache[cache_key] = (radar_path, aud_path)
        return radar_path, aud_path
    except Exception as e:
        st.error(f"图表生成失败: {str(e)}")
        return None, None

def generate_text_report(content):
    buf = BytesIO()
    buf.write(content.encode('utf-8'))
    buf.seek(0)
    return buf

def generate_qa_report_pdf():
    try:
        with st.spinner("正在生成PDF报告..."):
            time.sleep(0.5)
            buf = BytesIO()
            page_width, page_height = landscape(A4)
            doc = SimpleDocTemplate(
                buf, pagesize=landscape(A4),
                rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
            )
            frame = Frame(30, 30, page_width-60, page_height-60, id='normal')
            doc.addPageTemplates([PageTemplate(id='all', frames=[frame])])
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'title', parent=styles['Heading1'],
                fontSize=16, alignment=TA_CENTER, fontName=CHINESE_FONT,
                textColor=colors.darkblue, spaceAfter=12
            )
            section_style = ParagraphStyle(
                'section', parent=styles['Heading2'],
                fontSize=12, fontName=CHINESE_FONT, spaceAfter=8
            )
            normal_style = ParagraphStyle(
                'normal', parent=styles['Normal'],
                fontSize=10, fontName=CHINESE_FONT, spaceAfter=4
            )
            list_style = ParagraphStyle(
                'list', parent=styles['Normal'],
                fontSize=10, fontName=CHINESE_FONT, leftIndent=12, spaceAfter=3
            )
            
            elements = []
            elements.append(Paragraph("智能问答：未来7天热门投资IP推荐报告", title_style))
            elements.append(Spacer(1, 15))
            
            elements.append(Paragraph("一、用户提问", section_style))
            question = "业务人员提问：我想知道未来7天，有什么IP是比较火的，值得投资的？请给出具体IP推荐、核心数据支撑及投资建议。"
            elements.append(Paragraph(question, normal_style))
            elements.append(Spacer(1, 8))
            
            elements.append(Paragraph("二、智能体后台处理", section_style))
            steps = [
                "• 调取IP热度知识库：获取母婴乳品赛道近30天10大维度数据",
                "• 调用IP热度预测模型：输出未来7天评分与推荐指数",
                "• 生成交付物：TOP5列表、趋势图、雷达图、专业分析报告"
            ]
            for step in steps:
                elements.append(Paragraph(step, list_style))
            elements.append(Spacer(1, 10))
            
            elements.append(Paragraph("三、智能体全维度输出", section_style))
            answer = """
未来7天母婴乳品赛道TOP5值得投资的IP：
1. 《好好的时光》：综合80，传播78，风险低，ROI 210%，预算60-85万
   - 核心价值：都市情感剧，精准覆盖25-35岁核心消费女性，情感共鸣强，品牌植入场景自然
   - 受众洞察：25-35岁女性占比85%，亲子家庭渗透率89%，高消费能力用户76%，是典型的“高价值妈妈人群”
   - 投放建议：竞品抢投风险中等，建议48小时内锁定前3集黄金广告位，配合剧情节点做情感向营销
2. 巧虎：综合75，传播66，ROI 180%，预算50-70万
   - 核心价值：经典早教IP，用户信任度高，3-6岁儿童核心受众明确，内容安全合规
   - 受众洞察：宝妈群体渗透率98%，一二线城市家庭占比75%，高消费能力用户80%，是典型的“精致育儿”人群
   - 投放建议：内容合规风险低，可深度绑定早教课程做联合营销，推出IP定制款产品
3. 2026中国亲子运动会：综合60，官方背书，ROI 170%，预算70-90万
   - 核心价值：国家级体育赛事IP，官方背书公信力强，亲子运动场景天然适配健康品类
   - 受众洞察：亲子家庭占比92%，体育爱好者65%，一二线城市用户80%，是典型的“健康生活”人群
   - 投放建议：执行风险中等，提前确认赛事流程与赞助权益，重点布局线下亲子互动区

综合推荐：Top1：《好好的时光》，无负面舆情，各维度表现优秀，是当前母婴乳品赛道的最优投资选择。
            """
            for line in answer.strip().split('\n'):
                if line.strip():
                    elements.append(Paragraph(line.strip(), normal_style))
            elements.append(PageBreak())
            
            elements.append(Paragraph("四、核心数据图表", section_style))
            # 修复趋势图：前半段历史，后半段预测
            days = ["D-7","D-6","D-5","D-4","D-3","D-2","D-1","D0","D+1","D+2","D+3","D+4","D+5","D+6","D+7"]
            history = [20,25,30,35,40,45,50,60,70,80,85,82,78,75,70]
            predict = [60,65,70,75,80,85,90,95,100,98,95,90,85,80,75]
            
            history_x = days[:days.index("D0")+1]
            history_y = history[:len(history_x)]
            predict_x = days[days.index("D0"):]
            predict_y = predict[days.index("D0"):]
            
            fig_t = go.Figure()
            fig_t.add_trace(go.Scatter(
                x=history_x, y=history_y, name='历史热度',
                line=dict(color='#2563eb', width=3)
            ))
            fig_t.add_trace(go.Scatter(
                x=predict_x, y=predict_y, name='预测热度',
                line=dict(color='#93c5fd', width=2, dash='dash')
            ))
            fig_t.update_layout(
                title=dict(text="《好好的时光》热度趋势分析", x=0.5),
                xaxis_title="时间维度", yaxis_title="热度值",
                width=1000, height=400, font=dict(family=CHINESE_FONT)
            )
            
            # 使用云端可写临时目录
            trend_pdf = tempfile.mkstemp(suffix='.png', dir=tempfile.gettempdir())[1]
            fig_t.write_image(trend_pdf, scale=3)
            st.session_state.temp_files.append(trend_pdf)
            
            elements.append(Paragraph("1. 热度趋势图", section_style))
            elements.append(Image(trend_pdf, width=page_width*0.9, height=280, hAlign='CENTER'))
            elements.append(Spacer(1, 10))
            
            elements.append(Paragraph("2. 10大维度评分雷达图", section_style))
            labels_10 = ["综合素质(80)","传播裂变(78)","风险(2)","热度(60)","趋势(66)",
                        "商业(70)","话题(70)","适配(75)","情感(72)","圈层(70)"]
            values_10 =[80,78,2,60,66,70,70,75,72,70]
            industry_values = [60,60,5,60,60,60,60,60,60,60]
            
            fig_radar_10 = go.Figure()
            fig_radar_10.add_trace(go.Scatterpolar(
                r=values_10, theta=labels_10, fill='toself', name='《好好的时光》',
                line=dict(color='#2563eb', width=2)
            ))
            fig_radar_10.add_trace(go.Scatterpolar(
                r=industry_values, theta=labels_10, fill='toself', name='行业均值',
                line=dict(color='#94a3b8', width=1.5), opacity=0.6
            ))
            fig_radar_10.update_layout(
                polar=dict(radialaxis=dict(range=[0, 80])),
                width=600, height=600, font=dict(family=CHINESE_FONT)
            )
            
            # 使用云端可写临时目录
            radar_10_path = tempfile.mkstemp(suffix='.png', dir=tempfile.gettempdir())[1]
            fig_radar_10.write_image(radar_10_path, scale=3)
            st.session_state.temp_files.append(radar_10_path)
            
            elements.append(Image(radar_10_path, width=page_height*0.45, height=page_height*0.45, hAlign='CENTER'))
            doc.build(elements)
            buf.seek(0)
            return buf
    except Exception as e:
        st.error(f"PDF生成失败: {str(e)}")
        return generate_text_report(f"智能问答报告生成失败：{str(e)}")

def generate_ip_report_pdf(ip):
    """生成单个IP的PDF报告（保留原有完整功能）"""
    try:
        with st.spinner(f"正在生成《{ip['name']}》PDF报告..."):
            time.sleep(0.5)
            buf = BytesIO()
            page_width, page_height = landscape(A4)
            doc = SimpleDocTemplate(
                buf, pagesize=landscape(A4),
                rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
            )
            frame = Frame(30, 30, page_width-60, page_height-60, id='normal')
            doc.addPageTemplates([PageTemplate(id='all', frames=[frame])])
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'title', parent=styles['Heading1'],
                fontSize=16, alignment=TA_CENTER, fontName=CHINESE_FONT,
                textColor=colors.darkblue, spaceAfter=15
            )
            section_style = ParagraphStyle(
                'section', parent=styles['Heading2'],
                fontSize=12, fontName=CHINESE_FONT, spaceAfter=8
            )
            normal_style = ParagraphStyle(
                'normal', parent=styles['Normal'],
                fontSize=10, fontName=CHINESE_FONT, spaceAfter=4
            )
            list_style = ParagraphStyle(
                'list', parent=styles['Normal'],
                fontSize=10, fontName=CHINESE_FONT, leftIndent=12, spaceAfter=3
            )
            
            elements = []
            elements.append(Paragraph(f"{ip['name']} IP分析报告", title_style))
            elements.append(Spacer(1, 15))
            
            elements.append(Paragraph("一、IP综合价值定位", section_style))
            elements.append(Paragraph(ip['analysis']['value'], normal_style))
            elements.append(Spacer(1, 8))
            
            elements.append(Paragraph("二、基础信息", section_style))
            base_data = [
                ['IP类型', ip['type']],
                ['核心驱动', ip['driver']],
                ['预算范围', ip['budget']],
                ['预期ROI', ip['roi']],
                ['综合评分', f"{ip['comprehensive']}/20"],
                ['传播裂变力', f"{ip['communication']}/80"]
            ]
            base_table = Table(base_data, colWidths=[120, 300])
            base_table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 1, colors.grey),
                ('FONTNAME', (0,0), (-1,-1), CHINESE_FONT),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))
            elements.append(base_table)
            elements.append(Spacer(1, 10))
            
            elements.append(Paragraph("三、受众深度画像", section_style))
            elements.append(Paragraph(ip['analysis']['audience'], normal_style))
            elements.append(Spacer(1, 8))
            
            elements.append(Paragraph("四、风险提示", section_style))
            risk_data = [
                ['风险类型', ip['risk']['type']],
                ['风险等级', ip['risk']['level']],
                ['操作建议', ip['risk']['suggestion']]
            ]
            risk_table = Table(risk_data, colWidths=[120, 300])
            risk_table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 1, colors.grey),
                ('FONTNAME', (0,0), (-1,-1), CHINESE_FONT),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))
            elements.append(risk_table)
            elements.append(Spacer(1, 10))
            
            elements.append(Paragraph("五、核心优势", section_style))
            for advantage in ip['advantage']:
                elements.append(Paragraph(f"• {advantage}", list_style))
            elements.append(Spacer(1, 10))
            
            elements.append(Paragraph("六、核心维度评分", section_style))
            radar_img, aud_img = generate_chart_images(ip)
            if radar_img:
                elements.append(Image(radar_img, width=200, height=200, hAlign='CENTER'))
            elements.append(Spacer(1, 10))
            
            elements.append(Paragraph("七、受众画像图表", section_style))
            if aud_img:
                elements.append(Image(aud_img, width=380, height=220, hAlign='CENTER'))
            elements.append(Spacer(1, 10))
            
            elements.append(Paragraph("八、投放策略建议", section_style))
            elements.append(Paragraph(ip['analysis']['strategy'], normal_style))
            elements.append(Spacer(1, 8))
            
            elements.append(Paragraph("九、商业ROI拆解", section_style))
            elements.append(Paragraph(ip['analysis']['roi'], normal_style))
            elements.append(Spacer(1, 8))
            
            elements.append(Paragraph("十、投放效果预估", section_style))
            perf_data = [['评估维度', '预估数值']] + [[k, v] for k, v in ip['performance'].items()]
            perf_table = Table(perf_data, colWidths=[120, 300])
            perf_table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 1, colors.grey),
                ('FONTNAME', (0,0), (-1,-1), CHINESE_FONT),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))
            elements.append(perf_table)
            doc.build(elements)
            buf.seek(0)
            return buf
    except Exception as e:
        st.error(f"生成{ip['name']} PDF失败: {str(e)}")
        return generate_text_report(f"{ip['name']} 分析报告\n\n生成失败：{str(e)}")

# ===================== 页面渲染 =====================
def render_qa_page():
    """渲染智能问答页面（完全保留原有格式和功能）"""
    st.markdown('<div class="title-main">智能问答：未来7天热门投资IP推荐</div>', unsafe_allow_html=True)
    st.caption("提问 → 智能分析 → 推荐+图表+专业报告")

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;align-items:center"><span class="step-tag">1</span><span class="title-sub">用户提问</span></div>', unsafe_allow_html=True)
    # 保留原有修复：非空label + 隐藏
    st.text_area(
        "用户提问内容",
        "业务人员提问：我想知道未来7天，有什么IP是比较火的，值得投资的？请给出具体IP推荐、核心数据支撑及投资建议。",
        height=80, 
        disabled=True, 
        label_visibility="hidden"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;align-items:center"><span class="step-tag">2</span><span class="title-sub">智能体处理流程</span></div>', unsafe_allow_html=True)
    st.write("""
    1. **数据调取**：从IP知识库中提取近30天10大维度核心数据（综合评分、传播力、风险、热度等）
    2. **模型预测**：基于历史数据训练的热度预测模型，输出未来7天热度走势与投资价值评分
    3. **维度加权**：结合品牌适配度、商业价值、受众画像等维度，加权计算最终ROI与推荐等级
    4. **报告生成**：自动生成可视化图表与专业文字分析，输出可直接用于决策的投资报告
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;align-items:center"><span class="step-tag">3</span><span class="title-sub">TOP3 IP推荐与分析</span></div>', unsafe_allow_html=True)
    
    st.subheader("🏆 TOP1：《好好的时光》（影视IP）")
    st.write("**综合评分：80 | 预估ROI：210% | 预算：60-85万元**")
    st.write("""
    - **核心价值**：都市情感剧，精准覆盖25-35岁核心消费女性，情感共鸣强，品牌植入场景自然，是乳品/母婴品类的黄金载体
    - **受众洞察**：25-35岁女性占比85%，亲子家庭渗透率89%，高消费能力用户76%，是典型的“高价值妈妈人群”，消费意愿强、决策链路短
    - **风险提示**：竞品抢投风险中等（12%），建议48小时内锁定前3集黄金广告位，避免被竞品截胡
    - **投放建议**：配合剧情情感节点做“陪伴式”营销，突出品牌与剧集的情感共鸣，最大化转化效率
    """)
    
    st.subheader("🥈 TOP2：巧虎（动漫IP）")
    st.write("**综合评分：75 | 预估ROI：180% | 预算：50-70万元**")
    st.write("""
    - **核心价值**：经典早教IP，用户信任度高，3-6岁儿童核心受众明确，内容安全合规，是母婴品类的安全选择
    - **受众洞察**：宝妈群体渗透率98%，一二线城市家庭占比75%，高消费能力用户80%，是典型的“精致育儿”人群
    - **风险提示**：内容合规风险低（5%），需提前审核广告内容与IP调性的匹配度
    - **投放建议**：深度绑定早教课程做联合营销，推出IP定制款产品，提升用户粘性与复购率
    """)
    
    st.subheader("🥉 TOP3：2026中国亲子运动会（体育赛事IP）")
    st.write("**综合评分：60 | 预估ROI：170% | 预算：70-90万元**")
    st.write("""
    - **核心价值**：国家级体育赛事IP，官方背书公信力强，亲子运动场景天然适配健康品类
    - **受众洞察**：亲子家庭占比92%，体育爱好者65%，一二线城市用户80%，是典型的“健康生活”人群
    - **风险提示**：执行风险中等（10%），需提前确认赛事落地细节与赞助权益
    - **投放建议**：重点布局线下亲子互动区，结合赛事做直播带货，实现“体验+转化”闭环
    """)
    
    st.write("""**综合推荐**：Top1《好好的时光》，无负面舆情，各维度表现优秀，是当前母婴乳品赛道的最优投资选择。""")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 热度趋势分析")
        days = ["D-7","D-6","D-5","D-4","D-3","D-2","D-1","D0","D+1","D+2","D+3","D+4","D+5","D+6","D+7"]
        history = [20,25,30,35,40,45,50,60,70,80,85,82,78,75,70]
        predict = [60,65,70,75,80,85,90,95,100,98,95,90,85,80,75]
        
        history_x = days[:days.index("D0")+1]
        history_y = history[:len(history_x)]
        predict_x = days[days.index("D0"):]
        predict_y = predict[days.index("D0"):]
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=history_x, y=history_y, name='历史热度',
            line=dict(color='#2563eb', width=3), mode='lines+markers'
        ))
        fig_trend.add_trace(go.Scatter(
            x=predict_x, y=predict_y, name='预测热度',
            line=dict(color='#93c5fd', width=2, dash='dash'), mode='lines+markers'
        ))
        fig_trend.update_layout(
            xaxis_title="时间维度", yaxis_title="热度值",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            font=dict(family=CHINESE_FONT)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        st.caption("**趋势解读**：历史热度稳步攀升，D0为剧集开播节点，预测热度将在D+4达到峰值，建议提前布局投放")
    
    with col2:
        st.subheader("📊 10大维度评分雷达图")
        labels = ["综合素质","传播","风险","热度","趋势","商业","话题","适配","情感","圈层"]
        values = [80,78,2,60,66,70,70,75,72,70]
        fig_radar = go.Figure(go.Scatterpolar(r=values, theta=labels, fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(range=[0,80])), font=dict(family=CHINESE_FONT))
        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("**维度解读**：综合素质、传播力、品牌适配度均为行业顶尖，风险指数极低，是当前最优投资标的")
    st.markdown('</div>', unsafe_allow_html=True)
    pdf_buffer = generate_qa_report_pdf()
    st.download_button(
        "📄 下载完整PDF报告",
        data=pdf_buffer,
        file_name="智能问答_IP推荐报告.pdf",
        mime="application/pdf"
    )

def render_recommend_page():
    """渲染IP推荐榜单页面（保留原有功能）"""
    st.header("IP推荐榜单", divider="red")
    col1, col2 = st.columns([4,1])
    with col1:
        filter_type = st.selectbox("筛选", ["全部IP","影视IP","动漫IP","综艺IP","体育赛事IP","KOL IP"])
    with col2:
        list_text = "\n".join([f"{i['id']}.{i['name']} {i['type']} ROI:{i['roi']}" for i in all_ip_data])
        st.download_button("下载榜单", list_text, "IP推荐榜单.txt")

    filtered_ips = all_ip_data
    if filter_type != "全部IP":
        target_type = filter_type.replace("IP","").strip() + "IP"
        filtered_ips = [ip for ip in all_ip_data if ip['type'] == target_type]

    for ip in filtered_ips:
        with st.container(border=True):
            col1, col2 = st.columns([8,2])
            with col1:
                st.subheader(f"{ip['id']}.{ip['name']}")
                st.write(f"类型：{ip['type']} | 预算：{ip['budget']} | ROI：{ip['roi']}")
                st.write(f"**核心价值**：{ip['analysis']['value']}")
            with col2:
                if st.button("查看详情", key=f"detail_{ip['id']}", use_container_width=True):
                    st.session_state.selected_ip_id = ip['id']
                    st.rerun()

def render_ip_detail():
    """渲染IP详情页面（保留原有完整格式）"""
    selected_ip = next((ip for ip in all_ip_data if ip['id'] == st.session_state.selected_ip_id), None)
    if not selected_ip:
        st.warning("未选择任何IP，请返回榜单选择")
        if st.button("返回榜单", use_container_width=True):
            st.session_state.selected_ip_id = None
            st.rerun()
        return

    st.header(f"{selected_ip['name']} 详细分析报告", divider="red")
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.subheader("📌 IP综合价值定位", divider="gray")
        st.write(selected_ip['analysis']['value'])
        
        st.subheader("📊 基础信息", divider="gray")
        st.write(f"**IP类型**：{selected_ip['type']}")
        st.write(f"**核心驱动**：{selected_ip['driver']}")
        st.write(f"**预算范围**：{selected_ip['budget']}")
        st.write(f"**预估ROI**：{selected_ip['roi']}")
        st.write(f"**综合评分**：{selected_ip['comprehensive']}/20")
        st.write(f"**传播裂变力**：{selected_ip['communication']}/80")

        st.subheader("⚠️ 风险提示", divider="gray")
        st.write(f"**风险类型**：{selected_ip['risk']['type']}")
        st.write(f"**风险等级**：{selected_ip['risk']['level']}")
        st.write(f"**操作建议**：{selected_ip['risk']['suggestion']}")

        st.subheader("💡 核心优势", divider="gray")
        for idx, adv in enumerate(selected_ip['advantage'], 1):
            st.write(f"{idx}. {adv}")

    with col_right:
        st.subheader("🎯 核心维度评分", divider="gray")
        radar_labels = ["综合评分", "传播裂变", "风险指数", "话题热度", "品牌适配"]
        radar_values = [
            selected_ip['comprehensive'] / 2,
            selected_ip['communication'] / 8,
            list(selected_ip['risk'].values()).index(selected_ip['risk']['level']) + 1,
            selected_ip['topic'],
            selected_ip['brand_fit']
        ]
        fig_radar = go.Figure(go.Scatterpolar(
            r=radar_values, theta=radar_labels, fill='toself',
            line=dict(color='#2563eb', width=3),
            fillcolor='rgba(37, 99, 235, 0.3)',
            marker=dict(size=10, color='#2563eb')
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(range=[0, 10], tickvals=[0,2,4,6,8,10])),
            showlegend=False, width=400, height=400,
            font=dict(family=CHINESE_FONT)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        st.subheader("👥 受众深度画像", divider="gray")
        st.write(selected_ip['analysis']['audience'])
        df_aud = pd.DataFrame(list(selected_ip['audience'].items()), columns=["受众类型", "占比(%)"])
        fig_aud = px.bar(
            df_aud, x="受众类型", y="占比(%)",
            color_discrete_sequence=["#2563eb", "#3b82f6", "#60a5fa", "#93c5fd"]
        )
        fig_aud.update_layout(
            width=400, height=400, showlegend=False,
            font=dict(family=CHINESE_FONT)
        )
        st.plotly_chart(fig_aud, use_container_width=True)

    st.subheader("📈 投放策略建议", divider="gray")
    st.write(selected_ip['analysis']['strategy'])
    
    st.subheader("💰 商业ROI拆解", divider="gray")
    st.write(selected_ip['analysis']['roi'])

    st.subheader("📊 投放效果预估", divider="gray")
    perf_df = pd.DataFrame(list(selected_ip['performance'].items()), columns=["评估维度", "预估数值"])
    st.dataframe(perf_df, hide_index=True, use_container_width=True)

    st.divider()
    pdf_buffer = generate_ip_report_pdf(selected_ip)
    st.download_button(
        f"📄 下载{selected_ip['name']}完整报告",
        data=pdf_buffer,
        file_name=f"{selected_ip['name']}_IP分析报告.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    if st.button("返回IP推荐榜单", use_container_width=True):
        st.session_state.selected_ip_id = None
        st.rerun()

# ===================== 主函数 =====================
def main():
    cleanup_temp_files()
    if st.session_state.selected_ip_id:
        render_ip_detail()
    else:
        tab1, tab2 = st.tabs(["智能问答", "IP推荐榜单"])
        with tab1:
            render_qa_page()
        with tab2:
            render_recommend_page()

    st.divider()


if __name__ == "__main__":
    main()
