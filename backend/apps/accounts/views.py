from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.text import slugify

from apps.accounts.forms import (
    LoginForm,
    RegistrationForm,
)
from apps.organizations.models import Organization

User = get_user_model()


class UserLoginView(LoginView):
    """
    Branded ClientPilot AI login.
    """

    template_name = "accounts/login.html"

    authentication_form = LoginForm

    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard:index")


class UserLogoutView(LogoutView):
    """
    Logout user and return to the public landing page.
    """

    next_page = reverse_lazy("public:home")



def register(request):
    """
    Register a new ClientPilot AI account.
    Automatically creates an Organization and links the user.
    """

    if request.user.is_authenticated:
        return redirect("dashboard:index")

    form = RegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        company_name = form.cleaned_data["company_name"].strip()

        base_slug = slugify(company_name)
        slug = base_slug
        counter = 1

        while Organization.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        organization = Organization.objects.create(
            name=company_name,
            slug=slug,
            email=form.cleaned_data["email"],
        )

        full_name = form.cleaned_data["full_name"].strip()

        names = full_name.split(maxsplit=1)

        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ""

        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
            first_name=first_name,
            last_name=last_name,
            organization=organization,
        )

        login(request, user)

        return redirect("dashboard:index")

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )
