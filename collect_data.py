import requests
import csv
import time

# Your TMDB API Read Access Token
TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMjM2YmNlMmE5ODE4ZTc3OTMwZWRjZDk2ZWM5ZDgxMCIsIm5iZiI6MTc5MDk0NDg4NS4zNjQsInN1YiI6IjZhYmZhNjc1YjJhYjQ5NWQ5OGFhMGYyYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.BxxyJ4ewi4Vo-34aWbj3Oqv_XaUMm1L_CqaA6QC0_-U"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# Number of pages to collect
TOTAL_PAGES = 10

# Store movies here
all_movies = []

# Get movies from multiple pages
for page in range(1, TOTAL_PAGES + 1):

    print("\nGetting page", page)

    url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "with_origin_country": "IN",
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": page
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    all_movies.extend(data["results"])

    print("Movies collected:", len(all_movies))

    time.sleep(0.2)


# Remove duplicate movies
unique_movies = {}

for movie in all_movies:
    unique_movies[movie["id"]] = movie


# Create CSV
with open("data/movies.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "director",
        "release_date",
        "rating",
        "vote_count",
        "popularity",
        "language",
        "poster_path"
    ])

    # Process every movie
    for number, movie in enumerate(unique_movies.values(), start=1):

        movie_id = movie["id"]

        print("Processing", number, ":", movie["title"])

        # Movie details
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"

        details_response = requests.get(
            details_url,
            headers=headers
        )

        details = details_response.json()

        # Genres
        genres = []

        for genre in details.get("genres", []):
            genres.append(genre["name"])

        genres = ", ".join(genres)

        # Credits
        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

        credits_response = requests.get(
            credits_url,
            headers=headers
        )

        credits = credits_response.json()

        # Cast
        cast = []

        for person in credits.get("cast", [])[:5]:
            cast.append(person["name"])

        cast = ", ".join(cast)

        # Director
        director = ""

        for person in credits.get("crew", []):
            if person["job"] == "Director":
                director = person["name"]
                break

        # Keywords
        keywords_url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords"

        keywords_response = requests.get(
            keywords_url,
            headers=headers
        )

        keywords_data = keywords_response.json()

        keywords = []

        for keyword in keywords_data.get("keywords", []):
            keywords.append(keyword["name"])

        keywords = ", ".join(keywords)

        # Save everything
        writer.writerow([
            movie_id,
            movie["title"],
            movie["overview"],
            genres,
            keywords,
            cast,
            director,
            movie["release_date"],
            movie["vote_average"],
            movie["vote_count"],
            movie["popularity"],
            movie["original_language"],
            movie["poster_path"]
        ])

        time.sleep(0.2)


print("\n================================")
print("Movie dataset completed!")
print("Total movies:", len(unique_movies))
print("Saved to: data/movies.csv")
print("================================")