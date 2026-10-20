from django.urls import path

from .views import (
    GameList, GameByCategory, GameDetail, NewGame, SearchGames,
    about_view, user_login_view, user_logout, register_user_view,
    download_torrent, comment_save,
)

urlpatterns = [
    path('', GameList.as_view(), name='main'),
    path('about/', about_view, name='about'),
    path('category/<int:category_id>/', GameByCategory.as_view(), name='category'),
    path('game/<int:pk>/', GameDetail.as_view(), name='game_detail'),
    path('addgame/', NewGame.as_view(), name='add_game'),

    path('login/', user_login_view, name='login'),
    path('logout/', user_logout, name='logout'),
    path('registration/', register_user_view, name='register'),
    path('search/', SearchGames.as_view(), name='search'),
    path('download/<int:pk>/', download_torrent, name='download'),
    path('comment/save/<int:pk>/', comment_save, name='comment_save'),
]
