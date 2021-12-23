from django.db import models
from django.core.validators import RegexValidator


CUSTOM_NAME_REGEX = RegexValidator(
    "^[a-zA-Z0-9_ ,]*$", message="Invalid name!")
FLAG_SECRET_REGEX = RegexValidator(
    "^[a-zA-Z0-9_]+$", message="Invalid secret!")


class Participant(models.Model):
    name = models.CharField(max_length=20, unique=True)
    custom_name = models.CharField(
        max_length=40, blank=True, validators=[CUSTOM_NAME_REGEX])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.name


class Flag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    secret = models.CharField(
        max_length=200, unique=True, validators=[FLAG_SECRET_REGEX])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.name


class Submission(models.Model):
    flag = models.ForeignKey(Flag, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["flag", "participant"], name="unique_submission")
        ]

    def __str__(self) -> str:
        return f"{str(self.participant)}: {str(self.flag)}"


class Content(models.Model):
    content = models.TextField()  # contains HTML to display

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.content
