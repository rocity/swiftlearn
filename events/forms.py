from django import forms
from .models import Event, Feedback, EventComment


class EventForm(forms.ModelForm):

    title = forms.CharField(widget=forms.Textarea({
        'class': 'form-control event-title',
        'placeholder': 'Enter event title',
        'rows': '1',
    }))
    info = forms.CharField(widget=forms.Textarea({
        'class': 'form-control',
        'placeholder': 'Description details',
        'rows': '8',
    }))
    fee = forms.CharField(widget=forms.NumberInput({
        'class': 'form-control price',
        'placeholder': '$',
        'type': 'number',
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


class FeedbackForm(forms.ModelForm):
    
    rate_star = forms.IntegerField(widget=forms.NumberInput({
        'class':'form-control',
        'placeholder':'Rating Star, select 1 to 5!'}
        ),label='',required=False,max_value=5, min_value=1)
    feedback = forms.CharField(widget=forms.Textarea({
        'class':'form-control',
        'placeholder':'Feedback Message'
        }),label='')
    class Meta:
        model = Feedback
        fields = ('rate_star','feedback')


class EventCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea({
        'class': 'form-control',
        'rows': '2',
        'id': 'id_comment',
        'required': True, 
        }))
    class Meta:
        model = EventComment
        fields = ('comment',)
