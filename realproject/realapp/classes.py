class User:
    def __init__(self,user_id,user_username,user_password):
        self.user_id=user_id
        self.user_username=user_username
        self.user_password=user_password

    def authenticate_user(self,username,password):
        if self.user_username==username and self.user_password==password:
            return True


class Moderator(User):
    def __init__(self,id,username,password,type,status):
        User.__init__(self,id,username,password)
        self.user_type=type
        self.isActive=status

    def authenticate_user(self,username,password):
        if self.user_username==username and self.user_password==password:
            return True

class Manager(User):
    def __init__(self,id,username,password,type):
        User.__init__(self,id,username,password)
        self.user_type=type

    def authenticate_user(self,username,password):
        if self.user_username==username and self.user_password==password:
            return True

class Facility:
    def __init__(self,id,title,detail,status):
        self.id=id
        self.title=title
        self.detail=detail
        self.status=status

class Menu(Facility):
    def __init__(self,id,title,detail,status,type,cost_per_head):
        Facility.__init__(self,id,title,detail,status)
        self.type=type
        self.cost_per_head=cost_per_head

    def get_menu(self,id):
        if self.id==id:
            return self.detail+self.title

class Arrangement(Facility):
    def __init__(self,id,title,detail,status,type,cost,extra_charges):
        Facility.__init__(self,id,title,detail,status)
        self.type=type
        self.cost_per_head=cost
        self.extra_charges=extra_charges

    def get_arrangement(self,id):
        if self.id==id:
            return self.detail+self.title

class Expense:
    def __init__(self,id,type,title,detail,amount):
        self.expense_id=id
        self.expense_type=type
        self.title=title
        self.detail=detail
        self.amount=amount


class Event_Expense(Expense):
    def __init__(self,id,type,title,detail,amount,event_id,amount_per_head):
        Expense.__init__(self,id,type,title,detail,amount)
        self.event_id=event_id
        self.amount_per_head=amount_per_head

class General_Expense(Expense):
    def __init__(self,id,type,title,detail,amount,date):
        Expense.__init__(self,id,type,title,detail,amount)
        self.date=date

class Event:
    def __init__(self,id,no,title,guests,hall,slot,customer,menu,arrangements,booking_date,expenses,payment_details,advance_paid,conclude):
        self.event_id=id
        self.event_no=no
        self.title=title
        self.total_guests=guests
        self.hall=hall
        self.slot=slot
        self.customer=customer
        self.menu=menu
        self.arrangements=arrangements
        self.booking_date=booking_date
        self.expenses=expenses
        self.payment_details=payment_details
        self.advance_paid=advance_paid
        self.is_concluded=conclude

class Slot:
    def __init__(self,id,date,hall,isBooked):
        self.id=id
        self.date=date
        self.hall=hall
        self.isBooked=isBooked

class Customer:
    def __init__(self,id,phone,nic,phone2,name):
        self.cust_id=id
        self.cust_phone=phone
        self.cust_nic=nic
        self.cust_alternate_phone=phone2
        self.cust_name=name

class Employee:
    def __init__(self,id,name,date,salary,status,designation):
        self.emp_id=id
        self.emp_name=name
        self.emp_joindate=date
        self.emp_salary=salary
        self.emp_status=status
        self.emp_designation=designation

class SalarySlip:
    def __init__(self,id,no,date,emp,dur):
        self.slip_id=id
        self.slip_no=no
        self.slip_issue_date=date
        self.slip_employee=emp
        self.slip_salary_dur=dur

class Attendance:
    def __init__(self,id,date,name):
        self.att_id=id
        self.att_date=date
        self.att_name=name