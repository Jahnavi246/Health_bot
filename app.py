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
*An automated rules engine analyzing demographic metrics, lifestyle routines, and clinical health awareness parameters to provide dynamic educational lifestyle blueprints.*
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
    st.info("💡 **Tip:** Use the 'Live Awareness Chat' tab to ask questions about home remedies, exercise strategies, and sleep optimization.")

# =========================================================================
# 3. COMPREHENSIVE BASELINE HEALTH MATRIX (VEGETARIAN & NON-VEGETARIAN)
# =========================================================================
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

BASE_NUTRITION = {
    "Youth (1-18)": {
        "Vegetarian": {
            "sleep_ideal": "9 to 11 hours",
            "exercise": "60 minutes of active play daily (running, cycling, outdoor games).",
            "avoid": "Packed artificially flavored juices, highly processed maida biscuits, and spicy roadside mixtures.",
            "days": {
                "Monday": {"Breakfast": "Ragi porridge with whole milk & soft idli.", "Lunch": "Soft dal khichdi with ghee and carrots.", "Snack": "Apple slices with a tiny bit of honey.", "Dinner": "Wheat upma with grated carrots."},
                "Tuesday": {"Breakfast": "Millet porridge with organic jaggery.", "Lunch": "Curd rice with mashed carrots.", "Snack": "Homemade soft ragi biscuits.", "Dinner": "Soft paneer bhurji with a mini chapati."},
                "Wednesday": {"Breakfast": "Warm oats porridge with milk and sliced bananas.", "Lunch": "Soft-cooked rice, tomato rasam, and soft potato cubes.", "Snack": "Stewed apple.", "Dinner": "Moong dal soup with broken wheat khichdi."},
                "Thursday": {"Breakfast": "Ragi Java with a little milk and nuts.", "Lunch": "Vegetable khichdi with fresh curd.", "Snack": "Roasted makhana.", "Dinner": "Soft vermicelli upma with peas."},
                "Friday": {"Breakfast": "Oats porridge with mashed banana.", "Lunch": "Mashed rice, leafy green dal, and ghee.", "Snack": "Fresh curd with honey.", "Dinner": "Paneer cubes with soft wheat dahlia upma."},
                "Saturday": {"Breakfast": "Wheat pancake (Dosa style) with milk.", "Lunch": "Sambar rice with soft-cooked pumpkin.", "Snack": "A handful of boiled sweet corn.", "Dinner": "Light vegetable clear soup and idli."},
                "Sunday": {"Breakfast": "Ragi vermicelli sweet semiya.", "Lunch": "Soft rice, thick paneer dal.", "Snack": "Fresh fruit smoothie.", "Dinner": "Soft-cooked broken rice khichdi with ghee."}
            }
        },
        "Non-Vegetarian": {
            "sleep_ideal": "9 to 11 hours",
            "exercise": "60 minutes of active play daily (running, cycling, outdoor games).",
            "avoid": "Packed artificially flavored juices, deep-fried chicken nuggets, and heavy processed meats.",
            "days": {
                "Monday": {"Breakfast": "Scrambled eggs (2 eggs) with soft toast.", "Lunch": "Soft dal khichdi with shredded chicken breast.", "Snack": "Apple slices with a tiny bit of honey.", "Dinner": "Wheat upma with soft chicken strips."},
                "Tuesday": {"Breakfast": "Millet porridge with organic jaggery & one boiled egg.", "Lunch": "Curd rice with steamed mashed fish.", "Snack": "Homemade soft ragi biscuits.", "Dinner": "Soft chicken bhurji with a mini chapati."},
                "Wednesday": {"Breakfast": "Boiled eggs with sliced bananas.", "Lunch": "Soft-cooked rice, chicken clear soup, and soft potato cubes.", "Snack": "Stewed apple.", "Dinner": "Moong dal soup with boiled egg whites."},
                "Thursday": {"Breakfast": "Ragi Java with a little milk & scrambled eggs.", "Lunch": "Chicken khichdi with fresh curd.", "Snack": "Roasted makhana.", "Dinner": "Soft vermicelli upma with egg drop."},
                "Friday": {"Breakfast": "Oats porridge with mashed banana & boiled egg.", "Lunch": "Mashed rice, chicken dal soup, and ghee.", "Snack": "Fresh curd with honey.", "Dinner": "Shredded chicken with soft wheat dahlia upma."},
                "Saturday": {"Breakfast": "Wheat pancake (Dosa style) with milk and egg white.", "Lunch": "Sambar rice with soft boiled fish.", "Snack": "A handful of boiled sweet corn.", "Dinner": "Light chicken clear soup and idli."},
                "Sunday": {"Breakfast": "Ragi vermicelli sweet semiya with a boiled egg.", "Lunch": "Soft rice, chicken clear soup.", "Snack": "Fresh fruit smoothie.", "Dinner": "Soft-cooked chicken khichdi."}
            }
        }
    },
    "Adult (19-59)": {
        "Vegetarian": {
            "sleep_ideal": "7 to 9 hours",
            "exercise": "30-45 minutes of moderate exercise 5 days a week (brisk walking, gym, yoga).",
            "avoid": "Excessive white sugar, refined flour (maida), highly processed packaged snacks, and late-night heavy meals.",
            "days": {
                "Monday": {"Breakfast": "Unsweetened Ragi Java with buttermilk & sprouts.", "Lunch": "Jowar Roti, a bowl of Toor Dal, and ladyfinger (bhindi) sabzi.", "Snack": "A handful of roasted chana.", "Dinner": "Light Foxtail Millet Khichdi with curd."},
                "Tuesday": {"Breakfast": "Millet Poha with roasted peanuts and lemon juice.", "Lunch": "Brown rice, mixed vegetable sambar, and palak stir-fry.", "Snack": "One seasonal fruit (Guava or Apple).", "Dinner": "Two whole wheat chapatis with paneer bhurji."},
                "Wednesday": {"Breakfast": "Oats Idli with mint and coriander chutney.", "Lunch": "Bajra Roti, green moong dal, and ivy gourd sabzi.", "Snack": "Plain buttermilk with roasted cumin powder.", "Dinner": "Broken wheat (dalia) upma with carrots and peas."},
                "Thursday": {"Breakfast": "Moong Dal Chilla (savory pancake) with curd.", "Lunch": "Jowar Roti, chana masala, and cucumber salad.", "Snack": "Soaked almonds and walnuts.", "Dinner": "Little Millet curd rice with stir-fried veggies."},
                "Friday": {"Breakfast": "Ragi porridge with a dash of jaggery and almonds.", "Lunch": "Brown rice, tomato rasam, and paneer curry.", "Snack": "Roasted makhana.", "Dinner": "Mixed vegetable clear soup with grilled tofu/paneer."},
                "Saturday": {"Breakfast": "Vegetable Upma made from multi-millet semolina.", "Lunch": "Whole wheat chapatis, ridge gourd curry, and dal.", "Snack": "Coconut water.", "Dinner": "Foxtail Millet pulao with raita."},
                "Sunday": {"Breakfast": "Healthy Multi-grain Dosa with ginger chutney.", "Lunch": "Brown rice or Jowar Roti, sprouted methi dal.", "Snack": "A cup of green tea or spiced buttermilk.", "Dinner": "Light oats porridge or vegetable khichdi."}
            }
        },
        "Non-Vegetarian": {
            "sleep_ideal": "7 to 9 hours",
            "exercise": "30-45 minutes of moderate exercise 5 days a week (brisk walking, gym, strength training).",
            "avoid": "Excessive white sugar, deep-fried chicken, highly processed meats, and trans-fats.",
            "days": {
                "Monday": {"Breakfast": "Two scrambled eggs with spinach and whole wheat toast.", "Lunch": "Jowar Roti, yellow dal, and chicken breast curry.", "Snack": "A handful of roasted chana.", "Dinner": "Light Foxtail Millet chicken khichdi with curd."},
                "Tuesday": {"Breakfast": "Millet Poha with boiled egg whites.", "Lunch": "Brown rice, mixed vegetable sambar, and grilled fish.", "Snack": "One seasonal fruit (Guava or Apple).", "Dinner": "Two whole wheat chapatis with chicken minced kheema."},
                "Wednesday": {"Breakfast": "Oats omelette with chopped tomatoes and coriander.", "Lunch": "Bajra Roti, green moong dal, and chicken cubes.", "Snack": "Plain buttermilk with cumin powder.", "Dinner": "Broken wheat (dalia) upma with soft chicken strips."},
                "Thursday": {"Breakfast": "Moong Dal Chilla with egg drop and curd.", "Lunch": "Jowar Roti, chicken masala, and cucumber salad.", "Snack": "Soaked almonds and walnuts.", "Dinner": "Little Millet egg curd rice."},
                "Friday": {"Breakfast": "Ragi porridge with boiled eggs.", "Lunch": "Brown rice, tomato rasam, and steamed fish.", "Snack": "Roasted makhana.", "Dinner": "Mixed vegetable clear soup with shredded chicken breast."},
                "Saturday": {"Breakfast": "Egg bhurji (2 eggs) with single chapati.", "Lunch": "Whole wheat chapatis, chicken curry, and dal.", "Snack": "Coconut water.", "Dinner": "Foxtail Millet chicken pulao with raita."},
                "Sunday": {"Breakfast": "Healthy Multi-grain Dosa with chicken mince stuffing.", "Lunch": "Brown rice, simple fish curry, and curd.", "Snack": "A cup of green tea or spiced buttermilk.", "Dinner": "Light oats porridge with egg white drop."}
            }
        }
    },
    "Senior (60-80+)": {
        "Vegetarian": {
            "sleep_ideal": "7 to 8 hours",
            "exercise": "20-30 minutes of low-impact movement (gentle walking, joint mobility stretches, light pranayama).",
            "avoid": "Hard-to-chew vegetables, heavily oiled pickles, high-sodium papads, and gas-forming heavy lentils.",
            "days": {
                "Monday": {"Breakfast": "Warm Ragi Ambali (porridge) with thin buttermilk.", "Lunch": "Soft-cooked rice, ridge gourd dal, and curd.", "Snack": "Stewed apple (soft).", "Dinner": "Thin vegetable khichdi (easy to digest)."},
                "Tuesday": {"Breakfast": "Soft oats porridge with milk.", "Lunch": "Mashed brown rice with bottle gourd (lauki) curry and moong dal.", "Snack": "Warm papaya pieces.", "Dinner": "Soft broken wheat dahlia upma."},
                "Wednesday": {"Breakfast": "Well-cooked idli with light tomato chutney.", "Lunch": "Soft jowar roti soaked in dal, with mashed ash gourd sabzi.", "Snack": "A cup of warm milk with turmeric.", "Dinner": "Clear vegetable broth with soft boiled paneer."},
                "Thursday": {"Breakfast": "Finger millet flour rava upma (very soft).", "Lunch": "Mashed rice, curd, and a side of soft boiled ivy gourd.", "Snack": "One ripe banana.", "Dinner": "Moong dal soup with an idli."},
                "Friday": {"Breakfast": "Warm ragi malt (sweet version with little jaggery).", "Lunch": "Soft rice, drumstick sambar, and mashed carrot subzi.", "Snack": "Thin curd water.", "Dinner": "Oats porridge with no sugar, spices or oil."},
                "Saturday": {"Breakfast": "Soft-cooked vermicelli with carrots.", "Lunch": "Soft whole wheat chapati mashed inside yellow dal.", "Snack": "Stewed pear or warm papaya.", "Dinner": "Little millet khichdi cooked with extra water."},
                "Sunday": {"Breakfast": "Moong dal green chilla (soft texturized).", "Lunch": "Mashed rice, light cumin flavored rasam and curd.", "Snack": "Coconut water.", "Dinner": "Warm vegetable stock soup with soft idli."}
            }
        },
        "Non-Vegetarian": {
            "sleep_ideal": "7 to 8 hours",
            "exercise": "20-30 minutes of low-impact movement (gentle walking, joint mobility stretches, breathing exercises).",
            "avoid": "Hard-to-chew meats, highly spiced non-veg curries, heavily oiled pickles, and processed cold cuts.",
            "days": {
                "Monday": {"Breakfast": "Scrambled egg whites with soft warm milk.", "Lunch": "Soft-cooked rice with fish bone broth and curd.", "Snack": "Stewed apple (soft).", "Dinner": "Thin chicken khichdi (easy to digest)."},
                "Tuesday": {"Breakfast": "Soft oats porridge with milk and egg drop.", "Lunch": "Mashed brown rice with chicken dal broth.", "Snack": "Warm papaya pieces.", "Dinner": "Soft dahlia with shredded chicken."},
                "Wednesday": {"Breakfast": "Well-cooked idli with soft egg bhurji.", "Lunch": "Soft jowar roti soaked in chicken soup.", "Snack": "A cup of warm milk with turmeric.", "Dinner": "Clear chicken broth with boiled egg whites."},
                "Thursday": {"Breakfast": "Finger millet flour soft upma with egg white crumbs.", "Lunch": "Mashed rice, curd, and boiled soft fish.", "Snack": "One ripe banana.", "Dinner": "Moong dal soup with a soft chicken idli."},
                "Friday": {"Breakfast": "Warm ragi malt with egg whites.", "Lunch": "Soft rice, simple fish broth, and mashed carrot subzi.", "Snack": "Thin curd water.", "Dinner": "Oats porridge cooked in water with egg drop."},
                "Saturday": {"Breakfast": "Soft-cooked vermicelli with egg white drop.", "Lunch": "Soft chapati mashed inside chicken stew.", "Snack": "Stewed pear.", "Dinner": "Little millet chicken khichdi cooked with extra water."},
                "Sunday": {"Breakfast": "Moong dal green chilla (soft texturized) with chicken mince.", "Lunch": "Mashed rice, light chicken clear soup and curd.", "Snack": "Coconut water.", "Dinner": "Warm chicken stock soup with soft idli."}
            }
        }
    }
}

# =========================================================================
# 4. CLINICAL ADJUSTMENT RULES (Pathology Override Engine)
# =========================================================================
CLINICAL_RULES = {
    "Normal / Baseline": {
        "advice": "Keep maintaining a great, balanced, age-appropriate baseline health routine!",
        "avoid_add": [],
        "swap_rules": {}
    },
    "Diabetes / Sugar Awareness": {
        "advice": "⚠️ **Diabetes Protocol:** Focus on low-GI complex carbs. Avoid white sugar, maida, and refined white rice entirely. Restrict heavy starches and high-sugar fruits.",
        "avoid_add": ["White sugar", "White rice", "Maida", "Potato", "Fizzy juices", "Ice cream"],
        "swap_rules": {
            "rice": "brown rice / foxtail millet",
            "Roti": "Jowar Roti",
            "chapati": "Jowar Roti",
            "chapatis": "Jowar Rotis",
            "jaggery": "stevia / raw nuts",
            "sweet": "unsweetened option"
        }
    },
    "BP / Hypertension Awareness": {
        "advice": "⚠️ **Hypertension Protocol:** Restrict dietary sodium strictly. Remove all packaging-heavy foods, pickles, papads, and salted snacks. Focus on potassium-rich foods.",
        "avoid_add": ["Table salt", "Commercial pickles", "Salted papads", "Processed cheese", "Salted snacks"],
        "swap_rules": {
            "salt": "zero-sodium herb mix",
            "chana": "unsalted roasted chana",
            "nuts": "unsalted almonds",
            "curd": "unsalted thin curd"
        }
    },
    "PCOD / Ovarian Cyst Awareness": {
        "advice": "⚠️ **PCOD Protocol:** Focus heavily on clearing androgens and normalizing insulin sensitivity. Eliminate commercial dairy products. Focus on raw flaxseeds and pumpkin seeds.",
        "avoid_add": ["Commercial milk", "Full-fat dairy", "Processed white flour", "Soy isolates"],
        "swap_rules": {
            "milk": "almond/coconut milk",
            "curd": "dairy-free curd",
            "butter": "olive oil",
            "ghee": "flaxseed oil"
        }
    },
    "Thyroid Awareness": {
        "advice": "⚠️ **Thyroid Protocol:** Regulate your baseline metabolism. Strictly restrict raw goitrogenic vegetables (like raw cabbage, broccoli, cauliflower, or kale). Thoroughly steaming or cooking these items blocks goitrogenic enzymes.",
        "avoid_add": ["Raw cabbage", "Raw broccoli", "Raw cauliflower", "Raw kale"],
        "swap_rules": {
            "salad": "cooked carrot beetroot stir-fry",
            "veggies": "thoroughly steamed vegetables",
            "peanuts": "selenium-rich walnuts"
        }
    },
    "Stomach Pain / Nausea / Motions / Vomiting": {
        "advice": "⚠️ **Gastrointestinal Distress Protocol (Acute GI Rest):** Adopt a highly restricted Bland/BRAT regimen (Bananas, soft Rice, Applesauce, Toast). Minimize gastric workload—eliminate raw salads, heavy oils, dairy, and strong spices.",
        "avoid_add": ["Raw salads", "Chili powder", "Commercial milk", "Heavy oils", "Ghee", "Fibrous lentils"],
        "swap_rules": {
            "Breakfast": "Warm thin ragi water or dry toast",
            "Lunch": "Soft white rice & thin curd whey water",
            "Dinner": "Light watery rice gruel with a tiny pinch of salt",
            "Snack": "Soft ripe banana or stewed peeled applesauce"
        }
    },
    "Weight Loss Awareness": {
        "advice": "⚠️ **Weight Loss Protocol:** Enhance satiety and control calorie densities. Drink 1 glass of unsweetened ragi ambali mixed with buttermilk 20 minutes before core meals to block mechanical overeating.",
        "avoid_add": ["Deep-fried items", "Bakery sweets", "Late night heavy meals", "Sugary tea/coffee"],
        "swap_rules": {
            "sweet": "roasted makhana",
            "banana": "green apples",
            "rice": "quinoa or foxtail millet",
            "upma": "multi-vegetable oats upma"
        }
    },
    "Weight Gain / Malnutrition": {
        "advice": "⚠️ **Weight Gain / Malnutrition Protocol:** Ensure nutrient density and a healthy calorie surplus. Integrate healthy lipids (ghee, nuts, seeds, full-fat dairy) and structured high-quality proteins.",
        "avoid_add": ["Junk trans-fats", "Carbonated diet sodas", "Empty sugar calories"],
        "swap_rules": {
            "buttermilk": "creamy whole milk",
            "thin": "thick and nutrient-dense",
            "Snack": "Ragi porridge with whole milk, honey, and nuts"
        }
    },
    "Headache / Migraine Awareness": {
        "advice": "⚠️ **Headache/Migraine Protocol:** Remove vascular triggers. Avoid all amine-rich items (aged cheeses), cured meats, MSG, and artificial sweeteners. Focus on high-magnesium items.",
        "avoid_add": ["Aged cheese", "Nitrite-cured meats", "MSG / Chinese sauces", "Artificial sweeteners"],
        "swap_rules": {
            "peanuts": "magnesium-rich pumpkin seeds",
            "Snack": "Magnesium-dense pumpkin seeds"
        }
    },
    "Cold / Cough / Flu": {
        "advice": "⚠️ **Cold & Cough Protocol:** Soothe inflamed bronchial tracts. Eliminate all chilled beverages, ice creams, and excessive mucus-producing dairy. Emphasize warming bioactives (ginger, turmeric, pepper).",
        "avoid_add": ["Chilled drinks", "Ice creams", "Yogurt from fridge", "Cold raw salads"],
        "swap_rules": {
            "curd": "warm peppercorn clear rasam",
            "buttermilk": "warm ginger herbal infusion",
            "Dinner": "Steaming hot vegetable or chicken soup with ginger and garlic"
        }
    },
    "Tuberculosis (TB)": {
        "advice": "⚠️ **Tuberculosis Protocol:** High-protein, nutrient-dense configurations are mandatory to offset muscle wasting. Increase healthy fats (ghee, seeds) and easily absorbable minerals.",
        "avoid_add": ["Refined oil", "Alcohol", "Raw unpasteurized milk", "Fasting"],
        "swap_rules": {
            "rice": "protein-enriched brown rice with dal",
            "Snack": "High-protein seed mix and boiled eggs",
            "fruit": "banana with dry fruits"
        }
    },
    "Malaria": {
        "advice": "⚠️ **Malaria Protocol:** High-carbohydrate, high-protein, easily digestible foods are required to assist liver cells and fight infection. Ensure rigorous hydration with electrolytes.",
        "avoid_add": ["Heavy red meat", "Deep fried foods", "High-fiber raw salad", "Spicy masalas"],
        "swap_rules": {
            "Lunch": "Soft-cooked white rice with simple yellow dal soup",
            "Snack": "Fresh tender coconut water or sweet apple puree"
        }
    },
    "Chickenpox": {
        "advice": "⚠️ **Chickenpox Protocol:** Emphasize soft, cool, easily chewable, and non-acidic foods to soothe potential oral or gastrointestinal lesions. Maximize lysine-rich clean options.",
        "avoid_add": ["Chili powder", "Raw citrus fruits", "Salty chips", "Hot spicy curries"],
        "swap_rules": {
            "Breakfast": "Cool ragi malt or oats porridge with milk",
            "Snack": "Cool mashed banana or sweet coconut water",
            "Lunch": "Soft curd rice (cool, not hot)"
        }
    }
}

# Conflict Resolution Priority Index
CLINICAL_PRIORITY = {
    "Normal / Baseline": 0,
    "Diabetes / Sugar Awareness": 1,
    "BP / Hypertension Awareness": 1,
    "PCOD / Ovarian Cyst Awareness": 1,
    "Thyroid Awareness": 1,
    "Weight Loss Awareness": 1,
    "Weight Gain / Malnutrition": 1,
    "Headache / Migraine Awareness": 1,
    "Tuberculosis (TB)": 2,
    "Malaria": 2,
    "Chickenpox": 2,
    "Cold / Cough / Flu": 2,
    "Stomach Pain / Nausea / Motions / Vomiting": 3 # Highest Priority: Acute GI distress overrides all underlying choices
}

# =========================================================================
# 5. CORE LOGIC ENGINE (Diet, Exercise, & Sleep Plan Generator)
# =========================================================================
def compile_health_awareness_plan(age, diet, focuses):
    base = BASE_NUTRITION[age][diet]
    compiled_days = {day: meals.copy() for day, meals in base["days"].items()}
    
    active_focus = [f for f in focuses if f != "Normal / Baseline"]
    active_focus.sort(key=lambda x: CLINICAL_PRIORITY.get(x, 1))
    
    advice_list = []
    avoid_list = set(base["avoid"].split(", "))

    for f in active_focus:
        rule = CLINICAL_RULES[f]
        advice_list.append(rule["advice"])
        avoid_list.update(rule["avoid_add"])
        
        for day in compiled_days:
            for m_type, m_desc in compiled_days[day].items():
                if m_type in rule["swap_rules"]:
                    compiled_days[day][m_type] = rule["swap_rules"][m_type]
                else:
                    for old, new in rule["swap_rules"].items():
                        compiled_days[day][m_type] = re.sub(old, new, compiled_days[day][m_type], flags=re.IGNORECASE)

    return {
        "sleep": base["sleep_ideal"],
        "exercise": base["exercise"],
        "avoid": ", ".join(sorted(list(avoid_list))),
        "days": compiled_days,
        "advice": "\n\n".join(advice_list) if advice_list else CLINICAL_RULES["Normal / Baseline"]["advice"]
    }

# =========================================================================
# 6. CHATBOT CONFIGURATION MATRIX
# =========================================================================
CHAT_DATA = {
    ("hello", "hi", "hey", "greetings", "namaste"): (
        "👋 **Hello! Welcome to your Health & Lifestyle Awareness Assistant.**\n\n"
        "I am ready to help you with personalized health suggestions split completely across **Food, Exercise, and Rest**. You can ask me questions about any of the following parameters:\n"
        "- **Chronic Profiles:** Diabetes (Sugar), BP (Hypertension), Thyroid, PCOD/Ovarian Cysts, and Migraine Headaches.\n"
        "- **Acute/Infection Profiles:** Stomach pain, vomiting, diarrhea, nausea, cold, cough, fever, TB, Malaria, or Chickenpox.\n"
        "- **Weight Adjustments:** Sustainable Weight Loss or Weight Gain/Malnutrition frameworks.\n\n"
        "Please specify your query or keyword to pull immediate guidelines!"
    ),
    ("stomach", "pain", "nausea", "vomiting", "motions", "gastric", "acidity", "reflux", "gas", "bloating"): (
        "### 🤢 Gastric, Reflux & Stomach Distress Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Sip on cool, unsalted buttermilk mixed with fresh roasted cumin (jeera) powder.\n"
        "- Consume 100ml of raw alkaline ash gourd juice early in the morning on an empty stomach.\n"
        "- **Avoid:** Raw salads, chili powder, heavy oils, ghee, and commercial milk.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- Practice **Vajrasana (Thunderbolt Pose)** for 5-10 minutes immediately after taking light meals to assist digestion mechanics.\n"
        "- Avoid core twists, heavy crunches, or deadlifts that compress gastric cavities.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Elevate your torso by 4-6 inches during sleep using propped wedge pillows to counteract acid reflux.\n"
        "- Strictly avoid lying down flat on your back within 2-3 hours of eating."
    ),
    ("pcod", "pcos", "ovarian", "cyst", "irregular periods"): (
        "### 🦋 PCOD & Ovarian Restoration Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Drink two cups of hot organic spearmint tea daily to reduce systemic androgen levels.\n"
        "- Mix 1 tablespoon of raw organic pumpkin and flaxseeds into breakfast routines to leverage natural plant lignans.\n"
        "- **Avoid:** Commercial milk, full-fat commercial dairy, and processed white flour.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- Prioritize progressive strength training or High-Intensity Interval Training (HIIT) 3 times a week to optimize insulin sensitivity.\n"
        "- Perform pelvic-opening yoga postures like *Baddha Konasana* (Butterfly Pose) to stimulate regional blood flow.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Maintain a rigid circadian rhythm. Aim to be asleep by 10:30 PM to optimize the release of luteinizing and follicle-stimulating hormones."
    ),
    ("sugar", "diabetes", "glucose", "insulin"): (
        "### 🩸 Blood Glucose & Insulin Optimization Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Swallowing 1 teaspoon of soaked fenugreek (methi) seeds on an empty stomach supports healthy carbohydrate processing.\n"
        "- Brew organic green tea seasoned with true cinnamon powder instead of sugar.\n"
        "- **Avoid:** White sugar, refined white rice, maida, and potatoes.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- **Post-Meal Walk:** Undertake a continuous 15-minute steady brisk walk immediately following major core meals to sweep glucose directly out of your bloodstream.\n"
        "- Integrate moderate resistance weight training 3 times a week to improve muscle glycogen storage capacity.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Ensure a minimum of **7.5 hours of sleep** each night. Sleep restriction triggers excess cortisol production, compounding insulin resistance."
    ),
    ("bp", "hypertension", "heart", "cardiovascular", "cholesterol"): (
        "### 🫀 Hypertension & Cardiac Health Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Drink fresh, warm hibiscus tea which serves as a natural antioxidant and mild blood-vessel relaxer.\n"
        "- Incorporate unheated cold-pressed garlic cloves crushed inside a teaspoon of raw organic honey.\n"
        "- **Avoid:** Table salt, commercial pickles, salted papads, and processed snacks.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- Enjoy steady-state cardiovascular exercises like brisk walking or slow cycling for 30 minutes, 5 times a week.\n"
        "- Strictly avoid high-intensity explosive training or prolonged breath-holding (valsalva maneuver) which spikes blood pressure spikes.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Maintain a strict target of **8 hours of uninterrupted rest** daily to soothe the sympathetic nervous system and stabilize pressure variables."
    ),
    ("weight loss", "lose weight", "fat"): (
        "### 📉 Sustainable Weight Loss Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Drink 1 cup of warm ragi java mixed with thin buttermilk 20 minutes before core meals to block mechanical overeating.\n"
        "- Keep hydrating with cucumber slices, green tea, and warm water.\n"
        "- **Avoid:** Deep-fried items, bakery sweets, and late-night calorie-dense meals.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- Combine full-body strength/weight training 3 times a week with a step goal of 8,000 to 10,000 steps daily.\n"
        "- Squeeze in brief walks post-meals to prevent fat-storage insulin surges.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Secure **7.5 to 8.5 hours** of sleep. Rest deficit prompts the brain to produce more Ghrelin (the hunger hormone), making cravings difficult to stop."
    ),
    ("weight gain", "malnutrition", "lean"): (
        "### 📈 Healthy Weight & Malnutrition Recovery Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Prepare warm, thick ragi porridge with organic cow milk, a drizzle of honey, and a blend of crushed walnuts and almonds.\n"
        "- Snack on ghee-roasted organic makhana or soaked raisins.\n"
        "- **Avoid:** Junk trans-fats, carbonated diet sodas, and empty sugar calories.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- Focus on slow weight-bearing resistance training (squats, light weights) to construct healthy muscle mass instead of storing empty fats.\n"
        "- Limit exhausting cardiovascular cardio, which burns off required restorative calories.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Muscles rebuild and expand primarily during deep sleep. Prioritize **8.5 to 9 hours** of peaceful rest each night."
    ),
    ("headache", "migraine"): (
        "### 🧠 Migraine & Vascular Headache Management Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Brew hot ginger-peppermint tea to reduce associated migraine nausea.\n"
        "- Consume a handful of raw pumpkin seeds to boost your magnesium reserves.\n"
        "- **Avoid:** Aged cheese, nitrite-cured meats, MSG/Chinese sauces, and artificial sweeteners.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- Avoid fast-paced, high-impact activities that cause rapid heart-rate spikes during a flare-up.\n"
        "- Perform slow, methodical head-and-neck releases, shoulder rolls, and gentle walking in dim environments.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Rest in a completely pitch-black, soundproof, cool room. Keep highly consistent sleep-wake times to prevent waking migraine triggers."
    ),
    ("thyroid", "hypothroid", "tsh"): (
        "### 🦋 Thyroid Metabolic Regulation Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Consume 2-3 selenium-rich organic walnuts daily to support active T4 to T3 thyroid hormone conversion.\n"
        "- **Avoid:** Raw cabbage, raw broccoli, raw cauliflower, and raw kale.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- Focus on preserving muscle mass by performing low-impact strength training and yoga poses like *Sarvangasana* (Shoulder Stand) to stimulate thyroid circulation.\n"
        "- Walk at a brisk pace for 30 minutes daily.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Go to bed before 10:30 PM to align with normal endocrine output. Get 8 hours of sleep to reduce stress-induced TSH spikes."
    ),
    ("cold", "cough", "running nose", "flu"): (
        "### 🌡️ Respiratory Soothing & Cold/Cough Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Brew a warm tea using holy basil (Tulsi) leaves, crushed black pepper, fresh ginger, and a drop of honey.\n"
        "- Perform deep steam inhalation with 2 drops of eucalyptus oil twice daily.\n"
        "- **Avoid:** Chilled drinks, ice creams, yogurt/curd from the fridge, and cold raw salads.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- **The Neck Rule:** If your cold symptoms are strictly above the neck (mild runny nose), gentle walking is acceptable. If below the neck (fever, dry chest cough, severe body aches), rest completely.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Prop your chest and head up using multiple pillows to prevent nasal secretions from collecting in your airways. Target **9 hours of sleep**."
    ),
    ("tb", "tuberculosis"): (
        "### 🦠 Tuberculosis (TB) Lung & Weight Repair Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Sip warm milk enriched with organic raw ginger and turmeric to soothe inflamed throat linings.\n"
        "- Supplement daily meals with energy-dense elements (pure ghee, boiled egg whites, almond paste) to combat tissue wasting.\n"
        "- **Avoid:** Refined oil, raw unpasteurized milk, and fasting tabs.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- Active infection calls for complete rest. Limit physical workouts to soft joint rotations or gentle pranayama (alternate nostril breathing) to improve vital lung capacity.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Prioritize **9 to 10 hours** of resting recovery sleep. Lung tissues repair their cellular lining maximum during deep slumber."
    ),
    ("malaria"): (
        "### 🦟 Malaria Infection Care & Rehydration Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Drink fresh barley water, boiled apple puree, or light rice gruel to digest nutrients without taxing your liver.\n"
        "- Maintain hydration with mineral-balanced oral rehydration salts (ORS) to replace high-fever electrolyte losses.\n"
        "- **Avoid:** Heavy red meat, deep-fried foods, high-fiber raw salad, and spicy masalas.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- **Zero Exercise Protocol:** Confined to absolute bed rest during active malaria infection and the post-fever recovery phase.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Secure **10+ hours** of absolute bed rest. Avoid physical strain because your spleen may expand during malaria, making physical impacts dangerous."
    ),
    ("chickenpox"): (
        "### 🤒 Chickenpox Soothing & Lesion Care Blueprint\n\n"
        "**🌱 Food & Home Remedies:**\n"
        "- Take lukewarm oat-flour baths to naturally reduce intense skin itching and accelerate lesion dry-out.\n"
        "- Sip cool coconut water or lysine-dense cold milk to soothe sores inside your mouth.\n"
        "- **Avoid:** Chili powder, raw citrus fruits, salty chips, and hot spicy curries.\n\n"
        "**🏃‍♂️ Exercise & Movement Strategy:**\n"
        "- Absolutely no physical workouts. Confined to total rest until all lesions dry and crust over to prevent skin scarring.\n\n"
        "**🛌 Rest & Sleep Guidelines:**\n"
        "- Rest on highly breathable, soft, sanitized 100% cotton sheets. Keep your room cool to prevent sweat-induced rash irritation. Aim for 9-10 hours."
    )
}

# =========================================================================
# 7. USER INTERFACE (TABS MATRIX)
# =========================================================================
tab1, tab2 = st.tabs(["📋 Lifestyle Blueprint Generator", "💬 Live Awareness Chat"])

with tab1:
    st.subheader("📝 Profile & Awareness Settings")
    with st.form("main_form"):
        c1, c2 = st.columns(2)
        with c1:
            age = st.selectbox("Age Bracket Group:", list(BASE_NUTRITION.keys()))
            diet = st.selectbox("Diet Preference Profile:", ["Vegetarian", "Non-Vegetarian"])
            sleep = st.number_input("Average Daily Sleep (Hours Checked):", 1, 24, 7)
        with c2:
            focuses = st.multiselect("Areas of Interest / Clinical Focus Areas:", list(CLINICAL_RULES.keys()), default=["Normal / Baseline"])
            activity = st.selectbox("Current Activity Level Status:", ["Sedentary Profile", "Moderate Active", "High Intensity Activity"])
        
        btn = st.form_submit_button("⚡ Generate Complete Awareness Blueprint")

    if btn:
        if not focuses:
            focuses = ["Normal / Baseline"]
            
        plan = compile_health_awareness_plan(age, diet, focuses)
        
        st.subheader("📊 Awareness Metrics Summary")
        m1, m2, c3 = st.columns(3)
        m1.metric("Suggested Sleep Duration", plan["sleep"])
        m2.metric("Active Health Focus Profiles", len(focuses))
        c3.metric("User Activity Frame", activity)
        
        st.divider()
        
        st.info(f"**🏃‍♂️ Movement Guidelines & Exercise Protocol:** {plan['exercise']}")
        st.warning(plan["advice"])
        
        st.subheader("🍛 Suggested 7-Day Modified Health Menu Plan")
        st.write(f"The structure menus have been dynamically adjusted for your custom health profile configuration:")
        
        table_data = []
        for d in WEEK_DAYS:
            meals = plan["days"][d]
            table_data.append({
                "Day Order": d,
                "Breakfast Meal": meals["Breakfast"],
                "Lunch Core": meals["Lunch"],
                "Evening Snack Option": meals["Snack"],
                "Dinner Choice": meals["Dinner"]
            })
        st.table(table_data)
        
        st.error(f"🚫 **Strict Avoidance Food Awareness List:** {plan['avoid']}")

with tab2:
    st.subheader("💬 Live Lifestyle Awareness Chat Room")
    st.caption("Ask specific metabolic, infection, or recovery questions regarding Food, Exercise, or Rest parameters.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if p := st.chat_input("Ask about meals, home remedies, exercises, or rest timings..."):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): 
            st.markdown(p)
        
        resp = "🤖 I have specialized guidelines across Food, Exercise, and Rest for: Greetings, Stomach distress, PCOD, Diabetes (Sugar), Blood Pressure, Weight modifications, Headaches, Thyroid, Flu, TB, Malaria, and Chickenpox. Try typing those keywords!"
        p_low = p.lower()
        
        for keys, val in CHAT_DATA.items():
            if any(re.search(rf"\b{k}\b", p_low) for k in keys):
                resp = val
                break
        
        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant"): 
            st.markdown(resp)
