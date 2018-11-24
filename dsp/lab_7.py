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


def lab_7_get_source_data():
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
    d1 = (1 + m * np.cos(2 * math.pi * fm * np.arange(0, N0) / N0)) * (np.cos(2 * math.pi * f0 * np.arange(0, N0) / N0))
    fft_d1 = np.abs(np.fft.fft(d1))

    code = (np.array(rand_4) > 0.5).astype(int)
    f0Part2 = int(5 + np.floor(5 * rand_5))
    f02Part2 = int(2 * (5 + np.floor(5 * rand_5)))
    NePart2 = int(1 + np.floor(9 * rand_6))

    soob = ''.join([s for s in random.sample(string.ascii_uppercase, 5)])
    f0Part3 = 5 + np.floor(5 * rand_7)  # np.random.rand()
    NePart3 = 1 + np.floor(9 * rand_8)  # np.random.rand()

    code_tmp = ''.join("0" + format(ord(x), 'b') for x in soob)  # разобраться с ноликом в начале
    L_tmp = len(code_tmp)
    N1 = int(4 * f0Part3 * NePart3)
    S1 = np.repeat(np.array([ord(x) for x in code_tmp]), np.int(N1), axis=0) - 48
    S1p = (2 * (S1 - 0.5)) * np.cos(2 * math.pi * f0Part3 * np.arange(0, L_tmp * N1) / N1) + (0.5 * np.random.randn(np.int(N1 * L_tmp)))
    S10 = np.cos(2 * math.pi * f0Part3 * np.arange(0, L_tmp * N1) / N1)
    SD = S1p * S10

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

    correct_answer = dict()
    correct_answer["f0"] = f0
    correct_answer["fm"] = fm
    correct_answer["m"] = m
    correct_answer["d1"] = d1.tolist()
    correct_answer["fft_d1"] = fft_d1.tolist()

    correct_answer["soob"] = soob
    correct_answer["S1p"] = S1p.tolist()
    correct_answer["SD"] = SD.tolist()
    correct_answer["N1"] = N1

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


def lab_7_get_graphic_1(source_data, correct_answer):
    graphics = []
    N0 = source_data["N0"]
    # f0 = correct_answer["f0"]
    # fm = correct_answer["fm"]
    d1 = correct_answer["d1"]
    fft_d1 = correct_answer["fft_d1"]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(np.arange(N0), d1)

    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_1_1",
            "html": html
        }
    )

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.stem(np.arange(N0), fft_d1, 'c')
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_1_2",
            "html": html
        }
    )
    return graphics


def lab_7_get_graphic_2(student_data):
    student_sm = student_data["student_Sm"]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(student_sm, linewidth=2.0)
    html = mpld3.fig_to_d3(fig)
    graphic = {
        "id": "graphic_2",
        "html": html
    }
    return graphic


def lab_7_get_graphic_3(source_data, correct_answer):
    graphics = []
    N1 = int(correct_answer["N1"])
    S1p = correct_answer["S1p"]
    SD = correct_answer["SD"]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(np.arange(0, N1*8), S1p[0:np.int(N1*8)])

    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_3_1",
            "html": html
        }
    )

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(np.arange(0, N1 * 8), SD[0:np.int(N1*8)])
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_3_2",
            "html": html
        }
    )
    return graphics


def lab_7_get_graphic_4(student_data, correct_answer):
    graphics = []
    b_st = np.array(student_data["student_b"])
    a_st = np.array(student_data["student_a"])
    SD = np.array(correct_answer["SD"])
    N1 = int(correct_answer["N1"])

    z = signal.lfilter(b_st, a_st, SD)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(np.arange(0, np.int(N1*8)), z[0:np.int(N1*8)])
    ax.stem(np.arange(N1/2, N1*8, N1), np.take(z, np.arange(np.int(N1/2), np.int(N1*8), np.int(N1))), 'r', linewidth=3.0)

    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_4_1",
            "html": html,
        }
    )
    return graphics