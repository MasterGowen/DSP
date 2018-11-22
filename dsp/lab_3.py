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

from .calc_utils import arrays_is_equal, numbers_is_equal, arrays_is_equal_by_elements, values_count_in_array
from .display_utils import countdown_title

log = logging.getLogger(__name__)


def lab_3_get_source_data(correct_answer):
    N1 = 10
    signal_types = [
        {
            "name": "videopulse_Barker_13",
            "code": [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1],
            "title": "прямоугольный видеоимпульс амплитуды 1 с внутриимпульсной манипуляцией в соответствии с кодом (Баркер-13) и длиной элементарной посылки \(N_1 = {}\) {}".format(
                N1, countdown_title(N1))
        }
    ]
    signal_type = random.choice(signal_types)

    s = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]
    K = len(signal_type["code"])
    N0 = K * N1
    S = int(np.floor(np.random.uniform(0, 1) * N0))
    Ku = 10
    correct_answer["S"] = S
    context = dict()
    context["N1"] = N1
    context["s"] = s
    context["signal_type"] = signal_type
    context["lab_id"] = "lab_3"
    context["Ku"] = Ku

    return context, correct_answer


def get_correct_signal_filter(source_data):
    if source_data["signal_type"]["name"] == "videopulse_Barker_13":
        x = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
    else:
        x = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
    K = len(x)
    N1 = source_data["N1"]
    N0 = K * N1
    x2 = np.repeat(np.array(x), N1, axis=0)
    # y_et_clean = y_et
    y_et = np.append(x2, np.zeros(N0 * 2))
    b_et = y_et[0:N0][::-1]

    return x2, b_et


def lab_3_check_answer(student_data, source_data, lab_settings, correct_answer):
    student_y = student_data["student_signal"]
    student_b = student_data["student_filter"]
    student_s = student_data["student_s"]
    student_B = float(student_data["student_B"])

    # y - сигнал
    # b - фильтр

    y_et, b_et = get_correct_signal_filter(source_data)
    B_et = int(correct_answer["S"])
    s_et = correct_answer["s"]

    max_score = 4
    score = 0
    result = dict()
    result["correctness"] = dict()
    arr_tol = float(lab_settings["array_tolerance"])
    num_tol = float(lab_settings["number_tolerance"])

    if arrays_is_equal(y_et, student_y, tolerance=arr_tol):
        result["correctness"]["signal_correctness"] = True
        score += 1
    else:
        result["correctness"]["signal_correctness"] = False
    result["correctness"]["signal_correct"] = y_et.tolist()

    if arrays_is_equal(b_et, student_b, tolerance=arr_tol):
        result["correctness"]["filter_correctness"] = True
        score += 1
    else:
        result["correctness"]["filter_correctness"] = False
    result["correctness"]["filter_correct"] = b_et.tolist()

    if numbers_is_equal(B_et, student_B, tolerance=num_tol):
        result["correctness"]["B_correctness"] = True
        score += 1
    else:
        result["correctness"]["B_correctness"] = False
    result["correctness"]["B_correct"] = float(B_et)

    s_correctnes = arrays_is_equal_by_elements(s_et, student_s, tolerance=num_tol)
    s_score = 1
    score += np.round(s_score / float(len(s_correctnes)) * values_count_in_array(s_correctnes, value=True), 1)

    for idx, val in enumerate(s_correctnes):
        result["correctness"]["s"+str(idx)+"_correctness"] = s_correctnes[idx]

    result["correctness"]["s_correct"] = s_et

    result["score"] = float(score) / float(max_score)

    return result


def lab_3_get_graphic_1(student_data, source_data, correct_answer):
    b = student_data["student_filter"]
    N0 = len(b)
    y = np.append(student_data["student_signal"], np.zeros(N0 * 2))

    S = int(correct_answer["S"])
    y1_et = np.roll(np.roll(y, S), (1) * S)  # или -1?
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

    # S = int(correct_answer["S"])
    # y1_et = np.roll(np.roll(y, S), (1) * S)  # или -1?
    # y1_et = y1_et + 0.5 * np.random.randn(1, 3 * N0)[0]  # надо ли это ???

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