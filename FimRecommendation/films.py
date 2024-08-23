import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import datetime

# Load environment variables
load_dotenv()

client = OpenAI()

# Page configuration
st.set_page_config(page_title="Film Recommendation", layout="wide")

# Custom CSS for IMDb-like styling
imdb_style = """
<style>
    /* Main background and text color */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Title styling */
    .stTitle {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: bold !important;
    }
    
    /* Title and Header styling (white) */
    h1, h2 {
        color: #ffffff !important;
    }
   
    /* Header styling */
    .stHeader {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: bold !important;
    }

    /* Subheader styling */
    .stSubheader {
        color: #ffffff !important;
    }

    /* Button styling */
    .stButton>button {
        color: #000000;
        background-color: #f5c518;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #ffd700;
    }

    /* Input fields */
    .stTextInput>div>div>input {
        background-color: #2c2c2c;
        color: #ffffff;
        border: 1px solid #f5c518;
    }

    /* Multiselect */
    .stMultiSelect>div>div>div {
        background-color: #2c2c2c;
        color: #ffffff;
    }

    /* Table */
    .stTable {
        color: #ffffff;
    }

    /* Markdown text */
    .stMarkdown {
        color: #ffffff;
    }

    /* Slider */
    .stSlider {
        color: #f5c518;
    }
    
    /* Labels */
    label {
        color: #f5c518 !important;
        font-weight: bold !important;
    }
</style>
"""

# Inject custom CSS
st.markdown(imdb_style, unsafe_allow_html=True)

# Streamlit app
st.title("Film Recommendation")

# User input form
st.header("User Preferences")

# Get user's favorite genres
genres = ["Action", "Comedy", "Drama", "Science Fiction", "Horror", "Romance", "Thriller"]
selected_genres = st.multiselect("Select your favorite film genres:", genres)

# Get user's favorite films
favorite_films = []
for i in range(3):
    film = st.text_input(f"Favorite Film {i + 1}:", "")
    if film.strip():  # Only add non-empty strings
        favorite_films.append(film.strip())

# Get year range for recommendations
current_year = datetime.datetime.now().year
year_range = st.slider("Select year range for recommendations:", 1900, current_year, (1980, current_year))

# Initialize messages in session state if not present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful movie recommendation assistant. Provide film suggestions based on the user's favorite genres, films, and specified year range. Format your response as a markdown table with 4 film recommendations. The table should have four columns: 'Film Name', 'Year', 'Genre', and 'Brief Summary'. Ensure the recommendations are diverse, match the user's preferences, and fall within the specified year range. Avoid recommending films that the user has already listed as favorites."}
    ]

# Initialize recommendations in session state if not present
if "previous_recommendations" not in st.session_state:
    st.session_state.previous_recommendations = []

# Button to generate recommendations
if st.button("Get Film Recommendations"):
    if selected_genres and favorite_films:
        # Prepare the user message
        user_message = f"""
        Based on the following preferences:
        Favorite genres: {', '.join(selected_genres)}
        Favorite films: {', '.join(favorite_films)}
        Year range: {year_range[0]} to {year_range[1]}
        Please recommend 4 films. Provide the recommendations in a table format with columns for Film Name, Year, Genre, and a Brief Summary. Make sure the recommendations are diverse, match the user's preferences, and fall within the specified year range.
        """
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_message})
        try:
            # Generate recommendations using OpenAI
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
            )
            recommendations = completion.choices[0].message.content
            # Add assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": recommendations})
            # Display recommendations
            st.header("Film Recommendations")
            st.markdown(recommendations)
            # Save recommendations to file
            with open('film_recommendations.md', 'w') as f:
                f.write(recommendations)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please select at least one genre and enter at least one favorite film.")

