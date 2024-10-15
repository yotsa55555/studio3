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


def home(request):
    all_student = Student.objects.all()
    return render(request, "home.html", {"all_student": all_student})


def login(request):
    if request.method == "POST":
        all_student = Student.objects.all()
        all_staff = Staff.objects.all()
        all_admin = Admin.objects.all()

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


def catalog_user(request):
    all_equipment = Equipment.objects.all()
    all_status = Status.objects.all()
    selected_status = request.POST.get("filter")
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

    return render(
        request,
        "user/catalog_user.html",
        {
            "all_equipment": all_equipment,
            "all_status": all_status,
            "selected_status": selected_status,
        },
    )


def catalog_staff(request):
    all_equipment = Equipment.objects.all()
    all_status = Status.objects.all()
    selected_status = request.POST.get("filter")
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

    return render(
        request,
        "staff/catalog labstaff.html",
        {
            "all_equipment": all_equipment,
            "all_status": all_status,
            "selected_status": selected_status,
        },
    )


def catalog_admin(request):
    devices = Equipment.objects.all()
    return render(request, "admin/catalog admin.html", {"devices": devices})


def borrow_view(request):
    form = BorrowingForm()

    products = Equipment.objects.all()

    return render(
        request, "user/borrow_user.html", {"form": form, "products": products}
    )


def home_staff(request):
    return render(request, "staff/home_staff.html")


def approval_staff(request):
    return render(request, "staff/approval_staff.html")


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

    return render(request, "admin/edit admin.html", {"device": device})


def home_admin(request):
    return render(request, "admin/home_admin.html")


def report_admin(request):
    return render(request, "admin/Dashboard.html")


def history_admin(request):
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
