# -*- coding: utf-8 -*-

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import mpld3
import random


def get_source_data():
    N0 = random.randint(10, 200)
    Ns = random.randint(5, 12)
    a = 1
    signal_type = random.choice([
        {
            "name": "signal type name example",
            "title": "signal type title example"
        }
    ])
    filter_type = random.choice([
        {
            "name": "filter type name example",
            "title": "filter type title example"
        }
    ])
    filter_window = random.choice([
        {
            "name": "hamming",
            "title": "окно Хэмминга"
        },
        {
            "name": "blackman",
            "title": "окно Блэкмана"
        },
        {
            "name": "rectangular",
            "title": "прямоугольное окно"
        }
    ])
    context = dict()
    context["N0"] = N0
    context["Ns"] = Ns
    context["a"] = a
    context["signal_type"] = signal_type
    context["filter_type"] = filter_type
    context["filter_window"] = filter_window

    return context


def get_graphics():
    N0 = 100

    d = np.append([1, 1], np.zeros(N0 - 2))  # сигнал, вводимый студентом
    d_et = np.append([1, 1], np.zeros(N0 - 2))  # эталонный сигнал

    Ns = 5
    b = np.ones(Ns)
    b_et = np.ones(Ns)

    z = signal.lfilter(b, 1, d)
    z_et = signal.lfilter(b_et, 1, d_et)

    fz = np.abs(np.fft.fft(z))

    fig, ax = plt.subplots()

    ax.stem(np.arange(N0), z)
    ax.plot(np.arange(N0), z_et)
    ax.plot(np.arange(N0), np.full((N0, 1), 0.707 * max(z)), 'r')

    html = mpld3.fig_to_d3(fig)
    # print(type(html))
    return {"html": html}
