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
    signal_type = signal_types[0]  # random.choice(signal_types)  #

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

    filter_type = filter_types[0]  # random.choice(filter_types)
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
    a1 = source_data["a1"]
    filter = np.array([1, a1])
    return filter


def lab_4_check_answer(student_data, source_data):
    student_b = float(student_data["student_b"])
    student_d = student_data["student_signal"]
    student_a = student_data["student_filter"]
    student_F = float(student_data["student_F"])
    student_Dp = float(student_data["student_Dp"])
    student_filter_stable = student_data["student_filter_stable"]

    a_et = get_correct_filter(source_data)
    b_et = [1]
    d_et = get_correct_signal(source_data)
    N0 = len(d_et)

    z_et = signal.lfilter(b_et, a_et, d_et)
    fz_et = np.abs(np.fft.fft(z_et))

    f707 = [1 if x > 0.707*max(fz_et) else 0 for x in fz_et]
    F_et = N0/2 - (np.where(np.array(f707[::-1])[int(N0/2):] == 1)[0][0]+1) + 1
    mz = [1 if x > 0.05*max(abs(z_et)) else 0 for x in abs(z_et)]
    Dp_et = N0 - (np.where(np.array(f707[::-1]) == 1)[0][0]+1)

    if abs(float(source_data["a1"])) > 1:
        is_stable = "stable"
    else:
        is_stable = "unstable"

    max_score = 6
    score = 0
    result = dict()
    result["correctness"] = dict()
    if arrays_is_equal(d_et, student_d):
        result["correctness"]["signal_correctness"] = True
        score += 1
    else:
        result["correctness"]["signal_correctness"] = False
    result["correctness"]["signal_correct"] = d_et.tolist()

    if numbers_is_equal(b_et[0], student_b, tol=0.01):
        result["correctness"]["b_correctness"] = True
        score += 1
    else:
        result["correctness"]["b_correctness"] = False
    result["correctness"]["b_correct"] = float(b_et)

    if arrays_is_equal(a_et, student_a):
        result["correctness"]["filter_correctness"] = True
        score += 1
    else:
        result["correctness"]["filter_correctness"] = False
    result["correctness"]["filter_correct"] = a_et.tolist()

    if numbers_is_equal(F_et, student_F, tol=0.1):
        result["correctness"]["F_correctness"] = True
        score += 1
    else:
        result["correctness"]["F_correctness"] = False
    result["correctness"]["F_correct"] = float(F_et)

    if numbers_is_equal(Dp_et, student_Dp, tol=0.1):
        result["correctness"]["Dp_correctness"] = True
        score += 1
    else:
        result["correctness"]["Dp_correctness"] = False
    result["correctness"]["Dp_correct"] = float(Dp_et)

    if is_stable == student_filter_stable:
        result["correctness"]["filter_stable_correctness"] = True
        score += 1
    else:
        result["correctness"]["filter_stable_correctness"] = False
    result["correctness"]["filter_stable_correct"] = is_stable

    result["score"] = float(score) / float(max_score)

    return result


def lab_4_get_graphics(student_data, source_data):
    graphics = []
    N0 = len(student_data["student_signal"])
    d = student_data["student_signal"]  # сигнал, вводимый студентом
    b = np.array([float(student_data["student_b"])])
    a = student_data["student_filter"]  # фильтр, вводимый студентом

    fig, ax = plt.subplots(figsize=(6, 6))
    z = signal.lfilter(b, a, d)
    ax.plot(np.arange(N0), z, 'y', linewidth=2.0)
    ax.plot(np.arange(N0), np.ones((N0, 1)) * (0.05 * max(z)), 'r')
    ax.plot(np.arange(N0), np.ones((N0, 1)) * (-0.05 * max(z)), 'r')

    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_1",
            "html": html
        }
    )
    fig, ax = plt.subplots(figsize=(6, 6))
    fz = np.abs(np.fft.fft(z))
    plt.plot(np.arange(N0), fz, 'y', linewidth=2.0)
    plt.plot(np.arange(N0), np.ones((N0, 1)) * (0.707 * max(fz)), 'r')

    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_2",
            "html": html
        }
    )
    return graphics
