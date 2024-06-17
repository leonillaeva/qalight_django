from datetime import date

from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

from accounts.managers import CustomUserManager
from accounts.validators import validate_username, validate_name, validate_birth_date


class User(AbstractUser):
    username = models.CharField(
        max_length=30, unique=True, validators=[validate_username]
    )
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50, validators=[validate_name])
    last_name = models.CharField(max_length=50, validators=[validate_name])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)


class Profile(models.Model):
    GENDER_CHOICES = (("m", "Male"), ("f", "Female"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(validators=[validate_birth_date])
    info = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (
                today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age

class AbstractToken(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=64, unique=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def verify_token(self, days: int = 1) -> bool:
        validate_exp = timezone.localtime(
            self.create_at
        ) > timezone.now() - timezone.timedelta(days=days)
        return validate_exp

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=64)
        super().save(*args, **kwargs)


class ActivateToken(AbstractToken):

    class Meta:
        verbose_name_plural = "Activation tokens"

    def __str__(self):
        return f"{self.user}'s token activate: {self.token}"


class PasswordResetToken(AbstractToken):
    class Meta:
        verbose_name_plural = "Password reset tokens"

    def __str__(self):
        return f"{self.user}'s password reset token: {self.token}"


class AccessAPIToken(AbstractToken):
    def __str__(self):
        return f"{self.user.username}'s API access token"

    class Meta:
        verbose_name_plural = "API Access Tokens"

