from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class BlogForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Content'}))
    tag = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tags here'}), required=False,
                          help_text='multiple tags must separate by a comma')
    delete = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)