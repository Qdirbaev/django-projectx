import os

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView

from .forms import AddGameForm, CommentForm, LoginForm, RegisterForm
from .models import Category, Comment, Game


class GameList(ListView):
    model = Game
    context_object_name = 'games'
    template_name = 'xgame/index.html'
    extra_context = {
        'title': 'X-game, dl games free'
    }


def about_view(request):
    return render(request, 'xgame/about.html', {'title': 'About us'})


class GameByCategory(GameList):
    def get_queryset(self):
        return Game.objects.filter(category=self.kwargs['category_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        context['title'] = category.title
        return context


class GameDetail(DetailView):
    model = Game
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.object
        context['title'] = game.title
        context['games'] = Game.objects.exclude(pk=game.pk).order_by('-pk')[:3]
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(game=game).select_related('user').order_by('-pk')
        return context


class NewGame(UserPassesTestMixin, CreateView):
    form_class = AddGameForm
    template_name = 'xgame/add_game.html'
    extra_context = {
        'title': 'Add game!'
    }

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('main')


def user_login_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Successfully logged in!')
            return redirect('main')
    else:
        form = LoginForm()

    context = {
        'title': 'Authentication',
        'form': form,
    }
    return render(request, 'xgame/login.html', context)


def user_logout(request):
    logout(request)
    messages.info(request, 'Logged out!')
    return redirect('main')


def register_user_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Now you can log in.')
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'title': 'Registration',
        'form': form,
    }
    return render(request, 'xgame/register.html', context)


class SearchGames(GameList):
    def get_queryset(self):
        word = self.request.GET.get('q', '').strip()
        return Game.objects.filter(title__icontains=word)


def download_torrent(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    game = get_object_or_404(Game, pk=pk)
    if not game.torrent:
        raise Http404('Torrent file not found')

    return FileResponse(
        game.torrent.open('rb'),
        as_attachment=True,
        filename=os.path.basename(game.torrent.name),
    )


def comment_save(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.game = game
            comment.save()
        else:
            messages.error(request, 'Comment cannot be empty.')
    return redirect('game_detail', pk=game.pk)
