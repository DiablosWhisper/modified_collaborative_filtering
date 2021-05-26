#region				-----External Imports-----
from numpy import e
#endregion

#region				-----Internal Imports-----
import config
#endregion

class ModifiedCollaborativeFiltering(object):
    def calc_error(self, user):
        real=user[user["timestamp"]==0][["movieId", "rating"]]
        movie_ids=user[user["movieId"]!=int(real["movieId"])]
        sim=dict()
        for movieId in movie_ids["movieId"]:
            sim[movieId]=self._hybrid_similarity(
                self._marks[movieId][int(real["movieId"])],
                self._metas[movieId][int(real["movieId"])],
            )
        sim={k: v for k, v in sorted(
            sim.items(), key=lambda item: item[1], 
            reverse=True)}
        results=[]
        for i in range(6):
            chisel=0
            znam=0
            for movie_id, rank in list(sim.items())[:i+1]:
                f_t=float(decay(config.ALPHA, user[user["movieId"]==movie_id]["timestamp"]))
                rating=float(user[user["movieId"]==movie_id]["rating"])
                chisel+=rank*f_t*rating
                znam+=rank*f_t
            mark=float(chisel/znam)
            results.append(float(real["rating"])-mark)
        return results

    def _hybrid_similarity(self, mark_similarity: "Float", 
    meta_similarity: "Float")->"Float":
        """Calculates hybrid similarity for recommendation
            mark_similarity: similarity relying on ratings
            meta_similarity: similarity relying on meta
        return value ranged between 0 and 1
        """
        u, v=config.KSI*mark_similarity, config.TETA*meta_similarity
        return (u+v)/(2**(-u+v-1))
    
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
    return e**(-alpha*time)