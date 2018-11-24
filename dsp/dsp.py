# -*- coding: utf-8 -*-
import datetime
import logging
import json
import traceback
import sys
import pytz

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String, JSONField, Float, Boolean
from xblock.fragment import Fragment
from webob.response import Response
from django.http import JsonResponse

from xmodule.util.duedate import get_extended_due_date

from .utils import (
    render_template,
    load_resources,
    load_resource
)

from .calc_utils import merge_two_dicts

from lab_1 import lab_1_get_source_data, lab_1_get_graphics, lab_1_check_answer

from lab_3 import lab_3_get_source_data, lab_3_get_graphic_1, lab_3_get_graphic_2, lab_3_get_graphic_3, lab_3_check_answer
from lab_4 import lab_4_get_source_data, lab_4_get_graphics, lab_4_check_answer
from lab_5 import lab_5_get_source_data, lab_5_get_graphic_1, lab_5_get_graphic_2, lab_5_check_answer

from lab_7 import lab_7_get_source_data, lab_7_get_graphic_1, lab_7_get_graphic_2, lab_7_get_graphic_3, lab_7_get_graphic_4, lab_7_check_answer

log = logging.getLogger(__name__)


class DSPXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    display_name = String(
        display_name='Display Name',
        default="DSPxblock",
        scope=Scope.settings
    )

    lab_list = JSONField(
        display_name='Display Name',
        scope=Scope.settings,
        default=[
            {
                "id": "lab_1",
                "title": "Лабораторная 1. Исследование цифровых фильтров с конечной импульсной характеристикой",
            },
            {
                "id": "lab_2",
                "title": "Лабораторная 2. Цифровой спектральный анализ",
            },
            {
                "id": "lab_3",
                "title": "Лабораторная 3. Цифровой согласованный фильтр",
            },
            {
                "id": "lab_4",
                "title": "Лабораторная 4. Исследование рекурсивных цифровых фильтров",
            },
            {
                "id": "lab_5",
                "title": "Лабораторная 5. Исследование рекурсивных цифровых фильтров",
            },
            {
                "id": "lab_7",
                "title": "Лабораторная 7. Цифровые модуляторы и демодуляторы",
            },

        ]

    )

    max_attempts = Integer(
        display_name=u"Максимальное количество попыток",
        help=u"",
        default=None,
        scope=Scope.settings
    )

    attempts = Integer(
        display_name=u"Количество использованных попыток",
        help=u"",
        default=0,
        scope=Scope.user_state
    )

    maximum_score = Integer(
        display_name=u"Максимальное количество баллов",
        help=(u"Максимальное количество баллов",
              u"которое может получить студент."),
        default=10,
        scope=Scope.settings
    )

    score = Float(
        display_name=u"Текущее количество баллов студента",
        default=None,
        scope=Scope.user_state
    )

    current_lab = String(
        display_name=u"ID текущей лаборатории",
        help=u"ID текущей лаборатории",
        default="lab_1",
        scope=Scope.settings
    )

    lab_settings = JSONField(
        default={
            "array_tolerance": 0.01,
            "number_tolerance": 0.5,
            "show_reset_button": False,
        },
        scope=Scope.settings,
        help='Настройка лабораторной',
    )

    lab_source_data = JSONField(
        default={},
        scope=Scope.user_state,
        help='Начальные данные лабораторной для студента',
    )

    student_state = JSONField(
        default={},
        scope=Scope.user_state,
        help='Ответ студента',
    )

    correct_answer = JSONField(
        default={},
        scope=Scope.user_state,
        help='Правильный ответ',
    )


    def is_course_staff(self):
        """
        Проверка, является ли пользователь автором курса.
        """
        return getattr(self.xmodule_runtime, 'user_is_staff', False)

    def is_instructor(self):
        """
        Проверка, является ли пользователь инструктором.
        """
        return self.xmodule_runtime.get_user_role() == 'instructor'

    def past_due(self):
            """
            Проверка, истекла ли дата для выполнения задания.
            """
            due = get_extended_due_date(self)
            if due is not None:
                if _now() > due:
                    return False

    def answer_opportunity(self):
        """
        Возможность ответа (если количество сделанное попыток меньше заданного).
        """
        if self.max_attempts is not None and self.max_attempts <= self.attempts:
            return False
        else:
            return True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the DSPXBlock, shown to students
        when viewing courses.
        """
        context = self.lab_context()

        fragment = self.load_lab_static(self.current_lab, context)
        fragment.initialize_js('DSPXBlock', context)
        return fragment

    @XBlock.json_handler
    def student_submit(self, data, suffix=''):
        # TO-DO: проверка возможности ответа
        self.student_state["answer"] = data
        result = {}
        try:
            if not self.answer_opportunity():
                raise Exception('Maximum number of attempts exceeded')
            if self.current_lab == "lab_1":
                result = lab_1_check_answer(data, self.lab_source_data, self.lab_settings)
            elif self.current_lab == "lab_2":
                pass
            elif self.current_lab == "lab_3":
                result = lab_3_check_answer(data, self.lab_source_data, self.lab_settings, self.correct_answer)
            elif self.current_lab == "lab_4":
                result = lab_4_check_answer(data, self.lab_source_data, self.lab_settings)
            elif self.current_lab == "lab_5":
                result = lab_5_check_answer(data, self.lab_source_data, self.lab_settings)
            # elif self.current_lab == "lab_6":
            #     result = lab_6_check_answer(data, self.lab_source_data, self.lab_settings)
            elif self.current_lab == "lab_7":
                result = lab_7_check_answer(data, self.lab_source_data, self.lab_settings)
            else:
                raise Exception('Hiding bugs lol')

            self.score = round(self.maximum_score * result["score"], 1)
            self.student_state["score"] = self.score
            self.student_state["correctness"] = result["correctness"]

            if result["score"] == 1:
                self.student_state["is_success"] = "success"
            elif result["score"] == 0:
                self.student_state["is_success"] = "error"
            else:
                self.student_state["is_success"] = "partially"


            self.runtime.publish(self, 'grade', dict(value=self.score, max_value=self.maximum_score))
            self.student_state["maximum_score"] = self.maximum_score
            self.student_state["max_attempts"] = self.max_attempts
            self.attempts += 1
            self.student_state["attempts"] = self.attempts
            return Response(json_body=self.student_state)

        except Exception as e:
            ex = dict()
            ex["exception"] = str(e)
            # возможно, трейсбэк следует показывать только сотрудникам
            # if self.is_course_staff() is True or self.is_instructor() is True:
            trace = traceback.extract_tb(sys.exc_info()[2])
            output = "Traceback is:\n"
            for (file, linenumber, affected, line) in trace:
                output += "> Error at function {}\n".format(affected)
                output += "  At: {}:{}\n".format(file, linenumber)
                output += "  Source: {}\n".format(line)
            output += "> Exception: {}\n".format(e)
            ex["traceback"] = output
            return Response(json.dumps(ex), status=500)

    @XBlock.json_handler
    def lab_1_get_graphics(self, data, suffix=''):
        self.student_state["answer"] = data
        try:
            graphics = lab_1_get_graphics(data, self.lab_source_data)
            return Response(json_body={"graphics": graphics})
        except:
            return Response('Error!', 500)

    @XBlock.json_handler
    def lab_3_get_graphic_1(self, data, suffix=''):
        self.student_state["answer"] = data
        try:
            graphic = lab_3_get_graphic_1(data, self.lab_source_data, self.correct_answer)
            return Response(json_body={"graphic": graphic})
        except:
            return Response('Error!', 500)


    @XBlock.handler
    def lab_3_get_graphic_2(self, request, suffix=''):
        self.student_state["answer"] = json.loads(request.body)
        reload = False
        is_signal = ""
        # try:
        if 'reload' in request.GET:
            reload = True
        if 'is_signal' in request.GET:
            is_signal = request.GET["is_signal"]
        self.correct_answer, self.student_state, graphic = lab_3_get_graphic_2(self.correct_answer, self.student_state, self.lab_source_data, reload, is_signal)
        return Response(json_body={"graphic": graphic, "student_state": self.student_state, "correct_answer": self.correct_answer})
        # except:
        #     return Response('Error!', 500)


    @XBlock.json_handler
    def lab_3_get_graphic_3(self, data, suffix=''):
        self.student_state["answer"] = data
        try:
            graphic = lab_3_get_graphic_3(data, self.lab_source_data)
            return Response(json_body={"graphic": graphic})
        except:
            return Response('Error!', 500)

    @XBlock.handler
    def lab_3_reset_task(self, data, suffix=''):
        self.student_state["state"]["Ku_j"] = 1
        self.student_state["state"]["Ku_i"] = 1
        self.student_state["state"]["Ku_done"] = False
        self.student_state["state"]["there_is_signal_count"] = 0
        self.student_state["state"]["there_is_no_signal_count"] = 0
        # self.student_state["y2_s2"] = None
        self.student_state["state"]["there_is_signal_states"] = [{}] * len(self.lab_source_data["s"])
        # self.correct_answer["s"] = [None] * len(self.lab_source_data["s"])
        _, self.student_state, graphic = lab_3_get_graphic_2(self.correct_answer, self.student_state, self.lab_source_data, True)
        return Response(json_body={"graphic": graphic, "student_state": self.student_state})

    @XBlock.json_handler
    def lab_4_get_graphics(self, data, suffix=''):
        self.student_state["answer"] = data
        try:
            graphics = lab_4_get_graphics(data, self.lab_source_data)
            return Response(json_body={"graphics": graphics})
        except:
            return Response('Error!', 500)

    @XBlock.json_handler
    def lab_5_get_graphic_1(self, data, suffix=''):
        self.student_state["answer"] = data
        try:
            graphics = lab_5_get_graphic_1(data, self.lab_source_data)
            return Response(json_body={"graphics": graphics})
        except:
            return Response('Error!', 500)

    @XBlock.json_handler
    def lab_5_get_graphic_2(self, data, suffix=''):
        self.student_state["answer"] = data
        try:
            graphics = lab_5_get_graphic_2(data, self.lab_source_data)
            return Response(json_body={"graphics": graphics})
        except:
            return Response('Error!', 500)

    @XBlock.handler
    def lab_7_get_graphic_1(self, data, suffix=''):
        # try:
        graphics = lab_7_get_graphic_1(self.lab_source_data, self.correct_answer)
        return Response(json_body={"graphics": graphics})
        # except:
        #     return Response('Error!', 500)

    @XBlock.json_handler
    def lab_7_get_graphic_2(self, data, suffix=''):
        self.student_state["answer"] = data
        try:
            graphics = lab_7_get_graphic_2(data)
            return Response(json_body={"graphics": graphics})
        except:
            return Response('Error!', 500)

    @XBlock.handler
    def lab_7_get_graphic_3(self, data, suffix=''):
        try:
            graphics = lab_7_get_graphic_3(self.lab_source_data, self.correct_answer)
            return Response(json_body={"graphics": graphics})
        except:
            return Response('Error!', 500)

    @XBlock.json_handler
    def lab_7_get_graphic_4(self, data, suffix=''):
        self.student_state["answer"] = data
        # try:
        graphics = lab_7_get_graphic_4(data, self.correct_answer)
        return Response(json_body={"graphics": graphics})
        # except:
            # return Response('Error!', 500)

    @XBlock.json_handler
    def save_answer(self, data, suffix=''):
        self.student_state["answer"] = data
        return Response(json_body={"success": "success"})

    @XBlock.handler
    def reset_task(self, data, suffix=''):
        if self.lab_settings["show_reset_button"]:
            self.attempts = 0
            self.score = None
            self.correct_answer = {}
            self.student_state = {}
            self.lab_source_data = {}
            return Response(json_body={"success": "success"})
        else:
            return Response('Error!', 500)

    def get_general_context(self):
        general_context = {
            "current_lab": self.current_lab,
            "display_name": self.display_name,
            "maximum_score": self.maximum_score,
            "score": self.score,
            "max_attempts": self.max_attempts,
            "attempts": self.attempts,
            "student_state": self.student_state,
            "show_reset_button": self.lab_settings["show_reset_button"],
        }

        if self.answer_opportunity():
            general_context["answer_opportunity"] = True

        if self.is_course_staff() is True or self.is_instructor() is True:
            general_context['is_course_staff'] = True

        return general_context

    def lab_context(self):
        if not self.lab_source_data or self.lab_source_data["lab_id"] != self.current_lab:  # второе условие на случай смены лабораторной
            self.student_state = {}
            self.attempts = 0
            self.score = None

            if self.current_lab == "lab_1":
                self.lab_source_data = lab_1_get_source_data()
            elif self.current_lab == "lab_2":
                self.lab_source_data = lab_1_get_source_data()
            elif self.current_lab == "lab_3":
                state = dict()
                self.lab_source_data, self.correct_answer = lab_3_get_source_data(self.correct_answer)
                state["Ku_j"] = 1
                state["Ku_i"] = 1
                state["Ku_done"] = False
                state["there_is_signal_count"] = 0
                state["there_is_no_signal_count"] = 0
                state["y2_s2"] = None
                state["there_is_signal_states"] = [{}] * len(self.lab_source_data["s"])
                self.correct_answer["s"] = [None] * len(self.lab_source_data["s"])
                self.student_state["state"] = state
            elif self.current_lab == "lab_4":
                self.lab_source_data = lab_4_get_source_data()
            elif self.current_lab == "lab_5":
                self.lab_source_data = lab_5_get_source_data()
            # elif self.current_lab == "lab_6":
            #     self.lab_source_data = lab_6_get_source_data()
            elif self.current_lab == "lab_7":
                self.lab_source_data, self.correct_answer = lab_7_get_source_data()
        context = merge_two_dicts(self.get_general_context(), self.lab_source_data)
        return context

    def load_lab_static(self, lab_id, context):
        frag = Fragment()
        frag.add_content(
            render_template(
                "static/{}/{}.html".format(lab_id, lab_id),
                context
            )
        )
        frag.add_css(self.resource_string("static/{}/{}.css".format(lab_id, lab_id)))
        frag.add_css(self.resource_string("static/css/dsp.css"))
        frag.add_javascript(self.resource_string("static/{}/{}.js".format(lab_id, lab_id)))
        frag.add_javascript(self.resource_string("static/js/src/dsp.js"))
        return frag

    def studio_view(self, context=None):
        context = {
            "display_name": self.display_name,
            "current_lab": self.current_lab,
            "lab_list": self.lab_list,
            "maximum_score": self.maximum_score,
            "max_attempts": self.max_attempts,
            "number_tolerance": self.lab_settings["number_tolerance"],
            "array_tolerance": self.lab_settings["array_tolerance"],
            "show_reset_button": self.lab_settings["show_reset_button"],
        }
        fragment = Fragment()
        fragment.add_content(
            render_template(
                "static/html/dsp_studio.html",
                context
            )
        )

        js_urls = (
            "static/js/src/dsp_studio.js",
        )

        css_urls = (
            "static/css/dsp_studio.css",
        )

        load_resources(js_urls, css_urls, fragment)

        fragment.initialize_js('DSPXBlock')
        return fragment

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        self.display_name = data.get('display_name')
        self.current_lab = data.get('current_lab')
        self.maximum_score = int(float(data.get('maximum_score')))
        try:
            self.max_attempts = int(round(float(data.get('max_attempts'))))
            if self.max_attempts == 0:
                raise Exception('Zero attempts is not allowed')
        except:
            self.max_attempts = None
        self.lab_settings["array_tolerance"] = float(data.get('array_tolerance'))
        self.lab_settings["number_tolerance"] = float(data.get('number_tolerance'))
        self.lab_settings["show_reset_button"] = True if data.get('show_reset_button') == 'true' else False

        return {'result': 'success'}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("DSPXBlock",
             """<dsp/>
             """),
            ("Multiple DSPXBlock",
             """<vertical_demo>
                <dsp/>
                <dsp/>
                <dsp/>
                </vertical_demo>
             """),
        ]


def _now():
    """
    Получение текущих даты и времени.
    """
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)