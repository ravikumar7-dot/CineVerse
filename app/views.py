from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Movie, MyList


def home(request):
    query = request.GET.get('q', '')

    banner = Movie.objects.filter(is_featured=True).first()
    if not banner:
        banner = Movie.objects.first()

    trending_movies = Movie.objects.all().order_by('-created_at')[:10]
    new_movies = Movie.objects.all().order_by('-release_date')[:10]
    popular_movies = Movie.objects.all().order_by('-movie_views')[:10]

    search_results = []
    if query:
        search_results = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(genre__name__icontains=query)
        ).distinct()

    context = {
        'banner': banner,
        'trending_movies': trending_movies,
        'new_movies': new_movies,
        'popular_movies': popular_movies,
        'search_query': query,
        'search_results': search_results,
    }
    return render(request, 'home.html', context)


def movie_detail(request, uu_id):
    movie = get_object_or_404(Movie, uu_id=uu_id)
    movie.movie_views += 1
    movie.save()

    related_movies = Movie.objects.exclude(id=movie.id).order_by('-movie_views')[:8]

    context = {
        'movie': movie,
        'related_movies': related_movies,
    }
    return render(request, 'movie.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('app:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('app:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('app:signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('app:signup')

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('app:login')

    return render(request, 'signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('app:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('app:home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('app:login')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('app:login')


@login_required
def add_to_list(request, uu_id):
    movie = get_object_or_404(Movie, uu_id=uu_id)
    MyList.objects.get_or_create(user=request.user, movie=movie)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_from_list(request, uu_id):
    movie = get_object_or_404(Movie, uu_id=uu_id)
    MyList.objects.filter(user=request.user, movie=movie).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def my_list(request):
    movies = MyList.objects.filter(user=request.user).select_related('movie')
    return render(request, 'my_list.html', {'movies': movies})