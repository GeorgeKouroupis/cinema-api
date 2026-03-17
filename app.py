from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Movie(BaseModel):
    title: str
    director: str

@app.get("/")
def home():
    return {"message": "Καλωσηρθες στο API του Σινεμα!"}

movies_db = [
    {"id":1, "title": "Inception", "director": "Christopher Nolan"},
    {"id":2, "title": "The Matrix", "director": "Lana Wachowski, Lilly Wachowski"},
    {"id":3, "title": "Interstellar", "director": "Christopher Nolan"}
]

@app.get("/movies")
def get_movies():
    return movies_db


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in movies_db:
        if movie["id"] == movie_id:
            return movie
    
    return {"error": "Η ταινία δεν βρέθηκε!"}
    

@app.post("/movies")
def add_movie(new_movie: Movie):
    new_id = len(movies_db)+1

    movie_dict = {
        "id": new_id,
        "title": new_movie.title,
        "director": new_movie.director
    }

    movies_db.append(movie_dict)

    return {"message": "Η ταινία προστέθηκε!", "movie": movie_dict}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    for movie in movies_db:
        if movie["id"] == movie_id:
            movies_db.remove(movie)
            return {"message": f"Η ταινία με id {movie_id} διαγραφηκε επιτυχως!"}
    
    return {"error": "Η ταινία δεν βρέθηκε για να διαγραφεί"}

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, updated_movie: Movie):
    for movie in movies_db:
        if movie["id"] == movie_id:
            movie["title"] = updated_movie.title
            movie["director"] = updated_movie.director

            return {"message": "Η ταινία ενημερώθηκε!", "movie": movie}
        
    return {"error": "Η ταινία δεν βρέθηκε για να ενημερωθεί"}