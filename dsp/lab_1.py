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


def lab_1_get_source_data():
    N0 = 100  # random.randint(10, 200)
    Q = random.randint(2, int(N0 / 3))  # 2 < Q < N0/3
    Ns = 5  # random.randint(5, 12)
    K = 12.5
    signal_types = [
        {
            "name": "delta_func",
            "title": "дискретная дельта-функция длиной \({}\) {}".format(N0, countdown_title(N0))
        },
        {
            "name": "rectangular_videopulse",
            "title": "прямоугольный видеоимпульс скважности \({}\) и длиной сигнала \({}\) {}".format(Q, N0, countdown_title(N0))
        },
        {
            "name": "rectangular_radiopulse_f4",
            "title": "прямоугольный радиоимпульс (в форме cos) скважности \({}\) и длиной сигнала \({}\) {} с частотой \(f_d/4\)".format(
                Q, N0, countdown_title(N0))
        },
        {
            "name": "rectangular_radiopulse_f2",
            "title": "прямоугольный радиоимпульс (в форме cos) скважности \({}\) и длиной сигнала \({}\) {} с частотой \(f_d/2\)".format(
                Q, N0, countdown_title(N0))
        }
    ]
    signal_type = random.choice(signal_types)  # signal_types[1]  #

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
    filter_window = random.choice(filter_windows)  # filter_windows[2]
    sum_sub = random.choice([
        {
            "name": "sum",
            "title": "сумматор"
        },
        {
            "name": "sub",
            "title": "вычитатель"
        }
    ])  # {"name": "sum", "title": "сумматор"}
    filter_type = {
        "name": "filter_" + sum_sub['name'] + "_" + filter_window["name"],
        "title": "фильтр-{} длиной \({}\) отсчётов".format(sum_sub["title"], Ns),
        "window": filter_window
    }

    context = dict()
    context["N0"] = N0
    context["Ns"] = Ns
    context["K"] = K
    context["Q"] = Q
    context["signal_type"] = signal_type
    context["filter_type"] = filter_type
    context["lab_id"] = "lab_1"
    return context


def get_correct_signal(source_data):
    N0 = source_data["N0"]
    Q = source_data["Q"]
    if source_data["signal_type"]["name"] == "delta_func":
        signal = np.append(np.ones(1), np.zeros(N0 - 1))
    elif source_data["signal_type"]["name"] == "rectangular_videopulse":
        tmp = math.floor(N0 / Q)
        signal = np.append(np.ones(tmp), np.zeros(N0 - tmp))
    elif source_data["signal_type"]["name"] == "rectangular_radiopulse_f4":
        tmp = math.floor(N0 / Q)
        tmp1 = math.ceil(float(math.ceil(float(N0) / Q)) / 4)
        tmp2 = np.tile([1, 0, -1, 0], tmp1)[0:tmp]
        signal = np.append(tmp2, np.zeros(N0 - len(tmp2)))
    elif source_data["signal_type"]["name"] == "rectangular_radiopulse_f2":
        tmp = math.floor(N0 / Q)
        tmp1 = math.ceil(float(math.ceil(float(N0) / Q)) / 2)
        tmp2 = np.tile([1, -1], tmp1)[0:tmp]
        signal = np.append(tmp2, np.zeros(N0 - len(tmp2)))
    else:
        signal = np.zeros(N0)

    return signal


def get_correct_filter(source_data):
    Ns = float(source_data["Ns"])
    if source_data["filter_type"]["name"].split("_")[1] == "sum":
        filter = np.ones(Ns)
    else:  # sub
        tmp = math.ceil(Ns / 2)
        filter = np.tile([1, -1], tmp)[0:Ns]
    return filter


def lab_1_check_answer(student_data, source_data, lab_settings):
    student_d = student_data["student_signal"]
    student_b = student_data["student_filter"]
    student_a = float(student_data["student_a"])
    student_ubl = float(student_data["student_ubl"])
    student_p = float(student_data["student_p"])

    N0 = source_data["N0"]
    K = source_data["K"]
    d_et = get_correct_signal(source_data)
    b_et = get_correct_filter(source_data)
    a_et = 1

    if source_data["filter_type"]["window"]["name"] == "hamming":
        w_et = np.hamming(len(b_et))
        z_et = signal.lfilter(b_et * w_et, a_et, d_et)
        fz_et = np.abs(np.fft.fft(z_et))
    elif source_data["filter_type"]["window"]["name"] == "blackman":  # тут написать алгоритм для Блэкмана
        w_et = np.blackman(len(b_et))
        z_et = signal.lfilter(b_et * w_et, a_et, d_et)
        fz_et = np.abs(np.fft.fft(z_et))
    else:  # прямоугольное окно
        z_et = signal.lfilter(b_et, a_et, d_et)
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

    max_score = 5
    score = 0
    result = dict()
    result["correctness"] = dict()
    arr_tol = float(lab_settings["array_tolerance"])
    num_tol = float(lab_settings["number_tolerance"])
    if arrays_is_equal(d_et, student_d, tolerance=arr_tol):
        result["correctness"]["signal_correctness"] = True
        score += 1
    else:
        result["correctness"]["signal_correctness"] = False
    result["correctness"]["signal_correct"] = d_et.tolist()

    if arrays_is_equal(b_et, student_b, tolerance=arr_tol):
        result["correctness"]["filter_correctness"] = True
        score += 1
    else:
        result["correctness"]["filter_correctness"] = False
    result["correctness"]["filter_correct"] = b_et.tolist()

    if numbers_is_equal(a_et, student_a, tolerance=num_tol):
        result["correctness"]["a_correctness"] = True
        score += 1
    else:
        result["correctness"]["a_correctness"] = False
    result["correctness"]["a_correct"] = a_et

    if numbers_is_equal(ubl_et, student_ubl, tolerance=num_tol):
        result["correctness"]["ubl_correctness"] = True
        score += 1
    else:
        result["correctness"]["ubl_correctness"] = False
    result["correctness"]["ubl_correct"] = ubl_et

    if numbers_is_equal(p_et, student_p, tolerance=num_tol):
        result["correctness"]["p_correctness"] = True
        score += 1
    else:
        result["correctness"]["p_correctness"] = False
    result["correctness"]["p_correct"] = p_et

    result["score"] = float(score) / float(max_score)

    return result


def lab_1_get_graphics(student_data, source_data):
    graphics = []
    N0 = len(student_data["student_signal"])
    d = student_data["student_signal"]  # сигнал, вводимый студентом
    b = student_data["student_filter"]  # фильтр, вводимый студентом
    a = float(student_data["student_a"])

    if source_data["filter_type"]["window"]["name"] == "hamming":
        w = np.hamming(len(b))
        z = signal.lfilter(b * w, 1, d)
        fz = np.abs(np.fft.fft(z))
    elif source_data["filter_type"]["window"]["name"] == "blackman":
        w = np.blackman(len(b))
        z = signal.lfilter(b * w, a, d)  # тут написать алгоритм для Блэкмана
        fz = np.abs(np.fft.fft(z))
    else:  # прямоугольное окно
        z = signal.lfilter(b, a, d)
        fz = np.abs(np.fft.fft(z))

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.stem(np.arange(N0), z, 'c')
    ax.plot(np.arange(N0), z, 'y', linewidth=3.0)
    ax.plot(np.arange(N0), np.ones((N0, 1)) * (0.707 * max(z)), 'r', linewidth=3.0)

    # w = np.hamming(Ns)
    # z = signal.lfilter(b*w, a, d)
    # ax.stem(np.arange(N0), z)
    # ax.plot(np.arange(N0), np.ones((N0, 1)) * (0.707 * max(z)), 'r')
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_1",
            "html": html
        }
    )
    fig, ax = plt.subplots(figsize=(6, 6))

    # if source_data["filter_type"]["window"]["name"] == "hamming":
    #     ax.semilogy(fz)
    # else:
    ax.plot(np.arange(N0), fz, 'c', linewidth=3.0)
    ax.plot(np.arange(N0), np.ones((N0, 1)) * (0.707 * max(fz)), 'r', linewidth=3.0)

    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_2",
            "html": html
        }
    )
    return graphics
