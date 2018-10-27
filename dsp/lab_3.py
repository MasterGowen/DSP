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
            "title": "прямоугольный видеоимпульс амплитуды 1 с внутриимпульсной манипуляцией в соответствии с кодом (например, Баркер-13) и длиной элементарной посылки \(N_1 = {}\) отсчётов".format(
                N1)
        }
    ]
    signal_type = random.choice(signal_types)  # signal_types[0]  #

    s = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]
    # s = [0.0, 0.2, 0.4, 0.6, 0.8]

    context = dict()
    context["N1"] = N1
    context["s"] = s
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


def lab_3_get_graphic_2(student_data, source_data, reload="True", is_signal=""):
    y2 = []
    s2 = []
    Ku_i_max = len(source_data["s"])
    Ku_j_max = len(source_data["s"])
    y = np.array(student_data["answer"]["student_signal"])
    b = np.array(student_data["answer"]["student_filter"])
    N0 = len(b)
    s_st = np.array(source_data["s"])
    Ku_j = int(student_data["state"]["Ku_j"])
    Ku_i = int(student_data["state"]["Ku_i"])

    there_is_signal_count = int(student_data["state"]["there_is_signal_count"])
    there_is_no_signal_count = int(student_data["state"]["there_is_no_signal_count"])

    if is_signal == "there_is_signal":
        there_is_signal_count += 1
    elif is_signal == "there_is_no_signal":
        there_is_no_signal_count += 1
    else:
        pass

    if not student_data["state"]["Ku_done"]:
        student_data["state"]["there_is_signal_states"][Ku_j - 1] = {"there_is_signal_count": there_is_signal_count,
                                             "there_is_no_signal_count": there_is_no_signal_count}

    if not reload:
        if Ku_i == Ku_i_max:
            if Ku_j == Ku_j_max:
                student_data["state"]["Ku_done"] = True
            else:
                Ku_j += 1
                Ku_i = 1
            there_is_signal_count = 0
            there_is_no_signal_count = 0
        else:
            Ku_i += 1

    for j in np.arange(1, Ku_j + 1):
        for i in np.arange(1, Ku_i + 1):
            y2 = y + s_st[j - 1] * np.random.randn(1, 3 * N0)[0]
            s2 = signal.lfilter(b, 1, y2)

    student_data["state"]["Ku_j"] = Ku_j
    student_data["state"]["Ku_i"] = Ku_i
    student_data["state"]["there_is_signal_count"] = there_is_signal_count
    student_data["state"]["there_is_no_signal_count"] = there_is_no_signal_count


    # student_data["state"]["Ku_j_current"] = Ku_j
    # student_data["state"]["Ku_i_current"] = Ku_i

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(y2, linewidth=2.0)
    ax.plot(s2, linewidth=2.0)
    # ax.plot(np.arange(len(y)), np.full((len(y), 1), 0.707 * max(s2)), 'r')
    ax.plot(np.arange(len(y)), np.ones((len(y), 1)) * (0.707 * max(s2)), 'r')

    html = mpld3.fig_to_d3(fig)
    graphic = {
        "id": "graphic_2",
        "html": html
    }
    return student_data, graphic


def lab_3_get_graphic_3(student_data, source_data):
    s = np.array(source_data["s"])
    v = student_data["student_s"]
    fig, ax = plt.subplots(figsize=(6, 6))
    # (markers, stemlines, baseline) =
    ax.stem(s, v, 'y')
    # ax.setp(markers, marker='D', markersize=10, markeredgecolor="orange", markeredgewidth=2)

    html = mpld3.fig_to_d3(fig)
    graphic = {
        "id": "graphic_3",
        "html": html
    }
    return graphic