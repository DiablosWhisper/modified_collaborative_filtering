#region				-----External Imports-----
from collections import defaultdict
from numpy import array, e
#endregion

#region				-----Internal Imports-----
from similarity.similarity import Similarity
from config import KSI, TETA, ALPHA, VIEWED
#endregion

class ModifiedCollaborativeFiltering(object):
    def _hybrid_similarity(self, item_similarity: "Float", 
    meta_similarity: "Float")->"Float":
        """Calculates hybrid similarity for recommendation
            item_similarity: similarity relying on ratings
            meta_similarity: similarity relying on meta
        return value ranged between 0 and 1
        """
        u, v=KSI*item_similarity, TETA*meta_similarity
        return (u+v)/(2**-(u+v-1))

class MetaSimilarityMatrix(object):
    def _process(self, objects: "List[Object]")->"Dict[Dict[Float]]":
        """Calculates similarity between objects using meta
            objects: objects that contain meta attributes
        return processed matrix of similarity
        """
        table=defaultdict(lambda: defaultdict(float))
        for first in range(0, len(objects)):
            for second in range(first, len(objects)):
                table[first][second]=table[second][first]=\
                self._compare(first=objects[first],
                second=objects[second])
        return table
    def _compare(self, first: "Object", second: "Object")->"Float":
        """Compares two objects using their metas
            first: object with appropriate metas
            second: object with appropriate metas
        return value ranged between 0 and 1
        """
        similarities=list()
        for meta_attribute in self._meta_attributes:
            similarities.append(Similarity.sentence(
                second=getattr(second, meta_attribute),
                first=getattr(first, meta_attribute)
            ))
        return array(similarities).mean()
    def get(self)->"Dict[Dict[Float]]":
        """Similarity between object i and j
            i: id of the first object
            j: id of the second object
        return value ranged between 0 and 1 
        """
        return self._table

    def __init__(self, meta_attributes: "List[str]",
    objects: "List[Object]")->"None":
        """Initializes matrix of meta similarity
            meta_attributes: attributes to compare
            objects: objects that contain meta
        return None
        """
        self._meta_attributes=meta_attributes
        self._table=self._process(objects)

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