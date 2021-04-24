#region				-----External Imports-----
from numpy import e
#endregion

#region				-----Internal Imports-----
from config import KSI, TETA, ALPHA, VIEWED
#endregion

class ModifiedCollaborativeFiltering(object):
    def recommend(self, user: "User")->"Dict[Int, Float]":
        """
        """
        return
    def _hybrid_similarity(self, mark_similarity: "Float", 
    meta_similarity: "Float")->"Float":
        """Calculates hybrid similarity for recommendation
            mark_similarity: similarity relying on ratings
            meta_similarity: similarity relying on meta
        return value ranged between 0 and 1
        """
        u, v=KSI*mark_similarity, TETA*meta_similarity
        return (u+v)/(2**-(u+v-1))
    
    def __init__(self, marks: "Dataframe", 
    metas: "Dataframe")->"None":
        """Saves matrices of different similarities
            marks: matrix of objects marks similarity
            metas: matrix of objects metas similarity
        return None
        """
        self._marks, self._metas=marks, metas

def decay(alpha: "Float", time: "Int")->"Float":
    """Calculates how the element is old
        alpha: decay speed coefficient
        time: time of element creation
    return time weight coefficient
    """
    if not (0<=alpha<=1 or time>=0):
        raise ValueError("""
            Alpha or time value is incorrect
            Check the correction of inputs
        """)
    return e**(-alpha*t)