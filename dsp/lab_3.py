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
    N1 = 10
    signal_types = [
        {
            "name": "videopulse_ Barker_13",
            "title": "прямоугольный видеоимпульс амплитуды 1 с внутриимпульсной манипуляцией в соответствии с кодом (например, Баркер-13) и длиной элементарной посылки \(N_1 = {}\) отсчётов".format(N1)
        }
    ]
    signal_type = random.choice(signal_types)  # signal_types[0]  #

    context = dict()
    context["N1"] = N1
    context["signal_type"] = signal_type
    return context


def get_correct_signal(source_data):
    x = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
    K = len(x)
    N1 = source_data["N1"]
    N0 = K * N1
    x2 = np.matlib.repmat(x, N1, 1)
    y = np.append(x2.flatten('F'), np.zeros(N0 * 2))
    return y


def get_correct_filter(source_data):
    pass


def lab_3_check_answer(student_data, source_data):
    pass


def lab_3_get_graphic_1(student_data, source_data):
    y = student_data["student_signal"]
    b = student_data["student_filter"]
    N0 = len(b)

    # s_et = signal.lfilter(b_et, 1, y_et)
    S = int(np.floor(np.random.uniform(0, 1) * N0))
    y1_et = np.roll(np.roll(y, S), (-1) * S)

    ys1_et = y1_et + 0.5 * np.random.randn(1, 3 * N0)[0]
    z = signal.lfilter(b, 1, ys1_et)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(ys1_et, linewidth=2.0)
    ax.plot(z, linewidth=2.0)
    html = mpld3.fig_to_d3(fig)
    graphic = {
            "id": "graphic_1",
            "html": html
        }

    return graphic
