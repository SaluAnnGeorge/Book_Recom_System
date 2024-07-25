import streamlit as st
import pandas as pd
import numpy as np

# Title and description
st.title("Book Recommendation System")
st.markdown("""
This app provides a personalised book recommendation system. Enter your preferences and get book recommendations.
""")

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv('Books.csv')

df = load_data()

# User Inputs
st.sidebar.header("User Input Features")

def user_input_features():
    genres = st.sidebar.multiselect("Genres", df['generes'].unique())
    authors = st.sidebar.multiselect("Authors", df['author'].unique())
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5)
    max_price = st.sidebar.slider("Maximum Price", 0.0, 200.0, 50.0)
    return genres, authors, min_rating, max_price

genres, authors, min_rating, max_price = user_input_features()

# Recommendation Logic
def recommend_books(df, genres, authors, min_rating, max_price):
    filtered_books = df[
        (df['rating'] >= min_rating) &
        (df['price'] <= max_price)
    ]
    if genres:
        filtered_books = filtered_books[filtered_books['generes'].apply(lambda x: any(genre in x for genre in genres))]
    if authors:
        filtered_books = filtered_books[filtered_books['author'].isin(authors)]
    return filtered_books

recommended_books = recommend_books(df, genres, authors, min_rating, max_price)

# Display Recommendations
st.header("Recommended Books")
if not recommended_books.empty:
    for index, row in recommended_books.iterrows():
        st.subheader(row["title"])
        st.write(f"Author: {row['author']}")
        st.write(f"Rating: {row['rating']}")
        st.write(f"Price: {row['price']} {row['currency']}")
        st.write(f"Genres: {row['generes']}")
        st.write(f"Description: {row['description']}")
        st.write(f"Publisher: {row['publisher']}")
        st.write(f"Page Count: {row['page_count']}")
        st.write(f"Published Date: {row['published_date']}")
        st.write("-----")
else:
    st.write("No books found matching the criteria.")

# Optional: Add more functionality or visualizations as needed