from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    """Model representing a ticket created by a user."""

    title = models.CharField(max_length=128)
    description = models.TextField(
        max_length=2048, blank=True, help_text="Optional description for the ticket."
    )
    image = models.ImageField(
        null=True, blank=True, help_text="Optional image for the ticket."
    )
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets"
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    """Model representing a review on a ticket."""

    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(
        max_length=8192, blank=True, help_text="Optional detailed review."
    )
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )

    class Meta:
        ordering = ["-time_created"]  # Ordering reviews by the most recent first.

    def __str__(self):
        return f"{self.headline} - {self.rating}/5 by {self.user}"


class UserFollows(models.Model):
    """Model representing a user following another user."""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "followed_user"], name="unique_follows"
            )
        ]
        verbose_name_plural = (
            "User Follows"  # Optional, for better naming in the Django Admin.
        )

    def __str__(self):
        return f"{self.user} follows {self.followed_user}"
