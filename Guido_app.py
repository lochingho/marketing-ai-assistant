# Guido_app.py
import streamlit as st
import openai
import os
from datetime import datetime

st.set_page_config(page_title="Guido — AI Marketing Assistant", layout="centered")

# --- Helper: bilingual text ---
TEXT = {
    "en": {
        "title": "Guido — AI Marketing Assistant (MVP)",
        "subtitle": "Step-by-step marketing guidance + copy generation (MVP)",
        "intro": "Fill in your brand info and get a short marketing plan + ready-to-use copy. Requires an OpenAI API key set in Streamlit Secrets as OPENAI_API_KEY.",
        "brand_name": "Brand name",
        "industry": "Industry (e.g., Gym / Cafe / Online course)",
        "product_service": "Product / Service short description (1-2 lines)",
        "target_audience": "Target audience (e.g., Women 18-30, health conscious)",
        "budget": "Budget level",
        "marketing_goal": "Marketing goal",
        "tone": "Tone / Style for copy",
        "generate": "Generate plan & copy",
        "no_key": "OPENAI_API_KEY not found. Please add it in Streamlit Secrets (OPENAI_API_KEY).",
        "strategy": "AI Marketing Recommendations (strategy)",
        "copies": "AI-generated copy",
        "download": "Download full report (.txt)",
        "example": "Example outputs will appear here after generation.",
        "processing": "Generating — please wait...",
        "error": "Error calling OpenAI API:",
        "footer": "Built with ❤️ by Guido — Phase 1 MVP"
    },
    "zh": {
        "title": "Guido — AI 行銷助理（MVP）",
        "subtitle": "一步步行銷引導 + 文案產生（MVP）",
        "intro": "填寫品牌資料，系統會生成簡短的行銷計畫與可用文案。需在 Streamlit Secrets 設定 OPENAI_API_KEY。",
        "brand_name": "品牌名稱",
        "industry": "行業（例如：健身房 / 咖啡店 / 線上課程）",
        "product_service": "產品 / 服務簡介（1-2 行）",
        "target_audience": "目標受眾（例如：18-30 女生、注重健康）",
        "budget": "行銷預算等級",
        "marketing_goal": "行銷目標",
        "tone": "文案語氣 / 風格",
        "generate": "生成建議與文案",
        "no_key": "未找到 OPENAI_API_KEY。請在 Streamlit Secrets 設定 OPENAI_API_KEY。",
        "strategy": "AI 行銷建議（策略）",
        "copies": "AI 生成的文案",
        "download": "下載完整報告 (.txt)",
        "example": "產出會在按下生成後顯示於此。",
        "processing": "生成中—請稍候...",
        "error": "呼叫 OpenAI API 發生錯誤：",
        "footer": "由 Guido 製作 — Phase 1 MVP"
    }
}

# --- UI: language selection ---
lang = st.sidebar.radio("Language / 語言", ("English", "繁體中文"))
lang_code = "en" if lang == "English" else "zh"
t = TEXT[lang_code]

st.title(t["title"])
st.caption(t["subtitle"])
st.markdown(t["intro"])

# --- Get OpenAI key ---
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error(t["no_key"])
    st.stop()

openai.api_key = OPENAI_API_KEY

# --- Form: onboarding ---
with st.form("onboard", clear_on_submit=False):
    st.header(t["brand_name"] + " ▶ " + t["industry"])
    brand_name = st.text_input(t["brand_name"], value="")
    industry = st.text_input(t["industry"], value="")
    product_service = st.text_area(t["product_service"], value="", height=80)
    target_audience = st.text_area(t["target_audience"], value="", height=60)
    budget = st.selectbox(t["budget"], ["Low / 低", "Medium / 中", "High / 高"])
    marketing_goal = st.selectbox(t["marketing_goal"], ["Brand awareness / 品牌曝光", "Increase sales / 增加銷售", "Social engagement / 社群互動", "Website traffic / 導流到網站", "Other / 其他"])
    tone = st.selectbox(t["tone"], ["Professional / 專業", "Friendly / 活潑", "Warm / 溫暖", "Humorous / 幽默"])
    submitted = st.form_submit_button(t["generate"])

if submitted:
    if not brand_name or not product_service:
        st.warning("Please enter at least Brand name and Product/Service description. / 請至少填寫品牌名稱與產品/服務簡介。")
    else:
        with st.spinner(t["processing"]):
            # Prompt for strategy
            prompt_strategy = f\"\"\"You are an experienced digital marketing consultant. Provide a short actionable marketing recommendation (in { 'Chinese (Traditional)' if lang_code == 'zh' else 'English' }) for the brand below.\n\nBrand name: {brand_name}\nIndustry: {industry}\nProduct/service: {product_service}\nTarget audience: {target_audience}\nBudget level: {budget}\nMarketing goal: {marketing_goal}\n\nOutput (use bullet points):\n1) Recommended platforms and why (1-2 lines each)\n2) Recommended formats (e.g., short video, image post, carousel)\n3) Content direction & visual tone suggestion (50-80 words)\n4) Two short headline ideas (8-16 words)\n\nKeep it concise and directly actionable.\n\"\"\"

            # Call OpenAI for strategy
            try:
                res_strat = openai.ChatCompletion.create(
                    model=\"gpt-3.5-turbo\",
                    messages=[{\"role\": \"user\", \"content\": prompt_strategy}],
                    temperature=0.7,
                    max_tokens=600,
                )
                strategy = res_strat['choices'][0]['message']['content'].strip()
            except Exception as e:
                st.error(t["error"] + " " + str(e))
                st.stop()

            st.subheader(t["strategy"])
            st.write(strategy)

            # Prompt for copies
            prompt_copy = f\"\"\"Using the strategy above, generate the following { 'in Traditional Chinese' if lang_code == 'zh' else 'in English' } for the brand {brand_name} (Tone: {tone}):\n\n1) 3 short ad copies for Facebook/Instagram (max 90 chars each)\n2) 1 Instagram post caption (80-150 words)\n3) 1 LinkedIn post example (150-300 words)\n\nSeparate sections clearly.\n\"\"\"

            try:
                res_copy = openai.ChatCompletion.create(
                    model=\"gpt-3.5-turbo\",
                    messages=[{\"role\": \"user\", \"content\": prompt_copy}],
                    temperature=0.75,
                    max_tokens=900,
                )
                copies = res_copy['choices'][0]['message']['content'].strip()
            except Exception as e:
                st.error(t["error"] + " " + str(e))
                st.stop()

            st.subheader(t["copies"])
            st.write(copies)

            # Downloadable report (txt)
            timestamp = datetime.utcnow().strftime(\"%Y%m%d_%H%M%S\")
            report = f\"Brand: {brand_name}\\nIndustry: {industry}\\nProduct/service: {product_service}\\nTarget audience: {target_audience}\\nBudget: {budget}\\nMarketing goal: {marketing_goal}\\n\\n-- Strategy --\\n{strategy}\\n\\n-- Copies --\\n{copies}\\n\\nGenerated by Guido (MVP) on {timestamp} UTC\\n\"
            st.download_button(t["download"], data=report, file_name=f\"{brand_name}_Guido_report_{timestamp}.txt\", mime=\"text/plain\")

st.markdown(\"---\")
st.caption(TEXT[lang_code]["footer"])
