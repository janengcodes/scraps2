# Get size of json data
import json 
import numpy as np # linear algebra
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split


file_path = "scraps/api/cuisine_ingredients.json"

def find_size(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return len(data)

def get_data(file):
    data = None
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def peekData(data):
    for i in range(10):
        print(data[i])

def practice_model():

    # Convert the json into a dataframe, a 2D table structure 
    c = ["id", "cuisine", "ingredients"]
    train_df = pd.DataFrame(get_data(file_path), columns=c)


    # Get the shape of the data 
    rows = train_df.shape[0]
    cols = train_df.shape[1]

    # Simple Program to predict the cuisine of an ingredients list 
    # Join the ingredients list into a string
    for i in range(rows):
        train_df.at[i, 'ingredients'] = " ".join(train_df.loc[i, 'ingredients'])

    # Feature Abstraction
    # Helps count the frequency of ingredients for each cuisine
    vectorizer = CountVectorizer()

    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(
        train_df['ingredients'], train_df['cuisine'], test_size = 0.25, random_state = 42
    )
    model = make_pipeline(CountVectorizer(), MultinomialNB())
    model.fit(x_train, y_train)

    new_ingredients = ["rice tofu fish sauce"]

    # Predict the probabilities for each cuisine
    probabilities = model.predict_proba(new_ingredients)

    # Get the class labels (cuisine names)
    class_labels = model.classes_

    # Sort the probabilities in descending order and get the indices of top N cuisines
    top_n = 3  

    prob_array = np.argsort(probabilities[0])

    # order the probabilities from largest to smallest 
    prob_array = prob_array[::-1]

    # get the top_n probabilities 
    top_indices = prob_array[:top_n]

    # Retrieve the corresponding class labels and probabilities
    top_cuisines = []
    for i in top_indices:
        top_cuisines.append((class_labels[i], probabilities[0][i]))

    # Print the top N predicted cuisines
    for cuisine, prob in top_cuisines:
        print(f"Predicted cuisine: {cuisine}, Probability: {prob:.2f}")

def load_and_prepare_data():
    data = get_data(file_path)

    # have a table with columns id, cuisine, ingredients
    c = ["id", "cuisine", "ingredients"]
    train_df = pd.DataFrame(data, columns=c)

    # for each row, join the ingredients into a string
    for i in range(train_df.shape[0]):
        train_df.at[i, 'ingredients'] = " ".join(train_df.loc[i, 'ingredients'])

    return train_df

def train_model():
    train_df = load_and_prepare_data()

    # split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(
        train_df['ingredients'], train_df['cuisine'], test_size=0.25, random_state=42
    )

    # create a model pipeline
    # 1. convert text data to sparse matrix of word counts
    # 2. multinmoial naive bayes - calculate likelihoods of cuisine given ingredients
    # 3. fit the model 
    model = make_pipeline(CountVectorizer(), MultinomialNB())
    model.fit(x_train, y_train)

    return model