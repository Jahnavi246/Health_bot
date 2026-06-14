import streamlit as st
import re

# =========================================================================
# 1. APPLICATION CONFIGURATION & TITLE
# =========================================================================
st.set_page_config(
    page_title="Health & Lifestyle Awareness AI", 
    page_icon="🌱", 
    layout="wide"
)

# Mandatory Public Title
st.title("🤖 Rule-Based Driven Health and Lifestyle Awareness AI Chatbot")
st.markdown("""
*An automated rules engine analyzing demographic metrics, lifestyle routines, and general health awareness parameters to provide educational lifestyle blueprints.*
""")

# =========================================================================
# 2. LEGAL DISCLAIMER & SIDEBAR
# =========================================================================
with st.sidebar:
    st.header("⚖️ Legal & Privacy")
    st.warning("""
    **EDUCATIONAL PURPOSE ONLY**  
    This application is a rule-based informational tool designed to increase health and lifestyle awareness. 
    
    *   **NO DIAGNOSIS:** This app does NOT provide medical diagnoses or clinical treatments.
    *   **NOT MEDICAL ADVICE:** Information provided is for educational reference only.
    *   **CONSULT A DOCTOR:** Always seek the advice of a physician or qualified health provider regarding medical conditions.
    """)
    
    st.divider()
    st.info("💡 **Tip:** Use the 'Live Awareness Chat' tab to ask questions about home remedies and general health tips.")

# =========================================================================
# 3. COMPREHENSIVE BASELINE DATA
# =========================================================================
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

BASE_NUTRITION = {
    "Youth (1-18)": {
        "Vegetarian": {
            "sleep_min": 9, "sleep_max": 11,
            "exercise": "60 minutes of active play daily (running, outdoor games).",
            "avoid": "Packed juices, maida biscuits, and spicy roadside mixtures.",
            "days": {day: {"Breakfast": "Ragi porridge with milk.", "Lunch": "Soft dal khichdi.", "Snack": "Fruit.", "Dinner": "Wheat upma."} for day in WEEK_DAYS}
        },
        "Non-Vegetarian": {
            "sleep_min": 9, "sleep_max": 11,
            "exercise": "60 minutes of active play daily.",
            "avoid": "Deep-fried chicken nuggets, and heavy processed meats.",
            "days": {day: {"Breakfast": "Scrambled eggs.", "Lunch": "Chicken clear soup with rice.", "Snack": "Fruit.", "Dinner": "Soft chicken strips with upma."} for day in WEEK_DAYS}
        }
    },
    "Adult (19-59)": {
        "Vegetarian": {
            "sleep_min": 7, "sleep_max": 9,
            "exercise": "30-45 minutes of moderate movement (brisk walking, yoga).",
            "avoid": "Excessive sugar, refined flour (maida), and late-night heavy meals.",
            "days": {day: {"Breakfast": "Ragi Java & sprouts.", "Lunch": "Jowar Roti & Dal.", "Snack": "Roasted chana.", "Dinner": "Millet Khichdi."} for day in WEEK_DAYS}
        },
        "Non-Vegetarian": {
            "sleep_min": 7, "sleep_max": 9,
            "exercise": "30-45 minutes of moderate movement (gym, walking).",
            "avoid": "Deep-fried chicken, trans-fats, and high-sodium meats.",
            "days": {day: {"Breakfast": "Oatmeal with Egg whites.", "Lunch": "Fish Curry & Brown Rice.", "Snack": "Boiled egg.", "Dinner": "Chicken Khichdi."} for day in WEEK_DAYS}
        }
    },
    "Senior (60-80+)": {
        "Vegetarian": {
            "sleep_min": 7, "sleep_max": 8,
            "exercise": "20-30 minutes of low-impact movement (gentle walking, stretching).",
            "avoid": "Hard-to-chew vegetables, high-sodium papads, and heavy lentils.",
            "days": {day: {"Breakfast": "Warm Ragi Ambali.", "Lunch": "Soft rice & ridge gourd dal.", "Snack": "Stewed apple.", "Dinner": "Thin vegetable khichdi."} for day in WEEK_DAYS}
        },
        "Non-Vegetarian": {
            "sleep_min": 7, "sleep_max": 8,
            "exercise": "20-30 minutes of gentle movement.",
            "avoid": "Hard-to-chew meats, highly spiced curries, and processed cold cuts.",
            "days": {day: {"Breakfast": "Soft scrambled egg whites.", "Lunch": "Fish bone broth & soft rice.", "Snack": "Papaya.", "Dinner": "Chicken stew."} for day in WEEK_DAYS}
        }
    }
}

# =========================================================================
# 4. AWARENESS RULES (Mapping focuses to lifestyle modifications)
# =========================================================================
AWARENESS_RULES = {
    "Normal / Baseline": {"advice": "Maintain your balanced routine!", "avoid_add": [], "swap": {}},
    "Diabetes / Sugar Awareness": {
        "advice": "💡 Focus on low-GI complex carbs. Replace white rice with Millets.",
        "avoid_add": ["White sugar", "White rice", "Maida", "Potato"],
        "swap": {"rice": "brown rice / foxtail millet", "chapati": "Jowar Roti", "jaggery": "stevia/nuts"}
    },
    "BP / Hypertension Awareness": {
        "advice": "💡 Limit dietary sodium. Focus on potassium-rich foods (coconut water, banana).",
        "avoid_add": ["Table salt", "Pickles", "Papads", "Salted snacks"],
        "swap": {"salt": "zero-sodium herb mix", "nuts": "unsalted almonds", "curd": "unsalted thin curd"}
    },
    "PCOD / Ovarian Cyst Awareness": {
        "advice": "💡 Focus on hormonal balance. Incorporate raw flaxseeds and pumpkin seeds. Limit dairy.",
        "avoid_add": ["Commercial milk", "Processed white flour", "Soy isolates"],
        "swap": {"milk": "almond/coconut milk", "curd": "dairy-free curd", "butter": "olive oil"}
    },
    "Stomach Pain / Nausea Awareness": {
        "advice": "💡 Adopt a gentle Bland/BRAT regimen. Minimize gastric work.",
        "avoid_add": ["Raw salads", "Chili powder", "Heavy oils", "Ghee"],
        "swap": {"Breakfast": "Warm ragi water", "Lunch": "Soft white rice & thin curd", "Snack": "Ripe banana"}
    },
    "Weight Loss Awareness": {
        "advice": "💡 Enhance satiety. Drink warm ragi java 20 minutes before meals.",
        "avoid_add": ["Deep-fried items", "Sugary tea/coffee", "Bakery items"],
        "swap": {"sweet": "roasted makhana", "banana": "green apples", "rice": "quinoa"}
    },
    "Thyroid Awareness": {
        "advice": "💡 Regulate metabolism. Thoroughly cook/steam goitrogenic vegetables (cabbage/broccoli).",
        "avoid_add": ["Raw cabbage", "Raw broccoli", "Raw kale"],
        "swap": {"salad": "cooked carrot stir-fry", "peanuts": "selenium-rich walnuts"}
    }
}

PRIORITY = {"Normal": 0, "Diabetes": 1, "BP": 1, "PCOD": 1, "Weight Loss": 1, "Stomach Pain": 3}

# =========================================================================
# 5. CORE LOGIC ENGINE
# =========================================================================
def compile_awareness_plan(age, diet, focuses):
    base = BASE_NUTRITION[age][diet]
    compiled_days = {day: meals.copy() for day, meals in base["days"].items()}
    
    active_focus = [f for f in focuses if f != "Normal / Baseline"]
    active_focus.sort(key=lambda x: PRIORITY.get(x.split(' ')[0], 1))
    
    advice_list = []
    avoid_list = set(base["avoid"].split(", "))

    for f in active_focus:
        rule = AWARENESS_RULES[f]
        advice_list.append(rule["advice"])
        avoid_list.update(rule["avoid_add"])
        
        for day in compiled_days:
            for m_type, m_desc in compiled_days[day].items():
                if m_type in rule["swap"]:
                    compiled_days[day][m_type] = rule["swap"][m_type]
                else:
                    for old, new in rule["swap"].items():
                        compiled_days[day][m_type] = re.sub(old, new, compiled_days[day][m_type], flags=re.IGNORECASE)

    return {
        "sleep": f"{base['sleep_min']} to {base['sleep_max']} hours",
        "exercise": base["exercise"],
        "avoid": ", ".join(avoid_list),
        "days": compiled_days,
        "advice": "\n\n".join(advice_list) if advice_list else AWARENESS_RULES["Normal / Baseline"]["advice"]
    }

# =========================================================================
# 6. CHATBOT DATA
# =========================================================================
CHAT_DATA = {
    ("hello", "hi", "hey"): "👋 Hello! I am your Lifestyle Awareness Assistant. How can I help you with remedies or exercise tips today?",
    ("stomach", "pain", "nausea"): "🌱 **Remedy:** Ginger water. **Rest:** Side-lying position. **Avoid:** Spicy foods.",
    ("pcod", "pcos"): "🏃‍♂️ **Exercise:** Strength training 3x/week. 🌱 **Remedy:** Spearmint tea and raw flaxseeds.",
    ("sugar", "diabetes"): "🏃‍♂️ **Movement:** 15-minute brisk walk immediately after meals. 🌱 **Remedy:** Soaked methi seeds.",
    ("weight", "loss"): "🌱 **Remedy:** Ragi java before meals. 🏃‍♂️ **Movement:** Target 10,000 steps daily.",
    ("headache", "migraine"): "🛌 **Rest:** Pitch-black, cool room. 🌱 **Remedy:** Peppermint tea and magnesium-rich pumpkin seeds."
}

# =========================================================================
# 7. USER INTERFACE
# =========================================================================
tab1, tab2 = st.tabs(["📋 Lifestyle Blueprint", "💬 Live Awareness Chat"])

with tab1:
    st.subheader("📝 Profile & Awareness Settings")
    with st.form("main_form"):
        c1, c2 = st.columns(2)
        with c1:
            age = st.selectbox("Age Bracket:", list(BASE_NUTRITION.keys()))
            diet = st.selectbox("Diet Preference:", ["Vegetarian", "Non-Vegetarian"])
            sleep = st.number_input("Average Daily Sleep (Hours):", 1, 24, 7)
        with c2:
            focuses = st.multiselect("Areas of Interest / Focus Areas:", list(AWARENESS_RULES.keys()), default=["Normal / Baseline"])
            activity = st.selectbox("Current Activity Level:", ["Sedentary", "Moderate", "High"])
        
        btn = st.form_submit_button("⚡ Generate Awareness Blueprint")

    if btn:
        plan = compile_awareness_plan(age, diet, focuses)
        
        # --- THE NUMBERS / METRICS SECTION ---
        st.subheader("📊 Awareness Metrics")
        m1, m2, c3 = st.columns(3)
        m1.metric("Suggested Sleep", plan["sleep"])
        m2.metric("Total Focus Areas", len(focuses))
        c3.metric("Activity Goal", activity)
        
        st.divider()
        
        st.info(f"**🏃‍♂️ Movement Guidelines:** {plan['exercise']}")
        st.warning(plan["advice"])
        
        st.subheader("🍛 Suggested 7-Day Lifestyle Menu")
        table_data = [{"Day": d, **plan["days"][d]} for d in WEEK_DAYS]
        st.table(table_data)
        
        st.error(f"🚫 **Avoidance Awareness List:** {plan['avoid']}")

with tab2:
    st.subheader("💬 Live Lifestyle Awareness Chat")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if p := st.chat_input("Ask about remedies, exercise, or greetings..."):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        resp = "🤖 I have guidelines for: Greetings, Stomach pain, PCOD, Sugar, Weight loss, and Headaches. Try these keywords!"
        p_low = p.lower()
        
        for keys, val in CHAT_DATA.items():
            if any(k in p_low for k in keys):
                resp = val
                break
        
        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant"): st.markdown(resp)
