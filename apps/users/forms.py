

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User 


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ('username','first_name','last_name','email','is_staff','is_superuser','is_active')



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User 
        fields = ('username','first_name','last_name','email')
        error_class= 'error'