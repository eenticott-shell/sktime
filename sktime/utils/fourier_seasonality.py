# -*- coding: utf-8 -*-
"""Add fourier seasonality."""
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


def make_fourier(index, order, periods):
    """Produce a matrix of fourier seasonality terms.

    Inputs
    ------
    index - TimeSeriesIndex
    order - Integer
    periods-  list of strings
    """
    X = pd.DataFrame(index=index)

    def get_multiplier(X, p):
        if p == "h":
            return X.index.hour / 24
        if p == "dow":
            return X.index.dayofweek / 7
        if p == "dom":
            return X.index.day / 30
        if p == "m":
            return X.index.month / 12
        if p == "doy":
            return X.index.dayofyear / 365.25

    for i in range(1, order + 1):
        for p in periods:
            multiplier = get_multiplier(X, p)
            X["sin_" + str(p) + str(i)] = np.sin(2 * i * np.pi * multiplier)
            X["cos_" + str(p) + str(i)] = np.cos(2 * i * np.pi * multiplier)

    return X
