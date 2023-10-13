from django.forms import ModelForm, ModelMultipleChoiceField
from .models import Post, Author, Category

class PostForm(ModelForm):
    #category = ModelMultipleChoiceField(label="категория", queryset=Category.objects.all())
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'category' ]