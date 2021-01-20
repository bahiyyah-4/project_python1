  
from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import User, Job, Real_Category
from django.contrib import messages

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect('/dashboard')
    context = {
        'all_users' : User.objects.all()
    }

    return render(request, 'login.html', context)


def process_registration(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    users = User.objects.filter(email = request.POST['email'])
    if len(users) > 0:
        messages.error(request, "Email is already in use!")
        return redirect('/')
    password = request.POST['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed,
    )
    print(hashed)
    request.session['user_id'] = user.id

    return redirect('/')


def process_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    users_email = User.objects.filter(email=request.POST['email'])
    if bcrypt.checkpw(request.POST['password'].encode(), users_email[0].password.encode()):
        request.session['user_id'] = users_email[0].id
        return redirect('/')
    messages.error(request, "The password that you provided doesn't match !")

    return redirect('/')


def display_all_jobs(request):
    context = {
        'logged_in_user': User.objects.get(id=request.session['user_id']),
        'jobs': Job.objects.all(),
        'taken_jobs': User.objects.get(id=request.session['user_id']).taken_jobs.all()
    }

    return render(request, "dashboard.html", context)


def delete_job(request, job_id):
    job_to_delete = Job.objects.get(id=job_id)
    if job_to_delete.user.id != request.session['user_id']:
        messages.error(request, "You can only delete the jobs that you posted!")
        return redirect('/dashboard')
    job_to_delete.delete()

    return redirect('/dashboard')


def take_job(request, job_id):
    Job.objects.get(id=job_id).users.add(User.objects.get(id=request.session['user_id']))

    return redirect('/dashboard')


def delete_job(request, job_id):
    job_to_delete = Job.objects.get(id=job_id)
    job_to_delete.delete()

    return redirect('/dashboard')


def remove_job(request, job_id):
    User.objects.get(id=request.session['user_id']).taken_jobs.remove(Job.objects.get(id=job_id))

    return redirect('/dashboard')



def edit_job(request, job_id):
    if Job.objects.get(id=job_id).user.id != request.session['user_id']:
        messages.error(request, "You can only edit the jobs that you posted!")
        return redirect('/dashboard')
    context = {
        'logged_in_user': User.objects.get(id=request.session['user_id']),
        'job': Job.objects.get(id=job_id)
    }

    return render(request, 'edit_job.html', context)


def display_job(request, job_id):
    context = {
        'logged_in_user': User.objects.get(id=request.session['user_id']),
        'job': Job.objects.get(id=job_id),
        'real_categories': Job.objects.get(id=job_id).real_categories.all()
    }

    return render(request, 'display_job.html', context)


def process_update(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        print("error in process_update")
        for msg in errors.values():
            messages.error(request, msg)
        return redirect(f'/jobs/edit/{request.POST["job_id"]}')
    job_to_update = Job.objects.get(id=request.POST['job_id'])
    job_to_update.title = request.POST['title']
    job_to_update.description = request.POST['description']
    job_to_update.location = request.POST['location']
    job_to_update.save()
    return redirect('/dashboard')


def new_job(request):
    context = {
        'logged_in_user': User.objects.get(id=request.session['user_id']),
    }
    
    return render(request, 'new_job.html', context)


def create_job(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        print("error in create_job")
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/jobs/new')
    job_job = Job.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        location = request.POST['location'],
        user = User.objects.get(id=request.session['user_id'])
    )
    cate_add = Real_Category.objects.create(title=request.POST['real_category'])
    if cate_add != "None":
        job_job.real_categories.add(cate_add)

    cate_other = Real_Category.objects.create(title=request.POST['other'])
    if len(cate_other.title) != 0:
        job_job.real_categories.add(cate_other)
    return redirect('/dashboard')


def logout(request):
    request.session.clear()

    return redirect('/')