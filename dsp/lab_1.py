# -*- coding: utf-8 -*-

import numpy as np
from scipy import signal
# import matplotlib.pyplot as plt
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
