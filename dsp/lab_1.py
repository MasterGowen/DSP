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

log = logging.getLogger(__name__)

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


def get_graphics(student_data, source_data):
    graphics = []
    log.info("!!!!!!!!!!!!!!!!!!!!!!!")
    log.info(student_data["student_filter"])
    N0 = len(student_data["student_signal"])
    d = student_data["student_signal"]  # сигнал, вводимый студентом

    Ns = len(student_data["student_filter"])
    b = student_data["student_filter"]

    a = float(student_data["a"])
    z = signal.lfilter(b, a, d)
    # fz = np.abs(np.fft.fft(z))

    fig, ax = plt.subplots(figsize=(4, 4))

    ax.stem(np.arange(N0), z)
    ax.plot(np.arange(N0), np.full((N0, 1), 0.707 * max(z)), 'r')

    # b = np.ones(9)

    w = np.hamming(Ns)

    z = signal.lfilter(w, a, d)
    ax.plot(np.arange(N0), np.full((N0, 1), 0.707 * max(z)), 'r')

    html = mpld3.fig_to_d3(fig)
    graphics.append(
        {
            "id": "graphic_1",
            "html": html
        }
    )
    # print(html)

    fz = np.abs(np.fft.fft(z))
    # mz = max(fz)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.semilogy(fz)

    html = mpld3.fig_to_d3(fig)
    # print(html)
    graphics.append(
        {
            "id": "graphic_2",
            "html": html
        }
    )
    # print(type(html))
    return graphics
