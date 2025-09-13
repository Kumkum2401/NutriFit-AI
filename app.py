import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.graph_objs as go
import cohere
import sqlite3

# --- API Key Setup ---
# Use os.environ to get the API key directly from the environment variables
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")

if COHERE_API_KEY is None:
    # This block will run if the API key is not found (e.g., when running locally without setting the environment variable)
    st.error("Error: COHERE_API_KEY not found. Please set it as an environment variable in your local environment or on the Render dashboard for deployment.")
else:
    # This block will run if the API key is found. All app logic goes here.
    # Initialize the Cohere client with the API key
    co = cohere.Client(COHERE_API_KEY)

    # UI 
    st.set_page_config(
        page_title="Diet & Workout Planner", 
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("NutriFit AI🥗: Personalized Diet and Fitness Advisor")

    # Database Setup
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            weight REAL,
            height REAL,
            goal TEXT,
            diet TEXT,
            activity_level TEXT,
            medical_conditions TEXT,
            region TEXT,
            state TEXT
        )
    """)
    conn.commit()

    # --- Sidebar Inputs ---
    with st.sidebar:
        st.header("🍎 NutriFit AI")
        
        with st.expander("Basic Info"):
            name = st.text_input("Name", key="name_input")
            age = st.number_input("Age", 10, 100, key="age_input")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender_input")
        
        with st.expander("Physical Stats"):
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=60.0, step=0.5, key="weight_input")
            height = st.number_input("Height (cm)", min_value=100, max_value=220, value=165, step=1, key="height_input")

        with st.expander("Goals & Diet"):
            goal = st.selectbox("Goal", ["Weight Loss", "Weight Gain", "Muscle Gain", "Maintenance"], key="goal_input")
            diet = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"], key="diet_input")
            activity_level = st.selectbox("Activity Level", ["Sedentary", "Moderate", "Active"], key="activity_input")
        
        medical_conditions = st.text_area("Medical Conditions / Allergies", key="medical_input")
        region = st.text_input("Country/Region", key="region_input")
        state = st.text_input("State", key="state_input")
        
        if st.button("Save Preferences"):
            try:
                cursor.execute("""
                    INSERT INTO user_preferences 
                    (name, age, gender, weight, height, goal, diet, activity_level, medical_conditions, region, state) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, age, gender, weight, height, goal, diet, activity_level, medical_conditions, region, state))
                conn.commit()
                st.success("Preferences Saved!")
            except Exception as e:
                st.error(f"Error saving preferences: {e}")

    # Main page header
    st.header("🍎 NutriFit AI")
    st.subheader("Your Personalized Diet & Workout Planner")

    # Build the prompt string 
    def build_prompt(inputs):
        return (
            "Personalized Diet & Workout Plan:\n"
            f"Name: {inputs['name']}\n"
            f"Age: {inputs['age']}\n"
            f"Gender: {inputs['gender']}\n"
            f"Weight: {inputs['weight']} kg\n"
            f"Height: {inputs['height']} cm\n"
            f"Goal: {inputs['goal']}\n"
            f"Diet Preference: {inputs['diet']}\n"
            f"Activity Level: {inputs['activity_level']}\n"
            f"Medical Conditions: {inputs['medical_conditions']}\n"
            f"Region: {inputs['region']}\n"
            f"State: {inputs['state']}\n"
            "Provide a structured 7-day diet and workout plan. "
            "Format the plan with a 'Diet Plan:' heading followed by a detailed diet, and a separate 'Workout Plan:' heading followed by a detailed workout. "
            "Ensure both sections are clearly labeled."
        )

    if st.button("Generate Plan"):
        with st.spinner("Generating your personalized plan..."):
            try:
                user_inputs = {
                    "name": st.session_state.name_input, "age": st.session_state.age_input, "gender": st.session_state.gender_input,
                    "weight": st.session_state.weight_input, "height": st.session_state.height_input, "goal": st.session_state.goal_input,
                    "diet": st.session_state.diet_input, "activity_level": st.session_state.activity_input,
                    "medical_conditions": st.session_state.medical_input,
                    "region": st.session_state.region_input, "state": st.session_state.state_input
                }
                
                prompt = build_prompt(user_inputs)

                response = co.chat(
                    message=prompt,
                    model="command-r-plus",
                    temperature=0.6,
                    max_tokens=4096
                )

                plan_text = response.text
                
                # Split the response into Diet and Workout sections
                diet_plan_marker = "Diet Plan:"
                workout_plan_marker = "Workout Plan:"

                if diet_plan_marker in plan_text and workout_plan_marker in plan_text:
                    diet_section, workout_section = plan_text.split(workout_plan_marker, 1)
                    diet_section = diet_section.replace(diet_plan_marker, "")
                    workout_section = workout_section.strip()

                    # Add emojis to the markdown to make it more visually appealing
                    diet_section = diet_section.replace("Day 1:", "Day 1: 📅")
                    diet_section = diet_section.replace("Day 2:", "Day 2: 📅")
                    diet_section = diet_section.replace("Day 3:", "Day 3: 📅")
                    diet_section = diet_section.replace("Day 4:", "Day 4: 📅")
                    diet_section = diet_section.replace("Day 5:", "Day 5: 📅")
                    diet_section = diet_section.replace("Day 6:", "Day 6: 📅")
                    diet_section = diet_section.replace("Day 7:", "Day 7: 📅")
                    diet_section = diet_section.replace("Breakfast:", "**Breakfast:** 🍳")
                    diet_section = diet_section.replace("Lunch:", "**Lunch:** 🍲")
                    diet_section = diet_section.replace("Dinner:", "**Dinner:** 🍽️")
                    diet_section = diet_section.replace("Snack:", "**Snack:** 🍎")
                    diet_section = diet_section.replace("Rest Day:", "Rest Day: 🧘")
                    
                    # Add emojis to the workout section
                    workout_section = workout_section.replace("Day 1:", "Day 1: 🏋️")
                    workout_section = workout_section.replace("Day 2:", "Day 2: 💪")
                    workout_section = workout_section.replace("Day 3:", "Day 3: 🏃")
                    workout_section = workout_section.replace("Day 4:", "Day 4: 🧘")
                    workout_section = workout_section.replace("Day 5:", "Day 5: 🏋️")
                    workout_section = workout_section.replace("Day 6:", "Day 6: 💪")
                    workout_section = workout_section.replace("Day 7:", "Day 7: 🏃")

                    # Create two columns to display the content side-by-side
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown("### Diet Plan")
                        # Use a container for a card-like effect
                        with st.container(border=True):
                            st.markdown(diet_section)

                    with col2:
                        st.markdown("### Workout Plan")
                        # Use a container for a card-like effect
                        with st.container(border=True):
                            st.markdown(workout_section)
                    
                    st.markdown("---")
                    # Add a download button for the plan
                    st.download_button(
                        label="Download Plan",
                        data=plan_text,
                        file_name="diet_and_workout_plan.txt",
                        mime="text/plain"
                    )

                else:
                    st.markdown(plan_text)
                    
            except Exception as e:
                st.error(f"Error generating plan: {e}")
