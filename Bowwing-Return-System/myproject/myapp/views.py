from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from myapp.models import Student, Staff, Admin, Equipment, Borrowing
from django.db.models import Q
from django.core.exceptions import ValidationError

def home(request):
    all_student = Student.objects.all()
    return render(request, "home.html", {'all_student': all_student})

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        all_admin = Admin.objects.all()
        all_staff = Staff.objects.all()
        all_student = Student.objects.all()

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

@login_required
def catalog_user(request):
    all_equipment = Equipment.objects.all()
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
        "selected_status": selected_status,
        })

@login_required
def catalog_staff(request):
    all_equipment = Equipment.objects.all()
    selected_status = request.POST.get('filter')
    query = request.GET.get("q")
    print(selected_status)
    if query:
        all_equipment = all_equipment.filter(borrower__fullname__icontains=query)

    if selected_status:
        if selected_status == "Unavailable":
            all_equipment = Equipment.objects.filter(status = True)
        elif selected_status == "Available":
            all_equipment = Equipment.objects.filter(status = False)
        else:
            all_equipment = Equipment.objects.all()

    return render(request, "staff/catalog labstaff.html", {
        "all_equipment": all_equipment,
        "selected_status": selected_status,
        })

@login_required
def catalog_admin(request):
    devices = Equipment.objects.all()
    return render(request, "admin/catalog admin.html", {"devices": devices})

def borrow_view(request, equipment_id):
    equipment = Equipment.objects.get(equipment_id=equipment_id)
    if request.method == 'POST':
        date_borrow = request.POST.get('date_borrow')
        date_return = request.POST.get('date_return')
        borrow = Borrowing(equipment=equipment, borrower=request.user, borrowed_on=date_borrow, returned_on=date_return)
        borrow.save()
        print(borrow)
        return redirect('catalog_user')
    return render(request, 'user/borrow_user.html', {"equipment": equipment})

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

    return render(request, "admin/edit admin.html", {"device": device})


def home_admin(request):
    return render(request, "admin/home_admin.html")

def report_admin(request):
    return render(request, "admin/Dashboard.html")

def history_admin(request):
    return render(request, "admin/history_admin.html")
