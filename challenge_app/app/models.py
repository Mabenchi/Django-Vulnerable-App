from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Amount(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return self.amount
