from django import forms
from .models import Ticket
from django.contrib.auth.models import User

class TicketFormCreate(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'severity','assigned_to','deadline']

class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'severity', 'status','created_by', 'assigned_to','notes', 'completed_reason']

class TicketCloseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        restricted_users = kwargs.pop('restricted_users', [])
        super(TicketCloseForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_superuser=False, is_active=True, is_staff=True)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'severity', 'status', 'created_by', 'assigned_to', 'completed_reason', 'notes']

class TicketCloseFormEngineer(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['notes']

class TicketAssignForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketAssignForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_superuser=False, is_active=True, is_staff=True)

    class Meta:
        model = Ticket
        fields = ['assigned_to']
