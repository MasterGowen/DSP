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
    K = 4  # np.random.choice(np.array([2, 3, 4, 5]))
    signal_type = {
        "name": "harmonic_oscillations",
        "title": "Для гармонических колебаний (при \(f_0 = {}\) и \(f_д = {}\)) произвести компрессию частоты дискретизации в \({}\) раз путём отбрасывания отсчётов.".format(
            f0, fd, K)
    }
    context = dict()
    context["fd"] = fd
    context["f0"] = f0
    context["K"] = K
    context["signal_type"] = signal_type
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
    pass
