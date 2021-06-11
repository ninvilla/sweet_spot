from django.http import request
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


# login register
def index(request):
    request.session.flush()
    return render(request, 'login.html')

def success(request):
    if "user_id" not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user': this_user[0],
        'recipes': Recipe.objects.all()
    }
    return render(request, 'main.html', context)

def register(request):
    if request.method == 'POST':
        errors = User.objects.validate_reg(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'], 
            last_name = request.POST['last_name'], 
            email = request.POST['email'], 
            password = hashed_pw
            )

        request.session['user_id'] = new_user.id
        return redirect('/success')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        errors = User.objects.validate_login(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        if this_user:
            logged_user = this_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/success')
            messages.error(request, 'Invalid password')
            return redirect('/')
        messages.error(request, 'User does not exist')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')



# user profile
def profile(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user,
        'recipes': Recipe.objects.filter(poster=user)
        
    }
    return render(request, 'profile.html', context)


def edit_profile(request, id):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'edit_profile.html', context)

def update_profile(request, id):
    if request.method == 'POST':
        errors = User.objects.validate_profile(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/profile/{id}/edit')

        edit_user = User.objects.get(id=request.session['user_id'])
        edit_user.first_name = request.POST['first_name']
        edit_user.last_name = request.POST['last_name']
        edit_user.email = request.POST['email']
        edit_user.profile_img = request.POST['profile_img']
        edit_user.save()
        request.session['user_id'] = edit_user.id
    return redirect(f'/profile/{id}')

def delete_profile(request, id):
    delete_user = User.objects.get(id=id)
    delete_user.delete()
    return redirect('/')




# user recipes
def add_recipe(request, id):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'add_recipe.html', context)


def create_recipe(request, id):
    if request.method == 'POST':
        errors = Recipe.objects.validate_recipe(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/recipe/{id}')

        Recipe.objects.create(
            title = request.POST['title'],
            ingredients = request.POST['ingredients'],
            instructions = request.POST['instructions'],
            recipe_img = request.POST['recipe_img'],
            poster = User.objects.get(id=request.session['user_id'])
        )
    return redirect('/success')


def show_recipe(request, recipe_id):
    context = {
        'user_recipe': Recipe.objects.get(id=recipe_id),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'show_recipe.html', context)


def edit_recipe(request, recipe_id):
    context = {
        'user_recipe': Recipe.objects.get(id=recipe_id),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'edit_recipe.html', context)


def update_recipe(request, recipe_id):
    if request.method == 'POST':
        errors = Recipe.objects.validate_recipe(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/recipe/{recipe_id}/edit')
        edit_recipe = Recipe.objects.get(id=recipe_id)
        edit_recipe.title = request.POST['title']
        edit_recipe.ingredients = request.POST['ingredients']
        edit_recipe.instructions = request.POST['instructions']
        edit_recipe.recipe_img = request.POST['recipe_img']
        edit_recipe.save()
    return redirect(f'/recipe/{recipe_id}/show')


def delete_recipe(request, id, recipe_id):
    delete_recipe = Recipe.objects.get(id=recipe_id)
    delete_recipe.delete()
    return redirect(f'/recipe/{id}/my_recipes')

def add_like(request, recipe_id):
    recipe_liked = Recipe.objects.get(id=recipe_id)
    user_like = User.objects.get(id=request.session['user_id'])
    recipe_liked.likes.add(user_like)
    return redirect('/success')


def my_recipes(request, id):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'my_recipes.html', context)



def more_recipes(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'search.html', context)
