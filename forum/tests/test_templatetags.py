from django import forms
from django.test import TestCase
from ..templatetags.form_tags import field_type, input_class


class ExampleForm(forms.Form):
    """class for example and format of log in form"""
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ('name', 'password')


class FieldTypeTests(TestCase):
    def test_field_widget_type(self):
        """tests the fields in the log in widget form"""
        form = ExampleForm()
        self.assertEquals('TextInput', field_type(form['name']))
        self.assertEquals('PasswordInput', field_type(form['password']))


class InputClassTests(TestCase):
    def test_unbound_field_initial_state(self):
        """
        tests the log in form with unbound fields
        the form is an unbound form, no data or field
        """
        form = ExampleForm()
        self.assertEquals('form-control ', input_class(form['name']))

    def test_valid_bound_field(self):
        """
        tests that the log in form has valid bound fields
        form is bound with field and data
        """
        form = ExampleForm({'name': 'john', 'password': '123'})
        self.assertEquals('form-control is-valid', input_class(form['name']))
        self.assertEquals('form-control ', input_class(form['password']))

    def test_invalid_bound_field(self):
        """tests when the elog in form has invalid bound fields"""
        form = ExampleForm({'name': '', 'password': '123'})
        self.assertEquals('form-control is-invalid', input_class(form['name']))
