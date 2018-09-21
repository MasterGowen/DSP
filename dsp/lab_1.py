# -*- coding: utf-8 -*-
import matplotlib
import logging
import json

matplotlib.use('Agg')
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import mpld3
import random

from .calc_utils import arrays_is_equal, numbers_is_equal

log = logging.getLogger(__name__)


def get_source_data():
    N0 = 100 #random.randint(10, 200)
    Q = 2
    Ns = 5 #random.randint(5, 12)
    signal_type = random.choice([
        {
            "name": "delta_func",
            "title": "дискретная дельта-функция длиной {} отсчётов".format(N0)
        }
    ])
    filter_windows = [
        {
            "name": "hamming",
            "title": "Хэмминга"
        },
        {
            "name": "blackman",
            "title": "Блэкмана"
        },
        {
            "name": "rectangular",
            "title": "прямоугольное"
        }
    ]
    filter_type = random.choice([
        {
            "name": "filter_sum_hamming",
            "title": "фильтр-сумматор длиной {} отсчётов".format(Ns),
            "window": [x for x in filter_windows if x["name"] == "hamming"][0]
        }
    ])

    K = 12.5
    context = dict()
    context["N0"] = N0
    context["Ns"] = Ns
    context["K"] = K
    context["Q"] = Q
    context["signal_type"] = signal_type
    context["filter_type"] = filter_type
    return context


def check_answer(student_data, source_data):
    result = dict()

    N0 = source_data["N0"]
    Ns = source_data["Ns"]
    K = source_data["K"]
    Q = source_data["Q"]
    signal_type = source_data["signal_type"]
    filter_type = source_data["filter_type"]

    student_d = student_data["student_signal"]
    student_b = student_data["student_filter"]
    student_a = float(student_data["student_a"])
    student_ubl = float(student_data["student_ubl"])
    student_p = float(student_data["student_p"])

    d_et = np.append(np.ones(Q), np.zeros(N0 - Q))
    b_et = np.ones(Ns)
    a_et = 1
    w_et = np.hamming(Ns)
    z_et = signal.lfilter(w_et, 1, d_et)
    fz_et = np.abs(np.fft.fft(z_et))
    mz = max(fz_et)
    dz = np.diff(fz_et)

    dz_temp = np.multiply(dz[:-1], dz[1:])
    dz0 = [0 if d > 0 else 1 for d in dz_temp]
    mz1 = max(fz_et * np.append(dz0, np.zeros(len(fz_et) - len(dz0))))

    ubl_et = 20 * np.log10(mz1 / mz)
    i = 2
    kf = N0 / 2
    while kf > N0 / K:
        f_et = np.abs(np.fft.fft(signal.lfilter(np.ones((i)), 1, d_et)))
        z0 = [1 if d / max(f_et) < 0.707 else 0 for d in f_et]
        kf = len(np.where(np.array(z0[:int(np.floor(len(z0) / 2))]) < 1)[0]) + 1
        i = i + 1

    p_et = i - 1

    correct_answer = dict()
    correct_answer["d_et"] = d_et.tolist()
    correct_answer["b_et"] = b_et.tolist()
    correct_answer["a_et"] = a_et
    correct_answer["ubl_et"] = ubl_et
    correct_answer["p_et"] = p_et

    max_score = 7
    score = 0
    if arrays_is_equal(d_et, student_d):
        result["signal_correctness"] = True
        score += 1
    else:
        result["signal_correctness"] = False

    if arrays_is_equal(b_et, student_b):
        result["filter_correctness"] = True
        score += 1
    else:
        result["filter_correctness"] = False

    if numbers_is_equal(float(a_et), student_a, tol=0.1):
        result["a_correctness"] = True
        score += 1
    else:
        result["a_correctness"] = False

    if numbers_is_equal(float(ubl_et), student_ubl, tol=0.1):
        result["ubl_correctness"] = True
        score += 1
    else:
        result["ubl_correctness"] = False

    if numbers_is_equal(float(p_et), student_p, tol=0.1):
        result["p_correctness"] = True
        score += 1
    else:
        result["p_correctness"] = False

    result["success"] = True
    result["score"] = max_score/score
    result["answer"] = correct_answer
    return result


def get_graphics(student_data, source_data):
    graphics = []
    # log.info("!!!!!!!!!!!!!!!!!!!!!!!")
    # log.info(student_data["student_filter"])
    N0 = len(student_data["student_signal"])
    d = student_data["student_signal"]  # сигнал, вводимый студентом
    Ns = len(student_data["student_filter"])
    b = student_data["student_filter"]
    a = float(student_data["student_a"])
    z = signal.lfilter(b, a, d)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.stem(np.arange(N0), z)
    ax.plot(np.arange(N0), np.ones((N0, 1))*(0.707 * max(z)), 'r')
    w = np.hamming(Ns)
    z = signal.lfilter(w, a, d)
    ax.stem(np.arange(N0), z)
    ax.plot(np.arange(N0), np.ones((N0, 1))*(0.707 * max(z)), 'r')
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_1",
            "html": html
        }
    )
    fz = np.abs(np.fft.fft(z))
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.semilogy(fz)
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_2",
            "html": html
        }
    )
    return graphics
