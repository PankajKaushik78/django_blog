from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from blog.models import Post
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            human = True
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account is created! You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'You account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def public_profile(request, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(author=user, private=False)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, "users/public_profile.html", context)


def user_search_view(request):
    user_profiles = Profile.objects.all()
    if 'username' in request.GET:
        username = request.GET['username']
        if username:
            user = get_object_or_404(User, username=username)
            user_profiles = user_profiles.filter(user=user)
    return render(request, "users/search_user.html", {'user_profile': user_profiles})
