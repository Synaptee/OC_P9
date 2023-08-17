from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserFollows
from .forms import FollowUserForm, TicketForm


# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


@login_required
def flux(request):
    return render(request, "flux.html")


@login_required
def abonnements(request):
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
    if request.method == "POST":
        user_to_unfollow_id = request.POST.get("user_to_unfollow_id")
        UserFollows.objects.filter(
            user=request.user, followed_user_id=user_to_unfollow_id
        ).delete()
    return redirect(reverse("abonnements"))


@login_required
def create_ticket(request):
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
