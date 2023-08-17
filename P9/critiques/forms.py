from django import forms
from .models import Ticket


class FollowUserForm(forms.Form):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "nom d'utilisateur"}),
        max_length=150,
    )


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
