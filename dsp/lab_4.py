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


def lab_4_get_source_data():
    N0 = 100  # random.randint(10, 200)  # должно делится на 4 б/о
    signal_types = [
        {
            "name": "delta_func",
            "title": "дискретная дельта-функция длиной \({}\) отсчётов".format(N0)
        },
        {
            "name": "constant",
            "title": "постоянный сигнал длиной \({}\) отсчётов".format(Q)
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
    signal_type = random.choice(signal_types)  # signal_types[1]  #


    context = dict()
    context["N0"] = N0
    context["signal_type"] = signal_type
    return context


def get_correct_signal(source_data):
    pass


def get_correct_filter(source_data):
    pass


def lab_4_check_answer(student_data, source_data):
    pass


def lab_4_get_graphics(student_data, source_data):
    pass
