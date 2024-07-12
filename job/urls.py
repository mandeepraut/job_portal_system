from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index,name='index'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('user_login/',views.user_login,name='user_login'),
    path('recruiter_login/',views.recruiter_login,name='recruiter_login'),
    path('latestjob/',views.latestjob,name='latestjob'),
    path('contact/',views.contact,name='contact'),
    path('setting/',views.setting,name='setting'),
    path('user_setting/',views.user_setting,name='user_setting'),
    
    path('register/',views.register,name='register'),
    path('re_register/',views.re_register,name='re_register'),
    path('recruiter_home/',views.recruiter_home,name='recruiter_home'),
    
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),

    path('job_list/',views.job_list,name='job_list'),
    path('user_home/',views.user_home,name='user_home'),
    path('add_job/',views.add_job,name='add_job'),
    path('edit_jobdetail/<int:pid>',views.edit_jobdetail,name='edit_jobdetail'),
    path('delete_user/<int:pid>',views.delete_user,name='delete_user'),



    path('candidates_applied/',views.candidates_applied,name='candidates_applied'),
    
    path('Logout/',views.Logout,name='Logout'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('view_users/',views.view_users,name='view_users'),

    path('applyforjob/<int:pid>',views.applyforjob,name='applyforjob'),

    path('user_latestjob/',views.user_latestjob,name='user_latestjob'),

    path('recruiter_pending/',views.recruiter_pending,name='recruiter_pending'),
    path('recruiteraccept/',views.recruiteraccept,name='recruiteraccept'),
    path('recruiter_rejected/',views.recruiter_rejected,name='recruiter_rejected'),
    path('all_recruiters/',views.all_recruiters,name='all_recruiters'),
    path('delete_recruiter/<int:pid>',views.delete_recruiter,name='delete_recruiter'),
    path('job_detail/<int:pid>',views.job_detail,name='job_detail'),
    
    path('change_status/<int:pid>',views.change_status,name='change_status'),
    path('change_companylogo/<int:pid>',views.change_companylogo,name='change_companylogo'),

    path('change_passwordadmin/',views.change_passwordadmin,name='change_passwordadmin'),
    path('change_passworduser/',views.change_passworduser,name='change_passworduser'),
    path('change_passwordrecruiter/',views.change_passwordrecruiter,name='change_passwordrecruiter'),
    path('change_passwordrecruiter/',views.change_passwordrecruiter,name='change_passwordrecruiter'),
    
    path('recommend_jobs/', views.recommend_jobs, name='recommend_jobs'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('update_application_status/<int:pk>/', views.update_application_status, name='update_application_status'),

 

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
