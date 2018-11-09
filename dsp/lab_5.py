# -*- coding: utf-8 -*-
import random
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
from .display_utils import time_title, countdown_title

log = logging.getLogger(__name__)


def lab_5_get_source_data():
    fd = 100
    f0 = 23  # np.floor(50*np.random.uniform(0, 1)) 5...48
    K1 = 3  # random.choice([2, 3, 4, 5])  #
    K2 = 6
    signal_type_1 = {
        "name": "harmonic_oscillations",
        "title": "Для гармонических колебаний (при \(f_0 = {}\) и \(f_д = {}\)) произвести компрессию частоты дискретизации в \({}\) {} путём отбрасывания отсчётов.".format(
            f0, fd, K1, time_title(K1))
    }
    T = 10
    fe = 0
    fs = 20
    signal_type_2 = {
        "name": "lchm_signal",
        "title": "Сигнал с ЛЧМ с параметрами \(T = {}\), \(f_e = {}\), \(f_s = {}\), амплитуда = 1".format(T, fe, fs)
    }

    K_1 = 2  # np.random.choice(np.array([2, 3, 4, 5]))
    K_2 = 5  # np.random.choice(np.array([2, 3, 4, 5]))

    s2 = signal.lfilter(np.array([1, 1, 1]) / float(3), [1, -0.85], np.random.randn(250))
    s31 = s2[0::K_1]
    s32 = s2[0::K_2]
    s33 = signal.decimate(s2, K_1, ftype='fir')
    s34 = signal.decimate(s2, K_2, ftype='fir')

    s41 = signal.resample(s31, len(s31) * K_1)
    s42 = signal.resample(s32, len(s32) * K_2)
    s43 = signal.resample(s33, len(s33) * K_1)
    s44 = signal.resample(s34, len(s34) * K_2)

    context = dict()
    context["fd"] = fd
    context["f0"] = f0
    context["T"] = T
    context["fe"] = fe
    context["fs"] = fs
    context["K1"] = K1
    context["K2"] = K2
    context["K_1"] = K_1
    context["K_2"] = K_2
    context["s2"] = s2.tolist()
    context["s41"] = s41.tolist()
    context["s42"] = s42.tolist()
    context["s43"] = s43.tolist()
    context["s44"] = s44.tolist()

    context["signal_type_1"] = signal_type_1
    context["signal_type_2"] = signal_type_2
    return context


def get_correct_signals_1(source_data):
    K = float(source_data["K1"])
    f0 = float(source_data["f0"])
    fd = float(source_data["fd"])

    s = np.cos(2 * math.pi * f0 * (np.arange(fd)) / fd)
    s1 = s[0::K]

    return s, s1


def get_correct_signals_2(source_data):
    T = float(source_data["T"])
    fs = float(source_data["fs"])
    K = float(source_data["K2"])
    sl = signal.chirp(np.arange(0.01, T + 0.01, 0.01), 0, T, fs)
    slc = sl[0::K]

    return sl, slc


def lab_5_check_answer(student_data, source_data):
    student_s = student_data["student_s"]
    student_s1 = student_data["student_s1"]
    student_fn = float(student_data["student_fn"])
    student_sl = student_data["student_sl"]
    student_slc = student_data["student_slc"]
    student_Np = float(student_data["student_Np"])

    student_K1 = float(student_data["student_K1"])
    student_K2 = float(student_data["student_K2"])
    student_K3 = float(student_data["student_K3"])
    student_K4 = float(student_data["student_K4"])

    T = float(source_data["T"])
    fs = float(source_data["fs"])
    K = float(source_data["K2"])
    fd = float(source_data["fd"])
    s2 = np.array(source_data["s2"])
    s41 = np.array(source_data["s41"])
    s42 = np.array(source_data["s42"])
    s43 = np.array(source_data["s43"])
    s44 = np.array(source_data["s44"])

    s_et, s1_et = get_correct_signals_1(source_data)
    log.info(abs(np.fft.fft(s1_et)))
    m1_et, mi_et = abs(np.fft.fft(s1_et)).max(0), np.argmax(abs(np.fft.fft(s1_et))) + 1
    log.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!???????????????????????????")
    log.info(np.__version__)
    fn_et = fd * mi_et / len(s1_et)

    sl_et, slc_et = get_correct_signals_2(source_data)
    Np_et = math.pow(100, 2.0) / math.pow(K, 2) * T / fs

    K1_et = np.std(s2 - s41)
    K2_et = np.std(s2 - s42)
    K3_et = np.std(s2 - s43)
    K4_et = np.std(s2 - s44)

    max_score = 10
    score = 0
    result = dict()
    result["correctness"] = dict()
    if arrays_is_equal(s_et, student_s):
        result["correctness"]["s_correctness"] = True
        score += 1
    else:
        result["correctness"]["s_correctness"] = False
    result["correctness"]["s_correct"] = s_et.tolist()

    if arrays_is_equal(s1_et, student_s1):
        result["correctness"]["s1_correctness"] = True
        score += 1
    else:
        result["correctness"]["s1_correctness"] = False
    result["correctness"]["s1_correct"] = s1_et.tolist()

    if numbers_is_equal(fn_et, student_fn, tol=0.05):
        result["correctness"]["fn_et_correctness"] = True
        score += 1
    else:
        result["correctness"]["fn_et_correctness"] = False
    result["correctness"]["fn_et_correct"] = float(fn_et)

    if arrays_is_equal(sl_et, student_sl):
        result["correctness"]["sl_correctness"] = True
        score += 1
    else:
        result["correctness"]["sl_correctness"] = False
    result["correctness"]["sl_correct"] = sl_et.tolist()

    if arrays_is_equal(slc_et, student_slc):
        result["correctness"]["slc_correctness"] = True
        score += 1
    else:
        result["correctness"]["slc_correctness"] = False
    result["correctness"]["slc_correct"] = slc_et.tolist()

    if numbers_is_equal(Np_et, student_Np, tol=0.05):
        result["correctness"]["Np_correctness"] = True
        score += 1
    else:
        result["correctness"]["Np_correctness"] = False
    result["correctness"]["Np_correct"] = float(Np_et)

    if numbers_is_equal(K1_et, student_K1, tol=0.05):
        result["correctness"]["K1_correctness"] = True
        score += 1
    else:
        result["correctness"]["K1_correctness"] = False
    result["correctness"]["K1_correct"] = float(K1_et)

    if numbers_is_equal(K2_et, student_K2, tol=0.05):
        result["correctness"]["K2_correctness"] = True
        score += 1
    else:
        result["correctness"]["K2_correctness"] = False
    result["correctness"]["K2_correct"] = float(K2_et)

    if numbers_is_equal(K3_et, student_K3, tol=0.05):
        result["correctness"]["K3_correctness"] = True
        score += 1
    else:
        result["correctness"]["K3_correctness"] = False
    result["correctness"]["K3_correct"] = float(K3_et)

    if numbers_is_equal(K4_et, student_K4, tol=0.05):
        result["correctness"]["K4_correctness"] = True
        score += 1
    else:
        result["correctness"]["K4_correctness"] = False
    result["correctness"]["K4_correct"] = float(K4_et)

    result["score"] = float(score) / float(max_score)

    return result


def lab_5_get_graphic_1(student_data, source_data):
    graphics = []
    s = student_data["student_s"]
    s1 = student_data["student_s1"]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.stem(abs(np.fft.fft(s)))
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_1",
            "html": html
        }
    )
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.stem(abs(np.fft.fft(s1)))
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_2",
            "html": html
        }
    )
    return graphics


def lab_5_get_graphic_2(student_data, source_data):
    graphics = []
    sl = np.array(student_data["student_sl"])
    slc = np.array(student_data["student_slc"])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(sl)
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_3",
            "html": html
        }
    )
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(slc)
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_4",
            "html": html
        }
    )
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(np.fft.fft(sl))
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_5",
            "html": html
        }
    )
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(np.fft.fft(slc))
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_6",
            "html": html
        }
    )

    return graphics
