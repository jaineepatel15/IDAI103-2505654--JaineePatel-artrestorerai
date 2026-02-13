API_KEY = "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"
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="ArtRestorer AI",
    layout="wide"
)

# ------------------ SESSION STATE ------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "user" not in st.session_state:
    st.session_state.user = None

# ------------------ LANDING PAGE ------------------
if st.session_state.user is None:
    st.markdown("## 🎨 **ArtRestorer AI**")
    st.markdown(
        "### Restore & Preserve Your Artistic Legacy\n"
        "AI-powered conservation analysis for artworks."
    )

    with st.form("welcome_form"):
        name = st.text_input("Your Name *")
        role = st.selectbox(
            "Your Role *",
            [
                "Museum Professional",
                "Gallery Director",
                "Art Collector",
                "Restoration Specialist",
                "Art Student",
                "Researcher",
                "Other",
            ],
        )
        focus = st.selectbox(
            "Art Focus Area *",
            [
                "Paintings",
                "Sculptures",
                "Textiles",
                "Historical Periods",
                "Modern & Contemporary",
                "All Art Forms",
            ],
        )

        submitted = st.form_submit_button("Begin Analysis →")

        if submitted:
            if name.strip() == "":
                st.error("Please enter your name.")
            else:
                st.session_state.user = {
                    "name": name,
                    "role": role,
                    "focus": focus,
                }
                st.rerun()

# ------------------ MAIN APP ------------------
else:
    st.sidebar.markdown(f"👋 **Welcome, {st.session_state.user['name']}**")
    st.sidebar.caption(st.session_state.user["role"])

    tab_analyze, tab_history, tab_dashboard, tab_guide = st.tabs(
        ["🔍 Analyze", "📜 History", "📊 Dashboard", "📚 Guide"]
    )

    # -------- ANALYZE TAB --------
    with tab_analyze:
        st.header("Artwork Analysis")

        with st.form("analysis_form"):
            artwork_type = st.selectbox(
                "Artwork Type *",
                ["Painting", "Sculpture", "Textile", "Mural", "Fresco"],
            )
            period = st.selectbox(
                "Period / Style *",
                [
                    "Renaissance",
                    "Mughal",
                    "Baroque",
                    "Impressionist",
                    "Modernist",
                ],
            )
            artist = st.text_input("Artist (Optional)")
            damage = st.text_area(
                "Damage Description *",
                placeholder="Fading, cracks, water damage, flaking…",
            )
            condition = st.slider("Condition Rating", 1, 10, 5)
            analysis_type = st.selectbox(
                "Analysis Type",
                [
                    "Restoration Methods",
                    "Reconstruction Ideas",
                    "Conservation Plan",
                    "Damage Assessment",
                    "Cost Estimate",
                ],
            )

            generate = st.form_submit_button("Generate Analysis")

        if generate:
            result = {
                "date": datetime.now().strftime("%d %b %Y"),
                "artwork": artwork_type,
                "period": period,
                "damage": damage,
                "condition": condition,
                "type": analysis_type,
            }

            st.session_state.history.append(result)

            st.success("Analysis generated!")
            st.markdown("### 🧠 AI Result (Mock)")
            st.write(
                f"""
                **Artwork:** {artwork_type}  
                **Period:** {period}  
                **Condition:** {condition}/10  

                **Recommended Action:**  
                Based on the damage described, a controlled conservation
                approach using reversible materials is advised.
                """
            )

    # -------- HISTORY TAB --------
    with tab_history:
        st.header("Saved Analyses")

        if not st.session_state.history:
            st.info("No saved analyses yet.")
        else:
            for i, item in enumerate(st.session_state.history, 1):
                with st.expander(f"📄 Analysis {i} — {item['date']}"):
                    st.write(item)

    # -------- DASHBOARD TAB --------
    with tab_dashboard:
        st.header("Dashboard Overview")

        total = len(st.session_state.history)
        high_priority = len(
            [h for h in st.session_state.history if h["condition"] <= 3]
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Analyses", total)
        col2.metric("High Priority", high_priority)
        col3.metric("Periods Covered", len(set(h["period"] for h in st.session_state.history)))

    # -------- GUIDE TAB --------
    with tab_guide:
        st.header("Conservation Guide")

        st.markdown("""
        **Best Practices**
        - Maintain stable temperature (18–22°C)
        - Humidity between 45–55%
        - Use reversible restoration techniques
        - Document before & after treatment
        """)

    st.sidebar.button("Exit", on_click=lambda: st.session_state.clear())
