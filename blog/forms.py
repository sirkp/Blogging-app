from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        #Widgets help to design fields in form using class
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),#textinputclass, postcontent is our class
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})#editable and medium-editor-textarea are css classes
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
