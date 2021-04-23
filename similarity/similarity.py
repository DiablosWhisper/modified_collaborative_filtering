#region				-----External Imports-----
from sklearn.metrics.pairwise import cosine_similarity
from pandas import DataFrame
from spacy import load
#endregion

#region				 -----Global Imports-----
sentence=load("en_core_web_md")
#endregion

class Similarity(object):
    @staticmethod
    def sentence(first: "String", second: "String")->"Float":
        """Calculates similarity between two sentences
            first: sentence with arbitrary length
            second: sentence with arbitrary length
        return return value ranged between 0 and 1
        """
        return sentence(first).similarity(sentence(second))
    @staticmethod
    def cosine(self, ratings: "Dataframe")->"Dataframe":
        """Calculates cosine similarity between row
            ratings: dataframe with objects ids 
            on rows and user ids on columns
        return matrix of pairwise similarities
        """
        return DataFrame(cosine_similarity(ratings))