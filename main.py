from pandas import DataFrame, read_csv
from modified.data_processing import (MovieCollection, 
MetaSimilarityMatrix, MarkSimilarityMatrix, UserProfileStory)
import pickle
from random import choices

GLOBAL_COUNTER=666

def clear(x):
    if isinstance(x, str) and "tt" in x:
        return int(x.replace("tt", ""))
    return x

#*Ratings
movies=read_csv("movie_dataset/ratings_small_copy.csv")\
    [["userId", "movieId", "rating", "timestamp"]][:GLOBAL_COUNTER]

# movie_ratings=DataFrame(movies.pivot(index="movieId", 
# columns="userId", values="rating")).fillna(0)

# movie_ids=movie_ratings.index.values

# #*Linker
# linker=read_csv("movie_dataset/links_small.csv")\
#     [["movieId", "imdbId"]]

# linker_data=DataFrame(linker).applymap(clear)\
#     [linker["movieId"].isin(movie_ids)]

# #*Meta
# meta=read_csv("movie_dataset/movies_metadata.csv")\
#     [["imdb_id", "title", "overview"]].rename(
#         columns={"imdb_id": "imdbId"})
# meta["imdbId"]=meta["imdbId"].apply(clear)

# connected=linker_data.merge(meta, how="inner", on="imdbId")

# print("Processing csv file...")
# movies=MovieCollection(connected).get()
# pickle.dump(movie_ratings, open("movie_ratings.pickle", "wb"))

# print("Mark similarity matrix...")
# mark_matrix=MarkSimilarityMatrix(marks=movie_ratings).get()
# pickle.dump(mark_matrix, open("mark_matrix.pickle", "wb"))

# print("Meta similarity matrix...")
# meta_matrix=MetaSimilarityMatrix(objects=movies,
# meta_attributes=["title", "description"]).get()
# pickle.dump(meta_matrix, open("meta_matrix.pickle", "wb"))

movie_ratings=DataFrame(pickle.load(
    open("movie_ratings.pickle", "rb")))
mark_matrix=DataFrame(pickle.load(
    open("mark_matrix.pickle", "rb")))
meta_matrix=DataFrame(pickle.load(
    open("meta_matrix.pickle", "rb")))

# print(movie_ratings)
# print(mark_matrix)
# print(meta_matrix)

#print(test_user)

from modified.modified_implementation import ModifiedCollaborativeFiltering
import config

results=[]
errors_mod=[]
errors_van=[]

for i in range(1, 10):
    test_user=movies[movies["userId"]==i][["movieId", "rating", "timestamp"]]
    test_user=UserProfileStory(test_user).get()

    #? Weight of item similarity [0, 1]
    config.KSI=1
    #? Weight of meta similarity [0, 1]
    config.TETA=1
    #? Speed of aging objects [0, 1]
    config.ALPHA=0.001

    #print("\t\t\t\t\t Modified")
    error=ModifiedCollaborativeFiltering(
        marks=mark_matrix, metas=meta_matrix).calc_error(test_user)
    results.append(error)

    #? Weight of item similarity [0, 1]
    config.KSI=1
    #? Weight of meta similarity [0, 1]
    config.TETA=0
    #? Speed of aging objects [0, 1]
    config.ALPHA=0

    #print("\t\t\t\t\t Vanila")
    error=ModifiedCollaborativeFiltering(
        marks=mark_matrix, metas=meta_matrix).calc_error(test_user)
    results.append(error)

def rmse(errors):
    from math import sqrt
    res=0
    for error in errors:
        res+=error**2
    return sqrt(res/len(errors))

res_err_mod=[]
res_err_van=[]

from math import isnan
for col in range(len(results[0])):
    for row in range(len(results)):
        if row%2==0:
            res=results[row][col] if not isnan(results[row][col]) else 1.5
            errors_mod.append(res)
        else:
            res=results[row][col]
            errors_van.append(res)
    res_err_mod.append(rmse(errors_mod))
    res_err_van.append(rmse(errors_van))
    errors_mod=[]
    errors_van=[]

print(res_err_mod)
print(res_err_van)

from matplotlib import pyplot as plt
plt.plot(range(1, len(res_err_mod)+1), res_err_mod)
plt.plot(range(1, len(res_err_van)+1), res_err_van)
plt.legend(["Modified", "Vanila"])
plt.xlabel("Samples")
plt.ylabel("RMSE")
plt.savefig("result.png")