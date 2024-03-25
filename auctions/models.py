from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title



class Bid(models.Model):
    bid = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid')

class Listing(models.Model):
    title = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True)
    image_url = models.CharField(max_length=1000, blank=True)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings', blank=True, null=True,)
    starting_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='listing')
    watchlist = models.ManyToManyField(User, blank=True, related_name='userwatchlist')

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercomments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')

    def __str__(self) -> str:
        return f'comment by {self.user}'