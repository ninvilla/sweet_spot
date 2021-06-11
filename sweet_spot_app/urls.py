from django.urls import path
from . import views

urlpatterns = [
    # login register
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),


    # user profile
    path('profile/<int:id>', views.profile),
    path('profile/<int:id>/edit', views.edit_profile),
    path('profile/<int:id>/update', views.update_profile),
    path('profile/<int:id>/delete', views.delete_profile),


    # user recipe
    path('recipe/<int:id>', views.add_recipe),
    path('recipe/<int:id>/create', views.create_recipe),
    path('recipe/<int:recipe_id>/show', views.show_recipe),
    path('recipe/<int:recipe_id>/edit', views.edit_recipe),
    path('recipe/<int:recipe_id>/update', views.update_recipe),
    path('recipe/<int:recipe_id>/delete/<int:id>', views.delete_recipe),
    path('recipe/<int:recipe_id>/like', views.add_like),
    path('recipe/<int:id>/my_recipes', views.my_recipes),
    path('find_more', views.more_recipes),
]