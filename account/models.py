from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

# Create your models here.


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_registrar1 = models.BooleanField('Is student registrar', default=False)
    is_registrar2 = models.BooleanField('Is staff registrar', default=False)
    is_cashier = models.BooleanField('Is cashier', default=False)
    is_expenses = models.BooleanField('Is expenses', default=False)
    is_daily_report = models.BooleanField('Is Daily report', default=False)
    is_weekly_report = models.BooleanField('Is Weekly report', default=False)
    is_monthly_report = models.BooleanField('Is Monthly report', default=False)
    is_expenses_report = models.BooleanField('Is Expenses report', default=False)
    is_add = models.BooleanField('Is add', default=False)
    nin = models.CharField(max_length=255, blank=True)
    phone_num = models.CharField(max_length=255, blank=True)



class Intakes(models.Model):
    id = models.AutoField(primary_key=True)
    intake_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Departments(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Programme(models.Model):
    id = models.AutoField(primary_key=True)
    programme_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Paymenttype(models.Model):
    id = models.AutoField(primary_key=True)
    ptype_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# STUDENT_STATUS_CHOICES = (
#     ("applicant", "Applicant"),
#     ("current", "Current"),
# )


class student_status(models.Model):
    id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=50)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, blank=True, null=True)
    intake = models.ForeignKey(Intakes, on_delete=models.CASCADE,blank=True, null=True)
    department = models.ForeignKey(Departments,on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(student_status,on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField()
    nin = models.CharField(max_length=400, blank=True, null=True)
    ip_id = models.CharField(max_length=400, blank=True, null=True)
    totalFee = models.CharField(max_length=255, blank=True, null=True)
    student_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    first_name = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()




class Reciept(models.Model):
    TERMS = [
    ('14 days', '14 days'),
    ('30 days', '30 days'),
    ('60 days', '60 days'),
    ]

    TYPE = [
    ('cash', 'cash'),
    ('transfer', 'transfer'),
    ]

    STATUS = [
    ('TUTION', 'TUTION'),
    ('APPLICATION', 'APPLICATION'),
    ('ACCEPTANCE', 'ACCEPTANCE'),
    ('OTHERS', 'OTHERS'),
    ]
    date = models.DateField(auto_now=True, blank=True, null=True)
    # transaction_date = models.DateTimeField(auto_now_add=True, default='', db_index=True)
    student_name = models.CharField(max_length=255, blank=True, null=True)
    student_id = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    # student = models.ForeignKey(Students, on_delete=models.SET_NULL, blank=True, null=True)
    tution = models.BooleanField(default=False)
    acceptance = models.BooleanField(default=False)
    application = models.BooleanField(default=False)
    others = models.BooleanField(default=False)
    stu_programme = models.CharField(max_length=255, blank=True, null=True)
    stu_nin = models.CharField(max_length=255, blank=True, null=True)
    ptype = models.ForeignKey(Paymenttype, on_delete=models.CASCADE, blank=True, null=True)
    # type = models.CharField(choices=TYPE, default='cash', max_length=100)
    amount = models.CharField(blank=True, null=True, max_length=100)
    # paymentTerms = models.CharField(choices=TERMS, default='14 days', max_length=100)
    total = models.FloatField(default=0)
    balance = models.FloatField(default=0)

class Invoice(models.Model):
    TERMS = [
    ('14 days', '14 days'),
    ('30 days', '30 days'),
    ('60 days', '60 days'),
    ]

    TYPE = [
    ('cash', 'cash'),
    ('transfer', 'transfer'),
    ]

    STATUS = [
    ('TUTION', 'TUTION'),
    ('APPLICATION', 'APPLICATION'),
    ('ACCEPTANCE', 'ACCEPTANCE'),
    ('OTHERS', 'OTHERS'),
    ]
    date = models.DateField(blank=True, null=True)
    student = models.ForeignKey(Students, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(choices=STATUS, default='TUTION', max_length=100)
    type = models.CharField(choices=TYPE, default='cash', max_length=100)
    amount = models.CharField(blank=True, null=True, max_length=100)
    paymentTerms = models.CharField(choices=TERMS, default='14 days', max_length=100)
    total = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField(default=0)
    product_unit = models.CharField(max_length=255)
    product_is_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product_name)

class Sop(models.Model):
    date = models.DateField()
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)





class Cons(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    one = models.CharField(max_length=255, blank=True, null=True)
    amountOne = models.CharField(max_length=255, blank=True, null=True)
    two = models.CharField(max_length=255, blank=True, null=True)
    amountTwo = models.CharField(max_length=255, blank=True, null=True)
    three = models.CharField(max_length=255, blank=True, null=True)
    amountThree = models.CharField(max_length=255, blank=True, null=True)
    four = models.CharField(max_length=255, blank=True, null=True)
    amountFour = models.CharField(max_length=255, blank=True, null=True)
    five = models.CharField(max_length=255, blank=True, null=True)
    amountFive = models.CharField(max_length=255, blank=True, null=True)
    is_approved = models.BooleanField(default=False)


class SopDetail(models.Model):
    sop = models.ForeignKey(Sop, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField(default=0)

    @property
    def get_total_bill(self):
        total = float(self.product.product_price) * float(self.amount)
        return total


