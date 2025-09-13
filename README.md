NutriFit AI 🥗: Personalized Diet and Workout System
Elevate your health journey with AI-Powered Recommendations
NutriFit AI is your personalized diet and fitness advisor, powered by Cohere’s Command R+ model. Get tailored suggestions based on your age, gender, height, weight, region, dietary preferences, allergies, and activity level. Optimize your well-being effortlessly!

🔗Link
https://nutrifit-ai.onrender.com

🌟 Key Features
Personalized Recommendations: Generates a complete 7-day diet and workout plan customized to your individual needs and preferences.
AI-Powered Insights: Utilizes the advanced Cohere Command R+ model for structured, natural, and effective guidance.
User-Friendly Interface: A clean, intuitive, and easy-to-use interface built with Streamlit.
Persistent Storage: Stores user preferences securely using a local SQLite database for easy access.
Different Diets: Supports a variety of dietary preferences, including vegetarian, non-vegetarian, and vegan.

🛠️ Technologies Used
Streamlit: A powerful framework for building and deploying data-driven web applications in Python.
Cohere API (Command R+): Provides access to state-of-the-art text generation capabilities for creating personalized plans.
Backend: Python
Data Storage: SQLite

⚙️ Setup and Usage
Follow these steps to get the project running locally:

1. Obtain a Cohere API Key
You'll need a Cohere API key to use the application. You can get one by signing up on the official Cohere website.
2. Set Up Your Environment
You must set your API key as an environment variable for the application to function.
For Deployment (on Render): Add COHERE_API_KEY to the Environment variables section of your project on the Render dashboard.
For Local Use (Windows PowerShell):
$env:COHERE_API_KEY = "your_actual_api_key_here"

3. Install Required Libraries
Navigate to your project folder in the terminal and install the dependencies from requirements.txt.
pip install -r requirements.txt

4. Run the App
After setting the environment variable, you can run the Streamlit app.
streamlit run app.py  (locally)

🧠 How It Works: Flowchart
Start

User inputs personal preferences (age, gender, weight, etc.) through the UI.
The app prepares a detailed prompt based on the user's input.
A request is sent to the Cohere API using the COHERE_API_KEY environment variable.
The AI model processes the request and generates a comprehensive text output with recommendations.
The app parses and formats the response to clearly display the diet and workout plans.

🧑‍🤝‍🧑 Contributors
Sneha-sharma26
Kumkum2401
