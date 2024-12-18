from django import forms
import json

class JSONInputForm(forms.Form):
    json_data = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        label='JSON Data'
    )

    def clean_json_data(self):
        data = self.cleaned_data['json_data']
        try:
            # Проверяем, что данные являются валидным JSON
            json.loads(data)
            return data
        except json.JSONDecodeError:
            raise forms.ValidationError('Invalid JSON format')
