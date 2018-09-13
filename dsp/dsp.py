# -*- coding: utf-8 -*-
import logging
import json

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String, JSONField
from xblock.fragment import Fragment
from webob.response import Response


from .utils import (
    render_template,
    load_resources,
    merge_two_dicts,
)

from lab_1 import get_source_data
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

    count = Integer(
        default=3, scope=Scope.user_state,
        help="A simple counter, to show something happening",
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

    def lab_1_context(self):
        if not self.lab_source_data:
            self.lab_source_data = get_source_data()
        context = merge_two_dicts({"display_name": self.display_name}, self.lab_source_data)
        print(context)
        # context[""]

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
            "current_lab": self.current_lab

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
    def get_graphics(self, data, suffix=''):

        student_data = json.loads(str(data))
        log.info("!!!!!!!!!!!!!!!!!!!!!!!")
        log.info(str(student_data))

        return Response(json_body={})

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        self.display_name = data.get('display_name')

        return {'result': 'success'}

    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

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
