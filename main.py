from pandas import DataFrame, read_csv
from modified.data_processing import (MovieCollection, 
MetaSimilarityMatrix, MarkSimilarityMatrix)
import pickle
from random import choices

GLOBAL_COUNTER=5000

def rating(x):
    if x==0:
        return choices([0, 2, 3, 4], 
        weights=[0.6, 0.1, 0.1, 0.2])[0]
    return x

data=read_csv("movie_dataset/ratings_small.csv")\
    [["userId", "movieId", "rating"]][:GLOBAL_COUNTER]

data=DataFrame(data.pivot_table(index="movieId", 
columns="userId", values="rating")).fillna(0)\
    .applymap(rating)
print(data.head(10))
matrix=MarkSimilarityMatrix(marks=data).get()
print(matrix)
# data=read_csv("movie_dataset/movies_metadata.csv")\
#     [["id", "overview", "title"]][:GLOBAL_COUNTER]

# print("Processing csv file...")
# movies=MovieCollection(data).get()

# print("Calculating meta similarity matrix...")
# matrix=MetaSimilarityMatrix(
#     meta_attributes=["title", "description"], 
#     objects=movies).get()
# pickle.dump(matrix, open("meta_matrix.pickle", "wb"))

# print("Calculating similarity matrix...")
# matrix=MetaSimilarityMatrix(
#     meta_attributes=["title", "description"], 
#     objects=movies).get()
# pickle.dump(matrix, open("meta_matrix.pickle", "wb"))