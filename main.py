from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from pandas import DataFrame
from numpy import array
from time import time

data={
    "timestamp": [1, 2, 3, 4, 5],
    "check": [10, 32, 432, 32, 100]
}

dataframe=DataFrame(data, columns=["timestamp", "check"])

last_timestamp=dataframe.timestamp.max()

dataframe.timestamp=dataframe.timestamp\
    .apply(lambda x: abs(x-last_timestamp))

print(dataframe.sort_values(["timestamp"]))

# example={
#     "user_1":  [1, 0, 2, 0, 0, 1],
#     "user_2":  [0, 0, 4, 2, 0, 0],
#     "user_3":  [3, 5, 0, 4, 4, 3],
#     "user_4":  [0, 4, 1, 0, 3, 0],
#     "user_5":  [0, 0, 2, 5, 4, 3],
#     "user_6":  [5, 0, 0, 0, 2, 0],
#     "user_7":  [0, 4, 3, 0, 0, 0],
#     "user_8":  [0, 0, 0, 4, 0, 2],
#     "user_9":  [5, 0, 4, 0, 0, 0],
#     "user_10": [0, 2, 3, 0, 0, 0],
#     "user_11": [4, 1, 5, 2, 2, 4],
#     "user_12": [0, 3, 0, 0, 5, 0]
# }

# df=DataFrame(example, columns=["user_1", "user_2", "user_3",
# "user_4", "user_5", "user_6", "user_7", "user_8", "user_9",
# "user_10", "user_11", "user_12"])
# print(df, end="\n\n")
# print(df["user_1"])
# print("-----------Dataframe-----------")
# print(df, end="\n\n")
# print("-----------Pairwise-----------")
# sim_matrix=DataFrame(cosine_similarity(df))
# print(sim_matrix, end="\n\n")

# vec_1=array([[1, 0, 3, 0, 0, 5, 0, 0, 5, 0, 4, 0]])
# vec_2=array([[0, 0, 5, 4, 0, 0, 4, 0, 0, 2, 1, 3]])
# print(cosine_similarity(vec_1, vec_2))

# from matplotlib import pyplot as plt

# vanila_y=[0.712, 0.740, 0.753, 0.764, 0.773]
# vanila_x=[5, 10, 15, 20, 25]

# modified_y=[0.467, 0.483, 0.487, 0.493, 0.512]
# modified_x=[5, 10, 15, 20, 25]

# plt.plot(vanila_x, vanila_y)
# plt.plot(modified_x, modified_y)

# plt.ylabel("RMSE")
# plt.xlabel("Number of samples (V)")

# plt.legend(["Vanila", "Modified"])
# plt.savefig("result.png")