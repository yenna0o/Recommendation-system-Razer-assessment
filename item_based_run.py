#!/usr/bin/env python
# coding: utf-8

#import packages
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json
import gzip
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import argparse
import string
# Download necessary resources
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import warnings; warnings.simplefilter('ignore')

#read in datasets
#reading in data as pd dataframe
def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield json.loads(l)
def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

# df = getDF('Appliances.json.gz')
df_meta = getDF('meta_Appliances.json.gz')

#prepare simplified meta data
def simple_meta(df_meta):
    col_to_select=['asin','title','brand']
    simple_meta_df=df_meta[col_to_select]
    return simple_meta_df

#meta data cleaning
def clean_meta(simple_meta_df):
    clean_meta_df=simple_meta_df.applymap(lambda x: x if not isinstance(x, list) else x[0] if len(x) else '')
    return clean_meta_df

#preprocess title text in clean meta df
def preprocess_text(row):
    # Convert to lowercase
    title = row['title'].lower()
    # Remove punctuation
    title = title.translate(str.maketrans('', '', string.punctuation))
    # Tokenization
    tokens = word_tokenize(title)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # Join tokens back into a string
    preprocessed_text = ' '.join(tokens)
    # Update the 'title' column in the row
    row['title'] = preprocessed_text
    return row

#use text frequency-inverse document frequency technique
def cosine_sim(preprocessed_meta):
    #initialize vectorizer
    vectorizer = TfidfVectorizer(max_df=0.7,min_df=2)
    #fit
    tfidf_matrix = vectorizer.fit_transform(preprocessed_meta['title'])
    #calculate cosine similarity
    cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim_matrix

#output similar products
def similar_products(preprocessed_meta, cosine_sim_matrix, product_id):
    # Find the index of the specified product_id
    index = preprocessed_meta[preprocessed_meta['asin'] == product_id].index[0]
    # Get the cosine similarity scores of the specified product with all other products
    product_cosine_scores = cosine_sim_matrix[index]
    # Sort the cosine similarity scores in descending order
    sorted_indices = np.argsort(product_cosine_scores)[::-1]
    # Define the number of similar products you want to retrieve
    num_similar_products = 5
    # Exclude the specified product_id itself from the similar products and slice most 10 similar
    similar_product_indices = sorted_indices[1:11]
    # Randomly select 5 from the 10 most similar product indices
    random_similar_indices = random.sample(list(similar_product_indices), num_similar_products)
    # Retrieve the product_ids of the randomly selected similar products
    similar_product_ids = preprocessed_meta.loc[random_similar_indices, 'asin'].tolist()
    return similar_product_ids

#give title of the products
def give_title(preprocessed_meta, similar_product_ids):
    titles=[]
    for ids in similar_product_ids:
        title=preprocessed_meta[preprocessed_meta['asin']==ids]['title'].iloc[0]
        titles.append(title)
    return titles

#prepare final df for cos sim calculation
def df_prepare(df_meta):
    #simplify meta df
    simple_meta_df=simple_meta(df_meta)
    #remove empty lists in df
    clean_meta_df=clean_meta(simple_meta_df)
    # Apply preprocessing to the DataFrame
    preprocessed_meta = clean_meta_df.apply(preprocess_text, axis=1)
    return preprocessed_meta

preprocessed_meta=df_prepare(df_meta)

#item based recommendation
def item_based_recommendation(preprocessed_meta, product_id):
    #calculate cos sim
    cosine_sim_matrix=cosine_sim(preprocessed_meta)
    #randomly output 5 similar products out of the most similar 10 products
    similar_product_ids=similar_products(preprocessed_meta, cosine_sim_matrix, product_id)
    #return title name
    titles=give_title(preprocessed_meta, similar_product_ids)
    return titles

def main():
    product_id = input("Enter product ID: ")
    # Call the item_based_recommendation function
    result = item_based_recommendation(preprocessed_meta, product_id)
    print("Recommendations: ", result)
if __name__ == '__main__':
    main()




