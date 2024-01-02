import numpy as np

def RMSE(modeled, observed):
    """

    Parameters
    ----------
    modeled : numpy 1d array of modeled WSE at reference points.
    observed : numpy 1d array of the observed WSE at reference points.

    Returns
    -------
    scalar RMSE value

    """
    err = modeled - observed
    err_sqr = err ** 2
    RMSE = np.sqrt(err_sqr.mean())

    return RMSE