from string import digits
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from authapp.models import ShopUser

class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'first_name', 'age', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Только для совершеннолетних!')
        return data

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        username = self.cleaned_data['username']

        for letter in first_name:
            if letter in digits:
                raise forms.ValidationError('Только буквы!')

        if first_name not in username:
            raise forms.ValidationError('Имя пользователя не содержит Имя!')

        return first_name


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'first_name', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Только для совершеннолетних!')
        return data

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        username = self.cleaned_data['username']

        for letter in first_name:
            if letter in digits:
                raise forms.ValidationError('Только буквы!')

        if first_name not in username:
            raise forms.ValidationError('Имя пользователя не содержит Имя!')

        return first_name
