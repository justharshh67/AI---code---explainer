import streamlit as st

try:
    from streamlit_ace import st_ace
except ImportError:  # pragma: no cover - defensive fallback
    st_ace = None

try:
    import ollama
except ImportError:  # pragma: no cover - defensive fallback
    ollama = None

MODEL = "qwen2.5-coder:1.5b"

st.set_page_config(
    page_title="AI Code Explainer",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #07111f 0%, #0b1d35 45%, #102d4d 100%);
        color: #f8fafc;
    }
    #MainMenu, footer, header { visibility: hidden; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #081321, #0d2038);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    .hero {
        padding: 28px 32px;
        border-radius: 24px;
        margin-bottom: 22px;
        background: linear-gradient(135deg, rgba(37,99,235,0.28), rgba(124,58,237,0.18));
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 18px 50px rgba(0,0,0,0.22);
    }
    .hero-title { font-size: 38px; font-weight: 800; margin-bottom: 6px; }
    .hero-subtitle { font-size: 16px; color: #cbd5e1; }
    .app-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 16px;
    }
    .editor-shell {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 10px;
        background: rgba(7, 17, 31, 0.9);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }
    .stat-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 14px 16px;
        min-height: 92px;
    }
    .response-shell {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 20px;
        background: rgba(8, 15, 28, 0.86);
        margin-top: 16px;
    }
    .sidebar-pill {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(59,130,246,0.16);
        color: #bfdbfe;
        font-size: 12px;
        margin-top: 8px;
        border: 1px solid rgba(59,130,246,0.24);
    }
    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.12);
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: white;
        font-weight: 700;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        border-color: #60a5fa;
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 4px 20px 4px;">
            <div style="font-size: 18px; font-weight: 700; color: white;">🤖 AI Code Explainer</div>
            <div style="color: #94a3b8; margin-top: 6px;">Local AI coding assistant</div>
            <div class="sidebar-pill">Local AI • Private</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("<div style='font-size: 13px; font-weight: 700; color: #cbd5e1; margin-bottom: 8px;'>Model</div>", unsafe_allow_html=True)
    model = st.selectbox("", [MODEL], key="model_select")

    st.markdown("<div style='font-size: 13px; font-weight: 700; color: #cbd5e1; margin-bottom: 8px; margin-top: 10px;'>Explanation Level</div>", unsafe_allow_html=True)
    level = st.selectbox("", ["Beginner", "Intermediate", "Advanced"], key="level_select")

    st.divider()
    st.markdown("<div style='font-size: 13px; font-weight: 700; color: #cbd5e1; margin-bottom: 8px;'>Upload Code</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "",
        type=["py", "cpp", "cc", "c", "java", "js", "ts", "html", "css", "php", "txt"],
    )

    st.divider()
    st.markdown(
        """
        <div class="app-card" style="margin-top: 0; padding: 12px 14px;">
            <div style="color: #86efac; font-weight: 700;">● Ollama Connected</div>
            <div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Running locally with Qwen2.5-Coder.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">AI Code Explainer</div>
        <div class="hero-subtitle">Understand. Debug. Improve.</div>
        <div style="margin-top: 10px; color: #dbeafe;">Your local AI coding assistant powered by Qwen2.5-Coder.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-card">
        <div style="font-size: 13px; font-weight: 700; color: #93c5fd; text-transform: uppercase; letter-spacing: 0.08em;">Workspace</div>
        <div style="margin-top: 8px; color: #f8fafc; font-size: 16px; font-weight: 600;">Code editor, stats, and AI analysis in one focused workspace.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='font-size: 15px; font-weight: 700; color: #f8fafc; margin-bottom: 8px;'>Programming Language</div>", unsafe_allow_html=True)
language = st.selectbox(
    "",
    ["Python", "C++", "C", "Java", "JavaScript", "TypeScript", "Text"],
    key="language_select",
)

language_map = {
    "Python": "python",
    "C++": "c_cpp",
    "C": "c_cpp",
    "Java": "java",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "Text": "text",
}
selected_language = language_map[language]

default_code = '''def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
'''

if uploaded_file is not None:
    try:
        uploaded_code = uploaded_file.read().decode("utf-8")
        if uploaded_code.strip():
            default_code = uploaded_code
    except Exception:
        st.error("❌ Could not read the uploaded file.")

st.markdown("<div style='font-size: 15px; font-weight: 700; color: #f8fafc; margin-bottom: 8px;'>Code Editor</div>", unsafe_allow_html=True)
editor_container = st.container()
with editor_container:
    st.markdown("<div class='editor-shell'>", unsafe_allow_html=True)
    if st_ace is not None:
        code = st_ace(
            value=default_code,
            language=selected_language,
            theme="monokai",
            height=430,
            key="code_editor",
            font_size=14,
            tab_size=4,
            show_gutter=True,
            show_print_margin=False,
            wrap=False,
            auto_update=False,
        )
    else:
        code = st.text_area("", value=default_code, height=430, key="code_editor_fallback")
    st.markdown("</div>", unsafe_allow_html=True)

lines = len(code.splitlines())
characters = len(code)
words = len(code.split())
non_empty_lines = len([line for line in code.splitlines() if line.strip()])

st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='stat-card'><div style='font-size: 12px; color: #93c5fd;'>Lines</div><div style='font-size: 20px; font-weight: 700; color: white; margin-top: 6px;'>" + str(lines) + "</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='stat-card'><div style='font-size: 12px; color: #93c5fd;'>Characters</div><div style='font-size: 20px; font-weight: 700; color: white; margin-top: 6px;'>" + str(characters) + "</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='stat-card'><div style='font-size: 12px; color: #93c5fd;'>Words</div><div style='font-size: 20px; font-weight: 700; color: white; margin-top: 6px;'>" + str(words) + "</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='stat-card'><div style='font-size: 12px; color: #93c5fd;'>Code Lines</div><div style='font-size: 20px; font-weight: 700; color: white; margin-top: 6px;'>" + str(non_empty_lines) + "</div></div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
if st.button("✨ Explain Code", use_container_width=True):
    if not code.strip():
        st.warning("⚠️ Please enter some code first.")
    else:
        prompt = f"""
You are an expert software engineer and programming teacher.

Analyze this {language} code.
The user is at a {level} programming level.

Give a clear and practical explanation with these sections:
1. Overview
2. How It Works
3. Important Lines
4. Improvements

Here is the code:
```{selected_language}
{code}
```
"""

        if ollama is None:
            st.info("Ollama is not available in this environment, so the explanation could not be generated.")
        else:
            with st.spinner("Generating explanation..."):
                try:
                    response = ollama.generate(model=model, prompt=prompt)
                    explanation = response.get("response", str(response))
                except Exception as exc:
                    explanation = f"Unable to generate an explanation right now: {exc}"

            st.markdown("<div class='response-shell'>", unsafe_allow_html=True)
            st.markdown("### 🧠 AI Analysis", unsafe_allow_html=False)
            st.markdown(explanation)
            st.download_button(
                label="⬇️ Download explanation",
                data=explanation,
                file_name="ai_code_explanation.md",
                mime="text/markdown",
            )
            st.markdown("</div>", unsafe_allow_html=True)
