from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile

User = get_user_model()


class DateInputCustom(forms.DateInput):
    input_type = "date"

    def __init__(self, attrs=None, options=None):
        if attrs is None:
            attrs = {}
        if options is None:
            options = {}
        attrs.update({"class": "form-control mb-3", "data-date-format": "yyyy-mm-dd"})
        attrs.update(options)
        super().__init__(attrs=attrs)


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Enter a valid email address",
            }
        ),
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Enter password",
            }
        ),
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input me-2"}),
    )


class RegisterForm(UserCreationForm):
    agree_terms = forms.BooleanField(
        required=True,
        label="I agree all statements in Terms of service",
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

            if field_name == "agree_terms":
                field.widget.attrs.update({"class": "form-check-input me-2"})

            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("gender", "date_of_birth", "avatar", "info")

        labels = {"date_of_birth": "Date of your Birth", "avatar": "Avatar image"}

        placeholders = {
            "info": "Enter some additional information",
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control form-control-lg",
                    "placeholder": self.Meta.placeholders.get(field_name),
                }
            )
            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"

        self.fields["date_of_birth"].widget = DateInputCustom()
        if self.errors.get("date_of_birth"):
            self.fields["date_of_birth"].widget.attrs["class"] += " is-invalid"
