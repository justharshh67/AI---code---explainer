import streamlit as st
import ollama

st.set_page_config(
    page_title="AI Code Explainer",
    page_icon="🤖",
    layout="wide"
)

# ---------- Sidebar ----------
st.sidebar.title("🤖 AI Code Explainer")
st.sidebar.markdown("---")

level = st.sidebar.selectbox(
    "Explanation Level",
    ["Beginner", "Intermediate", "Expert"]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Code File",
    type=["py", "cpp", "java", "js", "txt"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 Powered by Ollama + Llama 3.2"
)

# ---------- Header ----------
st.title("🤖 AI Code Explainer")
st.caption("Explain • Debug • Improve your code")

# ---------- Read uploaded file ----------
code = ""

if uploaded_file:
    code = uploaded_file.read().decode("utf-8")

code = st.text_area(
    "Paste your code",
    value=code,
    height=400
)

# ---------- Statistics ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Lines", len(code.splitlines()))

with col2:
    st.metric("Characters", len(code))

with col3:
    st.metric("Words", len(code.split()))

# ---------- Button ----------
if st.button("🚀 Explain Code", use_container_width=True):

    if code.strip() == "":
        st.warning("Please enter some code.")

    else:

        prompt = f"""
Explain this code for a {level} programmer.

Include:

1. Purpose
2. Line by line explanation
3. Time Complexity
4. Space Complexity
5. Possible Bugs
6. Improvements

Code:

{code}
"""

        with st.spinner("🧠 AI is thinking..."):

            response = ollama.chat(
                model="llama3.2:3b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

        st.success("Explanation Generated!")

        st.markdown("## 🧠 AI Explanation")

        st.markdown(response["message"]["content"])