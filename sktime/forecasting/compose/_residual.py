#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)

"""Composition functionality for reduction approaches to forecasting."""

__author__ = ["eenticott-shell"]

from forecasting.base._base import BaseForecaster


class ResidualForecaster(BaseForecaster):
    """Residual forecaster.

    Inputs
    ------
    point_forecaster: forecaster, initialised
    residual_forecaster: forecaster, initialised
    method: str, "in_sample" or "rolling".

    """

    def __init__(
        self,
        point_forecaster,
        residual_forecaster,
        method="in_sample",
        residuals="squared",
    ):
        self.point_forecaster = point_forecaster
        self.residual_forecaster = residual_forecaster
        self.method = method

        # TODO: Checks on estimators

        super().__init__()

    _tags = {
        "capability:pred_int": True,
    }

    def _fit(self, y, X, fh):
        self.point_forecaster.fit(y, X, fh)

        if self.method == "in_sample":
            res = self.point_forecaster.predict_residuals()
            self.residual_forecaster.fit(res, X, fh)

        return self

    def _update(self, y, X, update_params):
        self.point_forecaster.update(y, X, update_params)
        if self.method == "in_sample":
            self.residual_forecaster.update(y, X, update_params)

    def _predict(self, fh, X):
        self.point_forecaster.predict(fh, X)

    def _predict_var(self, fh, X):
        self.residual_forecaster.predict(fh, X)

    def _update_predict(
        self,
        y,
        cv,
        X=None,
        update_params=True,
        reset_forecaster=True,
    ):

        super(self.point_forecaster).update_predict(
            y, cv, X, update_params, reset_forecaster
        )
