from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def validate_reg(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        elif not EMAIL_REGEX.match(postData['email']):           
            errors['email'] = "Invalid email address"

        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "Email is already in use"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Passwords do not match"
        
        return errors


    def validate_login(self, postData):
        errors = {}
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        return errors

    def validate_profile(self, postData):
        errors = {}
        if len(postData['first_name']) == 0:
            errors['first_name'] = "First name must be entered"

        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last name must be entered"
        
        if len(postData['profile_img']) == 0:
            errors['profile_img'] = "Image must be added"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        elif not EMAIL_REGEX.match(postData['email']):           
            errors['email'] = "Invalid email address"

        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    profile_img = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()



class RecipeManager(models.Manager):
    def validate_recipe(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = "Recipe title must be entered"
        if len(postData['ingredients']) == 0:
            errors['ingredients'] = "Ingredients must be entered"
        if len(postData['instructions']) == 0:
            errors['instructions'] = "Instructions must be entered"
        if len(postData['recipe_img']) == 0:
            errors['recipe_img'] = "Image must be added"
        return errors


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    recipe_img = models.TextField()
    poster = models.ForeignKey(User, related_name="user_recipes", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RecipeManager()