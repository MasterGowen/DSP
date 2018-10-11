# -*- coding: utf-8 -*-
import logging
import json

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String, JSONField, Float
from xblock.fragment import Fragment
from webob.response import Response


from .utils import (
    render_template,
    load_resources,
)

from .calc_utils import merge_two_dicts

from lab_1 import get_source_data, get_graphics, check_answer
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
        default={
            "lab_1": {
                "title":  "Лабораторная 1. Исследование цифровых фильтров с конечной импульсной характеристикой",
            },
            "lab_2": {
                "title": "Лабораторная 2. Цифровой спектральный анализ",
            },
            "lab_3": {
                "title": "Лабораторная 3. Цифровой согласованный фильтр",
            },
            "lab_4": {
                "title": "Лабораторная 4. Исследование рекурсивных цифровых фильтров",
            },
            "lab_5": {
                "title": "Лабораторная 5 . Исследование рекурсивных цифровых фильтров",
            },
        }

    )

    max_attempts = Integer(
        display_name=u"Максимальное количество попыток",
        help=u"",
        default=10,
        scope=Scope.settings
    )

    attempts = Integer(
        display_name=u"Количество использованных попыток",
        help=u"",
        default=0,
        scope=Scope.user_state
    )

    maximum_score = Float(
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
        # self.current_lab
        context = self.lab_1_context()
        # print(context)
        fragment = self.load_lab_static(self.current_lab, context)
        fragment.initialize_js('DSPXBlock', context)
        return fragment

    @XBlock.json_handler
    def student_submit(self, data, suffix=''):
        # TO-DO: проверка возможности ответа
        self.student_state["answer"] = data
        result = check_answer(data, self.lab_source_data)
        self.score = round(self.maximum_score * result["score"])
        self.student_state["score"] = self.score
        self.student_state["correctness"] = result["correctness"]
        self.runtime.publish(self, 'grade', dict(value=self.score, max_value=self.maximum_score))
        return Response(json_body=self.student_state)

    @XBlock.json_handler
    def get_graphics(self, data, suffix=''):
        self.student_state["answer"] = data

        try:
            graphics = get_graphics(data, self.lab_source_data)
            return Response(json_body={"graphics": graphics})
        except:
            return Response('Error!', 500)

    def get_general_context(self):
        general_context = {
            "display_name": self.display_name,
            "maximum_score": self.maximum_score,
            "score": self.score,
            "max_attempts": self.max_attempts,
            "attempts": self.attempts,
            "student_state": self.student_state
        }

        return general_context

    def lab_1_context(self):
        if not self.lab_source_data:
            self.lab_source_data = get_source_data()
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
