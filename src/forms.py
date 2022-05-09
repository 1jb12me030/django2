from django import forms
from src.models import Coffee
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit

class CoffeepaymentForm(forms.ModelForm) :
    class Meta:
        model=Coffee
        fields='__all__'
    def __init__(self, *args, **kwargs) :
        super().__init__(*args,**kwargs)   
        self.helper=FormHelper(self)
        self.helper.layout=Layout(
            'name',
            'amount',
            Submit('submit', 'Buy',css_class='button white btn-block btn-primary')
            
        )
     