from django.urls import path
from . import views

urlpatterns = [  
    path('', views.index),
    path('jobs/edit/<int:job_id>', views.edit_job),
    path('jobs/<int:job_id>', views.display_job),
    path('delete_job/<int:job_id>', views.delete_job),
    path('jobs/new', views.new_job),
    path('dashboard', views.display_all_jobs),
    path('process_registration', views.process_registration),
    path('process_login', views.process_login),
    path('logout', views.logout),
    path('create_job', views.create_job),
    path('process_update', views.process_update),
    path('remove_job/<int:job_id>', views.remove_job),
    path('delete_job/<int:job_id>', views.delete_job),
    path('take_job/<int:job_id>', views.take_job),
 
]