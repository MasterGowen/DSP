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


def lab_5_get_source_data():
    fd = 100
    f0 = 23  # np.floor(50*np.random.uniform(0, 1)) 5...48
    K1 = 4  # np.random.choice(np.array([2, 3, 4, 5]))
    K2 = 6
    signal_type_1 = {
        "name": "harmonic_oscillations",
        "title": "Для гармонических колебаний (при \(f_0 = {}\) и \(f_д = {}\)) произвести компрессию частоты дискретизации в \({}\) раз путём отбрасывания отсчётов.".format(
            f0, fd, K1)
    }
    T = 10
    fe = 0
    fs = 20
    signal_type_2 = {
        "name": "lchm_signal",
        "title": "Сигнал с ЛЧМ с параметрами \(T = {}\),\(f_e = {}\),\(f_s = {}\), амплитуда = 1".format(T, fe, fs)
    }

    K_1 = 2
    K_2 = 5

    s2 = signal.lfilter(np.array([1, 1, 1]) / 3, [1, -0.85], np.random.randn(250))
    s31 = s2[0::2]
    s32 = s2[0::5]
    s33 = signal.decimate(s2, 2, ftype='fir')
    s34 = signal.decimate(s2, 5, ftype='fir')

    s41 = signal.resample_poly(s31, 2, 1)
    s42 = signal.resample_poly(s32, 5, 1)
    s43 = signal.resample_poly(s33, 2, 1)
    s44 = signal.resample_poly(s34, 5, 1)

    context = dict()
    context["fd"] = fd
    context["f0"] = f0
    context["T"] = T
    context["fe"] = fe
    context["fs"] = fs
    context["K1"] = K1
    context["K2"] = K2
    context["s2"] = s2

    context["K_1"] = K_1
    context["K_2"] = K_2

    context["s41"] = s41
    context["s42"] = s42
    context["s43"] = s43
    context["s44"] = s44

    context["signal_type_1"] = signal_type_1
    context["signal_type_2"] = signal_type_2
    return context


def get_correct_signal(source_data):
    pass


def get_correct_filter(source_data):
    pass


def lab_5_check_answer(student_data, source_data):
    pass


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
