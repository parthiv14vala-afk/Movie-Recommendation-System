import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("data/ml_dataset.csv")

vectorizer = TfidfVectorizer(
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(
    data["combined_features"]
)

similarity = cosine_similarity(tfidf_matrix)

indices = pd.Series(
    data.index,
    index=data["title"].str.lower()
)

def recommend(title, number=5):

    title = title.lower()

    if title not in indices:
        print("Movie or TV show not found!")
        return

    index = indices[title]

    similarity_scores = list(
        enumerate(similarity[index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    similarity_scores = similarity_scores[1:number + 1]

    print("\nRecommendations for:", title)
    print("--------------------------------")

    for item in similarity_scores:

        movie_index = item[0]

        movie_title = data.iloc[movie_index]["title"]
        movie_type = data.iloc[movie_index]["type"]
        rating = data.iloc[movie_index]["rating"]

        print(
            movie_title,
            "|",
            movie_type,
            "| Rating:",
            rating
        )


first_title = data.iloc[0]["title"]

print("Testing with:", first_title)

recommend(first_title)