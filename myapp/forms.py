from django.forms import ModelForm
from .models import Posts
from django.contrib.auth.models import User


#Actualizar datos
class UpUser(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# class Picture(ModelForm):
#     class Meta:
#         model = Pict
#         fields = ['pict']
# # Registro
# class NewUserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
# # Inicio sesion
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

class NewPost(ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'desc']