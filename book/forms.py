from django.forms import ModelForm
from book.models import Publisher


class MyCommentForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'address', 'city', 'state_province', 'country', 'website']