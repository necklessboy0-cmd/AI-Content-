import streamlit as st
from groq import Groq

# Set page configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)

# Custom CSS for Premium Gold & Deep Purple Theme
custom_css = """
<style>
/* Main Background: Gold-to-Deep-Purple Gradient with Fixed Background */
.stApp {
    background: linear-gradient(180deg, #D4AF37 0%, #7B1FA2 35%, #2A0845 70%, #10002B 100%);
    background-attachment: fixed;
    color: #FFFFFF;
}

/* Twinkling Background Stars Overlay */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    background-image: 
        radial-gradient(2px 2px at 20px 30px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 50px 100px, #ffd700, rgba(0,0,0,0)),
        radial-gradient(1px 1px at 120px 40px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 200px 180px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1.5px 1.5px at 280px 70px, #ffd700, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 350px 250px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1px 1px at 420px 110px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 510px 200px, #ffd700, rgba(0,0,0,0)),
        radial-gradient(1.5px 1.5px at 600px 80px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 700px 290px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1px 1px at 800px 150px, #ffd700, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 900px 60px, #ffffff, rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 900px 350px;
    opacity: 0.8;
    z-index: 0;
}

/* Main Header Typography */
h1 {
    color: #FFF8DC !important;
    text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.7);
    font-weight: 800 !important;
}

.stCaption {
    color: #F0E68C !important;
    font-size: 1.05rem !important;
    font-weight: 500;
}

/* Form Container and Glassmorphism Input Cards */
div[data-testid="stForm"] {
    background: rgba(20, 10, 35, 0.55);
    border: 1px solid rgba(212, 175, 55, 0.4);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
}

/* Input Fields Styling */
div[data-baseweb="select"] > div, 
div[data-baseweb="input"] > div, 
div[data-baseweb="textarea"] > div {
    background-color: rgba(15, 5, 25, 0.6) !important;
    border: 1px solid rgba(212, 175, 55, 0.5) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
}

/* Input Labels */
label {
    color: #FFE4B5 !important;
    font-weight: 600 !important;
}

/* Custom Gold Button Styling */
div.stButton > button {
    background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
    color: #1A002C !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    border: 1px solid #FFF8DC !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    box-shadow: 0px 4px 20px rgba(212, 175, 55, 0.5) !important;
    transition: all 0.3s ease-in-out !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0px 6px 25px rgba(255, 215, 0, 0.8) !important;
}

/* Result Card Box */
.result-card {
    background: rgba(15, 5, 25, 0.75);
    border: 1px solid rgba(212, 175, 55, 0.6);
    border-radius: 14px;
    padding: 20px;
    margin-top: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.5);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("✍️ AI Content Assistant")
st.caption("Generate tailored social media posts, captions, and hashtags instantly.")

# Retrieve API key securely from Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing from Streamlit Secrets. Please configure secrets in app dashboard.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)

    with col1:
        content_type = st.selectbox(
            "Content Type",
            ["Social Media Post", "Blog Intro", "Product Announcement", "Newsletter Snippet", "Short Video Script"]
        )
        platform = st.selectbox(
            "Target Platform",
            ["LinkedIn", "Instagram", "X (Twitter)", "Facebook", "YouTube Shorts / TikTok"]
        )

    with col2:
        tone = st.selectbox(
            "Tone / Style",
            ["Professional", "Casual & Engaging", "Witty & Humorous", "Educational", "Persuasive / Sales"]
        )
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Tech Professionals, Fitness Enthusiasts, Students"
        )

    topic = st.text_area(
        "Topic / Core Message",
        placeholder="e.g., Introducing our new AI product that helps developers automate unit tests...",
        height=120
    )

    submit_button = st.form_submit_button("✨ Generate Content", use_container_width=True)

# Generation Handling
if submit_button:
    if not topic.strip():
        st.warning("Please enter a topic or core message before generating.")
    else:
        prompt = f"""
You are an expert social media content creator and copywriter.
Generate a complete post based on the following requirements:

- **Content Type:** {content_type}
- **Platform:** {platform}
- **Tone:** {tone}
- **Target Audience:** {target_audience if target_audience else "General Public"}
- **Topic:** {topic}

### Instructions:
1. Provide a strong hook that captures attention.
2. Structure the body content to match the chosen platform (e.g., appropriate line breaks, formatting).
3. Conclude with a clear Call to Action (CTA).
4. Provide a section at the bottom with 5–8 highly relevant, high-performing hashtags.
"""

        with st.spinner("Drafting your post with Groq AI..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "You are a professional social media content assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                generated_content = response.choices[0].message.content

                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.subheader("🎉 Your Generated Content")
                st.markdown(generated_content)
                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred while generating content: {e}")
