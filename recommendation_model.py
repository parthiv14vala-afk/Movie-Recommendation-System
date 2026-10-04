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
        return []

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

    recommendations = []

    for item in similarity_scores:

        movie_index = item[0]

        recommendations.append({
            "title": data.iloc[movie_index]["title"],
            "type": data.iloc[movie_index]["type"],
            "rating": data.iloc[movie_index]["rating"],
            "poster_path": data.iloc[movie_index]["poster_path"],
            "similarity": round(item[1] * 100, 2)
        })

    return recommendations

first_title = data.iloc[0]["title"]

print("Testing with:", first_title)

results = recommend(first_title)

print("\nRecommendations:")
print("--------------------------------")

for item in results:

    print(
        item["title"],
        "|",
        item["type"],
        "| Rating:",
        item["rating"],
        "| Similarity:",
        str(item["similarity"]) + "%"
    )