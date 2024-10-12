from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.models import Student, Staff, Admin, Equipment, Status
from .borrowing import BorrowingForm
from django.db.models import Q

def home(request):
    all_student = Student.objects.all()
    return render(request, "home.html", {'all_student': all_student})

def login(request):
    if request.method == "POST":
        all_student = Student.objects.all()
        all_staff = Staff.objects.all()
        all_admin = Admin.objects.all()

        kkumail = request.POST['kkumail']
        password = request.POST['password']

        for student in all_student:
            if kkumail == student.kkumail and password == student.password:
                return redirect('catalog_user')
            
        for staff in all_staff:
            if kkumail == staff.email and password == staff.password:
                return redirect('catalog_staff')
            
        for admin in all_admin:
            if kkumail == admin.email and password == admin.password:
                return redirect('catalog_admin')
            else:
                messages.error(request, 'Your email or password is incorrect!')
                return redirect('login')

    return render(request, "login.html")

def registor(request):
    if request.method == "POST":
        #get info
        fullname = request.POST['fullname']
        username = request.POST['username']
        kkumail = request.POST['kkumail']
        phone = request.POST['phone']
        password = request.POST['password']
        student_id_edu = request.POST['student_id_edu']
        major = request.POST['Major']
        print(f"fullname: {fullname}\nusername: {username}\nkkumail: {kkumail}\nphone: {phone}\npassword: {password}\nstudent id: {student_id_edu}\nmajor: {major}")
        
        #save info
        student = Student.objects.create(
            fullname = fullname,
            username = username,
            kkumail = kkumail,
            phone = phone,
            password = password,
            student_id_edu = student_id_edu,
            major = major
        )
        student.save()
        return redirect('login')
    
    return render(request, "registor.html")

def catalog_user(request):
    all_equipment = Equipment.objects.all()
    all_status = Status.objects.all()
    selected_status = request.POST.get('filter')
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
            all_equipment = Equipment.objects.filter(status = True)
        elif selected_status == "Available":
            all_equipment = Equipment.objects.filter(status = False)
        else:
            all_equipment = Equipment.objects.all()

    return render(request, "user/catalog_user.html", {
        "all_equipment": all_equipment,
        "all_status": all_status,
        "selected_status": selected_status,
        })


def catalog_staff(request):
    all_equipment = Equipment.objects.all()
    all_status = Status.objects.all()
    selected_status = request.POST.get('filter')
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
            all_equipment = Equipment.objects.filter(status = True)
        elif selected_status == "Available":
            all_equipment = Equipment.objects.filter(status = False)
        else:
            all_equipment = Equipment.objects.all()

    return render(request, "staff/catalog labstaff.html", {
        "all_equipment": all_equipment,
        "all_status": all_status,
        "selected_status": selected_status,
        })

def catalog_admin(request):
    return render(request, "admin/catalog admin.html")

def borrow_view(request, equipment_id):
    equipment = Equipment.objects.get(equipment_id=equipment_id)

    return render(request, 'user/borrow_user.html', {"equipment": equipment})

def home_staff(request):
    return render(request, "staff/home_staff.html")

def approval_staff(request):
    return render(request, "staff/approval_staff.html")

def history_staff(request):
    return render(request, "staff/borrow_lab.html")

def home_user(request):
    return render(request, "user/home_user.html")

def edit_admin(request):
    return render(request, "admin/edit admin.html")

def home_admin(request):
    return render(request, "admin/home_admin.html")

def report_admin(request):
    return render(request, "admin/Dashboard.html")

def history_admin(request):
    return render(request, "admin/history_admin.html")
