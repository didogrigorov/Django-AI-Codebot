from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class OpenAIForm(forms.Form):
    languages = ['Select Your Language', 'C', 'Clike', 'CoffeeScript', 'cpp', 'Csharp', 'CSS', 'Dart', 'Django', 'Go',
                 'HTML', 'Java',
                 'Javascript', 'JSX', 'Markdown', 'Markup', 'Markup-templating', 'Matlab', 'Mongodb', 'Objective-C',
                 'Perl', 'PHP', 'Powershell', 'Python', 'R', 'Ruby', 'Rust', 'Sass', 'Scala', 'Scss', 'SQL',
                 'Swift',
                 'TSX', 'Typescript']

    LANGUAGE_CHOICES = [(lang, lang) for lang in languages]

    user_request = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Query...'}))

    language_selection = forms.ChoiceField(label="", choices=LANGUAGE_CHOICES,
                                           widget=forms.Select(attrs={'class': 'form-select'}))

    def clean(self):
        cleaned_data = super().clean()
        language_selection = cleaned_data.get('language_selection')

        # Check if there are existing errors for the 'language_selection' field
        if 'language_selection' in self._errors:
            return cleaned_data  # Skip further validation if there are errors

        if language_selection == 'Select Your Language':
            raise ValidationError("Hey! You forgot to pick a programming language!")

        return cleaned_data


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address...'}), )

    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))

    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
