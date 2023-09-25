from django import forms
from .models import Ticket, Review


class FollowUserForm(forms.Form):
    """Form to follow another user by entering their username."""

    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={"placeholder": "Entrez le nom d'utilisateur"}),
        max_length=150,
    )


class TicketForm(forms.ModelForm):
    """Form to create or edit a ticket."""

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Description du ticket"}
            ),
        }
        labels = {
            "title": "Titre",
            "description": "Description",
            "image": "Image (optionnel)",
        }


class ReviewForm(forms.ModelForm):
    """Form to create or edit a review."""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "headline": forms.TextInput(attrs={"placeholder": "Titre de votre avis"}),
            "body": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Détails de votre avis"}
            ),
        }
        labels = {
            "headline": "Titre",
            "rating": "Note (1-5)",
            "body": "Commentaire",
        }
