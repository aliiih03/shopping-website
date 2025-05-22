from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import Profile
from django.contrib.auth.models import User


class UpdateInfoForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'phone'}),
                            required=False)
    address1 = forms.CharField(label="",
                               widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'address 1'}),
                               required=False)
    address2 = forms.CharField(label="",
                               widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'address 2'}),
                               required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'city'}),
                           required=False)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'state'}),
                            required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'country'}),
                              required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'address1', 'address2', 'city', 'state', 'country']


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['label'] = ''

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['label'] = ''


class UpdateUserForm(UserChangeForm):
    password = None
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': "form-control", 'label': "", }))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'label': "", }))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'label': "", }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['label'] = ''


class signUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': "form-control", 'label': "", }))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'label': "", }))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'label': "", }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(signUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['label'] = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['label'] = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['label'] = ''
