from django import forms
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        required=True
        # help_text="Пароль должен содержать минимум 8 символов, включая заглавную букву и цифру."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтверждение пароля",
        required=True
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        if len(password1) < 8 or not any(
            c.isupper() for c in password1
        ) or not any(
            c.isdigit() for c in password1
        ):
            raise ValidationError(
                '''Пароль должен содержать минимум 8 символов,
                включая заглавную букву и цифру.
                '''
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        help_text="Оставьте пустым, если не хотите менять пароль."
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        help_text="Подтвердите новый пароль, если меняете."
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Пароли не совпадают.")
            if len(password1) < 8 or not any(
                c.isupper() for c in password1
            ) or not any(
                c.isdigit() for c in password1
            ):
                raise ValidationError(
                    '''Пароль должен содержать минимум 8 символов,
                    одну заглавную букву и одну цифру.
                    '''
                )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
