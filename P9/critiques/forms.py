from django import forms


class FollowUserForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur à suivre", max_length=150)
