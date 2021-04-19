#region				-----External Imports-----
from numpy import square, sqrt
#endregion

class Validate(object):
    @staticmethod
    def rmse(predictions: "Numpy", real: "Numpy")->"Float":
        """Finds root mean squared error
            predictions: vector of predictions
            real: vector of real values
        return difference between them
        """
        return sqrt(square(real-predictions).mean())
    @staticmethod
    def mse(predictions: "Numpy", real: "Numpy")->"Float":
        """Finds mean squared error
            predictions: vector of predictions
            real: vector of real values
        return difference between them
        """
        return square(real-predictions).mean()