from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'post_image', 'text', )
        # Alterando os labels do formulário
        labels = {
        'title': "Título:",
        'post_image': "Imagem de destaque:",
        'text': "Texto:",
        }


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('author', 'text', )
        labels = {
        'author': "Nome:",
        'text': "Comentário:",
        }
