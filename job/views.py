from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator as token_generator
from .models import StudentUser, Recruiter, Job, Apply
from .forms import ApplicationStatusForm
from .tokens import account_activation_token
from datetime import date

def index(request):
    return render(request, 'index.html')
def recruiter_home(request):
    return render(request, 'recruiter_home.html')

def premium_home(request):
    return render(request, 'premium/premium_home.html')


def user_home(request):
    user_applications = Apply.objects.filter(student__user=request.user)
    return render(request, 'user_home.html', {'applications': user_applications})

def admin_login(request):
    error=""
    if request.method=="POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error': error}    
    return render(request, 'admin_login.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    rcount = Recruiter.objects.all().count()
    scount = StudentUser.objects.all().count()

    context = {'rcount': rcount, 'scount': scount}
    return render(request, 'admin_home.html', context)

def recruiter_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter":
                    if user1.status == "pending":
                        error = "pending"
                    else:
                        login(request, user)
                        error = "no"
                else:
                    error = "not_a_recruiter"
            except Recruiter.DoesNotExist:
                error = "recruiter_not_found"
        else:
            error = "invalid_credentials"
        
    return render(request, 'recruiter_login.html', {'error': error})   

def latestjob(request):
    search_query = request.GET.get('search', '')
    if search_query:
        data = Job.objects.filter(title__icontains=search_query).order_by('-start_date')
    else:
        data = Job.objects.all().order_by('-start_date')
    
    context = {
        'data': data,
        'search_query': search_query,
    }
    return render(request, 'latestjob.html', context)

@login_required
def user_latestjob(request):
    search_query = request.GET.get('search', '')
    if search_query:
        job = Job.objects.filter(title__icontains=search_query).order_by('-start_date')
    else:
        job = Job.objects.all().order_by('-start_date')

    user = request.user
    try:
        student = StudentUser.objects.get(user=user)
        data = Apply.objects.filter(student=student)
        li = [i.job.id for i in data]
    except StudentUser.DoesNotExist:
        # Handle the case where the StudentUser does not exist
        student = None
        li = []

    d = {'job': job, 'li': li, 'search_query': search_query}
    return render(request, 'user_latestjob.html', d)


def job_detail(request,pid):
    job=Job.objects.get(id=pid)
   
    d={'job':job}
    return render(request,'job_detail.html',d)

def contact(request):
    return render(request, 'contact.html')

def job_list(request):
    return render(request, 'job_list.html')

def change_password(request):
    return render(request, 'change_password.html')


# from django.contrib.auth.decorators import login_required
# @login_required(login_url='user_login')

def user_setting(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name') 
        con = request.POST.get('contact')
        gender = request.POST.get('gender')
        skill_list = request.POST.get('skill_list')

        student.user.first_name = first_name
        student.user.last_name = last_name
        student.user.mobile = con
        student.user.gender = gender
        student.skill_list = skill_list
        
        image = request.FILES.get('image')

        try:
            student.user.save()
            if image:
                student.image = image
            student.save()
            error = "no"
        except Exception as ex:
            print(f"Exception occurred: {ex}")
            error = str(ex)

    context = {'student': student, 'error': error}
    return render(request, 'user_setting.html',context)

def setting(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')    
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    error = ""  
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name') 
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')

        recruiter.user.first_name = first_name
        recruiter.user.last_name = last_name
        recruiter.user.contact = contact
        recruiter.user.gender = gender
        
        image = request.FILES.get('image')

        try:
            recruiter.user.save()
            if image:
                recruiter.image = image
            recruiter.save()
            error = "no"
        except Exception as ex:
            print(f"Exception occurred: {ex}")
            error = str(ex)

    context = {'recruiter': recruiter, 'error': error}
    return render(request, 'settings.html', context)

def user_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except StudentUser.DoesNotExist:
                error = "yes"
        else:
            error = "yes"
    return render(request, 'user_login.html', {'error': error})

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=StudentUser.objects.all()
    d={'data':data}
    return render(request,'view_users.html',d)


def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student=User.objects.get(id=pid)
    student.delete() 
    return redirect('view_users')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status="pending")
    
    return render(request, 'recruiter_pending.html', {'data': data})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Recruiter
def change_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    try:
        recruiter = Recruiter.objects.get(id=pid)
    except Recruiter.DoesNotExist:
        return redirect('recruiter_pending')  # or an appropriate page if the recruiter does not exist
    error = None
    if request.method == "POST":
        s = request.POST['status']
        recruiter.status = s
        try:
            recruiter.save()
            error = "no"
        except:
            error = "yes"

    d = {'recruiter': recruiter, 'error': error}
    return render(request, 'change_status.html', d)

def recruiteraccept(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Accepted')
    d={'data':data}
    return render(request,'recruiteraccept.html',d)

def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Rejected')
    d={'data':data}
    return render(request,'recruiter_rejected.html',d)

def all_recruiters(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    d={'data':data}
    return render(request,'all_recruiters.html',d)

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter=User.objects.get(id=pid)
    recruiter.delete()
   
    return redirect('all_recruiters')

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = None
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']    
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error="not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'change_passwordadmin.html', d)

def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = None
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']    
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error="not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'change_passworduser.html', d)

def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = None
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']    
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error="not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'change_passwordrecruiter.html', d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    
    error = ""
    if request.method == 'POST':
        jt = request.POST.get('jobtitle')
        sd = request.POST.get('startdate')
        ed = request.POST.get('enddate')
        s = request.POST.get('salary')
        l = request.FILES.get('logo')
        d = request.POST.get('description')
        sk = request.POST.get('skill')
        exp = request.POST.get('experience')
        loc = request.POST.get('location')
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        try:
            Job.objects.create(
                recruiter=recruiter,
                start_date=sd,
                end_date=ed,
                title=jt,
                salary=s,
                image=l,
                description=d,
                skills=sk,
                experience=exp,
                location=loc,
                creationdate=date.today()
            )
            error = "no"
        except Exception as e:
            error = f"yes: {str(e)}"
    
    d = {'error': error}
    return render(request, 'add_job.html', d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request, 'job_list.html',d)

def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job=Job.objects.get(id=pid)
    if request.method == 'POST':
        jt = request.POST.get('jobtitle')
        sd = request.POST.get('startdate')
        ed = request.POST.get('enddate')
        s = request.POST.get('salary')
        d = request.POST.get('description')
        sk = request.POST.get('skill')
        exp = request.POST.get('experience')
        loc = request.POST.get('location')
        job.title=jt
        job.salary=s
        job.experience=exp
        job.location=loc
        job.description=d
        job.skills=sk
        try:
            job.save()
            error = "no"
        except Exception as e:

            error = f"yes: {str(e)}"
        if sd:
            try:
                job.start_date=sd
                job.save()
            except:
                pass
        else:
            pass
        if ed:
            try:
                job.end_date=ed
                job.save()
            except:
                pass
        else:
            pass
    
    d = {'error': error,'job':job}
    return render(request, 'edit_jobdetail.html', d)


def change_companylogo(request, pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id=pid)
    if request.method == 'POST':
        cl = request.FILES.get('logo')
        if cl:
            job.image = cl
            try:
                job.save()
                error = "no"
            except Exception as e:
                error = f"yes: {str(e)}"
        else:
            error = "yes: No file uploaded"
    
    d = {'error': error, 'job': job}
    return render(request, 'change_companylogo.html', d)

def applyforjob(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')

    error = ""
    user = request.user
    student = StudentUser.objects.get(user=user)
    job = Job.objects.get(id=pid)
    date1 = date.today()

    if job.end_date < date1:
        error = "no"
    elif job.start_date > date1:
        error = "notopen"
    else:
        if request.method == 'POST':
            r = request.FILES['resume']
            Apply.objects.create(job=job, student=student, resume=r, applydate=date.today())
            error = "Done"

    d = {'error': error}
    return render(request, 'applyforjob.html', d)

def candidates_applied(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    
    data = Apply.objects.all()
    
    d = {'data': data}
    return render(request, 'candidates_applied.html', d)

def delete_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    job = Job.objects.get(id=job_id)
    job.delete()
    return redirect('job_list')  # Redirect to the job list page after deletion
from django.shortcuts import render, redirect
from .models import Job, Apply, StudentUser

def recommend_jobs(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    user = request.user
    try:
        student = StudentUser.objects.get(user=user)
    except StudentUser.DoesNotExist:
        return render(request, 'recommendation.html', {'recommended_jobs': []})

    user_skills = set(skill.strip() for skill in student.skill_list.split(',') if skill.strip())  # Convert skill_list to a set of skills

    # Get applied jobs
    applied_jobs = Apply.objects.filter(student=student).values_list('job', flat=True)

    # Fetch all jobs excluding those already applied
    all_jobs = Job.objects.exclude(id__in=applied_jobs)
    recommended_jobs = []

    for job in all_jobs:
        job_skills = set(skill.strip() for skill in job.skills.split(',') if skill.strip())  # Convert job skills to a set of skills
        # Calculate the number of matching skills
        matching_skills = user_skills.intersection(job_skills)
        if matching_skills:
            recommended_jobs.append((job, len(matching_skills)))

    # Sort jobs by the number of matching skills in descending order
    recommended_jobs.sort(key=lambda x: x[1], reverse=True)

    context = {
        'recommended_jobs': [job for job, match_count in recommended_jobs]
    }

    return render(request, 'recommendation.html', context)

 
def Logout(request):
    logout(request)
    return redirect('index')
    
def re_register(request):
    error = ""
    success_message = ""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company = request.POST.get('company')
        email = request.POST.get('email')
        username = email
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')

        if password != confirm_password:
            error = "Passwords do not match"
        else:
            try:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_active=False)
                Recruiter.objects.create(user=user, mobile=contact, image=image, gender=gender, company=company, type="recruiter", status="pending")

                # Send activation email
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                send_mail(mail_subject, message, 'djangoproject33@gmail.com', [email])
                
                success_message = "A confirmation email has been sent to your email address. Please check your email to activate your account."
            except IntegrityError:
                error = "Username already exists"
            except Exception as ex:
                print(f"Exception occurred: {ex}")
                error = "An error occurred during registration"
    
    return render(request, 're_register.html', {'error': error, 'success_message': success_message})




def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'acc_active_success.html')
    else:
        return render(request, 'acc_active_invalid.html')






def register(request):
    error = ""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = email
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')
        skill_list = request.POST.get('skill_list')

        if password != confirm_password:
            error = "Passwords do not match"
        else:
            try:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                StudentUser.objects.create(user=user, mobile=contact, image=image, gender=gender, type="student",skill_list=skill_list)
                error = "no"
            except Exception as ex:
                print(f"Exception occurred: {ex}")
                error = str(ex)
    
    return render(request, 'register.html', {'error': error})

def update_application_status(request, pk):
    application = get_object_or_404(Apply, pk=pk)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('candidates_applied')
    else:
        form = ApplicationStatusForm(instance=application)
    return render(request, 'update_application_status.html', {'form': form})

