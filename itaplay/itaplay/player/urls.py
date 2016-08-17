from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^player_view/', views.PlayerView.as_view()),
    url(r'^current_player_view/(?P<pk>\d+)/', views.PlayerView.as_view()),
    url(r'^delete_player/(?P<pk>\d+)/', views.DeletePlayer.as_view()),
]	
