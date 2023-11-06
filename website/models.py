from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Code(models.Model):
    user = models.ForeignKey(User, related_name="code", on_delete=models.DO_NOTHING)
    question = models.TextField(max_length=10000)
    code_response = models.TextField(max_length=10000)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.question
