import streamlit as st
import pandas as pd
import pickle
import numpy as np

with open('popular.pkl', 'rb') as f:
    popular_df = pickle.load(f)

pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

st.title("Book Recommendation System")
st.markdown("""
    This is a book recommendation system built using collaborative filtering. 
    Select a book below to get recommendations!
""")

st.header("Popular Books")
book_options = list(popular_df['Book-Title'].values)
selected_book = st.selectbox("Select a book", book_options)

if selected_book:
    index = np.where(pt.index == selected_book)[0][0]

    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6] 

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
        data.append(item)

    st.header("Recommended Books")
    for i, item in enumerate(data):
        st.subheader(f"Recommendation {i + 1}")
        st.write(f"**Title**: {item[0]}")
        st.write(f"**Author**: {item[1]}")
        st.image(item[2], width=150)

