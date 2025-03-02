from datetime import datetime
from os.path import exists
from django.contrib.auth import authenticate, login as dj_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect

# file render
import os
import pdfkit
from django.template.loader import get_template
from pyvirtualdisplay import Display
from qrcode import *
from django.template.loader import render_to_string
from django.core.files import File
# endfile render

from index.util.types import *
from .models import *
from django.db import transaction, IntegrityError
import random
def Home(request):
    global data
    if request.method == "POST":
        data = request.POST['data']
        img = make(data)
        img.save('data/qr_codes/test.png')
    return render(request, "home.html")

def login_page(request):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    request.session['captcha_result'] = num1 + num2
    context = {
        'num1': num1,
        'num2': num2,
    }
    return render(request, "worker/login_page.html", context)


def sign_in(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        captcha_result = request.POST.get('captcha_result')
        expected_result = request.session.get('captcha_result')
        user = authenticate(request, username=login, password=password)
        # Check CAPTCHA
        if str(captcha_result) != str(expected_result):
            messages.error(request, 'Tizimga kirish uchun topshiriq yechimi noto\'g\'ri kiritildi!')
            return redirect('sign_in')

        if user is not None:
            dj_login(request, user)
            messages.success(request, 'Siz tizimga kirdingiz')
            return redirect('worker_home_page')
        else:
            messages.error(request, 'Login yoki parol xato')
            return redirect('login_page')

    # Generate CAPTCHA
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    request.session['captcha_result'] = num1 + num2
    context = {
        'num1': num1,
        'num2': num2,
    }
    return render(request, 'worker/login_page.html', context)

# def sign_in(request):
#     if request.method == "POST":
#         login = request.POST['login']
#         password = request.POST['password']
#         user = authenticate(request, username=login, password=password)
#         if user is not None:
#             dj_login(request, user)
#
#             messages.success(request, 'Siz tizimga kirdingiz')
#             return redirect('worker_home_page')
#         else:
#             messages.error(request, 'Login yoki parol xato')
#             return redirect('login_page')


def search(request):
    if request.method == "POST":
        code = request.POST['search_code']
        values = code.split("-", 1)

        if code:
            seria = values[0]
            number = values[1]
            certificate = Certificate.objects.filter(number=number, seria=seria, permission=True).first()
            if certificate:
                msg = msg_type.isset
                content = {'work': certificate, 'msg': msg}
                messages.success(request, 'Sertifikat mavjud')
                return render(request, "home.html", content)

        messages.error(request, 'Kiritilgan seria va nomerdagi sertifikat topilmadi!')
        return render(request, "home.html")

def search_big(request):
    if request.method == "POST":
        seria = request.POST['seria']
        number = request.POST['number']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        fathername = request.POST['fathername']
        time_from = request.POST['time_from']
        time_to = request.POST['time_to']
        hours = request.POST['hours']
        name = request.POST['name']

        content = {}
        if seria:
            certificate = Certificate.objects.filter(seria=seria).all()
        if number:
            certificate = Certificate.objects.filter(number=number).all()
        if firstname:
            certificate = Certificate.objects.filter(user_firstname=firstname).all()
        if lastname:
            certificate = Certificate.objects.filter(user_lastname=lastname).all()
        if fathername:
            certificate = Certificate.objects.filter(user_fathername=fathername).all()
        if firstname:
            certificate = Certificate.objects.filter(firstname=firstname).all()

        # ko'rish kerak
        if time_to and time_from:
            certificate = Certificate.objects.filter(issue_date__gte=time_from, expiry_date__lte=time_to).all()
        # ko'rish kerak
        
        if hours:
            certificate = Certificate.objects.filter(hours=hours).all()
        if name:
            certificate = Certificate.objects.filter(name__contains=name).all()

        content = {'works': certificate}
        return render(request, "worker/home_page.html", content)


@login_required(login_url='/login_page')
def worker_home_page(request):

    works = Certificate.objects.all().order_by('-id').values()
    content = {'works': works}
    return render(request, "worker/home_page.html", content)



def generete_num(number):
    numstr = str(number)

    while len(numstr) != 3:
        numstr = '0'+numstr

    date = datetime.now()
    year = date.year % 100
    month = '%02d' % date.month
    number = str(numstr) + str(month) + str(year)
    return number



def create_certificate(request):
    if request.method == "POST":

        seria = request.POST['seria']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        fathername = request.POST['fathername']

        name = request.POST['name']
        hours = request.POST['hours']
        teacher = request.POST['teacher']
        from_time = request.POST['from']
        to_time = request.POST['to']

        try:
            with transaction.atomic():
                certificate = Certificate(seria=seria, user_fathername=fathername,
                                          name=name, hours=hours,teacher=teacher,
                                          user_firstname=firstname, user_lastname=lastname,
                                          issue_date=from_time,
                                          expiry_date=to_time)
                certificate.save()


                messages.success(request, 'Talabnoma yaratildi')
                return redirect('worker_home_page')

        except IntegrityError:
            messages.error(request, 'Ma\'lumotlar bazasiga saqlashda xatolik bor')
            return redirect('worker_home_page')


def delete(request,id):

    certificate = Certificate.objects.filter(id=id).first()
    certificate.delete()

    messages.error(request, 'Sertifikat o\'chirildi')
    return redirect('worker_home_page')

def show(request,id):

    certificate = Certificate.objects.filter(id=id).first()
    content = {'work':certificate}

    return render(request, "worker/show.html", content)

def edit(request,id):
    certificate = Certificate.objects.filter(id=id).first()
    content = {'work':certificate}
    return render(request, "worker/edit.html", content)

def edit_certificate(request,id):
    if request.method == "POST":
        seria = request.POST['seria']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        fathername = request.POST['fathername']

        name = request.POST['name']
        hours = request.POST['hours']
        teacher = request.POST['teacher']
        from_time = request.POST['from']
        to_time = request.POST['to']

        certificate = Certificate.objects.filter(id=id).first()
        if certificate:
            certificate.seria = seria
            certificate.user_fathername = fathername
            certificate.name = name
            certificate.hours = hours
            certificate.teacher = teacher
            certificate.user_firstname = firstname
            certificate.user_lastname = lastname
            if from_time:
                certificate.issue_date = from_time
            else:
                certificate.issue_date = certificate.issue_date
            if from_time:
                certificate.expiry_date = to_time
            else:
                certificate.expiry_date = certificate.expiry_date
            certificate.save()
            messages.success(request, "Ma'lumotlar o'zgartirildi")
            return redirect('edit',id=id)
        else:
            messages.error(request, "Ma'lumotlar topilmadi bu ID da")
            return redirect('edit', id=id)



def give_permission(request,id):
    if request.method == "POST":
        try:
            with transaction.atomic():
                certificate = Certificate.objects.filter(id=id).first()
                certificate.permission = True
                certificate.save()

                today = datetime.now()
                works = Certificate.objects.filter(active_time__month=today.month, permission=True,
                                                   active_time__year=today.year).count()
                print('==>', works)
                from_time = certificate.issue_date.strftime("%d-%m-%Y")
                to_time = certificate.expiry_date.strftime("%d-%m-%Y")
                if certificate.number:
                    number = certificate.number
                else:
                    number = generete_num(works)


                url = f"https://certificate.dshk.uz/data/certificates/{certificate.seria}-{number}.pdf"
                img = make(url, border=0)
                img.save('data/qr_codes/test.png')

                template = get_template("rendered_file/render_file.html", using=None)

                qr_image = "data/qr_codes/test.png"

                print(number)
                contextPage = {
                    'firstname': certificate.user_firstname,
                    'lastname': certificate.user_lastname,
                    'fathername': certificate.user_fathername,
                    "from_time": from_time,
                    'to_time': to_time,
                    'hours': certificate.hours,
                    'name': certificate.name,
                    'seria': certificate.seria,
                    'number': number,
                    'teacher': certificate.teacher,
                    'qr_image': qr_image,
                    "director": "Yu.Magrupov",
                    "leader": "G.Xadjibaeva",
                }

                htmlPage = template.render(contextPage)

                options = {
                    'page-size': 'A4',
                    'encoding': "UTF-8",
                    'margin-top': '0.5in',
                    'margin-right': '0.5in',
                    'margin-bottom': '0.2in',
                    'margin-left': '0.5in',
                    'orientation': 'portrait',
                    "enable-local-file-access": "",
                    # landscape bu albomiy qiladi
                }
                display = Display(visible=0, size=(500, 500)).start()
                pdfkit.from_string(htmlPage, f"data/certificates/{certificate.seria}-{number}.pdf", options)

                print("=>", certificate.id)
                path = f"data/certificates/{certificate.seria}-{number}.pdf"
                print(path)

                certificate.file = path
                certificate.number = number
                certificate.save()

                messages.success(request, 'Tasdiqlandi')
                return redirect('worker_home_page')
        except IntegrityError:
            messages.error(request, 'Ma\'lumotlar bazasiga saqlashda xatolik bor')
            return redirect('worker_home_page')

def logout(request):
    auth_logout(request)
    return redirect('/login_page')

