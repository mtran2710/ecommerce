from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("product/<int:pk>", views.product_detail, name="product"),
    path("category/", views.all_categories, name="all_categories"),
    path("category/<str:category_name>", views.category, name="category")
]
