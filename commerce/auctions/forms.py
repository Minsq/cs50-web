from django.forms import ModelForm

from .models import Listing, Bid, Comment

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['seller', 'title', 'description',
                  'start_price', 'image', 'category']
    # note: 'creation_timestamp' cannot be specified as it is a non-editable field
# class BidForm(ModelForm):
#     class Meta:
#         model = Bid
#         fields = ['buyer','product','bid_price']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']