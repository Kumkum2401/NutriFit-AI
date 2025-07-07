import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.graph_objs as go
from langchain.prompts import PromptTemplate
from langchain_cohere import ChatCohere
from langchain_core.runnables import RunnableLambda
import sqlite3

# UI 
st.set_page_config(page_title="Diet & Workout Planner", layout="wide")
st.title("NutriFit AI🥗: Personalized Diet and Fitness Advisor")

# Secure API Key (Using Streamlit Secrets instead of hardcoding)
if "COHERE_API_KEY" in st.secrets:
    cohere_api_key = st.secrets["COHERE_API_KEY"]
else:
    st.error("API Key not found. Please check your secrets.toml file.")

generation_config = {"temperature": 0.6, "max_tokens": 2048}
model = ChatCohere(model="command-r-plus", cohere_api_key= cohere_api_key, generation_config=generation_config)

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

with st.sidebar:
    st.header("User Preferences")
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=10, max_value=100, step=1)
    gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
    weight = st.number_input("Enter your weight (kg):", min_value=30.0, max_value=200.0, step=0.5)
    height = st.number_input("Enter your height (cm):", min_value=100, max_value=220, step=1)
    goal = st.selectbox("Select your goal:", ["Weight Loss", "Weight Gain", "Muscle Gain", "Maintenance"])
    diet = st.radio("Diet Preference:", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    activity_level = st.selectbox("Activity Level:", ["Sedentary", "Moderate", "Active"])
    medical_conditions = st.text_area("Any medical conditions or allergies?")
    region = st.text_input("Enter your country/region:")
    state = st.text_input("Enter your state:")
    
    if st.button("Save Preferences"):
        cursor.execute("""
            INSERT INTO user_preferences 
            (name, age, gender, weight, height, goal, diet, activity_level, medical_conditions, region, state) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, weight, height, goal, diet, activity_level, medical_conditions, region, state))
        conn.commit()
        st.success("Preferences Saved!")

prompt_template = PromptTemplate(
    input_variables=['name', 'age', 'gender', 'weight', 'height', 'goal', 'diet', 'activity_level', 'medical_conditions', 'region', 'state'],
    template="Personalized Diet & Workout Plan:\n"
            "Name: {name}\n"
            "Age: {age}\n"
            "Gender: {gender}\n"
            "Weight: {weight} kg\n"
            "Height: {height} cm\n"
            "Goal: {goal}\n"
            "Diet Preference: {diet}\n"
            "Activity Level: {activity_level}\n"
            "Medical Conditions: {medical_conditions}\n"
            "Region: {region}\n"
            "State: {state}\n"
            "Provide a structured 7-day diet and workout plan."
)

chain = RunnableLambda(lambda inputs: prompt_template.format(**inputs)) | model

if st.button("Generate Plan"):
    response = chain.invoke({
        "name": name, "age": age, "gender": gender, "weight": weight, "height": height,
        "goal": goal, "diet": diet, "activity_level": activity_level,
        "medical_conditions": medical_conditions, "region": region, "state": state
    })
    st.markdown(response.content)
    # st.write(response)
