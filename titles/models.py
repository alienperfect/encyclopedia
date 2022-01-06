from django.db import models


class Title(models.Model):
    title = models.CharField(unique=True, max_length=256)

    def __str__(self):
        return self.title
