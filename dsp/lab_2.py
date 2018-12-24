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


def lab_2_get_source_data():
    N3 = 128
    K_1 = 4  # random.choice([2, 4, 8])
    K_2 = (N3/2-1) * 0.53413  # * np.random.rand()

    rand_number_1 = 0.9  # round(np.random.uniform(0,1,1)[0], 5)
    Nk = 2 + math.floor(8 * rand_number_1)

    rand_array = [0.19555953593700792, 0.82765677859013131, 0.62288302263001183, 0.35987965025942981,
                  0.4051999223051288, 0.089630611785237457, 0.36642628173153158, 0.55466526262884241,
                  0.75511140802148402]  # rand_array = [x for x in np.random.uniform(0, 1, Nk)]  # [50*x for x in np.random.uniform(0, 1, Nk)]
    f = np.sort([50 * x for x in rand_array])
    df = np.diff(f)
    df_tmp = np.append(df, np.repeat(999, len(f) - len(df)))
    f_tmp = np.empty((0))
    for idx, val in enumerate(df_tmp):
        if val >= 3:
            f_tmp = np.append(f_tmp, f[idx])
    f = f_tmp

    correct_answer = dict()
    correct_answer["K_1"] = K_1
    correct_answer["K_2"] = K_2
    correct_answer["f"] = f
    context = dict()
    context["N3"] = N3
    # context["N3"] = N3

    context["lab_id"] = "lab_2"

    return context, correct_answer


def lab_2_check_answer():
    pass


def lab_2_get_graphics_1(source_data, correct_answer):
    graphics = []

    K = int(correct_answer["K_1"])
    N3 = int(source_data["N3"])

    fig, ax = plt.subplots(figsize=(6, 6))
    d3 = [math.cos((math.pi * x) / 2) for x in np.arange(N3)]
    ax.plot(np.arange(N3), d3, 'y', linewidth=2.0)
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_1",
            "html": html
        }
    )
    fig, ax = plt.subplots(figsize=(6, 6))
    sp = np.abs(np.fft.fft(d3))
    ax.stem(np.arange(N3), sp, 'c')

    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_2",
            "html": html
        }
    )
    return graphics


def lab_2_get_graphics_2(source_data, correct_answer):
    graphics = []

    K = float(correct_answer["K_2"])
    N3 = int(source_data["N3"])

    fig, ax = plt.subplots(figsize=(6, 6))
    d3 = [np.exp(2j * math.pi * K * x / N3) for x in np.arange(N3)]
    ax.plot(np.arange(N3), np.real(d3), 'y', linewidth=2.0)
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_3",
            "html": html
        }
    )
    fig, ax = plt.subplots(figsize=(6, 6))
    sp = np.abs(np.fft.fft(d3))
    ax.stem(np.arange(N3), sp, 'c')
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_4",
            "html": html
        }
    )
    return graphics


def lab_2_get_graphics_3(source_data, correct_answer):
    graphics = []

    f = np.array(correct_answer["f"])
    Nk0 = len(f)
    N3 = int(source_data["N3"])

    fig, ax = plt.subplots(figsize=(6, 6))

    d9 = np.zeros(N3)

    for i in np.arange(1, Nk0 + 1):
        d9 = np.array(d9) + np.array([math.cos(2 * math.pi * f[i - 1] * x / N3) for x in np.arange(N3)])

    ax.plot(np.arange(N3), d9, 'y', linewidth=2.0)
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_5",
            "html": html
        }
    )
    fig, ax = plt.subplots(figsize=(6, 6))
    sp = np.abs(np.fft.fft(d9))
    ax.stem(np.arange(N3), sp, 'c')
    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_6",
            "html": html
        }
    )
    return graphics
