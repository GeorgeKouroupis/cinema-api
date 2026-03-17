from fastapi import FastAPI
from pydantic import BaseModel

import sqlite3

def init_db():
    conn = sqlite3.connect("cinema_db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   director TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

app = FastAPI()

class Movie(BaseModel):
    title: str
    director: str



@app.get("/")
def home():
    return {"message": "Καλωσηρθες στο API του Σινεμα!"}



@app.get("/movies")
def get_movies():
    conn = sqlite3.connect("cinema_db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies")

    rows = cursor.fetchall()
    conn.close()

    movies_list = []
    for row in rows:
        movie_dict = {
            "id": row[0],
            "title": row[1],
            "director": row[2]
        }
        movies_list.append(movie_dict)

    return movies_list


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
   conn = sqlite3.connect("cinema_db")
   cursor = conn.cursor()

   cursor.execute("SELECT * FROM movies WHERE id = ?",(movie_id,))
   row = cursor.fetchone()

   conn.close()

   if row is None:
       return {"error": "Η ταινία δεν βρεθηκε"}
   return{
       "id": row[0],
       "title": row[1],
       "director": row[2]
   }
    

@app.post("/movies")
def add_movie(new_movie: Movie):
    conn = sqlite3.connect("cinema_db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO movies (title,director) VALUES (?, ?)",
        (new_movie.title, new_movie.director)
    )

    conn.commit()
    conn.close()

    return {"message": f"Η ταινία '{new_movie.title}' αποθηκεύτηκε μόνιμα!"}



@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    conn = sqlite3.connect("cinema_db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM movies WHERE id = ?",(movie_id,))
    deleted_rows = cursor.rowcount

    conn.commit()
    conn.close()

    if deleted_rows == 0:
        return {"error": "Η ταινία δεν βρεθηκε για να διαγραφτεί"}
    
    return{"message": f"Η ταινία με ID {movie_id} διαγραφηκε οριστικά απο την βάση!"}

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, updated_movie: Movie):
    conn = sqlite3.connect("cinema_db")
    cursor = conn.cursor()

    cursor.execute("""UPDATE movies 
                   SET title = ?, director = ?
                   WHERE id = ?
                """,(updated_movie.title, updated_movie.director, movie_id))
    
    updated_rows = cursor.rowcount
    conn.commit()
    conn.close()

    if updated_rows == 0:
        return {"error": "Η ταινία δεν βρέθηκε για να ενημερωθεί"}
    
    return {"message": "Τα στοιχεία της ταινίας ενημερώθηκαν επιτυχώς!"}
