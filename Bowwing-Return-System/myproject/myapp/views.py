<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.models import Student, Staff, Admin, Equipment, Status
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from .borrowing import BorrowingForm
from django.db.models import Q
from myapp.models import Equipment
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Staff, Admin
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import random
import string

=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from myapp.models import Student, Staff, Admin, Equipment, Borrowing
from django.db.models import Q
from django.core.exceptions import ValidationError
>>>>>>> 4d37d50192df075348887d69b36444bd3702e540

def home(request):
    all_student = Student.objects.all()
    return render(request, "home.html", {"all_student": all_student})


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

<<<<<<< HEAD
        kkumail = request.POST["kkumail"]
        password = request.POST["password"]

        for student in all_student:
            if kkumail == student.kkumail and password == student.password:
                return redirect("catalog_user")

        for staff in all_staff:
            if kkumail == staff.email and password == staff.password:
                return redirect("catalog_staff")

        for admin in all_admin:
            if kkumail == admin.email and password == admin.password:
                return redirect("catalog_admin")
            else:
                messages.error(request, "Your email or password is incorrect!")
                return redirect("login")

    return render(request, "login.html")

=======
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            try:
                if Admin.objects.get(email=user):
                    print("admin checked!")
                    login(request, user)
                    return redirect('catalog_admin')
            except:
                try:
                    if Staff.objects.get(email=user):
                        print("staff checked!")
                        login(request, user)
                        return redirect('catalog_staff')
                except:
                    try:    
                        if Student.objects.get(kkumail=user):
                                print("student checked!")
                                login(request, user)
                                return redirect('catalog_user')
                    except:
                        messages.error(request, 'Invalid credentials')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect('login')
>>>>>>> 4d37d50192df075348887d69b36444bd3702e540

def registor(request):
    if request.method == "POST":
        # get info
        fullname = request.POST["fullname"]
        username = request.POST["username"]
        kkumail = request.POST["kkumail"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        student_id_edu = request.POST["student_id_edu"]
        major = request.POST["Major"]
        print(
            f"fullname: {fullname}\nusername: {username}\nkkumail: {kkumail}\nphone: {phone}\npassword: {password}\nstudent id: {student_id_edu}\nmajor: {major}"
        )

        # save info
        student = Student.objects.create(
            fullname=fullname,
            username=username,
            kkumail=kkumail,
            phone=phone,
            password=password,
            student_id_edu=student_id_edu,
            major=major,
        )
        student.save()
        return redirect("login")

    return render(request, "registor.html")

<<<<<<< HEAD

def catalog_user(request):
    all_equipment = Equipment.objects.all()
    all_status = Status.objects.all()
    selected_status = request.POST.get("filter")
=======
@login_required
def catalog_user(request):
    all_equipment = Equipment.objects.all()
    selected_status = request.POST.get('filter')
>>>>>>> 4d37d50192df075348887d69b36444bd3702e540
    query = request.GET.get("q")
    print(selected_status)

    if query:
        all_equipment = all_equipment.filter(
            Q(name__icontains=query)
            | Q(brand__icontains=query)
            | Q(parcel_id__icontains=query)
        )

    if selected_status:
        if selected_status == "Unavailable":
            all_equipment = Equipment.objects.filter(status=True)
        elif selected_status == "Available":
            all_equipment = Equipment.objects.filter(status=False)
        else:
            all_equipment = Equipment.objects.all()

<<<<<<< HEAD
    return render(
        request,
        "user/catalog_user.html",
        {
            "all_equipment": all_equipment,
            "all_status": all_status,
            "selected_status": selected_status,
        },
    )
=======
    return render(request, "user/catalog_user.html", {
        "all_equipment": all_equipment,
        "selected_status": selected_status,
        })
>>>>>>> 4d37d50192df075348887d69b36444bd3702e540

@login_required
def catalog_staff(request):
    all_equipment = Equipment.objects.all()
<<<<<<< HEAD
    all_status = Status.objects.all()
    selected_status = request.POST.get("filter")
=======
    selected_status = request.POST.get('filter')
>>>>>>> 4d37d50192df075348887d69b36444bd3702e540
    query = request.GET.get("q")
    print(selected_status)
    if query:
        all_equipment = all_equipment.filter(borrower__fullname__icontains=query)

    if selected_status:
        if selected_status == "Unavailable":
            all_equipment = Equipment.objects.filter(status=True)
        elif selected_status == "Available":
            all_equipment = Equipment.objects.filter(status=False)
        else:
            all_equipment = Equipment.objects.all()

<<<<<<< HEAD
    return render(
        request,
        "staff/catalog labstaff.html",
        {
            "all_equipment": all_equipment,
            "all_status": all_status,
            "selected_status": selected_status,
        },
    )

=======
    return render(request, "staff/catalog labstaff.html", {
        "all_equipment": all_equipment,
        "selected_status": selected_status,
        })
>>>>>>> 4d37d50192df075348887d69b36444bd3702e540

@login_required
def catalog_admin(request):
    devices = Equipment.objects.all()
    selected_status = request.POST.get('filter')
    query = request.GET.get("q")
    print(selected_status)
    if query:
        devices = devices.filter(borrower__fullname__icontains=query)

<<<<<<< HEAD

def borrow_view(request):
    form = BorrowingForm()
=======
    if selected_status:
        if selected_status == "Unavailable":
            devices = Equipment.objects.filter(status=True)
        elif selected_status == "Available":
            devices = Equipment.objects.filter(status=False)
        else:
            devices = Equipment.objects.all()
>>>>>>> 4d37d50192df075348887d69b36444bd3702e540

    return render(request, "admin1/catalog admin.html", {
        "devices": devices,
        "selected_status": selected_status,
        })
    # return render(request, "admin1/catalog admin.html", {"devices": devices})

<<<<<<< HEAD
    return render(
        request, "user/borrow_user.html", {"form": form, "products": products}
    )

=======
def borrow_view(request, equipment_id):
    equipment = Equipment.objects.get(equipment_id=equipment_id)
    if request.method == 'POST':
        date_borrow = request.POST.get('date_borrow')
        date_return = request.POST.get('date_return')
        all_borrow = Borrowing.objects.all()
        for borrow in all_borrow:
            if borrow.equipment == equipment and borrow.borrower == request.user:
                borrow.borrowed_on = date_borrow
                borrow.returned_on = date_return
                borrow.save()
                return redirect('catalog_user')
                
        borrow = Borrowing(equipment=equipment, borrower=request.user, borrowed_on=date_borrow, returned_on=date_return)
        borrow.save()
        return redirect('catalog_user')
    return render(request, 'user/borrow_user.html', {"equipment": equipment})
>>>>>>> 4d37d50192df075348887d69b36444bd3702e540

def home_staff(request):
    return render(request, "staff/home_staff.html")


def approval_staff(request):
    all_borrow = Borrowing.objects.all()
    return render(request, "staff/approval_staff.html", { "all_borrow": all_borrow })

def borrow_pass(request, borrow_id):
    borrow = Borrowing.objects.get(id=borrow_id)
    equipment = Equipment.objects.get(equipment_id=borrow.equipment.equipment_id)
    if request.method == "POST":
        if 'action' in request.POST:
            if request.POST['action'] == 'agree':
                print('pass', borrow_id)
                equipment.status = True
                equipment.date_borrow = borrow.borrowed_on
                equipment.date_return = borrow.returned_on
                equipment.borrower = borrow.borrower
                equipment.save()
                borrow.delete()

            elif request.POST['action'] == 'disagree':
                print('no pass', borrow_id)
                borrow.delete()

    return redirect('approval_staff')

def return_item(request, equipment_id):
    equipment = Equipment.objects.get(equipment_id=equipment_id)
    if request.method == "POST":
        print('pass')
        equipment.status = False
        equipment.clean()
        equipment.save()
    return redirect('catalog_staff')


def history_staff(request):
    return render(request, "staff/history_staff.html")


def home_user(request):
    return render(request, "user/home_user.html")

def edit_admin(request, equipment_id):
    device = get_object_or_404(Equipment, equipment_id=equipment_id)

    if request.method == "POST":
        device.name = request.POST["deviceName"]
        device.parcel_id = request.POST["parcelName"]
        device.brand = request.POST["brand"]

        status = request.POST["status"]
        if status == "available":
            device.status = False
        elif status == "unavailable":
            device.status = True

        if request.FILES.get("uploadPhoto"):
            device.image = request.FILES["uploadPhoto"]

        try:
            device.clean()
            device.save()
            messages.success(request, "Device updated successfully!")
            return redirect("catalog_admin")
        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, "admin1/edit admin.html", {"device": device})

def delete_item(request, equipment_id):
    equipment = Equipment.objects.get(equipment_id=equipment_id)
    equipment.delete()
    return redirect("catalog_admin")

def add_item(request):
    if request.method == "POST":
        name = request.POST["deviceName"]
        parcel_id = request.POST["parcelName"]
        brand = request.POST["brand"]
        status = False
        image = request.FILES["uploadPhoto"]

        try:
            equipment = Equipment(image=image, name=name, parcel_id=parcel_id, brand=brand, status=status)
            equipment.save()
            messages.success(request, "Device add successfully!")
            return redirect("catalog_admin")
        except ValidationError as e:
            messages.error(request, e.message)
    return render(request, "admin1/add_item.html")

def home_admin(request):
    return render(request, "admin1/home_admin.html")


def report_admin(request):
    return render(request, "admin1/Dashboard.html")


def history_admin(request):
<<<<<<< HEAD
    return render(request, "admin/history_admin.html")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        user_type = None
        user = None
        try:
            student = Student.objects.get(kkumail=email)
            user = student
            user_type = "student"
        except Student.DoesNotExist:
            try:
                staff = Staff.objects.get(email=email)
                user = staff
                user_type = "staff"
            except Staff.DoesNotExist:
                try:
                    admin = Admin.objects.get(email=email)
                    user = admin
                    user_type = "admin"
                except Admin.DoesNotExist:
                    messages.error(request, "Email not found!")
                    return redirect("forgot_password")

        print(user)
        if user:
            try:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                mail_subject = "Reset your password"
                message = render_to_string(
                    "reset_password_email.html",
                    {
                        "user": user,
                        "uid": uid,
                        "token": token,
                    },
                )
                send_mail(mail_subject, message, "your_email@example.com", [email])
                messages.success(request, "A reset link has been sent to your email.")
                return redirect("login")
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            except Exception as e:
                return HttpResponse(f"Error occurred: {e}")

    return render(request, "forgot_password.html")


def reset_password(request, token):
    user = None
    for model in [Student, Staff, Admin]:
        try:
            user = model.objects.get(reset_token=token)
            break
        except model.DoesNotExist:
            continue

    if not user:
        messages.error(request, "Invalid or expired reset link.")
        return redirect("login")

    if request.method == "POST":
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        if new_password == confirm_password:
            user.password = new_password
            user.reset_token = None
            user.save()
            messages.success(request, "Password reset successfully.")
            return redirect("login")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, "reset_password.html")
=======
    return render(request, "admin1/history_admin.html")
>>>>>>> 4d37d50192df075348887d69b36444bd3702e540
