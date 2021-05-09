#region				-----External Imports-----
from sklearn.metrics.pairwise import cosine_similarity
import spacy
#endregion

#region				 -----Global Imports-----
sentence=spacy.load("en_core_web_sm")
#endregion

class Similarity(object):
    @staticmethod
    def sentence(first: "String", second: "String")->"Float":
        """Calculates similarity between two sentences
            first: sentence with arbitrary length
            second: sentence with arbitrary length
        return return value ranged between 0 and 1
        """
        first, second=sentence(first), sentence(second)
        return first.similarity(second)
    @staticmethod
    def cosine(ratings: "Dataframe")->"Numpy[Numpy[Float]]":
        """Calculates cosine similarity between row
            ratings: dataframe with objects ids 
            on rows and user ids on columns
        return matrix of pairwise similarities
        """
        return cosine_similarity(ratings)