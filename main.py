import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
import sqlalchemy
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

#Initialize app
app = Flask(__name__)

@app.route("/")
def login():
    if (request.args):
        args=request.args
        #print(args["user-id"])
        user_searched_id=args["user-id"]
        #print(user_searched_id)
        recommender_df=pd.read_csv("collab_filter_recommendations.csv")
        movies_df=pd.read_csv("collab_filter_movies.csv")
        movies_recommender=recommender_df.merge(movies_df, on="movieId")
        filtered_movie_user_df=movies_recommender[movies_recommender["userId"]==int(user_searched_id)]
        filtered_movie_user_df["genres"]=filtered_movie_user_df["genres"].str.replace("|"," ")
        #print(movies_recommender)
        prediction=filtered_movie_user_df[["title","genres"]].values.tolist()
        #args["user-id"]].values.tolist()
        #print(movies_recommender)
        #prediction=movies_recommender.iloc[:,[5,6]].values.tolist()
        print(prediction)
        return render_template('user-recommender.html', prediction_string=prediction) 

    else:
        return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
def my_movie_recommender():
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
            sim_scores = sim_scores[1:11]
            movie_indices = [i[0] for i in sim_scores]
            return loaded_df.iloc[movie_indices[1:11],[1,2,3]].values.tolist()

        result_text=genre_recommendations(processed_text)
        
        if (request.args):
            args=request.args
            #print(args["user-id"])
            user_searched_id=args["user-id"]
            #print(user_searched_id)
            recommender_df=pd.read_csv("collab_filter_recommendations.csv")
            movies_df=pd.read_csv("collab_filter_movies.csv")
            movies_recommender=recommender_df.merge(movies_df, on="movieId")
            filtered_movie_user_df=movies_recommender[movies_recommender["userId"]==int(user_searched_id)]
            filtered_movie_user_df["genres"]=filtered_movie_user_df["genres"].str.replace("|"," ")
            #print(movies_recommender)
            prediction=filtered_movie_user_df[["title","genres"]].values.tolist()
            #args["user-id"]].values.tolist()
            #print(movies_recommender)
            #prediction=movies_recommender.iloc[:,[5,6]].values.tolist()
            print(prediction)

    processed_text='Because you searched for "'+processed_text+'", you may also like the following movies:'
    return render_template('user-recommender.html', movie_prediction_string=result_text,prediction_string=prediction,searched_string=processed_text)

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
            sim_scores = sim_scores[1:11]
            movie_indices = [i[0] for i in sim_scores]
            return loaded_df.iloc[movie_indices[1:11],[1,2,3]].values.tolist()

        result_text=genre_recommendations(processed_text)
        # movie_list=[]
        # for i, row in processed_text.iterrows():
        #     movie_list.append(row["title"])

        # print(movie_list)
       
    # return jsonify(processed_text)
    processed_text='Because you liked "'+processed_text+'", you may also like the following movies:'
    return render_template('home.html', prediction_string=result_text,searched_string=processed_text)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/data")
def data():
    return render_template("data.html")


if __name__ == "__main__":
    app.run(debug=True)