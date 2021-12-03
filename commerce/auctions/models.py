from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.utils import timezone

class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = (
    ('fashion','Fashion'),
    ('food','Food'),
    ('toys', 'Toys'),
    ('electronics','Electronics'),
    ('entertainment','Entertainment'),
    ('automotive', 'Automotive'),
    ('office','Office'),
    ('furniture', 'Furnishing'),
    ('others','Others')
)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sellers')
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_price =  models.FloatField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to="images/auctions", blank=True)
    category = models.CharField(max_length=64, choices=CATEGORIES, blank=False)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner', blank=True, null=True)
    class Meta:
        ordering = ['-status','category', 'title']
    def __str__(self):
        return f"{self.id}: {self.title} ({self.seller})"
        
class Bid(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyers')
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bid_price = models.FloatField(validators=[MinValueValidator(0)])
    bid_timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Buyer({self.buyer}), Product({self.product}), Price ${self.bid_price}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    item = models.ManyToManyField(Listing, blank=True, related_name="watchlists")
    def __str__(self):
        return f"{self.user}'s Watchlist"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentors')
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='product_comments')
    comment = models.TextField(max_length=1024, blank=False, default="")
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.commenter} commented on {self.product}"

