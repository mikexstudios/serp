from django.conf import settings
from django import forms

#from .models import 

#import re

class AddURLForm(forms.Form):
    #We choose a length based on the Google's value.
    keyword = forms.CharField(max_length = 2048, label = 'Search Keyword')
    #Min length is '*' (wildcard), max_length is roughly 2000.
    url = forms.CharField(min_length = 1, max_length = 2000, initial = 'http://', 
                          label = 'URL')

    #TODO: Maybe remove all query params from URL? Or we do that when checking?

class RefreshForm(forms.Form):
    #We just want to use the CSRF token, so the form is pretty much empty.
    pass

class MultipleField(forms.MultipleChoiceField):
    def validate(self, value):
        if self.required and not value:
            raise forms.ValidationError(self.error_messages['required'])
        #We won't validate that each val in value is in choices.
ACTION_CHOICES = (
    ('refresh', 'Refresh Track'),
    ('archive', 'Archive Track'),
    ('unarchive', 'Unarchive Track'),
    ('delete', 'Delete Track'),
)
class ActionsForm(forms.Form):
    '''
    NOTE: We override error messages since we want to display them inline. Thus,
          we want to have more context.
    '''
    #We choose a length based on the Google's value.
    action = forms.ChoiceField(choices = ACTION_CHOICES, label = 'Actions', 
                               error_messages = {'required': 'A valid action is required', 
                                                 'invalid_choice': 'A valid action choice is required.'})
    #NOTE: Values returned from this field are unicode strings!
    id = MultipleField(label = 'List of IDs', 
                       error_messages = {'required': 'At least one ID must be selected.', 
                                         'invalid_list': 'Invalid list of IDs submitted.'})

    def clean_id(self):
        '''
        Make ids a list of integers.
        '''
        ids = self.cleaned_data['id']
        return map(int, ids)
