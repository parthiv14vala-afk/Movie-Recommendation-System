import requests

TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMjM2YmNlMmE5ODE4ZTc3OTMwZWRjZDk2ZWM5ZDgxMCIsIm5iZiI6MTc5MDk0NDg4NS4zNjQsInN1YiI6IjZhYmZhNjc1YjJhYjQ5NWQ5OGFhMGYyYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.BxxyJ4ewi4Vo-34aWbj3Oqv_XaUMm1L_CqaA6QC0_-U"

# TMDB popular movies API
url = "https://api.themoviedb.org/3/movie/popular"

# Send request to TMDB
response = requests.get(
    url,
    headers={
        "Authorization": f"Bearer {TOKEN}"
    }
)

# Convert the response into Python data
data = response.json()

# Print first 5 movie names
for movie in data["results"][:5]:
    print(movie["title"])