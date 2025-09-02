# from django import forms
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError


# class CustomUserCreationForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput,
#         label="Пароль",
#         required=True
#     )
#     password_confirm = forms.CharField(
#         widget=forms.PasswordInput,
#         label="Подтверждение пароля",
#         required=True
#     )

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirm = cleaned_data.get("password_confirm")
#         if password != password_confirm:
#             raise ValidationError("Пароли не совпадают.")
#         if len(password) < 8 or not any(
#             c.isupper() for c in password
#         ) or not any(
#             c.isdigit() for c in password
#         ):
#             raise ValidationError(
#                 '''Пароль должен содержать минимум 8 символов,
#                 включая заглавную букву и цифру.
#                 '''
#             )
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user


# class UserChangeForm(forms.ModelForm):
#     password = forms.CharField(
#         required=False,
#         widget=forms.PasswordInput,
#         help_text="Оставьте пустым, если не хотите менять пароль."
#     )
#     password_confirm = forms.CharField(
#         required=False,
#         widget=forms.PasswordInput,
#         help_text="Подтвердите новый пароль, если меняете."
#     )

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirm = cleaned_data.get("password_confirm")
#         if password or password_confirm:
#             if password != password_confirm:
#                 raise ValidationError("Пароли не совпадают.")
#             if len(password) < 8 or not any(
#                 c.isupper() for c in password
#             ) or not any(
#                 c.isdigit() for c in password
#             ):
#                 raise ValidationError(
#                     '''Пароль должен содержать минимум 8 символов,
#                     одну заглавную букву и одну цифру.
#                     '''
#                 )
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         password = self.cleaned_data.get("password")
#         if password:
#             user.set_password(password)
#         if commit:
#             user.save()
#         return user
