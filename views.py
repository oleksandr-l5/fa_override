from flask import request
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.model.ajax import AjaxModelLoader
from flask_admin.model.fields import AjaxSelectField

import models


class SecondSelectFieldLoader(AjaxModelLoader):
    def format(self, value):
        if value:
            return (value, value)
        return ""

    def get_one(self, pk):
        return pk

    def get_list(self, query, offset=0, limit=100):
        first = request.args.get("first", "")
        return [first[::-1]]


class ThirdSelectFieldLoader(AjaxModelLoader):
    def format(self, value):
        if value:
            return (value, value)
        return ""

    def get_one(self, pk):
        return pk

    def get_list(self, query, offset=0, limit=100):
        first = request.args.get("first", "")
        second = request.args.get("second", "")
        return [f"{first}_and_{second}"]


class SecondSelectField(AjaxSelectField):
    def __init__(self, loader=SecondSelectFieldLoader(name="second", options=dict(minimum_input_length=0)), label=None,
                 validators=None, allow_blank=False,
                 blank_text=u'', **kwargs):
        super(SecondSelectField, self).__init__(loader=loader, label=label, validators=validators,
                                                allow_blank=allow_blank, blank_text=blank_text, **kwargs)


class ThirdSelectField(AjaxSelectField):
    def __init__(self, loader=ThirdSelectFieldLoader(name="third", options=dict(minimum_input_length=0)), label=None,
                 validators=None, allow_blank=False,
                 blank_text=u'', **kwargs):
        super(ThirdSelectField, self).__init__(loader=loader, label=label, validators=validators,
                                               allow_blank=allow_blank, blank_text=blank_text, **kwargs)


class ExampleView(ModelView):
    def __init__(self, name=None, category=None, endpoint=None, url=None):
        super(ExampleView, self).__init__(models.Example, name, category, endpoint, url)

    form_overrides = dict(
        second=SecondSelectField,
        third=ThirdSelectField
    )

    form_ajax_refs = dict(
        second=SecondSelectFieldLoader(name="second", options=dict(minimum_input_length=0)),
        third=ThirdSelectFieldLoader(name="third", options=dict(minimum_input_length=0))
    )
