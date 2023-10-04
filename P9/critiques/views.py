from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Value, CharField
from itertools import chain

from .models import UserFollows, Ticket, Review
from .forms import FollowUserForm, TicketForm, ReviewForm


# -----------------------
# User and Authentication Views
# -----------------------


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


@login_required
def abonnements(request):
    """Function that allows a user to follow another user"""
    user = request.user
    message = ""

    if request.method == "POST":
        form = FollowUserForm(request.POST)
        if form.is_valid():
            username_to_follow = form.cleaned_data["username"]
            try:
                user_to_follow = User.objects.get(username=username_to_follow)
                if user != user_to_follow:
                    # Vérifie si l'utilisateur est déjà suivi
                    already_follows = UserFollows.objects.filter(
                        user=user, followed_user=user_to_follow
                    ).exists()
                    if not already_follows:
                        UserFollows.objects.create(
                            user=user, followed_user=user_to_follow
                        )
                        form = FollowUserForm()  # Ou où vous voulez rediriger
                    else:
                        message = "Vous suivez déjà cet utilisateur."
                else:
                    message = "Vous ne pouvez pas vous suivre vous-même."
            except User.DoesNotExist:
                message = "L'utilisateur n'existe pas."
    else:
        form = FollowUserForm()

    abonnements = UserFollows.objects.filter(user=user)
    abonnes = UserFollows.objects.filter(followed_user=user)

    context = {
        "abonnements": abonnements,
        "abonnes": abonnes,
        "form": form,
        "message": message,
    }
    return render(request, "abonnements.html", context)


@login_required
def unsubscribe(request):
    """Function that allows a user to unfollow another user"""
    if request.method == "POST":
        user_to_unfollow_id = request.POST.get("user_to_unfollow_id")
        UserFollows.objects.filter(
            user=request.user, followed_user_id=user_to_unfollow_id
        ).delete()
    return redirect(reverse("abonnements"))


# -----------------------
# Ticket CRUD Views
# -----------------------


@login_required
def create_ticket(request):
    """Function that allows a user to create a ticket"""
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(reverse("flux"))
    else:
        form = TicketForm()

    context = {
        "form": form,
    }
    return render(request, "ticket.html", context)


@login_required
def user_tickets(request):
    """Function that allows a user to see his tickets"""
    user_tickets = Ticket.objects.filter(user=request.user)
    return render(request, "posts.html", {"tickets": user_tickets})


@login_required
def edit_ticket(request, ticket_id):
    """Function that allows a user to edit a ticket"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = TicketForm(instance=ticket)
    return render(request, "edit_ticket.html", {"form": form, "ticket": ticket})


@login_required
def delete_ticket(request, ticket_id):
    """Function that allows a user to delete a ticket"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == "POST":
        ticket.delete()
        return render(request, "suppression.html")
    return render(request, "posts.html", {"ticket": ticket})


@login_required
def answer_ticket(request, ticket_id):
    """Function that allows a user to answer a ticket"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("flux")
    else:
        form = ReviewForm()
    return render(request, "answer_ticket.html", {"form": form, "ticket": ticket})


# -----------------------
# Review CRUD Views
# -----------------------


@login_required
def edit_review(request, review_id):
    """Function that allows a user to edit a review"""
    review = get_object_or_404(Review, pk=review_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect("flux")
    else:
        form = ReviewForm(instance=review)
    return render(request, "edit_critic.html", {"form": form, "review": review})


@login_required
def delete_review(request, review_id):
    """Function that allows a user to delete a review"""
    review = get_object_or_404(Review, pk=review_id)
    if request.method == "POST":
        review.delete()
        return render(request, "suppression.html")
    return render(request, "flux.html", {"review": review})


@login_required
def create_critic(request):
    """Function that allows a user to create a ticket and a review at the same time"""
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("flux")

    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {"ticket_form": ticket_form, "review_form": review_form}
    return render(request, "create_critic.html", context)


# -----------------------
# Miscellaneous Views
# -----------------------


@login_required
def flux(request):
    """Function that allows a user to see his feed"""
    # Les tickets et critiques de l'utilisateur connecté
    user_reviews = Review.objects.filter(user=request.user).annotate(
        content_type=Value("REVIEW", CharField())
    )
    user_tickets = Ticket.objects.filter(user=request.user).annotate(
        content_type=Value("TICKET", CharField())
    )

    # Les utilisateurs que l'utilisateur actuel suit
    followed_users = [uf.followed_user for uf in request.user.following.all()]

    # Les tickets et critiques des utilisateurs suivis
    followed_reviews = Review.objects.filter(user__in=followed_users).annotate(
        content_type=Value("REVIEW", CharField())
    )
    followed_tickets = Ticket.objects.filter(user__in=followed_users).annotate(
        content_type=Value("TICKET", CharField())
    )

    # Les critiques associées aux tickets de l'utilisateur connecté
    reviews_on_user_tickets = Review.objects.filter(ticket__in=user_tickets).annotate(
        content_type=Value("REVIEW", CharField())
    )

    # Combiner tous les tickets et critiques
    combined_posts = chain(
        user_reviews,
        user_tickets,
        followed_reviews,
        followed_tickets,
        reviews_on_user_tickets,
    )
    unique_posts = {
        f"{post.id}_{post.content_type}": post for post in combined_posts
    }.values()

    # Trier les articles
    posts = sorted(unique_posts, key=lambda post: post.time_created, reverse=True)

    return render(request, "flux.html", context={"posts": posts})


@login_required
def deleted(request):
    """Page that confirms the deletion of a ticket or a review"""
    return render(request, "suppression.html")
