from django.db import models

# 🚨 Flaw 1: Store passwords in plain text
class InsecureUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
