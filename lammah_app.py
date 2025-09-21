import streamlit as st
import base64
import joblib
from PIL import Image

# --------------------------------
# Load logo
# --------------------------------
def load_logo(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_path = r"Logo(lammah).jpg"
logo_base64 = load_logo(logo_path)

# --------------------------------
# Load Models + Vectorizers
# --------------------------------
sentiment_model = joblib.load(r"sentiment\sentiment_model.pkl")
sentiment_vectorizer = joblib.load(r"sentiment\vectorizer.pkl")

article_model = joblib.load(r"artical\model.pkl")
article_vectorizer = joblib.load(r"artical\vectorizer.pkl")

dialect_model = joblib.load(r"accents\model2.pkl")
dialect_vectorizer = joblib.load(r"accents\vectorizer.pkl")

# Labels
sentiment_labels = {0: "سلبي", 1: "إيجابي"}
article_labels = {0: "ثقافة", 1: "تنوع", 2: "اقتصاد", 3: "سياسة", 4: "رياضة"}
dialect_labels = {
    "Egyptian": "المصرية",
    "Gulf": "الخليجية",
    "Levantine": "بلاد الشام",
    "Maghrebi": "المغرب العربي",
    "Sudanese-Iraqi": "السودانية أو العراقية"
}

# --------------------------------
# Page config
# --------------------------------
st.set_page_config(page_title=" ", page_icon="👁", layout="wide")

# --------------------------------
# Mobile-style CSS
# --------------------------------
mobile_style = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(135deg, #fdf9f3, #ffe6f0);
    padding: 10px 0;
}}
.logo-container {{
    text-align: center;
    margin-top: 15px;
    margin-bottom: 15px;
}}
.logo-container img {{
    width: 140px;
    border-radius: 50%;
    transition: transform 0.3s;
}}
.logo-container img:hover {{
    transform: scale(1.1);
}}
.title {{
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #6b1b8c;
    margin-bottom: 25px;
    font-family: "Cairo", sans-serif;
}}
.stTextArea textarea {{
    font-size: 18px;
    padding: 15px;
    border-radius: 15px;
    border: 2px solid #6b1b8c;
    width: 100%;
}}
.stButton>button {{
    width: 100%;
    padding: 15px 0;
    font-size: 20px;
    color: #fff;
    background: linear-gradient(90deg, #6b1b8c, #d73adf);
    border-radius: 25px;
    margin-top: 10px;
    transition: transform 0.2s;
}}
.stButton>button:hover {{
    transform: scale(1.05);
}}
.card {{
    background: #fff;
    border-radius: 20px;
    padding: 20px;
    margin-top: 20px;
    text-align: center;
    font-size: 20px;
    color: #333;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    animation: fadeIn 0.5s;
}}
.card-title {{
    font-weight: bold;
    font-size: 22px;
    margin-bottom: 10px;
}}
.model-select button {{
    width: 100%;
    font-size: 20px;
    padding: 15px 0;
    margin-top: 10px;
    border-radius: 25px;
    background: linear-gradient(90deg, #6b1b8c, #d73adf);
    color: white;
    border: none;
    transition: transform 0.2s;
}}
.model-select button:hover {{
    transform: scale(1.05);
}}
@keyframes fadeIn {{
    from {{opacity: 0; transform: translateY(20px);}}
    to {{opacity: 1; transform: translateY(0);}}
}}
</style>
"""
st.markdown(mobile_style, unsafe_allow_html=True)

# --------------------------------
# Logo and title
# --------------------------------
st.markdown(
    f"""
    <div class="logo-container">
        <img src="data:image/jpg;base64,{logo_base64}">
    </div>
    <div class="title">لماح</div>
    """,
    unsafe_allow_html=True
)

# --------------------------------
# Initialize session state for pages
# --------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# --------------------------------
# Result card function
# --------------------------------
def show_result(title, result, color="#6b1b8c"):
    st.markdown(
        f"""
        <div class="card" style="border-top: 5px solid {color}">
            <div class="card-title">{title}</div>
            <p>{result}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# Home page
# ----------------------------
def home_page():
    st.markdown('<div class="model-select">', unsafe_allow_html=True)
    if st.button("تصنيف الإحساس"):
        st.session_state.page = "sentiment"
    if st.button("تصنيف المقالات"):
        st.session_state.page = "article"
    if st.button("تصنيف اللهجات"):
        st.session_state.page = "dialect"
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Sentiment page
# ----------------------------
def sentiment_page():
    st.subheader("تصنيف الإحساس")
    text = st.text_area("أدخل النص للتحليل", key="sentiment_text")
    
    if st.button("تحليل"):
        if text.strip():
            X = sentiment_vectorizer.transform([text])
            pred = sentiment_model.predict(X)[0]
            sentiment = sentiment_labels[pred]
            color = "#4caf50" if pred == 1 else "#f44336"
            show_result("نتيجة الإحساس", f"النص مصنف على أنه: {sentiment}", color)
        else:
            st.warning("يرجى إدخال نص")
    
    if st.button("العودة للقائمة الرئيسية"):
        st.session_state.page = "home"

# ----------------------------
# Article page
# ----------------------------
def article_page():
    st.subheader("تصنيف المقالات")
    text = st.text_area("أدخل نص المقال", key="article_text")
    
    if st.button("تصنيف"):
        if text.strip():
            X = article_vectorizer.transform([text])
            pred = article_model.predict(X)[0]
            category = article_labels[pred]
            show_result("نتيجة المقال", f"النص مصنف على أنه: {category}", "#2196f3")
        else:
            st.warning("يرجى إدخال نص المقال")
    
    if st.button("العودة للقائمة الرئيسية"):
        st.session_state.page = "home"

# ----------------------------
# Dialect page
# ----------------------------
def dialect_page():
    st.subheader("تصنيف اللهجات")
    text = st.text_area("أدخل النص باللهجة", key="dialect_text")
    
    if st.button("تحليل"):
        if text.strip():
            X = dialect_vectorizer.transform([text])
            pred = dialect_model.predict(X)[0]
            dialect = dialect_labels[pred]
            show_result("نتيجة اللهجة", f"النص مصنف على أنه: {dialect}", "#ff9800")
        else:
            st.warning("يرجى إدخال نص باللهجة")
    
    if st.button("العودة للقائمة الرئيسية"):
        st.session_state.page = "home"

# ----------------------------
# Page router
# ----------------------------
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "sentiment":
    sentiment_page()
elif st.session_state.page == "article":
    article_page()
elif st.session_state.page == "dialect":
    dialect_page()
