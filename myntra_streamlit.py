import pandas as pd 
import matplotlib.pyplot as plt
import nltk
import streamlit as st
pd.options.display.float_format = '{:,.2f}'.format
st.title("Mytra Product Analysis - Mens T-Shirt")

# Reading the raw dataset
df = pd.read_csv('https://raw.githubusercontent.com/VivekS-DS/E-Com_Web-Scraping/main/myntra_tshirt_data_cleaned.csv')
brand_list = df['product_name'].tolist()

st.sidebar.title('Select the Brand')
brand = st.sidebar.selectbox('Brand',df['product_name'].unique())
selected_brand = df[df['product_name'] == brand]

selected_product_id = st.sidebar.selectbox('product_id',selected_brand['product_id'].unique())

selected_product = selected_brand[selected_brand['product_id'] == selected_product_id]

product_details = st.sidebar.button('Price')
product_spec = st.sidebar.button('Specification')
product_rating = st.sidebar.button('Rating')
sentiment = st.sidebar.button('Review Sentiment')
st.sidebar.subheader('Find Top brands Based on')
crosstab_collar = st.sidebar.button('Collar Type')

if product_details:
    st.subheader('Product Information')
    st.write("Brand: ", selected_product['product_name'].iloc[0])
    st.write("Product id: ", selected_product['product_id'].iloc[0])
    st.write("Product Description: ", selected_product['product_description'].iloc[0])
    price_difference = int(selected_product['discounted_price'].iloc[0]) - int(selected_product['original_price'].iloc[0])
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Myntra Price ₹:", selected_product['discounted_price'].iloc[0], price_difference)
    col2.metric("Actual Price ₹:", selected_product['original_price'].iloc[0])
    col3.metric("Discount %:", selected_product['discount_percentage'].iloc[0])

if product_spec:
    st.subheader('Product Specification')
    st.write("Fabric: ", selected_product['fabric_material'].iloc[0])
    st.write("Collar Type: ", selected_product['neck_type'].iloc[0])

if product_rating:
    st.subheader('Customer Rating')
    st.write("Overall Rating: ", selected_product['overall_rating'].iloc[0])
    st.write("Votes by verified Buyers: ", selected_product['votes'].iloc[0])
    
    
    fig, ax = plt.subplots(figsize=(10, 8))
    plot_data = selected_product['customer_rated_rating'].iloc[0]
    plot_data = list(map(int, eval(plot_data)))
    ax.hist(plot_data, bins='auto', color='blue', edgecolor='black')
    st.pyplot(fig)

if crosstab_collar:
    # Calculate the joint probability table using crosstab
    brand_collar = (pd.crosstab(index=df['product_name'],
                                            columns=df['neck_type'],
                                            margins=True,
                                            normalize=False))
    brand_collar = brand_collar.sort_values(by='All',ascending=False).nlargest(10, 'All')        
    # Display the Joint Probability Table
    st.table(data=brand_collar)

if sentiment:
    st.subheader('Customer Sentiment')
    label = selected_product['review_label'].iloc[0]

    if label == 'Positive':
        st.success(selected_product['review_label'].iloc[0])
    else: st.error(selected_product['review_label'].iloc[0])

    all_words = []
    for text in selected_product['review_cleaned']:
        all_words.extend(text.split())
    
    # Frequency Distribution
    freq_dist = nltk.FreqDist(all_words)
    st.table(freq_dist)

