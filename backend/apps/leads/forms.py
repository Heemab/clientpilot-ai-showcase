from django import forms

from .models import Lead, LeadTask


class LeadForm(forms.ModelForm):

    class Meta:
        model = Lead

        fields = [
            "company_name",
            "contact_name",
            "email",
            "phone",
            "website",
            "status",
            "priority",
            "assigned_to",
            "notes",
        ]

        widgets = {
            "company_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "contact_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "website": forms.URLInput(
                attrs={"class": "form-control"}
            ),
            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
            "priority": forms.Select(
                attrs={"class": "form-select"}
            ),
            "assigned_to": forms.Select(
                attrs={"class": "form-select"}
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        self.fields["assigned_to"].required = False

        if not user:
            self.fields["assigned_to"].queryset = (
                self.fields["assigned_to"].queryset.none()
            )
            return

        organization = getattr(user, "organization", None)

        if (
            organization is not None
            and hasattr(organization, "users")
        ):
            self.fields["assigned_to"].queryset = (
                organization.users.all()
            )
        else:
            self.fields["assigned_to"].queryset = (
                self.fields["assigned_to"].queryset.none()
            )


class LeadTaskForm(forms.ModelForm):

    class Meta:
        model = LeadTask

        fields = [
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "assigned_to",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Task title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Task description (optional)",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "due_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        self.fields["assigned_to"].required = False
        self.fields["due_date"].required = False
        self.fields["description"].required = False

        if self.instance.pk and self.instance.due_date:
            self.initial["due_date"] = (
                self.instance.due_date.strftime("%Y-%m-%dT%H:%M")
            )

        if not user:
            self.fields["assigned_to"].queryset = (
                self.fields["assigned_to"].queryset.none()
            )
            return

        organization = getattr(user, "organization", None)

        if (
            organization is not None
            and hasattr(organization, "users")
        ):
            self.fields["assigned_to"].queryset = (
                organization.users.all()
            )
        else:
            self.fields["assigned_to"].queryset = (
                self.fields["assigned_to"].queryset.none()
            )