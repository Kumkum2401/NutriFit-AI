# Diet-and-workout-Recommendation-using-Cohere-Command-R+
Elevate your health journey with our NutriFit AI - your Personalized Diet and Workout Recommendation System powered by **Cohere’s Command R+ model**! Get personalized suggestions based on age, Gender, height, weight, region, dietary preferences, allergies, and acticity level. Optimize your well-being effortlessly!

## Key Features

- **Personalized recommendations:** Generates diet and workout plans customized to individual needs and preferences.
- **AI-powered insights:** Utilizes Cohere Command R+ for structured, natural, and effective guidance.
- **User-friendly interface:** Streamlined interaction through a simple and intuitive interface.

## Technologies Used

- **Streamlit:** Framework for building web applications in Python.
- **Cohere API (Command R+):** Access to AI model for text-generating capabilities.
- **Langchain:** Framework for chaining prompts and managing LLM outputs.

## Flowchart: Using Cohere API Key in Diet and Workout Recommendation Project

**Start**

**--> User inputs preferences** - Age - Gender - Weight - Height - Goal - Veg or Non-Veg - Activity Level - Allergies - Region - State

**--> Prepare request for API** - Format user input into structured API request - Include prompts and parameters as needed

**--> Send request to Cohere via Langchain** - Use Langchain library or other method - Submit request with API key

**--> Receive response from the model** - API processes request - Generates text output with recommendations

**--> Parse and format response** - Extract relevant information: - Food suggestions - Workout - Fitness tips.

**--> Present recommendations to user** - Display information in Streamlit interface


**End**

## Live Project

https://nutrifit-ai.streamlit.app

## Setup and Usage

1. Obtain a Cohere API key.
2. **Install required libraries**

   ```bash
   pip install "library"

## Run the Streamlit app:

   ````Bash
   streamlit run app.py   
