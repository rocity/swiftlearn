from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    title = forms.CharField(widget=forms.Textarea({
        'class': 'form-control event-title',
        'placeholder': 'Enter event title',
        'rows': '1',
    }))
    info = forms.CharField(widget=forms.Textarea({
        'class': 'form-control',
        'placeholder': 'Description details',
    }))
    start_date = forms.DateField(widget=forms.DateInput({
        'class': 'form-control',
        'placeholder': 'Select date',
        'type': 'date',
    }))
    start_time = forms.TimeField(widget=forms.TimeInput({
        'class': 'form-control',
        'placeholder': 'Start time',
        'type': 'time',
    }))
    end_time = forms.TimeField(widget=forms.TimeInput({
        'class': 'form-control',
        'placeholder': 'End time',
        'type': 'time',
    }))

    class Meta:
        model = Event
        fields = (
            'title',
            'info',
            'start_date',
            'start_time',
            'end_time',
            'fee',
            'tags',
        )