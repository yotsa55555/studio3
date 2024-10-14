from django.db import models
from django.core.exceptions import ValidationError

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    kkumail = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=17)
    password = models.CharField(max_length=20)
    student_id_edu = models.CharField(max_length=10)
    major = models.CharField(max_length=100)

    def __str__(self):
        return f'Fullname: {self.fullname}, Usename: {self.username}, Phone number: {self.phone}'

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=17)
    password = models.CharField(max_length=20)
    employee_id = models.CharField(max_length=10)

    def __str__(self):
        return f"Staff: {self.fullname}, Username: {self.username}"


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username= models.CharField(max_length=100, default="admin")
    email = models.EmailField(max_length=100, default="admin@kku.ac.th")
    password = models.CharField(max_length=20, default="admin1234")

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/', default='media/images/default.jpg')
    name = models.CharField(max_length=100)
    parcel_id = models.CharField(max_length=20)
    brand = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    date_borrow = models.DateField(null=True, blank=True, help_text="Date when the item was borrowed")
    date_return = models.DateField(null=True, blank=True, help_text="Date when the item is returned")
    borrower = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    STATUS_CHOICES = [
        ("available", "Available"),
        ("borrowed", "Borrowed"),
    ]


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['parcel_id'], name='unique_parcel_id')
        ]

    def clean(self):
        if self.status:
            if not self.date_borrow or not self.date_return or not self.borrower:
                raise ValidationError("Both borrow and return dates are required when status is True.")
            if self.date_borrow > self.date_return:
                raise ValidationError("Borrow date cannot be after return date.")
        else:
            self.date_borrow = None
            self.date_return = None
            self.borrower = None

    def __str__(self):
        return f'Equipment: {self.name}, Status: {"Borrowed" if self.status else "Available"}'