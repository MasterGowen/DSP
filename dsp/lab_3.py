# -*- coding: utf-8 -*-
import matplotlib
import logging
import json
import math

matplotlib.use('Agg')
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import mpld3
import random

from .calc_utils import arrays_is_equal, numbers_is_equal

log = logging.getLogger(__name__)


def lab_3_get_source_data():
    N0 = 100  # random.randint(10, 200)  # должно делится на 4 б/о
    a1 = random.choice([random.randint(1, 10), np.round(np.random.uniform(0.01, 1), decimals=2)])
    signal_types = [
        {
            "name": "delta_func",
            "title": "дискретная дельта-функция длиной \({}\) отсчётов".format(N0)
        },
        {
            "name": "constant",
            "title": "постоянный сигнал длиной \({}\) отсчётов".format(N0)
        },
        {
            "name": "harmonic_f4",
            "title": "гармоническое колебание длиной \({}\) отсчётов (в форме cos) с частотой \(f_d/4\)".format(N0)
        },
        {
            "name": "harmonic_f2",
            "title": "гармоническое колебание длиной \({}\) отсчётов (в форме cos) с частотой \(f_d/2\)".format(N0)
        }
    ]
    signal_type = random.choice(signal_types)  # signal_types[0]  #

    filter_types = [
        {
            "name": "nch_filter",
            "title": "устойчивый НЧ-фильтр I порядка (накопитель) с коэффициентом знаменателя передаточной функции \(a_1 = {}\) и полосой пропускания по уровню -3 дБ, равной \(F_s\). Этот фильтр имеет передаточную характеристику вида \(H(z) = \\".format(a1) + "frac{1}{1 + a_1 z^{-1}} \)",
        },
        {
            "name": "vch_filter",
            "title": "устойчивый ВЧ-фильтр I порядка (рециркулятор) с коэффициентом знаменателя передаточной функции \(a_1 = -{}\) и полосой пропускания по уровню -3 дБ, равной \(F_s\). Этот фильтр имеет передаточную характеристику вида \(H(z) = \\".format(a1) + "frac{1}{1 - a_1 z^{-1}} \)",
        }
        # ,{
        #     "name": "band_filter",
        #     "title": "Полосовой фильтр"
        # }
    ]

    filter_type = random.choice(filter_types)  # filter_types[0]  #
    context = dict()
    context["N0"] = N0
    context["a1"] = a1
    context["signal_type"] = signal_type
    context["filter_type"] = filter_type
    return context


def get_correct_signal(source_data):
    N0 = source_data["N0"]
    if source_data["signal_type"]["name"] == "delta_func":
        signal = np.append(np.ones(1), np.zeros(N0 - 1))
    elif source_data["signal_type"]["name"] == "constant":
        signal = np.ones(N0)
    elif source_data["signal_type"]["name"] == "harmonic_f4":
        signal = np.tile([1, 0, -1, 0], int(N0 / 4))
    elif source_data["signal_type"]["name"] == "harmonic_f2":
        signal = np.tile([1, -1], int(N0 / 2))
    else:
        signal = np.append(np.ones(1), np.zeros(N0 - 1))
    return signal


def get_correct_filter(source_data):
    a1 = float(source_data["a1"])
    if source_data["filter_type"]["name"] == "nch_filter":
        a1 = a1
    elif source_data["filter_type"]["name"] == "vch_filter":
        a1 = (-1) * a1
    else:
        a1 = a1
    filter = np.array([1, a1])
    return filter


def lab_3_check_answer(student_data, source_data):
    pass


def lab_3_get_graphics(student_data, source_data):
    pass
