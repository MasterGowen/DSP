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
from .display_utils import countdown_title

log = logging.getLogger(__name__)


def lab_3_get_source_data():
    N1 = 10
    signal_types = [
        {
            "name": "videopulse_ Barker_13",
            "title": "прямоугольный видеоимпульс амплитуды 1 с внутриимпульсной манипуляцией в соответствии с кодом (например, Баркер-13) и длиной элементарной посылки \(N_1 = {}\) {}".format(
                N1, countdown_title(N1))
        }
    ]
    signal_type = random.choice(signal_types)

    s = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]
    # s = [0.0, 0.2, 0.4, 0.6, 0.8]
    context = dict()
    context["N1"] = N1
    context["s"] = s
    context["signal_type"] = signal_type
    context["lab_id"] = "lab_3"
    context["Ku"] = 10
    return context


def get_correct_signal(source_data):
    x = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
    K = len(x)
    N1 = source_data["N1"]
    N0 = K * N1
    x2 = np.matlib.repmat(x, N1, 1)
    y = np.append(x2.flatten('F'))
    return y, K


def get_correct_filter(source_data):
    x = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
    K = len(x)
    N1 = source_data["N1"]
    N0 = K * N1
    x2 = np.matlib.repmat(x, N1, 1)
    y = np.append(x2.flatten('F'), np.zeros(N0 * 2))
    b = y[0:N0][::-1]
    return b


def lab_3_check_answer(student_data, source_data, lab_settings, correct_answer):
    student_y = student_data["student_signal"]
    student_b = student_data["student_filter"]
    student_B = float(student_data["student_B"])

    y_et, K = get_correct_signal(source_data)
    b_et = get_correct_filter(source_data)
    pass


def lab_3_get_graphic_1(student_data, source_data):
    b = student_data["student_filter"]
    N0 = len(b)
    y = np.append(student_data["student_signal"], np.zeros(N0 * 2))
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


def get_y2_s2(Ku_j, Ku_i, N0, s_st, b, K, y):
    res = dict()
    res["y2"] = [[res_y2_1 for res_y2_1 in np.zeros(Ku_j)] for res_y2_2 in np.zeros(Ku_j)]
    res["s2"] = [[res_s2_1 for res_s2_1 in np.zeros(Ku_j)] for res_s2_2 in np.zeros(Ku_j)]
    correct_s = [correct_s_1 for correct_s_1 in np.zeros(Ku_j)]
    for j in np.arange(1, Ku_j + 1):
        pp = 2 * math.sqrt(N0)
        q = 0
        for i in np.arange(1, Ku_i + 1):
            y2 = y + s_st[j - 1] * np.random.randn(1, 3 * N0)[0]
            s2 = signal.lfilter(b, 1, y2)
            res["s2"][j-1][i-1] = s2.tolist()
            res["y2"][j-1][i-1] = y2.tolist()
            w = (np.array(s2) > np.array(pp)).astype(int)
            for x in np.arange(math.floor(N0-float(K)/2)-1, math.floor(N0+float(K)/2)+3):
                w[x-1] = 0
            q = q + np.double(sum(w) > 0)
        correct_s[j-1] = float(q/Ku_i)
    return res, correct_s


def lab_3_get_graphic_2(correct_answer, student_data, source_data, reload="True", is_signal=""):

    Ku_i_max = int(source_data["Ku"])
    Ku_j_max = int(source_data["Ku"])

    b = np.array(student_data["answer"]["student_filter"])
    N0 = len(b)
    y = np.append(np.array(student_data["answer"]["student_signal"]), np.zeros(N0 * 2))
    s_st = np.array(source_data["s"])
    Ku_j = int(student_data["state"]["Ku_j"])
    Ku_i = int(student_data["state"]["Ku_i"])

    K = 13  # сделать не так

    there_is_signal_count = int(student_data["state"]["there_is_signal_count"])
    there_is_no_signal_count = int(student_data["state"]["there_is_no_signal_count"])

    if student_data["state"]["y2_s2"] is None:
        student_data["state"]["y2_s2"], correct_answer["s"] = get_y2_s2(Ku_j_max, Ku_i_max, N0, s_st, b, K, y)

    if is_signal == "there_is_signal":
        there_is_signal_count += 1
    elif is_signal == "there_is_no_signal":
        there_is_no_signal_count += 1
    else:
        pass

    if not student_data["state"]["Ku_done"]:
        student_data["state"]["there_is_signal_states"][Ku_j - 1] = {"there_is_signal_count": there_is_signal_count,
                                             "there_is_no_signal_count": there_is_no_signal_count}

    y2 = student_data["state"]["y2_s2"]["y2"][Ku_j-1][Ku_i-1]
    s2 = student_data["state"]["y2_s2"]["s2"][Ku_j-1][Ku_i-1]

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


    student_data["state"]["Ku_j"] = Ku_j
    student_data["state"]["Ku_i"] = Ku_i
    student_data["state"]["there_is_signal_count"] = there_is_signal_count
    student_data["state"]["there_is_no_signal_count"] = there_is_no_signal_count

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
    return correct_answer, student_data, graphic


def lab_3_get_graphic_3(student_data, source_data):
    v = student_data["student_s"]
    for idx, v_value in enumerate(v):
        try:
            v[idx] = float(v_value)
        except:
            v[idx] = 0
    s = np.array(source_data["s"])

    fig, ax = plt.subplots(figsize=(6, 6))
    # (markers, stemlines, baseline) =
    ax.stem(s, v, 'y')
    # ax.setp(markers, marker='D', markersize=10, markeredgecolor="orange", markeredgewidth=2)

    html = mpld3.fig_to_d3(fig)
    graphic = {
        "id": "graphic_3",
        "html": html,

    }
    return graphic