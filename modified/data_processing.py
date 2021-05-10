#region				-----External Imports-----
from collections import defaultdict
from pandas import DataFrame
from numpy import array
#endregion

#region				-----Internal Imports-----
from similarity.similarity import Similarity
from models.movie import Movie
#endregion

class MetaSimilarityMatrix(object):
    def _process(self, objects: "List[Object]")->"Dict[Dict[Float]]":
        """Calculates similarity between objects using metas
            objects: objects that contain meta attributes
        return processed matrix of similarity
        """
        table=defaultdict(dict)
        for first in range(0, len(objects)):
            for second in range(first, len(objects)):
                table[objects[first].id][objects[second].id]=\
                table[objects[second].id][objects[first].id]=\
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
    def get(self)->"Dataframe":
        """Calculates similarity matrix using metas\n
        return processed matrix of similarity
        """
        return DataFrame(self._table)

    def __init__(self, meta_attributes: "List[str]",
    objects: "List[Object]")->"None":
        """Initializes matrix of meta similarity
            meta_attributes: attributes to compare
            objects: objects that contain meta
        return None
        """
        self._meta_attributes=meta_attributes
        self._table=self._process(objects)

class MarkSimilarityMatrix(object):
    def _process(self, marks: "Dataframe")->"Numpy[Numpy[Float]]":
        """Calculates similarity between objects using marks
            marks: dataframe with objects ids 
            on rows and user ids on columns
        return processed matrix of similarity
        """
        return Similarity.cosine(ratings=marks)
    def get(self)->"Dataframe":
        """Calculates similarity matrix using marks\n
        return processed matrix of similarity
        """
        return DataFrame(self._marks,
        columns=self._indeces,
        index=self._indeces)

    def __init__(self, marks: "Dataframe")->"None":
        """Initializes matrix of marks similarity
            marks: dataframe with objects ids 
            on rows and user ids on columns
        return None
        """
        self._indeces=marks.index.values
        self._marks=self._process(marks)

class UserProfileStory(object):
    def _process(self, user: "Dataframe")->"Tuple[Dataframe]":
        """Divides objects into seen and not seen groups
            user: column with information about objects
        return divided groups
        """
        last=user["timestamp"].max()
        user["timestamp"]=user["timestamp"]\
            .apply(lambda item: abs(item-last))
        user=user.sort_values(by=["timestamp"])

        return (user[user["rating"]!=0],
                user[user["rating"]==0])
    def get(self)->"Tuple[Dataframe]":
        """Divides objects into two groups\n
        return divided groups
        """
        return self._seen, self._not_seen

    def __init__(self, user: "Dataframe")->"None":
        """Creates user profile story
            user: dataframe that contains objects ids
            and time when the objects were seen last
        return None
        """
        self._seen, self._not_seen=self._process(user)

class MovieCollection(object):
    def get(self)->"List[Movie]":
        """Transforms csv to Movie class collection\n
        return transformed objects
        """
        return [Movie(*parameters) for parameters
        in self._movies.itertuples(index=False)]

    def __init__(self, movies: "Dataframe")->"None":
        """Creates collection of Movie classes
            movies: dataframe that contains all
            necessary information about movies
        return None
        """
        self._movies=movies[["movieId", "overview",
        "title"]].fillna("Empty string")