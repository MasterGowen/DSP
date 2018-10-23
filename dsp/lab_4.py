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
    pass


def get_correct_filter(source_data):
    pass


def lab_4_check_answer(student_data, source_data):
    pass


def lab_4_get_graphics(student_data, source_data):
    graphics = []
    N0 = len(student_data["student_signal"])
    d = student_data["student_signal"]  # сигнал, вводимый студентом
    b = student_data["student_b"]
    a = student_data["student_filter"]  # фильтр, вводимый студентом

    fig, ax = plt.subplots(figsize=(6, 6))
    z = signal.lfilter(b, a, d)
    ax.plot(np.arange(N0), z, 'y', linewidth=2.0)
    ax.plot(np.arange(N0), np.full((N0, 1), 0.05 * max(z)), 'r')
    ax.plot(np.arange(N0), np.full((N0, 1), -0.05 * max(z)), 'r')

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
    plt.plot(np.arange(N0), np.full((N0, 1), 0.707 * max(fz)), 'r')

    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_2",
            "html": html
        }
    )
    return graphics
