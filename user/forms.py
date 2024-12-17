from django import forms

class ExpenseCalculatorForm(forms.Form):
    country = forms.ChoiceField(choices=[])
    tuition_fees = forms.DecimalField(label="Tuition Fees (in USD)", max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(ExpenseCalculatorForm, self).__init__(*args, **kwargs)
        
        self.fields['country'].choices = self.get_country_choices()

    def get_country_choices(self):
        
        import json
        with open(r'C:\Users\Sagnik\OneDrive\Desktop\PROJECTS\scholarship\static\country_expenses.JSON', 'r') as file:
            data = json.load(file)
            choices = [(country['country'], country['country']) for country in data['countries']]
        return choices



