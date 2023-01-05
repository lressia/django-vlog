from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Posts
from .forms import NewPost, UpUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import os

# Create your views here.


def index(request):
    posts = Posts.objects.all()
    return render(request, 'index.html',{
        'posts': posts
    })

@login_required(login_url='/login')
def new(request):
    if request.method == 'GET':
        return render(request, 'new.html',{
            'name': request.user,
            'form': NewPost
        })
    else:
        try:
            post = Posts.objects.create(title=request.POST['title'], desc=request.POST['desc'], date=timezone.now(),user_id=request.user)
            post.save()
            return redirect('index')
        except ValueError:
            return render(request, 'new.html',{
                'error': ValueError,
                'form': NewPost,
                'name': request.user
            })

@login_required(login_url='/login')
def post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Posts, id=post_id)
        print(post)
        return render(request, 'post.html',{
            'post': post
        })

def delete(request, del_id):
    post = get_object_or_404(Posts, id=del_id)
    if request.method == 'POST':
        post.delete()
        return redirect('index')

@login_required(login_url='/login')
def profile(request, id):
    first_name, last_name, email, disabled_fn, disabled_ln = 'First Name', 'Last Name', 'Email', '', ''
    if request.method == 'GET':
        if request.user.id == id:
            profile = get_object_or_404(User, id=id)
            if profile.first_name != '':
                first_name = profile.first_name
                disabled_fn = 'disabled'
            if profile.last_name != '':
                last_name = profile.last_name
                disabled_ln = 'disabled'
            if profile.email != '':
                email = profile.email
            return render(request, 'profile.html',{
                    'profile': profile,
                    'first_name_disabled': disabled_fn,
                    'last_name_disabled': disabled_ln,
                    'first_name': first_name,
                    'last_name':last_name,
                    'email': email
                })
        else:
            # no esta autorizado a entrar a este perfil
            return HttpResponse('404 Not Found')
    else:
        try:
            profile = get_object_or_404(User, id=id)
            if profile.first_name == '':
                profile.first_name = request.POST['first_name']
            if profile.last_name == '':
                profile.last_name = request.POST['last_name']
            if request.POST['email'] != '':
                print(request.POST['email'])
                if User.objects.filter(email=request.POST['email']).exists():
                    return render(request, 'profile.html',{
                        'error': 'The email is registered',
                    })
                else:
                    profile.email = request.POST['email']
                    print(request.POST['email'])
                    print(profile.email)
            if request.POST['new_password1'] != '':
                if request.POST['new_password1'] == request.POST['new_password2']:
                    profile.password = make_password(request.POST['new_password1'])
                    print(profile.password)
            profile.save()
            return redirect('index')
        except ValueError:
            return render(request, 'profile.html',{
                        'error': ValueError,
                        'profile': profile,
                    })

@login_required(login_url='/login')
def edit(request, edit_id):
    if request.method == 'GET':
        return render(request, 'edit.html', {
            'form': NewPost
        })
    else:
        try:
            post = get_object_or_404(Posts, id=edit_id)
            post.title = request.POST['title']
            post.desc = request.POST['desc']
            post.date = timezone.now()
            post.save()
            return redirect('index')
        except ValueError:
            return render(request, 'edit.html', {
                'error': ValueError,
                'form': NewPost
            })
# Iniciar sesion
def login_f(request):
    if request.method == 'GET':
        return render(request, 'login.html',{
            'form': AuthenticationForm
        })
    else:
        user_v = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user_v is None:
            return render(request, 'login.html',{
                'error': 'Contraseña o usuario erroneo',
                'form': AuthenticationForm
            })
        else:
            login(request, user_v)
            return redirect('index')

# registrarse
def singin(request):
    if request.method == 'GET':
        return render(request, 'singin.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user_v = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user_v.save()
                login(request, user_v)
                return redirect('index')
            except:
                return render(request, 'singin.html',{
                    'error': 'El usuario ya existe',
                    'form': UserCreationForm
                })
        else:
            return render(request, 'singin.html',{
                'error': 'Las contraseñas no coinciden',
                'form': UserCreationForm
            })

@login_required
def logout_f(request):
    logout(request)
    return redirect('index')