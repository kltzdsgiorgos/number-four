from django import forms

class WorkoutUploadForm(forms.Form):
    file = forms.FileField(
        label="Select FIT File",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'id': 'id_file',
            'required': True,
        })
    )
