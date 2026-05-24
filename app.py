import streamlit as st
import tempfile

from utils.llm_helper import get_gemini_response
from utils.prompt_helper import SYSTEM_PROMPT
from utils.rag_helper import create_vectorstore, search_docs
from utils.itinerary_helper import generate_itinerary
from utils.budget_helper import generate_budget
from utils.packing_helper import generate_packing
from utils.ui_helper import load_css

st.set_page_config(
    page_title="Smart AI Travel Assistant",
    page_icon="✈️",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
✈️ Smart AI Travel Assistant
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
Travel smarter with AI-powered recommendations ✨
</div>
""", unsafe_allow_html=True)

# HERO IMAGE
st.container()
st.image(
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
    width='stretch'
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    📍 Travel Recommendation
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    💰 Budget Planner
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    🧳 Packing Checklist
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<h3 style='color:white; margin-top:10px;'>
💬 Ask Anything About Traveling
</h3>
""", unsafe_allow_html=True)

# session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# sidebar
st.sidebar.title("✈️ Smart Features")

feature = st.sidebar.selectbox(
    "Pilih fitur",
    [
        "General Chat",
        "Itinerary Generator",
        "Budget Planner",
        "Packing Checklist"
    ]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Travel PDF",
    type="pdf"
)

if uploaded_file:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:

        tmp_file.write(uploaded_file.read())

        tmp_path = tmp_file.name

    with st.spinner("Processing PDF..."):

        vectorstore = create_vectorstore(tmp_path)

        st.session_state.vectorstore = vectorstore

    st.sidebar.success("PDF berhasil diproses!")

# GENERAL CHAT
if feature == "General Chat":

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    prompt = st.chat_input("Tanyakan tentang traveling...")

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("✈️ AI sedang berpikir..."):

                final_prompt = SYSTEM_PROMPT

                if st.session_state.vectorstore:

                    context = search_docs(
                        st.session_state.vectorstore,
                        prompt
                    )

                    final_prompt += f"""

                    Berikut konteks dokumen:

                    {context}

                    """

                final_prompt += f"""

                Pertanyaan user:
                {prompt}

                """

                response = get_gemini_response(final_prompt)

                st.markdown(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

# ITINERARY
elif feature == "Itinerary Generator":

    destination = st.text_input("Destinasi")

    days = st.number_input(
        "Jumlah hari",
        min_value=1,
        max_value=30
    )

    budget = st.text_input("Budget")

    if st.button("Generate Itinerary"):

        with st.spinner("Generating..."):

            result = generate_itinerary(
                destination,
                days,
                budget
            )

            st.markdown(result)

# BUDGET
elif feature == "Budget Planner":

    destination = st.text_input("Destinasi")

    days = st.number_input(
        "Jumlah hari",
        min_value=1,
        max_value=30
    )

    if st.button("Generate Budget"):

        with st.spinner("Generating..."):

            result = generate_budget(
                destination,
                days
            )

            st.markdown(result)

# PACKING
elif feature == "Packing Checklist":

    destination = st.text_input("Destinasi")

    if st.button("Generate Checklist"):

        with st.spinner("Generating..."):

            result = generate_packing(destination)

            st.markdown(result)

st.markdown("""
<div class="footer">
Made with ❤️ using Gemini AI + Streamlit
</div>
""", unsafe_allow_html=True)