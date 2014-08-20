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
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                            label='Title')
    content = forms.CharField(widget=forms.HiddenInput, label='Content')
    tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags here'}),
                          required=False, help_text='multiple tags must separate by a comma', label='Tags',)
    delete = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)