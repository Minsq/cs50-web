from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories/<str:category_name>", views.categories, name="categories"),
    path('<int:product_id>/bid', views.bid, name='bid'),
    path('<int:product_id>/comment', views.comment, name='comment'),
    path('<int:product_id>/add_to_watchlist', views.add_to_watchlist, name='add_to_watchlist'),
    path('<int:product_id>/close_auction', views.close_auction, name='close_auction'),
    path('watchlist',views.watchlist,name='watchlist'),



]

