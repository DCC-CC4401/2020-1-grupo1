from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reporte

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        # widgets = {"username" : forms.TextInput(attrs={"class" : "input"}),
        #         "email" : forms.EmailInput(attrs={"class" : "input"})}
        # def __init__(self, *args, **kwargs):
        #     super(UserRegisterForm, self).__init__(*args, **kwargs)

        #     self.fields['username'].widget.attrs['class'] = 'form-control'
        #     self.fields['email'].widget.attrs['class'] = 'form-control'
        #     self.fields['password1'].widget.attrs['class'] = 'form-control'
        #     self.fields['password2'].widget.attrs['class'] = 'form-control'
class ReportCreationForm(forms.ModelForm):
    
    class Meta:
        model = Reporte
        fields = ['titulo', 'descripcion', 'foto', 'ciudad', 'ubicacion']
        
class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')