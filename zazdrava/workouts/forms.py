from django import forms


class WorkoutUploadForm(forms.Form):
    file = forms.FileField(label="Upload FIT File")

