import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import sqlalchemy
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

#Initialize app
app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home")
def home():    
    return render_template("home.html")

@app.route("/home", methods=["GET", "POST"])
def my_form_post():
    processed_text = "This Failed"
    if request.method=="POST":
        processed_text = request.form['title']
        print(processed_text)
        loaded_sim=pickle.load(open("genrepredictor-similaritymatrix.pckl","rb"))
        loaded_df=pickle.load(open("movie_df.pckl","rb"))
        indices = pd.Series(loaded_df.index, index=loaded_df['title'])

        # Function that get movie recommendations based on the cosine similarity score of movie genres
        def genre_recommendations(title):
            idx = indices[title]
            sim_scores = list(enumerate(loaded_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:21]
            movie_indices = [i[0] for i in sim_scores]
            return list(loaded_df.iloc[movie_indices]["title"])
             
        processed_text=str(genre_recommendations(processed_text))
       
    return processed_text

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/data")
def data():
    return render_template("data.html")


if __name__ == "__main__":
    app.run(debug=True)