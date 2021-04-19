#region				-----External Imports-----
from sklearn.metrics.pairwise import cosine_similarity
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
    def cosine(first: "Numpy", second: "Numpy")->"Float":
        """Calculates similarity between two vectors
            first: vector that has length 'n'
            second: vector that has length 'n'
        return value ranged between 0 and 1
        """
        return cosine_similarity(first, second)