from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'headline', 'post_image', 'tags', 'text', )
        # Alterando os labels do formulário
        labels = {
            'title': "Título:",
            'post_image': "Imagem de destaque:",
            'text': "Texto:",
            'headline': "Chamada:",
        }
        widgets = {
          'text': forms.Textarea(attrs={'rows':40, 'cols':40, 'class': 'textP'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text', )
        labels = {
            'author': "Nome:",
            'text': "Comentário:",
        }
