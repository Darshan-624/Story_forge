import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import pdfkit
import time

st.set_page_config(
    page_title="EduForge Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    .header {
        color: #2E4053;
        font-family: 'Arial Rounded MT Bold', sans-serif;
        font-size: 3rem;
        text-align: center;
        padding: 2rem;
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 2rem auto;
        width: 90%;
    }
    .section {
        background: rgba(255,255,255,0.95);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    .stButton>button {
        background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
        color: white!important;
        border: none!important;
        border-radius: 15px!important;
        padding: 1rem 2rem!important;
        font-size: 1.1rem!important;
        transition: all 0.3s ease!important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(52,152,219,0.3);
    }
    .install-guide {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

def generate_content(content_type, topic, age, **kwargs):
    """Generate educational content based on type"""
    prompts = {
        "Learning Material": f"""Create comprehensive learning material about {topic} for {age}-year-olds. Include:
        1. Key Concepts with simple explanations
        2. Real-world Applications
        3. Visual Metaphors
        4. Common Misconceptions
        5. 3 Interesting Facts""",
        
        "Story": f"""Write a {kwargs.get('paragraphs', 3)}-paragraph story about {topic} for {age}-year-olds. Include:
        1. Named AI-generated characters
        2. Dialogue between characters
        3. Moral lesson
        4. Plot twist""",
        
        "Quiz": f"""Create {kwargs.get('num_questions', 5)} MCQ questions about {topic} for {age}-year-olds. Include:
        1. Clear question stem
        2. 3 Distractors
        3. Correct answer with explanation""",
        
        "Lesson Plan": f"""Create lesson plan about {topic} for {age}-year-olds. Include:
        1. Learning Objectives
        2. Materials Needed
        3. Warm-up Activity
        4. Core Lesson
        5. Group Activity
        6. Assessment"""
    }
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompts[content_type])
    return response.text

if "content" not in st.session_state:
    st.session_state.content = None
if "content_type" not in st.session_state:
    st.session_state.content_type = "Learning Material"

st.markdown('<div class="header">📚 EduForge Pro - Smart Learning Studio</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    with st.container():
        st.markdown('<div class="section">', unsafe_allow_html=True)
        
        content_type = st.radio(
            "Select Content Type:",
            ["Learning Material", "Story", "Quiz", "Lesson Plan"],
            index=0
        )
        
        topic = st.text_input("Enter Topic:", placeholder="e.g., Artificial Intelligence")
        age = st.number_input("Target Age:", min_value=5, max_value=100, value=25)
        
        if content_type == "Story":
            paragraphs = st.slider("Number of Paragraphs:", 1, 7, 3)
        elif content_type == "Quiz":
            num_questions = st.slider("Number of Questions:", 3, 30, 5)
        
        if st.button(f"✨ Generate {content_type}", use_container_width=True):
            if topic.strip():
                with st.spinner(f"Generating {content_type}..."):
                    args = {}
                    if content_type == "Story":
                        args["paragraphs"] = paragraphs
                    elif content_type == "Quiz":
                        args["num_questions"] = num_questions
                    
                    st.session_state.content = generate_content(
                        content_type, topic, age, **args
                    )
            else:
                st.error("Please enter a topic!")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if st.session_state.content:
        with st.container():
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown(f"### 📚 Generated {content_type}")
            st.markdown(st.session_state.content)
            
            # PDF Export
            try:
                pdf = pdfkit.from_string(st.session_state.content, False)
                st.download_button(
                    "📥 Download PDF",
                    data=pdf,
                    file_name=f"{topic}_{content_type.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except OSError:
                st.error("PDF export requires wkhtmltopdf installation - see setup guide below")
            
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="install-guide">
    <h3>🚀 Setup Instructions</h3>
    <ol>
        <li>Install Python requirements:
            <code>pip install streamlit python-dotenv google-generativeai pdfkit</code>
        </li>
        <li>Install wkhtmltopdf:
            <ul>
                <li>Windows: Download from <a href="https://wkhtmltopdf.org/downloads.html" target="_blank">wkhtmltopdf.org</a></li>
                <li>Mac: <code>brew install --cask wkhtmltopdf</code></li>
                <li>Linux: <code>sudo apt-get install wkhtmltopdf</code></li>
            </ul>
        </li>
        <li>Create .env file with your Gemini API key:
            <code>GEMINI_API_KEY=your_api_key_here</code>
        </li>
        <li>Run the app: <code>streamlit run app.py</code></li>
    </ol>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    Powered by Google Gemini AI | Educational Content Generator v2.0
</div>
""", unsafe_allow_html=True)