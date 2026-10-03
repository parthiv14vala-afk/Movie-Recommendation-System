import requests
import csv
import time

# Your TMDB API Read Access Token
TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMjM2YmNlMmE5ODE4ZTc3OTMwZWRjZDk2ZWM5ZDgxMCIsIm5iZiI6MTc5MDk0NDg4NS4zNjQsInN1YiI6IjZhYmZhNjc1YjJhYjQ5NWQ5OGFhMGYyYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.BxxyJ4ewi4Vo-34aWbj3Oqv_XaUMm1L_CqaA6QC0_-U"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# Number of pages
TOTAL_PAGES = 10

# Store all TV shows
all_shows = []

# Get TV shows from multiple pages
for page in range(1, TOTAL_PAGES + 1):

    print("\nGetting page", page)

    url = "https://api.themoviedb.org/3/discover/tv"

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

    all_shows.extend(data["results"])

    print("TV shows collected:", len(all_shows))

    time.sleep(0.2)


# Remove duplicate shows
unique_shows = {}

for show in all_shows:
    unique_shows[show["id"]] = show


# Create CSV
with open("data/tv_shows.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "creator",
        "first_air_date",
        "rating",
        "vote_count",
        "popularity",
        "language",
        "number_of_seasons",
        "number_of_episodes",
        "poster_path"
    ])

    # Process every TV show
    for number, show in enumerate(unique_shows.values(), start=1):

        show_id = show["id"]

        print("Processing", number, ":", show["name"])

        # TV show details
        details_url = f"https://api.themoviedb.org/3/tv/{show_id}"

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
        credits_url = f"https://api.themoviedb.org/3/tv/{show_id}/credits"

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

        # Creator
        creator = ""

        creators = details.get("created_by", [])

        if len(creators) > 0:
            creator = creators[0]["name"]

        # Keywords
        keywords_url = f"https://api.themoviedb.org/3/tv/{show_id}/keywords"

        keywords_response = requests.get(
            keywords_url,
            headers=headers
        )

        keywords_data = keywords_response.json()

        keywords = []

        for keyword in keywords_data.get("results", []):
            keywords.append(keyword["name"])

        keywords = ", ".join(keywords)

        # Save data
        writer.writerow([
            show_id,
            show["name"],
            show["overview"],
            genres,
            keywords,
            cast,
            creator,
            show["first_air_date"],
            show["vote_average"],
            show["vote_count"],
            show["popularity"],
            show["original_language"],
            details.get("number_of_seasons", 0),
            details.get("number_of_episodes", 0),
            show["poster_path"]
        ])

        time.sleep(0.2)


print("\n================================")
print("TV show dataset completed!")
print("Total TV shows:", len(unique_shows))
print("Saved to: data/tv_shows.csv")
print("================================")