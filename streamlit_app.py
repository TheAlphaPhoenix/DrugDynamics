import streamlit as st

# ----------------------------
# Data Definitions
# ----------------------------

# Demo drug database (data based on reputable sources such as FDA guidelines and Micromedex)
drug_data = {
    "Aspirin": {
        "description": "Aspirin is a non-steroidal anti-inflammatory drug (NSAID) that works by inhibiting COX enzymes, reducing inflammation and platelet aggregation.",
        "mechanism": "COX enzyme inhibition",
        "side_effects": ["Gastrointestinal bleeding", "Tinnitus", "Allergic reactions"],
        "timeline": {
            "Initial": {"Brain": 1, "Heart": 1, "Liver": 0, "Kidneys": 0, "Lungs": 0, "Stomach": 3},
            "1 Week": {"Brain": 1, "Heart": 1, "Liver": 0, "Kidneys": 0, "Lungs": 0, "Stomach": 4},
            "1 Month": {"Brain": 1, "Heart": 1, "Liver": 0, "Kidneys": 1, "Lungs": 0, "Stomach": 4},
            "Long Term": {"Brain": 1, "Heart": 2, "Liver": 0, "Kidneys": 2, "Lungs": 0, "Stomach": 5},
        },
        "pharmacist_consultation": "Advise patients to take aspirin with food to reduce GI upset and to monitor for signs of bleeding."
    },
    "Metformin": {
        "description": "Metformin is a biguanide used in type 2 diabetes. It reduces hepatic gluconeogenesis and improves insulin sensitivity.",
        "mechanism": "Decreases hepatic glucose production; increases peripheral insulin sensitivity",
        "side_effects": ["Gastrointestinal upset", "Diarrhea", "Rare risk of lactic acidosis"],
        "timeline": {
            "Initial": {"Brain": 0, "Heart": 0, "Liver": 2, "Kidneys": 1, "Lungs": 0, "Stomach": 3},
            "1 Week": {"Brain": 0, "Heart": 0, "Liver": 1, "Kidneys": 1, "Lungs": 0, "Stomach": 2},
            "1 Month": {"Brain": 0, "Heart": 0, "Liver": 1, "Kidneys": 0, "Lungs": 0, "Stomach": 1},
            "Long Term": {"Brain": 0, "Heart": 0, "Liver": 1, "Kidneys": 0, "Lungs": 0, "Stomach": 1},
        },
        "pharmacist_consultation": "Recommend taking metformin with meals to reduce GI side effects. Remind patients to monitor renal function periodically."
    },
    "Lisinopril": {
        "description": "Lisinopril is an ACE inhibitor used for hypertension and heart failure management.",
        "mechanism": "Inhibits the angiotensin converting enzyme (ACE), reducing the formation of angiotensin II",
        "side_effects": ["Dry cough", "Hyperkalemia", "Angioedema", "Hypotension"],
        "timeline": {
            "Initial": {"Brain": 0, "Heart": 2, "Liver": 0, "Kidneys": 1, "Lungs": 1, "Stomach": 0},
            "1 Week": {"Brain": 0, "Heart": 2, "Liver": 0, "Kidneys": 1, "Lungs": 1, "Stomach": 0},
            "1 Month": {"Brain": 0, "Heart": 2, "Liver": 0, "Kidneys": 1, "Lungs": 1, "Stomach": 0},
            "Long Term": {"Brain": 0, "Heart": 2, "Liver": 0, "Kidneys": 1, "Lungs": 1, "Stomach": 0},
        },
        "pharmacist_consultation": "Educate patients about the possibility of a dry cough and instruct them to report any signs of angioedema immediately."
    },
    "Atorvastatin": {
        "description": "Atorvastatin is a statin used to lower LDL cholesterol and reduce cardiovascular risk.",
        "mechanism": "HMG-CoA reductase inhibition, reducing cholesterol synthesis",
        "side_effects": ["Muscle pain", "Liver enzyme abnormalities", "Digestive issues"],
        "timeline": {
            "Initial": {"Brain": 0, "Heart": 1, "Liver": 2, "Kidneys": 0, "Lungs": 0, "Stomach": 1},
            "1 Week": {"Brain": 0, "Heart": 1, "Liver": 2, "Kidneys": 0, "Lungs": 0, "Stomach": 1},
            "1 Month": {"Brain": 0, "Heart": 1, "Liver": 2, "Kidneys": 0, "Lungs": 0, "Stomach": 1},
            "Long Term": {"Brain": 0, "Heart": 1, "Liver": 2, "Kidneys": 0, "Lungs": 0, "Stomach": 1},
        },
        "pharmacist_consultation": "Instruct patients to report any unexplained muscle pain or weakness and advise periodic monitoring of liver enzymes."
    }
}

# List of organs (used in the avatar)
organs = ["Brain", "Lungs", "Heart", "Stomach", "Liver", "Kidneys"]

# Approximate coordinates for each organ on a 0-1 scale (for plotting the avatar)
organ_coords = {
    "Brain":   (0.5, 0.95),
    "Lungs":   (0.5, 0.85),
    "Heart":   (0.5, 0.75),
    "Stomach": (0.5, 0.65),
    "Liver":   (0.5, 0.55),
    "Kidneys": (0.5, 0.45),
}

# ----------------------------
# Helper Functions
# ----------------------------

def get_color_for_rating(rating):
    """Map a numerical rating to a color (green: low effect, orange: moderate, red: high)."""
    if rating < 2:
        return "green"
    elif rating < 4:
        return "orange"
    else:
        return "red"

def plot_avatar(timeline_data):
    """Plot a simple avatar with organs represented by circles.
       The size and color of each marker reflects the effect rating from timeline_data."""
    plt.figure(figsize=(4, 8))
    
    for organ in organs:
        x, y = organ_coords[organ]
        rating = timeline_data.get(organ, 0)
        color = get_color_for_rating(rating)
        size = 300 + 100 * rating  # Increase marker size with rating
        
        plt.scatter(x, y, s=size, color=color, alpha=0.7, edgecolors="black")
        plt.text(x, y, organ, ha="center", va="center", fontsize=10, color="white", weight="bold")
    
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.axis("off")
    st.pyplot(plt.gcf())
    plt.clf()

# ----------------------------
# Streamlit App Layout
# ----------------------------

st.set_page_config(page_title="PharmD Educational Drug Impact Simulator", layout="wide")
st.title("💊 PharmD Educational App: Drug Impact Simulator")
st.markdown("""
This interactive demo app is designed for PharmD students to learn about how various medications affect the human body over time. 
Select a medication below to see its mechanism of action, side effects, and a timeline view of its impact on major organ systems.
*Reputable clinical sources such as FDA guidelines and Micromedex inform the data used in this demo.*
""")

# Sidebar: Medication selection and timeline
st.sidebar.header("Select Medication & Timeline")
drug_choice = st.sidebar.selectbox("Medication", list(drug_data.keys()))
timeline_choice = st.sidebar.select_slider("Select Timepoint", options=["Initial", "1 Week", "1 Month", "Long Term"])

# Display Drug Information
selected_drug = drug_data[drug_choice]
st.subheader(f"Drug Information: {drug_choice}")
st.markdown(f"**Description:** {selected_drug['description']}")
st.markdown(f"**Mechanism:** {selected_drug['mechanism']}")

# Display Side Effects
st.markdown("**Common Side Effects:**")
for effect in selected_drug["side_effects"]:
    st.write(f"- {effect}")

# Timeline Effects
st.markdown(f"### Impact Over Time: {timeline_choice}")
timeline_data = selected_drug["timeline"][timeline_choice]
st.write("Below is a visual representation of how this drug affects various organ systems. The marker size and color indicate the intensity of the effect (green: minimal; orange: moderate; red: severe).")

plot_avatar(timeline_data)

# Pharmacist Consultation Area
st.markdown("### 💼 Pharmacist Consultation")
st.markdown("**Counseling Recommendations:**")
st.info(selected_drug["pharmacist_consultation"])

st.markdown("---")
st.markdown("**Note:** This is a demo version with preloaded drug data. In a full application, the database would include an extensive range of medications and dynamically updated clinical data.")
