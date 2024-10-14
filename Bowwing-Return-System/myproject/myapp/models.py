from django.db import models
from django.core.exceptions import ValidationError
from django.db.backends.signals import connection_created
from django.dispatch import receiver

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    kkumail = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=17)
    password = models.CharField(max_length=20)
    student_id_edu = models.CharField(max_length=10)
    major = models.CharField(max_length=100)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.kkumail
    
    @property
    def is_authenticated(self):
        return True

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=17)
    password = models.CharField(max_length=20)
    employee_id = models.CharField(max_length=10)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email
    
    @property
    def is_authenticated(self):
        return True


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username= models.CharField(max_length=100, default="admin")
    email = models.EmailField(max_length=100, default="admin@kku.ac.th")
    password = models.CharField(max_length=20, default="admin1234")
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email
    
    @property
    def is_authenticated(self):
        return True

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
    
class Borrowing(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, to_field='equipment_id')
    borrower = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrowed_on = models.DateTimeField(null=True, blank=True)
    returned_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.borrower.username} want to borrow {self.equipment}"
    
@receiver(connection_created)
def enforce_foreign_keys(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')