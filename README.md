# Movie Recommendations (MovieLens)
In this project, we built machine learning models to predict movie recommendations based on user input and preferences. We showcased our predictive models through an interactive website. We used datasets from [MovieLens](https://grouplens.org/datasets/movielens/) with 25 million movie ratings.

## Models
1. Content-Based Model (for New Users)- Uses item features to recommend other items similar to what the user likes, based on their previous actions or explicit feedback.

Dataset sampling using below conditions:
</br>● Remove movies with unknown genre
</br>● Keep movies with ratings greater than or equal to 4
</br>● Keep movies with ratings equal or greater than 3.2 and released in 1995 or later

Create "Count Vector" for feature column and calculate cosine similarity between each count vector to calculate similarity between movies based on feature.

Recommend movies similar to another movie based on the similarity matrix created between movies.

2. Collaborative Filtering Model (for Returning Users)- A method of making automatic predictions (filtering) about the interests of a user by collecting preferences or taste information from many users (collaborating).

</br>● Sample dataset taking only ratings for movies having average rating greater than 4, removing unknown genres, and get random sample of 50K records.
</br>● Divide the original data into train and test data
</br>● Create the basic model with Alternating Least Squares (ALS)
</br>● Fit cross validator to the 'train' dataset to find the best model
</br>● Get rating predictions
</br>● Evaluate the model with RMSE score (our score = 1.672)

## Deployment
We used Flask to deploy our website. Go to the site by running "python main.py" in your terminal or command prompt and going to localhost:5000 in your browser. From there, you may wish to get movie recommendations as a New User or maybe you're a returning user, in which case you'd have to input a User ID (perhaps your user ID is 500 - try it!). 




