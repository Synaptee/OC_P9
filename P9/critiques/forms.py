from django import forms


class FollowUserForm(forms.Form):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "nom d'utilisateur"}),
        max_length=150,
    )
