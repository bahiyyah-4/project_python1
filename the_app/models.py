from django.db import models
import re

# Create your models here.
class User_Manager(models.Manager):
    def user_validator(self, form_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(form_data['first_name']) < 2:
            errors['first_name'] = "You need at least 2 characters for first name!"
        if len(form_data['last_name']) < 2:
            errors['last_name'] = "You need at least 2 characters for last name!"
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = "Email is invalid!"
        if len(form_data['password']) < 8:
            errors['password_length'] = "Your password should be 8 characters long!"
        if form_data['password'] != form_data['confirm_password']:
            errors['password_match'] = "Your password doesn't match!"
        
        return errors

    def login_validator(self, form_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = "Email is invalid!"

        return errors


class Job_Manager(models.Manager):
    def job_validator(self, form_data):
        errors = {}
        if len(form_data['title']) < 3:
            errors['title'] = "Your job title must be at least 3 characters"
        if len(form_data['description']) < 3:
            errors['description'] = "that's not enough to describe the job, use at least 3 characters!"
        if len(form_data['location']) < 3:
            errors['location'] = "A location must be provided,  Use at  least 3 characters!"
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = User_Manager()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="jobs", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="taken_jobs")
    objects = Job_Manager()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Category(models.Model):
    title = models.CharField(max_length=255)
    job = models.ForeignKey(Job, related_name="categories", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Real_Category(models.Model):
    title = models.CharField(max_length=255)
    jobs = models.ManyToManyField(Job, related_name="real_categories")