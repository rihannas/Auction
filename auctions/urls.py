from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:pk>", views.get_listing, name="listing"),
    path("bid/<int:pk>", views.place_bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add-watchlist/<int:pk>", views.add_watchlist, name="add-watchlist"),
    path("remove-watchlist/<int:pk>", views.remove_watchlist, name="remove-watchlist"),
    path("comment/<int:pk>", views.add_comment, name="comment"),
    path("close-auction/<int:pk>", views.close_auction, name="close-auction"),

]

