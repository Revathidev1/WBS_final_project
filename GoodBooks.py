import pandas as pd
import streamlit as st
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity 




@st.cache(suppress_st_warning=True)
def recommend(book_name):
    index = np.where(Fin_rate.index==book_name)[0][0]
    similar_books = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1], reverse=True)[1:6]
    
    data = []
    
    for i in similar_books:
        item = []
        temp_df = books[books['Book-Title'] == Fin_rate.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    return data

@st.cache
def get_top_50():
    # Load and preprocess the data here
    return final_top_50

with open('final_top_50.pickle', 'rb') as f:
    final_top_50 = pickle.load(f)
with open('Book_list.pickle', 'rb') as f:
    Book_list = pickle.load(f)   
with open('books.pickle', 'rb') as f:
    books = pickle.load(f)      
with open('Fin_rate.pickle', 'rb') as f:
    Fin_rate = pickle.load(f)
with open('similarity_score.pickle', 'rb') as f:
    similarity_score = pickle.load(f)


def main():
    """Main function of the multipage app"""
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Homepage", "Top 50 Books", "Similar Interest Books"])

    if app_mode == "Homepage":
        #st.image('ibook1.jpeg')
        st.title('GoodBooks')
        st.subheader('Welcome to our Book Recommender')
        st.subheader('Interesting Facts about Book Reading')
        st.write('Reading for just 20 minutes a day can expose you to about 1.8 million words per year.')

        st.write("Reading for 30 minutes a day can reduce your risk of Alzheimer's disease by as much as 50%.")

        st.write("Reading books for just 6 minutes can reduce stress levels by up to 68%.")

        st.write("The average CEO reads about 60 books per year.")

        st.write("Reading can improve your vocabulary and language skills. The average person knows around 20,000 words, but avid readers can know over 100,000 words.")

        st.write("According to a study by the National Endowment for the Arts, adults who read for pleasure are more likely to engage in positive civic and individual activities, such as volunteering and exercising.")

        st.write("Children who read for just 20 minutes a day score higher on standardized tests than children who do not read regularly.")

        st.write("The more you read, the faster you can read. According to a study by Forbes, the average reading speed is about 200-400 words per minute, but with practice, you can increase your speed to over 1000 words per minute.")

        st.write("The average non-fiction book contains about 50,000 words, which means that reading just one book per month can expose you to 600,000 new words per year.")



    elif app_mode == "Top 50 Books":
        page1()

    elif app_mode == "Similar Interest Books":
        page2()

def page1():
    """Function to display page 1"""
    #st.image('topbook.jpg')
    st.title("Top 50 Books")
       
    final_top_50 = get_top_50()
    st.write('<p style="font-family: Arial; font-weight: bold; font-size: 35;">Here is our top 50 books recommendetion</p>', unsafe_allow_html=True)
    container = st.container()
    container.markdown("<h1 style='color: white;'></h1>", unsafe_allow_html=True)
    container.background_color = 'white'
    with container:
        listC =[]
        C1, C2, C3, C4 = st.columns([4,2,2,2])
        with C1:
            st.markdown("**Book Title**")
        with C2:
            st.markdown("**Author**")
        with C3:
            st.markdown("**Publisher**")
        with C4:
            st.markdown("**Poster**")
        for i in range(len(final_top_50)):
            list2 = st.columns([4,2,2,2])
            listC.append(list2)
            with listC[i][0]:
                st.markdown("<div style='max-width: 200px; word-wrap: break-word;'>"+final_top_50.iloc[i]['Book-Title']+"</div>", unsafe_allow_html=True)
            with listC[i][1]:
                st.text(final_top_50.iloc[i]['Book-Author'])
            with listC[i][2]:
                st.text(final_top_50.iloc[i]['Publisher'])
            with listC[i][3]:
                st.image(final_top_50.iloc[i]['Image-URL-M'])           
     
    
    
def page2():
    """Function to display page 2"""
    st.title("Similar Interest Books")
    book_name = st.selectbox("Select a book from the list below to see the similar book recommendation from us", Book_list['Book-Title'])  
    if book_name != 'None':
        try:
            data = recommend(book_name)
        except Exception as e:
            st.error(f"An error occurred while processing your request: {str(e)}")
            st.stop()
        st.write('<p style="font-family: Arial; font-weight: bold;">Here are our Top 5 recommendation based on your book selection</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown("**Book Title**")
        with col2:    
            st.markdown("**Author**")
        with col3:    
            st.markdown("**Poster**")
        
        for item in data:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(item[0])  # Book title
            with col2:    
                st.write(item[1])  # Book author
            with col3:    
                st.image(item[2])  # Book Poster
if __name__ == "__main__":
    main()