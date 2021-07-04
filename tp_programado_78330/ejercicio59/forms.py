from django import forms
from crispy_forms.helper import FormHelper

class ParametersForm(forms.Form):
    fin = forms.IntegerField(label='Cantidad de minutos a simular', initial=600, min_value=0)
    #min_inicio = forms.IntegerField(label='Minuto de inicio del informe', initial=0, min_value=0)
    #min_fin = forms.IntegerField(label='Minuto fin del informe', initial=600, min_value=0)

    def __init__(self, *args, **kwargs):
        super(ParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False