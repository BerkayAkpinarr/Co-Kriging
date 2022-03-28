import numpy as np
import pandas as pd


def calculate_md(prediction, observation):
    observation_mean = observation.mean()
    sum_pay = 0
    sum_payda = 0
    for P, O in np.nditer([prediction, observation]):
        pay = np.abs((O - P))
        difference_p_i = np.abs(P - observation_mean)
        difference_o_i = np.abs(O - observation_mean)
        payda = (difference_p_i + difference_o_i)
        sum_pay = sum_pay + pay
        sum_payda = sum_payda + payda
    md = 1 - (sum_pay/sum_payda)
    return md


def calculate_nrmse(prediction, observation):
    observation_mean = observation.mean()
    observation_max = observation.max()
    observation_min = observation.min()

    sum_pay = 0
    sum_payda = 0
    count = 0
    for O, P in np.nditer([observation, prediction]):
        count = count + 1
        pay = np.square(P - O)
        sum_pay = sum_pay + pay

    nRMSE = (np.sqrt(sum_pay/count)) / (observation_max-observation_min)
    return nRMSE


def calculate_kge(prediction, observation):
    alpha = np.corrcoef(prediction, observation)[0, 1]

    mean_observation = observation.mean()
    mean_prediction = prediction.mean()
    bias_ratio = (mean_prediction/mean_observation)

    variability_ratio = (np.cov(prediction) / np.cov(observation))
    kge = 1 - np.sqrt(np.square(alpha-1) + np.square(bias_ratio-1) + np.square(variability_ratio-1))
    return kge
