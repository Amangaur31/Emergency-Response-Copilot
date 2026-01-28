import streamlit as st
from rag.pipeline import RAGPipeline

# -------------------------------
# App Title
# -------------------------------
st.title("🚑 Emergency Response Copilot")
st.markdown(
    "An AI assistant that helps ambulance drivers and traffic police using official emergency protocols."
)

# -------------------------------
# Load RAG Pipeline Once
# -------------------------------
if "rag" not in st.session_state:
    st.session_state.rag = RAGPipeline()

rag = st.session_state.rag

# -------------------------------
# Upload Emergency Protocol Docs
# -------------------------------
st.markdown("## Upload Emergency Protocol Documents")

uploaded = st.file_uploader(
    "Upload PDF/TXT files (Traffic SOP, Ambulance Rules, Accident Guidelines)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if st.button(" Index Emergency Documents"):
    if uploaded:
        import os
        os.makedirs("books", exist_ok=True)

        for file in uploaded:
            with open("books/" + file.name, "wb") as f:
                f.write(file.read())

        rag.index_folder("books")
        st.success(" Emergency Protocol Documents Indexed Successfully!")

# -------------------------------
# Emergency Dashboard Inputs
# -------------------------------
st.markdown("## 🚨 Live Emergency Situation Input")

location = st.selectbox(
    "📍 Location",
    ["AIIMS Delhi", "Connaught Place", "NH-48 Highway", "Dwarka Sector 21", "Other"]
)

emergency_type = st.selectbox(
    "🚑 Emergency Type",
    ["Road Accident",
        "Medical Emergency",
        "Fire / Explosion",
        "Flood Emergency",
        "Earthquake",
        "Bomb Threat",
        "Cyclone"]
)

traffic_level = st.selectbox(
    "🚦 Current Traffic Level",
    ["Low", "Moderate", "High"]
)

# -------------------------------
# User Query
# -------------------------------
question = st.text_input("Ask the Emergency Copilot:")

# -------------------------------
# Get Answer Button
# -------------------------------
if st.button("🚀 Get Emergency Guidance"):
    if question:

        #  Inject Real-Time Context into Query
        full_query = f"""
        Emergency Situation:
        Location: {location}
        Emergency Type: {emergency_type}
        Traffic Level: {traffic_level}

        User Question: {question}
        """
        
        #  Map UI emergency types to document routing types
        type_map = {
            "Road Accident": "accident",
            "Medical Emergency": "ambulance",
            "Fire / Explosion": "fire",
            "Flood Emergency": "flood",
            "Earthquake": "disaster",
            "Bomb Threat": "disaster",
            "Cyclone": "disaster"
        }

        selected_type = type_map.get(emergency_type, "general")


        answer, sources = rag.ask(full_query, emergency_type=selected_type)

        # -------------------------------
        # Display Answer
        # -------------------------------
        st.markdown("## Emergency Copilot Response")
        st.success(answer)

        # -------------------------------
        # Display Sources
        # -------------------------------
        st.markdown("## 📌 Protocol Sources Used")
        for s in sources:
            st.caption(s)
