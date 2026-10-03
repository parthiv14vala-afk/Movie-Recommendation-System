import pandas as pd

# -----------------------------------
# 1. Read both CSV files
# -----------------------------------

movies = pd.read_csv("data/movies.csv")
tv_shows = pd.read_csv("data/tv_shows.csv")


# -----------------------------------
# 2. Add type column
# -----------------------------------

movies["type"] = "movie"
tv_shows["type"] = "tv"


# -----------------------------------
# 3. Rename TV show columns
# -----------------------------------

tv_shows = tv_shows.rename(columns={
    "title": "title",
    "creator": "creator"
})


# -----------------------------------
# 4. Add creator column to movies
# -----------------------------------

movies["creator"] = movies["director"]


# -----------------------------------
# 5. Select common columns
# -----------------------------------

columns = [
    "id",
    "title",
    "type",
    "overview",
    "genres",
    "keywords",
    "cast",
    "creator",
    "rating",
    "vote_count",
    "popularity",
    "language",
    "poster_path"
]

movies = movies[columns]
tv_shows = tv_shows[columns]


# -----------------------------------
# 6. Combine movies and TV shows
# -----------------------------------

data = pd.concat(
    [movies, tv_shows],
    ignore_index=True
)


# -----------------------------------
# 7. Fill empty values
# -----------------------------------

text_columns = [
    "title",
    "overview",
    "genres",
    "keywords",
    "cast",
    "creator"
]

for column in text_columns:
    data[column] = data[column].fillna("")


# -----------------------------------
# 8. Create combined features
# -----------------------------------

data["combined_features"] = (
    data["overview"] + " " +
    data["genres"] + " " +
    data["keywords"] + " " +
    data["cast"] + " " +
    data["creator"]
)


# -----------------------------------
# 9. Convert text to lowercase
# -----------------------------------

data["combined_features"] = data["combined_features"].str.lower()


# -----------------------------------
# 10. Remove duplicate titles
# -----------------------------------

data = data.drop_duplicates(
    subset=["title", "type"]
)


# -----------------------------------
# 11. Reset index
# -----------------------------------

data = data.reset_index(drop=True)


# -----------------------------------
# 12. Save ML dataset
# -----------------------------------

data.to_csv(
    "data/ml_dataset.csv",
    index=False
)


# -----------------------------------
# 13. Display results
# -----------------------------------

print("\n===================================")
print("ML DATASET CREATED SUCCESSFULLY!")
print("===================================")

print("Movies:", len(movies))
print("TV Shows:", len(tv_shows))
print("Total items:", len(data))

print("\nColumns:")
print(data.columns.tolist())

print("\nSaved to:")
print("data/ml_dataset.csv")

print("===================================")