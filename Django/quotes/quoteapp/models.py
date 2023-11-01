from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    fullname = models.CharField(max_length=150)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'authors'

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'quotes'  

    def __str__(self):
        return f"{self.name}"
