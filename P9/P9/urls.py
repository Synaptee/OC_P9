"""P9 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from critiques.views import (
    SignUpView,
    abonnements,
    flux,
    unsubscribe,
    create_ticket,
    user_tickets,
    edit_ticket,
    edit_review,
    delete_ticket,
    deleted,
    create_critic,
)
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("flux/", flux, name="flux"),
    path("abonnements/", abonnements, name="abonnements"),
    path("unsubscribe/", unsubscribe, name="unsubscribe"),
    path("ticket/", create_ticket, name="ticket"),
    path("posts", user_tickets, name="posts"),
    path("edit_ticket/<int:ticket_id>/", edit_ticket, name="edit_ticket"),
    path("edit_review/<int:review_id>/", edit_review, name="edit_review"),
    path("delete/<int:ticket_id>/", delete_ticket, name="delete_ticket"),
    path("deleted/", deleted, name="deleted"),
    path("critics/", create_critic, name="critics"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
