# -*- coding: utf-8 -*-
import random
import matplotlib
import logging
import string
import json
import math

matplotlib.use('Agg')
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import mpld3
import random

from .calc_utils import arrays_is_equal, numbers_is_equal
from .display_utils import time_title

log = logging.getLogger(__name__)


def lab_5_get_source_data():
    rand_1 = 0.82038
    rand_2 = 0.413
    rand_3 = 0.04766
    rand_4 = [0.33308, 0.81950, 0.68199, 0.52076, 0.90551, 0.28840, 0.63247, 0.11402, 0.88244, 0.82465]
    rand_5 = 0.28217  # np.random.rand()
    rand_6 = 0.78565  # np.random.rand()
    rand_7 = 0.45263
    rand_8 = 0.87775

    N0 = 1000

    f0 = 200 + np.floor(250 * rand_1)  # np.random.rand()
    fm = np.floor(50 * rand_2)  # np.random.rand()
    m = 0.2 + 0.8 * rand_3  # np.random.rand()

    code = (np.array(rand_4) > 0.5).astype(int)
    f0Part2 = 5 + np.floor(5 * rand_5)
    f02Part2 = 2 * (5 + np.floor(5 * rand_5))
    NePart2 = 1 + np.floor(9 * rand_6)

    f0Part3 = 5 + np.floor(5 * rand_7) # np.random.rand()
    NePart3 = 1 + np.floor(9 * rand_8) # np.random.rand()

    shift_keying_types = [{
            "name": "amplitude_shift",
            "title": "амплитудной"
        },
        {
            "name": "frequency_shift",
            "title": "частотной"
        },
        {
            "name": "phase_shift",
            "title": "фазовой"
        }
    ]
    shift_keying_type = random.choice(shift_keying_types)

    soob = ''.join([s for s in random.sample(string.ascii_uppercase, 5)])

    correct_answer = dict()
    correct_answer["f0"] = f0
    correct_answer["fm"] = fm
    correct_answer["m"] = m
    correct_answer["soob"] = soob

    context = dict()
    context["N0"] = N0
    context["shift_keying_type"] = shift_keying_type
    context["code"] = code.tolist()
    context["f0Part2"] = f0Part2
    context["f02Part2"] = f02Part2
    context["NePart2"] = NePart2

    context["f0Part3"] = f0Part3
    context["NePart3"] = NePart3

    context["lab_id"] = "lab_7"

    return context, correct_answer

def lab_7_check_answer(student_data, source_data, lab_settings, correct_answer):
    pass

def lab_7_get_graphic_1(student_data, source_data, correct_answer):
    pass


def lab_7_get_graphic_2(student_data, source_data, correct_answer):
    pass


def lab_7_get_graphic_3(student_data, source_data, correct_answer):
    pass


def lab_7_get_graphic_4(student_data, source_data, correct_answer):
    pass