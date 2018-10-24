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


def lab_3_get_source_data():
    N1 = 10
    signal_types = [
        {
            "name": "videopulse_ Barker_13",
            "title": "прямоугольный видеоимпульс амплитуды 1 с внутриимпульсной манипуляцией в соответствии с кодом (например, Баркер-13) и длиной элементарной посылки \(N1 = {}\) отсчётов".format(N1)
        }
    ]
    signal_type = random.choice(signal_types)  # signal_types[0]  #

    context = dict()
    context["N1"] = N1
    context["signal_type"] = signal_type
    return context


def get_correct_signal(source_data):
    pass


def get_correct_filter(source_data):
    pass

def lab_3_check_answer(student_data, source_data):
    pass


def lab_3_get_graphic_1(student_data, source_data):
    pass
