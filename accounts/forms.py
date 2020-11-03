from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

User = get_user_model()



class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password confirmation', widget=forms.PasswordInput)

    class meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("password dont match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user




class UserAdminChangeForm(forms.ModelForm):
    """
    A form for updating useres Includes all the fields on the user, but replaces the password feild on the user
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"

    def clean_password(self):
        return self.initial['password']
