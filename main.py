from pandas import DataFrame, read_csv
from modified.data_processing import (MovieCollection, 
MetaSimilarityMatrix, MarkSimilarityMatrix)
import pickle
from random import choices

GLOBAL_COUNTER=160

def rating(x):
    if x==0:
        return choices([0, 2, 3, 4], 
        weights=[0.6, 0.1, 0.1, 0.2])[0]
    return x
def clear(x):
    if isinstance(x, str) and "tt" in x:
        return int(x.replace("tt", ""))
    return x

#*Ratings
movies=read_csv("movie_dataset/ratings_small_copy.csv")\
    [["userId", "movieId", "rating"]][:GLOBAL_COUNTER]

movie_ratings=DataFrame(movies.pivot(index="movieId", 
columns="userId", values="rating")).fillna(0)\
    .applymap(rating)

movie_ids=movie_ratings.index.values

#*Linker
linker=read_csv("movie_dataset/links_small.csv")\
    [["movieId", "imdbId"]]

linker_data=DataFrame(linker).applymap(clear)\
    [linker["movieId"].isin(movie_ids)]

#*Meta
meta=read_csv("movie_dataset/movies_metadata.csv")\
    [["imdb_id", "title", "overview"]].rename(
        columns={"imdb_id": "imdbId"})
meta["imdbId"]=meta["imdbId"].apply(clear)

connected=linker_data.merge(meta, how="inner", on="imdbId")

marks=MarkSimilarityMatrix(movie_ratings).get()

print("Processing csv file...")
movies=MovieCollection(connected).get()

# print("Calculating meta similarity matrix...")
# metas=MetaSimilarityMatrix(
#     meta_attributes=["title", "description"], 
#     objects=movies).get()

# print("Meta similarity matrix:")
# print(metas)
print("Mark similarity matrix:")
print(marks)
print("User ratings:")
print(movie_ratings)
#pickle.dump(marks, open("mark_matrix.pickle", "wb"))
# pickle.dump(metas, open("meta_matrix.pickle", "wb"))

# print("Calculating similarity matrix...")
# matrix=MetaSimilarityMatrix(
#     meta_attributes=["title", "description"], 
#     objects=movies).get()
# pickle.dump(matrix, open("meta_matrix.pickle", "wb"))