from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Event(models.Model):
    event_id=models.AutoField(primary_key=True)
    event_no=models.IntegerField()
    event_date=models.DateField()
    event_hall=models.CharField(max_length=1)
    event_slot=models.CharField(max_length=20)
    event_booking_date=models.DateField()
    event_cust_name=models.CharField(max_length=70)
    event_cust_email=models.EmailField(max_length=264)
    event_cust_contactno=models.TextField(max_length=20)
    event_cust_contactno2 = models.TextField(max_length=20)
    event_cust_nic=models.TextField(max_length=15)
    event_total_guests=models.IntegerField()
    event_total_amount=models.BigIntegerField()
    event_advance=models.BigIntegerField()
    event_total_expense=models.BigIntegerField()
    event_payments_details=models.TextField(null=True,blank=True)
    event_details=models.TextField(null=True,blank=True)
    conclude_event=models.CharField(default=False,max_length=20)
    additional_cost_perhead=models.IntegerField(default=0)
    additional_overall_cost=models.IntegerField(default=0)
    discount = models.IntegerField(default=0)


    def __str__(self):
        return str(self.event_id)


class Employee(models.Model):
    emp_id=models.AutoField(primary_key=True)
    emp_name=models.CharField(max_length=264)
    emp_joindate=models.DateField()
    emp_salary=models.IntegerField()
    emp_status=models.CharField(max_length=30)
    emp_designation=models.CharField(max_length=100)

    def __str__(self):
        return str(self.emp_id)

class Attendance(models.Model):
    att_id=models.AutoField(primary_key=True)
    att_emp_id=models.ForeignKey(Employee)
    att_date=models.DateField()
    att_status=models.CharField(max_length=30)

    def __str__(self):
        return str(self.att_id)

class Salary(models.Model):
    salary_id=models.AutoField(primary_key=True)
    salary_emp_id=models.ForeignKey(Employee)
    salary_month=models.DateField()
    salary_amount_paid=models.IntegerField()
    salary_total_amount=models.IntegerField()
    paid_status=models.CharField(max_length=30)
    salary_remarks=models.CharField(max_length=500)
    loan=models.CharField(max_length=1000,default=0)
    advance=models.CharField(max_length=1000,default=0)

    def __str__(self):
        return str(self.salary_id)

class Business_Details(models.Model):
    business_details_id=models.IntegerField(primary_key=True)
    business_logo=models.ImageField()
    business_name=models.CharField(max_length=500)
    business_ownername = models.CharField(max_length=70)
    business_ownername2 = models.CharField(max_length=70)
    business_owner_contactno = models.CharField(max_length=20)
    business_owner_contactno2 = models.CharField(max_length=20)

    def __str__(self):
        return str(self.business_details_id)


class Arrangement(models.Model):
    arrange_id=models.AutoField(primary_key=True)
    arrange_title=models.CharField(max_length=200)
    arrange_cost=models.IntegerField()
    arrange_details=models.CharField(max_length=1000)
    arrange_status=models.CharField(max_length=50)

    def __str__(self):
        return str(self.arrange_id)

class Special_Arrangement(models.Model):
    special_arrange_id=models.AutoField(primary_key=True)
    special_arrange_title=models.CharField(max_length=200)
    special_arrange_cost=models.IntegerField()
    special_arrange_details=models.CharField(max_length=1000)
    special_arrange_status=models.CharField(max_length=50)

    def __str__(self):
        return str(self.special_arrange_id)

class Event_Special_Arrangement(models.Model):
    event_special_arrangement_id = models.AutoField(primary_key=True,default=None)
    event_arrangement_event_id = models.ForeignKey(Event, null=True)
    event_special_arrange_id=models.ForeignKey(Special_Arrangement,null=True,default=None)
    event_arrange_quantity = models.IntegerField(default=0)
    event_arrange_cost = models.IntegerField()
    event_arrange_details=models.CharField(max_length=50,default="")
    event_arrange_title=models.CharField(max_length=60,default="")

    def __str__(self):
        return str(self.event_special_arrangement_id)

class Event_Arrangement(models.Model):
    event_arrangement_id=models.AutoField(primary_key=True)
    event_arrangement_event_id=models.ForeignKey(Event,null=True)
    event_arrangement_arrange_id=models.ForeignKey(Arrangement,null=True)
    event_arrange_cost=models.IntegerField()
    event_arrange_details=models.TextField()
    event_arrange_quantity=models.IntegerField(default=0)

    def __str__(self):
       return str(self.event_arrangement_id)

class Booked_Slot(models.Model):
    booked_id=models.AutoField(primary_key=True)
    booked_slot_event_id=models.ForeignKey(Event)
    booked_date=models.DateField()
    booked_hall=models.CharField(max_length=2)
    booked_slot=models.CharField(max_length=50)

    def __str__(self):
        return str(self.booked_id)

class Print(models.Model):
    print_id=models.AutoField(primary_key=True)
    print_details=models.CharField(max_length=50,default="")

    def __str__(self):
        return str(self.print_id)

class Expense(models.Model):
    expense_id=models.AutoField(primary_key=True)
    expense_event_id=models.ForeignKey(Event,null=True)
    expense_title=models.CharField(max_length=100)
    expense_date=models.DateField()
    expense_details=models.TextField()
    expense_amount=models.BigIntegerField()


    def __str__(self):
        return str(self.expense_id)

class Menu(models.Model):
    menu_id=models.AutoField(primary_key=True)
    menu_title=models.CharField(max_length=500)
    menu_cost_perhead=models.IntegerField()
    menu_details=models.TextField()
    menu_status=models.CharField(max_length=50)


    def __str__(self):
        return str(self.menu_id)

class Event_Menu(models.Model):
    event_menu_id=models.AutoField(primary_key=True)
    event_menu_event_id=models.ForeignKey(Event,null=True)
    event_menu_menu_id=models.ForeignKey(Menu,null=True)
    menu_cost_perhead=models.IntegerField()
    menu_details=models.TextField()

    def __str__(self):
        return str(self.event_menu_id)


class Terms(models.Model):
    term_id=models.IntegerField(primary_key=True)
    term_title=models.CharField(max_length=100)
    term_statement=models.TextField()

    def __str__(self):
        return str(self.term_id)

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return str(self.user.username)

