from django.shortcuts import render
import realapp.models
from realapp.models import Booked_Slot,Terms
from realapp.models import Event
from realapp.models import Expense
from realapp.models import Arrangement
from realapp.models import Menu, Employee,Print
from realapp.models import Event_Arrangement, Event_Menu, Salary,Event_Special_Arrangement,Special_Arrangement
import datetime
from django.db.models import Q
from dateutil.parser import parse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.messages import constants as messages
from django.contrib import messages
import json
from win32 import win32print,win32api
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, A4
from time import gmtime, strftime
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Image

import reportlab
from operator import attrgetter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, A4,inch
# from datetime import *
# from time import gmtime, strftime
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Image, Paragraph, Table,TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

# Create your views here.
def index(request):

    if request.session.test_cookie_worked():
        print("Test Cookie Worked")
        request.session.delete_test_cookie()
    object = Event.objects.all()
    event_list = []

    for event in object:
        event_list.append(
            {'event_cust_info': event.event_cust_name + " " + event.event_cust_contactno, 'event_id': event.event_id,
             'event_no': event.event_no})

    info = request.GET.get('event_id', default=None)
    info1 = request.POST.get('event_id', default=None)
    print(info)
    print(info1)
    return render(request, 'realapp/index.html', {'event_list': event_list})

def gallery(request):
    return render(request, 'realapp/gallery.html')

def salary(request):
    object = Employee.objects.all()

    emp_list = []
    obj = Salary.objects.filter(salary_month__year=str(datetime.datetime.today().year),
                                salary_month__month=str(datetime.datetime.today().month))
    emp_list1 = []
    for emp in obj:
        obj1 = Employee.objects.get(emp_id=str(emp.salary_emp_id))
        name = obj1.emp_name
        emp_list1.append({'salary_id':emp.salary_id,'emp_id': emp.salary_emp_id, 'emp_name': name, 'emp_salary': emp.salary_amount_paid,
                          'salary_month': emp.salary_month, 'paid_status': emp.paid_status,'total_salary':emp.salary_amount_paid,
                          'advance':emp.advance})

    print(emp_list1)

    for emp in object:
        emp_list.append({'emp_id': emp.emp_id, 'emp_name': emp.emp_name, 'emp_joindate': emp.emp_joindate,
                         'emp_salary': emp.emp_salary, 'emp_status': emp.emp_status,
                         'emp_designation': emp.emp_designation})

    return render(request, 'realapp/salary.html', {'emp_list1': emp_list1, 'emp_list': emp_list})

def salary2(request):
    object = Employee.objects.all()

    obj = Salary.objects.filter(salary_month__year=str(datetime.datetime.today().year),
                                salary_month__month=str(datetime.datetime.today().month))

    # obj = Salary.objects.filter(salary_month__year=2018,
    #                             salary_month__month=str(3))
    emp_list1 = []
    for emp in obj:
        obj1 = Employee.objects.get(emp_id=str(emp.salary_emp_id))
        name = obj1.emp_name
        emp_list1.append({'salary_id': emp.salary_id, 'emp_id': emp.salary_emp_id, 'emp_name': name,
                          'emp_salary': emp.salary_amount_paid,
                          'salary_month': emp.salary_month, 'paid_status': emp.paid_status,
                          'total_salary': emp.salary_total_amount,
                          'advance': emp.advance,'salary_remarks':emp.salary_remarks})
    return render(request,'realapp/salary2.html',{'emp_list1':emp_list1})

def filter_salary2(request):
    month=request.POST.get('month',default="")

    obj = Salary.objects.filter(salary_month__year=str(datetime.datetime.today().year),
                                salary_month__month=month)

    # obj = Salary.objects.filter(salary_month__year=2018,
    #                             salary_month__month=str(3))
    emp_list1 = []
    for emp in obj:
        obj1 = Employee.objects.get(emp_id=str(emp.salary_emp_id))
        name = obj1.emp_name
        emp_list1.append({'salary_id': emp.salary_id, 'emp_id': emp.salary_emp_id, 'emp_name': name,
                          'emp_salary': emp.salary_amount_paid,
                          'salary_month': emp.salary_month, 'paid_status': emp.paid_status,
                          'total_salary': emp.salary_total_amount,
                          'advance': emp.advance, 'salary_remarks': emp.salary_remarks})

    return render(request,'realapp/salary2.html',{'emp_list1':emp_list1})

def get_table_data(request):
    object = Employee.objects.all()

    emp_list = []

    for emp in object:
        emp_list.append({'emp_id': emp.emp_id, 'emp_name': emp.emp_name, 'emp_joindate': emp.emp_joindate,
                         'emp_salary': emp.emp_salary, 'emp_status': emp.emp_status,
                         'emp_designation': emp.emp_designation})

    salary_id = request.POST.getlist('salary_id[]', default="")
    advance=request.POST.getlist('advance[]',default="")
    salary=request.POST.getlist('salary[]',default="")
    remarks=request.POST.getlist('remarks[]',default="")

    print(advance)
    print(salary)
    print(remarks)
    print(salary_id)

    for i in range(len(advance)):
        obj=Salary.objects.filter(salary_id=salary_id[i])
        obj.update(salary_amount_paid=int(salary[i]),advance=str(advance[i]),salary_remarks=remarks[i])

    return render(request,'realapp/employee.html',{'emp_list':emp_list})

def filter_event_reports(request):

    day1=request.POST.get('day1',default="")
    day2 = request.POST.get('day2', default="")
    month1 = request.POST.get('month1', default="")
    month2 = request.POST.get('month2', default="")
    year1 = request.POST.get('year1', default="")
    year2 = request.POST.get('year2', default="")

    try:
        if year1!="" and year2=="" and month1=="" and month2=="" and day1=="" and day2=="":
            print("here")
            object = Event.objects.filter(event_date__year=year1)
            ob = Expense.objects.filter(expense_date__year=year1)

        if year1 !="" and month1!="":
            object = Event.objects.filter(event_date__year=year1,event_date__month=month1)
            ob = Expense.objects.filter(expense_date__year=year1, expense_date__month=month1)

        if year1 !="" and month1!="" and day1!="":
            object = Event.objects.filter(event_date__year=year1,event_date__month=month1,event_date__day=day1)
            ob = Expense.objects.filter(expense_date__year=year1, expense_date__month=month1,expense_date__day=day1)

        if year1 !="" and month1!="" and day1!="" and year2!="":
            date=year1+"-"+month1+"-"+day1
            object = Event.objects.exclude(event_date__year__gte=year2).filter(event_date__gte=date)
            ob = Expense.objects.exclude(expense_date__year__gte=year2).filter(expense_date__gte=date)

        if year1!="" and year2!="":
            object = Event.objects.exclude(event_date__year__gte=year2).filter(event_date__year__gte=year1)
            ob = Expense.objects.exclude(expense_date__year__gte=year2).filter(expense_date__year__gte=year1)

        if year1 !="" and month1!="" and day1!="" and year2!="" and month2!="":
            date=year1+"-"+month1+"-"+day1
            object = Event.objects.exclude(event_date__year__gte=year2,event_date__month__gte=month2).filter(event_date__gte=date)
            ob = Expense.objects.exclude(expense_date__year__gte=year2, expense_date__month__gte=month2).filter(
                expense_date__gte=date)

        if year1 !="" and month1!="" and day1!="" and year2!="" and month2!="" and day2!="":
            date=year1+"-"+month1+"-"+day1
            date2 = year2 + "-" + month2 + "-" + day2
            object = Event.objects.exclude(event_date__gte=date2).filter(event_date__gte=date)
            ob = Expense.objects.exclude(expense_date__gte=date2).filter(expense_date__gte=date)

        if year1 == "" and month1 == "" and day1 == "" and year2 == "" and month2 == "" and day2 == "":
            currentDT = datetime.datetime.now()
            date = (currentDT.strftime("%Y-%m-%d"))
            object = Event.objects.filter(event_date__gte=date)
            ob = Expense.objects.filter(expense_date__gte=date)

        if year1 !="" and month1!="" and year2!="" and month2!="":
            object = Event.objects.exclude(event_date__year__gte=year2,event_date__month__gte=month2).filter(event_date__year__gte=year1,event_date__month__gte=month1)
            ob = Expense.objects.exclude(expense_date__year__gte=year2, expense_date__month__gte=month2).filter(
                expense_date__year__gte=year1, expense_date__month__gte=month1)

        if year1 =="" and month1!="" and day1!="" and year2=="" and month2!="" and day2!="":
            date=datetime.now().year+"-"+month1+"-"+day1
            object = Event.objects.exclude(event_date__year__gte=str(datetime.datetime.today().year),event_date__month__gte=month2).filter(event_date__gte=date)
            ob = Expense.objects.exclude(expense_date__year__gte=str(datetime.datetime.today().year),
                                           expense_date__month__gte=month2).filter(expense_date__gte=date)

        if year1=="" and year2=="" and month1!="" and month2!="":
            object = Event.objects.exclude(event_date__year__gte=str(datetime.datetime.today().year), event_date__month__gte=month2).filter(event_date__year__gte=str(datetime.datetime.today().year),
                event_date__month__gte=month1)
            ob = Expense.objects.exclude(expense_date__year__gte=str(datetime.datetime.today().year),
                                           expense_date__month__gte=month2).filter(
                expense_date__year__gte=str(datetime.datetime.today().year),
                expense_date__month__gte=month1)

        if month1!="":
            object = Event.objects.filter(event_date__month=month1)
            ob = Expense.objects.filter(expense_date__month=month1)

        if month2!="":
            object = Event.objects.exclude(event_date__year__gte=str(datetime.datetime.today().year),
                                           event_date__month__gte=month2).filter(
                event_date__year__gte=str(datetime.datetime.today().year))
            ob = Expense.objects.exclude(expense_date__year__gte=str(datetime.datetime.today().year),
                                           expense_date__month__gte=month2).filter(
                expense_date__year__gte=str(datetime.datetime.today().year))

        if object.count()==0:
            return render(request,'realapp/ereport.html')



        event_list = []

        total_events=0
        total_revenue=0
        total_expense=0
        total_profit=0
        g_amount=0
        object1=object.filter(conclude_event=True).order_by('-event_date')
        for event in object1:
            ob1 = Expense.objects.filter(expense_event_id=str(event.event_id))
            j = 0
            if ob1.count() > 0:
                for i in ob1:
                    j = j + i.expense_amount
            total_events=total_events+1
            total_revenue=total_revenue+event.event_advance
            total_expense=total_expense+j
            total_profit=total_profit+(event.event_advance-j)
            concat=""
            arrange_expense=0
            menu=0
            arrangements=0
            try:
                menu=Event_Menu.objects.get(event_menu_event_id=event.event_id)
            except:
                print("None")
            try:
                arrangements=Event_Arrangement.objects.filter(event_arrangement_event_id=event.event_id)
                concat=""
                for i in arrangements:
                    concat=concat+i.event_arrange_details
                    concat=concat+", "
                    arrange_expense=arrange_expense+i.event_arrange_cost
            except:
                print("none")
            if menu==0:
                if arrangements==0:
                    event_list.append({'event_id': event.event_id, 'event_id2': event.event_id, 'event_no': event.event_no,
                               'event_cust_name': event.event_cust_name, 'event_cust_email': event.event_cust_email,
                               'event_cust_nic': event.event_cust_nic, 'event_cust_contactno': event.event_cust_contactno,
                               'event_cust_contactno2': event.event_cust_contactno2,
                               'event_total_guests': event.event_total_guests, 'event_advance': event.event_advance,
                               'event_total_amount': event.event_total_amount,
                               'event_total_expense': j, 'event_payments_details': event.event_payments_details,
                               'event_date': event.event_date,
                               'event_hall': event.event_hall, 'event_slot': event.event_slot,
                               'event_booking_date': event.event_booking_date,'event_details':event.event_details,'event_profit':event.event_advance-j,
                               'menu_details':"",'menu_cost_perhead':"",'arrange_details':"",'arrange_expense':arrange_expense})
                else:
                    event_list.append({'event_id': event.event_id, 'event_id2': event.event_id, 'event_no': event.event_no,
                               'event_cust_name': event.event_cust_name, 'event_cust_email': event.event_cust_email,
                               'event_cust_nic': event.event_cust_nic, 'event_cust_contactno': event.event_cust_contactno,
                               'event_cust_contactno2': event.event_cust_contactno2,
                               'event_total_guests': event.event_total_guests, 'event_advance': event.event_advance,
                               'event_total_amount': event.event_total_amount,
                               'event_total_expense': j, 'event_payments_details': event.event_payments_details,
                               'event_date': event.event_date,
                               'event_hall': event.event_hall, 'event_slot': event.event_slot,
                               'event_booking_date': event.event_booking_date,'event_details':event.event_details,'event_profit':event.event_advance-j,
                               'menu_details':"",'menu_cost_perhead':"",'arrange_details':concat,'arrange_expense':arrange_expense})
            else:
                if arrangements==0:
                    event_list.append({'event_id': event.event_id, 'event_id2': event.event_id, 'event_no': event.event_no,
                               'event_cust_name': event.event_cust_name, 'event_cust_email': event.event_cust_email,
                               'event_cust_nic': event.event_cust_nic, 'event_cust_contactno': event.event_cust_contactno,
                               'event_cust_contactno2': event.event_cust_contactno2,
                               'event_total_guests': event.event_total_guests, 'event_advance': event.event_advance,
                               'event_total_amount': event.event_total_amount,
                               'event_total_expense': j, 'event_payments_details': event.event_payments_details,
                               'event_date': event.event_date,
                               'event_hall': event.event_hall, 'event_slot': event.event_slot,
                               'event_booking_date': event.event_booking_date,'event_details':event.event_details,'event_profit':event.event_advance-j,
                               'menu_details':menu.menu_details,'menu_cost_perhead':menu.menu_cost_perhead,'arrange_details':"",'arrange_expense':arrange_expense})
                else:
                    event_list.append({'event_id': event.event_id, 'event_id2': event.event_id, 'event_no': event.event_no,
                               'event_cust_name': event.event_cust_name, 'event_cust_email': event.event_cust_email,
                               'event_cust_nic': event.event_cust_nic, 'event_cust_contactno': event.event_cust_contactno,
                               'event_cust_contactno2': event.event_cust_contactno2,
                               'event_total_guests': event.event_total_guests, 'event_advance': event.event_advance,
                               'event_total_amount': event.event_total_amount,
                               'event_total_expense': j, 'event_payments_details': event.event_payments_details,
                               'event_date': event.event_date,
                               'event_hall': event.event_hall, 'event_slot': event.event_slot,
                               'event_booking_date': event.event_booking_date,'event_details':event.event_details,'event_profit':event.event_advance-j,
                               'menu_details':menu.menu_details,'menu_cost_perhead':menu.menu_cost_perhead,'arrange_details':concat,'arrange_expense':arrange_expense})

        for i in ob:
            g_amount = g_amount + i.expense_amount

        report_list=[]

        report_list1 = []

        report_list1.append({'gen_expense': g_amount, 't_profit': total_profit, 'net_profit': total_profit - g_amount})

        report_list.append({'t_expense':total_expense,'t_revenue':total_revenue,'t_profit':total_profit,'t_events':total_events})


        return render(request,'realapp/ereport.html',{'event_list':event_list,'report_list':report_list,'report_list1':report_list1})

    except:
        print("no filteration")
        return render(request, 'realapp/ereport.html')

def ereport(request):
    currentDT = datetime.datetime.now()
    date = (currentDT.strftime("%Y-%m-%d"))
    object = Event.objects.filter(event_date__gte=date,conclude_event=True).order_by('-event_date')

    count=0
    concat1=""


    event_list = []

    total_events = 0
    total_revenue = 0
    total_expense = 0
    total_profit = 0
    g_amount=0

    g_expense=Expense.objects.filter(expense_date__lte=date,expense_event_id=None)
    for i in g_expense:
        g_amount=g_amount+i.expense_amount

    tt_expense=0

    for event in object:
        ob1 = Expense.objects.filter(expense_event_id=str(event.event_id))
        j = 0
        if ob1.count() > 0:
            for i in ob1:
                j = j + i.expense_amount
        # for s in object:
        #     for k in s.event_payments_details:
        #         semi_colon_count=0
                # if k == ";":
                #     count = count + 1
                #     concat1 = concat1 + " "
                #
                # if count == 2:
                #     semi_colon_count=semi_colon_count+1
                    # concat1 = concat1 + ", "
                    # count = 0
                # if k != ";":
                #     concat1 = concat1 + k
        total_events = total_events + 1
        total_revenue = total_revenue + event.event_advance
        total_expense = total_expense + j
        total_profit = total_profit + (event.event_advance - total_expense)
        arrange_expense=0
        concat=""
        menu=0
        arrangements=0
        try:
            menu=Event_Menu.objects.get(event_menu_event_id=event.event_id)
        except:
            print("None")
        try:
            arrangements=Event_Arrangement.objects.filter(event_arrangement_event_id=event.event_id)
            concat=""
            for i in arrangements:
                concat=concat+i.event_arrange_details
                concat=concat+", "
                arrange_expense=arrange_expense+i.event_arrange_cost
        except:
            print("none")
        if menu==0:
            if arrangements==0:
                event_list.append({'event_id': event.event_id, 'event_id2': event.event_id, 'event_no': event.event_no,
                           'event_cust_name': event.event_cust_name, 'event_cust_email': event.event_cust_email,
                           'event_cust_nic': event.event_cust_nic, 'event_cust_contactno': event.event_cust_contactno,
                           'event_cust_contactno2': event.event_cust_contactno2,
                           'event_total_guests': event.event_total_guests, 'event_advance': event.event_advance,
                           'event_total_amount': event.event_total_amount,
                           'event_total_expense': j, 'event_payments_details': event.event_payments_details,
                           'event_date': event.event_date,
                           'event_hall': event.event_hall, 'event_slot': event.event_slot,
                           'event_booking_date': event.event_booking_date,'event_details':event.event_details,'event_profit':event.event_advance-j,
                           'menu_details':"",'menu_cost_perhead':"",'arrange_details':"",'arrange_expense':arrange_expense})
            else:
                event_list.append({'event_id': event.event_id, 'event_id2': event.event_id, 'event_no': event.event_no,
                           'event_cust_name': event.event_cust_name, 'event_cust_email': event.event_cust_email,
                           'event_cust_nic': event.event_cust_nic, 'event_cust_contactno': event.event_cust_contactno,
                           'event_cust_contactno2': event.event_cust_contactno2,
                           'event_total_guests': event.event_total_guests, 'event_advance': event.event_advance,
                           'event_total_amount': event.event_total_amount,
                           'event_total_expense': j, 'event_payments_details': event.event_payments_details,
                           'event_date': event.event_date,
                           'event_hall': event.event_hall, 'event_slot': event.event_slot,
                           'event_booking_date': event.event_booking_date,'event_details':event.event_details,'event_profit':event.event_advance-j,
                           'menu_details':"",'menu_cost_perhead':"",'arrange_details':concat,'arrange_expense':arrange_expense})
        else:
            if arrangements==0:
                event_list.append({'event_id': event.event_id, 'event_id2': event.event_id, 'event_no': event.event_no,
                           'event_cust_name': event.event_cust_name, 'event_cust_email': event.event_cust_email,
                           'event_cust_nic': event.event_cust_nic, 'event_cust_contactno': event.event_cust_contactno,
                           'event_cust_contactno2': event.event_cust_contactno2,
                           'event_total_guests': event.event_total_guests, 'event_advance': event.event_advance,
                           'event_total_amount': event.event_total_amount,
                           'event_total_expense': j, 'event_payments_details': event.event_payments_details,
                           'event_date': event.event_date,
                           'event_hall': event.event_hall, 'event_slot': event.event_slot,
                           'event_booking_date': event.event_booking_date,'event_details':event.event_details,'event_profit':event.event_advance-j,
                           'menu_details':menu.menu_details,'menu_cost_perhead':menu.menu_cost_perhead,'arrange_details':"",'arrange_expense':arrange_expense})
            else:
                event_list.append({'event_id': event.event_id, 'event_id2': event.event_id, 'event_no': event.event_no,
                           'event_cust_name': event.event_cust_name, 'event_cust_email': event.event_cust_email,
                           'event_cust_nic': event.event_cust_nic, 'event_cust_contactno': event.event_cust_contactno,
                           'event_cust_contactno2': event.event_cust_contactno2,
                           'event_total_guests': event.event_total_guests, 'event_advance': event.event_advance,
                           'event_total_amount': event.event_total_amount,
                           'event_total_expense': j, 'event_payments_details': event.event_payments_details,
                           'event_date': event.event_date,
                           'event_hall': event.event_hall, 'event_slot': event.event_slot,
                           'event_booking_date': event.event_booking_date,'event_details':event.event_details,'event_profit':event.event_advance-j,
                           'menu_details':menu.menu_details,'menu_cost_perhead':menu.menu_cost_perhead,'arrange_details':concat,'arrange_expense':arrange_expense})
    report_list = []
    report_list1=[]

    report_list1.append({'gen_expense':g_amount,'t_profit':total_profit,'net_profit':total_profit-g_amount})

    report_list.append(
        {'t_expense': total_expense, 't_revenue': total_revenue, 't_profit': total_profit, 't_events': total_events})

    return render(request,'realapp/ereport.html',{'event_list':event_list,'report_list':report_list,'report_list1':report_list1})

def employee(request):
    object = Employee.objects.all()

    emp_list = []

    for emp in object:
        emp_list.append({'emp_id': emp.emp_id, 'emp_name': emp.emp_name, 'emp_joindate': emp.emp_joindate,
                         'emp_salary': emp.emp_salary, 'emp_status': emp.emp_status,
                         'emp_designation': emp.emp_designation})

    print('employee emp list', emp_list)

    return render(request, 'realapp/employee.html', {'emp_list': emp_list})

def contact(request):
    return render(request, 'realapp/contact.html')

def update_form(request):
    event_id = request.POST.get('event_id', default=None)
    e_date = request.POST.get('event_date', default=None)
    date = request.POST.get('event_booking_date', default=None)
    hall = request.POST.get('event_hall', default=None)
    slot1 = request.POST.get('event_slot', default=None)
    e_no = request.POST.get('event_no', default=None)
    e_cust_name = request.POST.get('event_cust_name', default=None)
    e_cust_email = request.POST.get('event_cust_email', default=None)
    e_cust_nic = request.POST.get('event_cust_nic', default=None)
    e_cust_contact = request.POST.get('event_cust_contactno', default=None)
    e_cust_contact2 = request.POST.get('event_cust_contactno2', default=None)
    e_guests = request.POST.get('event_total_guests', default=None)
    e_expense = request.POST.get('event_total_expense', default=None)
    e_total_amount = request.POST.get('event_total_amount', default="")
    e_advance = request.POST.get('event_advance', default=None)
    details = request.POST.get('event_other_details', default=None)
    other_time = request.POST.get('other_time', default="")
    quantity = request.POST.get('quantity', default="")

    if quantity=="":
        quantity=0
    else:
        quantity=int(quantity)


    currentDT = datetime.datetime.now()
    date1 = (currentDT.strftime("%Y-%m-%d"))

    slot=str(slot1)

    if slot=="3":
        if other_time=="":
            slot=date1
        else:
            slot=str(other_time)

    u_value = request.POST.get('update', default=None)
    d_value = request.POST.get('delete', default=None)
    c_value = request.POST.get('conclude', default=None)

    # try:
    currentDT = datetime.datetime.now()
    date1 = (currentDT.strftime("%Y-%m-%d"))

    obj=Event.objects.get(event_id=event_id)
    e_payment = obj.event_payments_details + e_total_amount + ";" + date1 + ";"
    e_advance=int(e_advance)+int(e_total_amount)

# getting selected menu and arrangements

    menu_items1 = request.POST.getlist('menu_list1[]')
    checkboxes1 = request.POST.getlist('checkbox[]')
    print("checkboxes1",checkboxes1)
    menu_items=[]
    checkboxes=[]
    for i in menu_items1:
        menu_items.append(int(i))

    for i in checkboxes1:
        checkboxes.append(int(i))

    # parsing booking and function dates
    dt = parse(str(e_date))
    e_date = dt.strftime('%Y-%m-%d')

    dt1 = parse(str(date))
    date = dt1.strftime('%Y-%m-%d')

    obj = Event.objects.get(event_id=event_id)

    previous_guests=obj.event_total_guests

    arrangement_change=False
    menu_change=False

    event_arr_list=[]

    arr=Event_Arrangement.objects.filter(event_arrangement_event_id=event_id)
    if arr.count()>0:
        for i in arr:
            arrangement=Arrangement.objects.get(arrange_id=str(i.event_arrangement_arrange_id))
            event_arr_list.append(arrangement.arrange_id)

    event_menu_list=[]

    menu=Event_Menu.objects.filter(event_menu_event_id=event_id)
    if len(menu)!=0:
        for j in menu:
            men=Menu.objects.get(menu_id=str(j.event_menu_menu_id))
            event_menu_list.append(men.menu_id)



    if set(event_menu_list)!=set(menu_items):
        menu_change=True

    if set(checkboxes)!=set(event_arr_list):
        arrangement_change=True

    print("previous guests",previous_guests)
    print("e guests", e_guests)
    special_arr_change = False
    e_ar = Event_Special_Arrangement.objects.filter(event_arrangement_event_id=event_id)
    print("eaaaaaaaaaaaaaaaaaaaaaaaaaarrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",e_ar)
    if len(e_ar)>0:
        for k in e_ar:
            print("quantityyyyyyyyyyyyyyyyyyyyyyyyyyy",quantity,k.event_arrange_quantity)
            if quantity != k.event_arrange_quantity:
                special_arr_change = True

                print("special change is trueeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",special_arr_change)
    if len(e_ar)==0 and quantity>0:
        special_arr_change=True

    total_cost=0
    arr_cost=0
    menu_cost=0
# if guests are changing

    if int(previous_guests)<int(e_guests) or int(previous_guests)>int(e_guests):
        if arrangement_change==True:
            for i in checkboxes:
                obj_cost=Arrangement.objects.get(arrange_id=str(i))
                arr_cost=arr_cost+obj_cost.arrange_cost
            print(arr_cost)
            # delete previous event_arrangements
        else:
            for i in event_arr_list:
                obj_cost=Event_Arrangement.objects.get(event_arrangement_arrange_id=str(i),event_arrangement_event_id=event_id)
                arr_cost=arr_cost+obj_cost.event_arrange_cost
            print(arr_cost)

        if special_arr_change == True:
            e_ar = Event_Special_Arrangement.objects.filter(event_arrangement_event_id=event_id)
            if e_ar.count() > 0:
                for i in e_ar:
                    special_arr_cost = i.event_arrange_cost * quantity
                arr_cost += special_arr_cost

        else:
            e_ar = Event_Special_Arrangement.objects.filter(event_arrangement_event_id=event_id)
            if e_ar.count()>0:
                for i in e_ar:
                    special_arr_cost = i.event_arrange_cost * i.event_arrange_quantity
                arr_cost += special_arr_cost

        if len(menu_items)!=0:
            if menu_change==True:
                for i in menu_items:
                    obj1_cost=Menu.objects.get(menu_id=str(i))
                    menu_cost=obj1_cost.menu_cost_perhead
                print(menu_cost)

            # delete previous event_menu
            else:
                for i in event_menu_list:
                    obj1_cost=Event_Menu.objects.get(event_menu_menu_id=str(i),event_menu_event_id=event_id)
                    menu_cost=obj1_cost.menu_cost_perhead
                    print(menu_cost)

        if obj.additional_cost_perhead>0:
            overall_cost=menu_cost+obj.additional_cost_perhead
            print(overall_cost)
        else:
            overall_cost = menu_cost
            print("addition of menu and arrangement",overall_cost)
        if obj.discount>0:
            temp=int(e_guests)*(overall_cost)
            total_cost=(temp+arr_cost)-obj.discount
            print("total cost with discount",total_cost)
        else:
            total_cost = int(e_guests) * (overall_cost)+arr_cost
            print("total_cost without discount",total_cost)
        print(total_cost)

        # if guests are not changing

    if int(previous_guests) == int(e_guests):
        if arrangement_change==True:
            for i in checkboxes:
                obj_cost=Arrangement.objects.get(arrange_id=str(i))
                arr_cost=arr_cost+obj_cost.arrange_cost
            print("arr oosttttttttttt",arr_cost)
            # delete previous event_arrangements
        else:
            for i in event_arr_list:
                obj_cost=Event_Arrangement.objects.get(event_arrangement_arrange_id=str(i),event_arrangement_event_id=event_id)
                arr_cost=arr_cost+obj_cost.event_arrange_cost
            print("arrv costttttttttt",arr_cost)

        if special_arr_change == True:
            e_ar = Event_Special_Arrangement.objects.filter(event_arrangement_event_id=event_id)
            if e_ar.count() > 0:
                for i in e_ar:
                    special_arr_cost = i.event_arrange_cost * quantity
                arr_cost += special_arr_cost
                print("arrv costttttttttt", arr_cost)
        else:
            e_ar = Event_Special_Arrangement.objects.filter(event_arrangement_event_id=event_id)
            if e_ar.count()>0:
                for i in e_ar:
                    special_arr_cost = i.event_arrange_cost * i.event_arrange_quantity
                arr_cost += special_arr_cost
                print("arrv costttttttttt", arr_cost)

        if len(menu_items)!=0:
            if menu_change==True:
                for i in menu_items:
                    obj1_cost=Menu.objects.get(menu_id=str(i))
                    menu_cost=obj1_cost.menu_cost_perhead
                print("menuuuuuuuu",menu_cost)

                # delete previous event_menu
            else:
                for i in event_menu_list:
                    obj1_cost=Event_Menu.objects.get(event_menu_menu_id=str(i),event_menu_event_id=event_id)
                    menu_cost=obj1_cost.menu_cost_perhead
                    print("menuuuuuuuu",menu_cost)

        if obj.additional_cost_perhead>0:
            overall_cost=menu_cost+obj.additional_cost_perhead
            print(overall_cost)
        else:
            overall_cost = menu_cost
            print("addition of menu and arrangement",overall_cost)
        if obj.discount>0:
            temp = int(e_guests) * (overall_cost)
            total_cost = (temp + arr_cost) - obj.discount
            print("total cost with discount",total_cost)
        else:
            total_cost = (int(e_guests) * (overall_cost))+arr_cost
            print("total_cost without disscount",total_cost)
            print(e_total_amount,type(e_total_amount))
        print(total_cost)

    if d_value == "DELETE":
        obj=Event.objects.get(event_id=event_id)
        obj.delete()
        messages.info(request,'Event Deleted.')


    if e_total_amount!="0":
        currentDT = datetime.datetime.now()
        date1 = (currentDT.strftime("%Y-%m-%d"))

        obj = Event.objects.get(event_id=event_id)
        e_payment = obj.event_payments_details + e_total_amount + ";" + date1 + ";"
        if u_value=="UPDATE":
            obj2 = Event.objects.filter(event_id=event_id)
            obj2.update(event_no=e_no, event_date=e_date, event_booking_date=date, event_hall=hall, event_slot=str(slot),
                                    event_cust_name=e_cust_name, event_cust_email=e_cust_email, event_cust_nic=e_cust_nic,
                                    event_cust_contactno=e_cust_contact, event_cust_contactno2=e_cust_contact2,
                                    event_total_guests=e_guests, event_total_amount=total_cost,
                                    event_advance=e_advance, event_payments_details=e_payment,event_details=details)
            if arrangement_change==True:
                event_ar = Event_Arrangement.objects.filter(event_arrangement_event_id=event_id)
                event_ar.delete()
                for i in range(0, len(checkboxes)):
                    cost = Arrangement.objects.get(arrange_id=checkboxes[i])
                    event_arrange = Event_Arrangement(event_arrangement_event_id=Event(event_id),
                                                      event_arrangement_arrange_id=Arrangement(checkboxes[i]),
                                                      event_arrange_cost=cost.arrange_cost,
                                                      event_arrange_details=cost.arrange_details)
                    event_arrange.save()
            else:
                print("didn't change")
            if len(menu_items)!=0:
                if menu_change==True:
                    event_me = Event_Menu.objects.filter(event_menu_event_id=event_id)
                    event_me.delete()
                    menu_vaganza = Menu.objects.get(menu_id=menu_items[0])
                    event_menu = Event_Menu(event_menu_event_id=Event(event_id), event_menu_menu_id=Menu(menu_items[0]),
                                            menu_cost_perhead=menu_vaganza.menu_cost_perhead, menu_details=menu_vaganza.menu_details)
                    # saving menu
                    event_menu.save()

                else:
                    print("didn't change")

            if special_arr_change==True:
                sp_arrange=Event_Special_Arrangement.objects.filter(event_arrangement_event_id=event_id)
                if sp_arrange.count()>0:
                    sp_arrange.delete()
                obb=Special_Arrangement.objects.get(special_arrange_id=1)
                sp_arrange1=Event_Special_Arrangement(event_arrangement_event_id=Event(event_id),
                                                      event_special_arrange_id=Special_Arrangement(1),
                                                      event_arrange_quantity=quantity,
                                                      event_arrange_cost=obb.special_arrange_cost,
                                                      event_arrange_title=obb.special_arrange_title)
                sp_arrange1.save()
            Booked_Slot.objects.filter(booked_slot_event_id=Event(event_id)).update(booked_date=e_date, booked_hall=hall,
                                                                                                booked_slot=slot)
            messages.info(request, 'Event Updated.')
        if c_value=="CONCLUDE":
            obj2 = Event.objects.filter(event_id=event_id)
            obj2.update(event_no=e_no, event_date=e_date, event_booking_date=date, event_hall=hall, event_slot=str(slot),
                        event_cust_name=e_cust_name, event_cust_email=e_cust_email, event_cust_nic=e_cust_nic,
                        event_cust_contactno=e_cust_contact, event_cust_contactno2=e_cust_contact2,
                        event_total_guests=e_guests, event_total_amount=total_cost,
                        event_advance=e_advance, event_payments_details=e_payment, event_details=details,conclude_event=True)
            if arrangement_change == True:
                event_ar = Event_Arrangement.objects.filter(event_arrangement_event_id=event_id)
                event_ar.delete()
                for i in range(0, len(checkboxes)):
                    cost = Arrangement.objects.get(arrange_id=checkboxes[i])
                    event_arrange = Event_Arrangement(event_arrangement_event_id=Event(event_id),
                                                      event_arrangement_arrange_id=Arrangement(checkboxes[i]),
                                                      event_arrange_cost=cost.arrange_cost,
                                                      event_arrange_details=cost.arrange_details)
                    event_arrange.save()
            else:
                print("didn't change")
            if len(menu_items)!=0:
                if menu_change == True:
                    event_me = Event_Menu.objects.filter(event_menu_event_id=event_id)
                    event_me.delete()
                    menu_vaganza = Menu.objects.get(menu_id=menu_items[0])
                    event_menu = Event_Menu(event_menu_event_id=Event(event_id), event_menu_menu_id=Menu(menu_items[0]),
                                            menu_cost_perhead=menu_vaganza.menu_cost_perhead,
                                            menu_details=menu_vaganza.menu_details)
                    # saving menu
                    event_menu.save()

                else:
                    print("didn't change")

            if special_arr_change==True:
                sp_arrange=Event_Special_Arrangement.objects.filter(event_arrangement_event_id=event_id)
                if sp_arrange.count()>0:
                    sp_arrange.delete()
                obb=Special_Arrangement.objects.get(special_arrange_id=1)
                sp_arrange1=Event_Special_Arrangement(event_arrangement_event_id=Event(event_id),
                                                      event_special_arrange_id=Special_Arrangement(1),
                                                      event_arrange_quantity=quantity,
                                                      event_arrange_cost=obb.special_arrange_cost,
                                                      event_arrange_title=obb.special_arrange_title)
                sp_arrange1.save()
            Booked_Slot.objects.filter(booked_slot_event_id=Event(event_id)).update(booked_date=e_date, booked_hall=hall,
                                                                                    booked_slot=slot)
            messages.info(request, 'Event Concluded.')

    if e_total_amount == "0":
        if u_value == "UPDATE":
            obj2 = Event.objects.filter(event_id=event_id)
            obj2.update(event_no=e_no, event_date=e_date, event_booking_date=date, event_hall=hall, event_slot=str(slot),
                        event_cust_name=e_cust_name, event_cust_email=e_cust_email, event_cust_nic=e_cust_nic,
                        event_cust_contactno=e_cust_contact, event_cust_contactno2=e_cust_contact2,
                        event_total_guests=e_guests, event_total_amount=total_cost,event_advance=e_advance, event_details=details)
            if arrangement_change == True:
                event_ar = Event_Arrangement.objects.filter(event_arrangement_event_id=event_id)
                event_ar.delete()
                for i in range(0, len(checkboxes)):
                    cost = Arrangement.objects.get(arrange_id=checkboxes[i])
                    event_arrange = Event_Arrangement(event_arrangement_event_id=Event(event_id),
                                                      event_arrangement_arrange_id=Arrangement(checkboxes[i]),
                                                      event_arrange_cost=cost.arrange_cost,
                                                      event_arrange_details=cost.arrange_details)
                    event_arrange.save()
            else:
                print("didn't change")
            if len(menu_items)!=0:
                if menu_change == True:
                    event_me = Event_Menu.objects.filter(event_menu_event_id=event_id)
                    event_me.delete()
                    menu_vaganza = Menu.objects.get(menu_id=menu_items[0])
                    event_menu = Event_Menu(event_menu_event_id=Event(event_id), event_menu_menu_id=Menu(menu_items[0]),
                                            menu_cost_perhead=menu_vaganza.menu_cost_perhead,
                                            menu_details=menu_vaganza.menu_details)
                    # saving menu
                    event_menu.save()

                else:
                    print("didn't change")

            if special_arr_change==True:
                sp_arrange=Event_Special_Arrangement.objects.filter(event_arrangement_event_id=event_id)
                if sp_arrange.count()>0:
                    sp_arrange.delete()
                obb=Special_Arrangement.objects.get(special_arrange_id=1)
                sp_arrange1=Event_Special_Arrangement(event_arrangement_event_id=Event(event_id),
                                                      event_special_arrange_id=Special_Arrangement(1),
                                                      event_arrange_quantity=quantity,
                                                      event_arrange_cost=obb.special_arrange_cost,
                                                      event_arrange_title=obb.special_arrange_title)
                sp_arrange1.save()

            Booked_Slot.objects.filter(booked_slot_event_id=Event(event_id)).update(booked_date=e_date, booked_hall=hall,
                                                                                    booked_slot=slot)
            messages.info(request, 'Event Updated.')
        if c_value == "CONCLUDE":
            obj2 = Event.objects.filter(event_id=event_id)
            obj2.update(event_no=e_no, event_date=e_date, event_booking_date=date, event_hall=hall, event_slot=str(slot),
                        event_cust_name=e_cust_name, event_cust_email=e_cust_email, event_cust_nic=e_cust_nic,
                        event_cust_contactno=e_cust_contact, event_cust_contactno2=e_cust_contact2,
                        event_total_guests=e_guests, event_total_amount=total_cost,
                        event_advance=e_advance, event_details=details,
                        conclude_event=True)
            if arrangement_change == True:
                event_ar = Event_Arrangement.objects.filter(event_arrangement_event_id=event_id)
                event_ar.delete()
                for i in range(0, len(checkboxes)):
                    cost = Arrangement.objects.get(arrange_id=checkboxes[i])
                    event_arrange = Event_Arrangement(event_arrangement_event_id=Event(event_id),
                                                      event_arrangement_arrange_id=Arrangement(checkboxes[i]),
                                                      event_arrange_cost=cost.arrange_cost,
                                                      event_arrange_details=cost.arrange_details)
                    event_arrange.save()
            else:
                print("didn't change")
            if len(menu_items)!=0:
                if menu_change == True:
                    event_me = Event_Menu.objects.filter(event_menu_event_id=event_id)
                    event_me.delete()
                    menu_vaganza = Menu.objects.get(menu_id=menu_items[0])
                    event_menu = Event_Menu(event_menu_event_id=Event(event_id), event_menu_menu_id=Menu(menu_items[0]),
                                            menu_cost_perhead=menu_vaganza.menu_cost_perhead,
                                            menu_details=menu_vaganza.menu_details)
                    # saving menu
                    event_menu.save()

                else:
                    print("didn't change")

            if special_arr_change==True:
                sp_arrange=Event_Special_Arrangement.objects.filter(event_arrangement_event_id=event_id)
                if sp_arrange.count()>0:
                    sp_arrange.delete()
                obb=Special_Arrangement.objects.get(special_arrange_id=1)
                sp_arrange1=Event_Special_Arrangement(event_arrangement_event_id=Event(event_id),
                                                      event_special_arrange_id=Special_Arrangement(1),
                                                      event_arrange_quantity=quantity,
                                                      event_arrange_cost=obb.special_arrange_cost,
                                                      event_arrange_title=obb.special_arrange_title)
                sp_arrange1.save()
            Booked_Slot.objects.filter(booked_slot_event_id=Event(event_id)).update(booked_date=e_date, booked_hall=hall,
                                                                                    booked_slot=slot)

            messages.info(request, 'Event Concluded.')
    if len(event_menu_list)!=0 and len(menu_items)==0:
        menu.delete()

    term=[]
    term_obj = Terms.objects.all()
    for i in term_obj:
        term.append(i.term_statement)

    # term = ["non refundable", "conditions apply", "yeah baby my rules"]
    price = ""
    if len(menu_items) > 0:
        for j in menu_items:
            m = Menu.objects.get(menu_id=str(j))
            price = str(m.menu_cost_perhead)

    object = Event.objects.filter(event_id=event_id)
    for o in object:
        add_cost = o.additional_cost_perhead

    print("adddddddddddddddddddddddddddddddddddddddddddddd",add_cost)

    account_list = [["", ""], ["Total Guests", int(e_guests)], ["Extra Tables/Chairs", ""],
                    ["Special Arrangements", "none"],
                    ["Total Amount", int(total_cost)], ["Paid", int(e_advance)],
                    ["Part Payment", int(int(total_cost) - int(e_advance))],
                    ["", ""], ["", ""], ["", ""], ["", ""], ["Total Receipts", int(e_advance)]]

    selected_arr = []
    unselected_arr = []
    for i in checkboxes:
        selected_arr.append(int(i))

    all_arr = Arrangement.objects.all()

    for j in all_arr:
        unselected_arr.append(int(j.arrange_id))

    unselected_arr = set(unselected_arr) - set(selected_arr)
    li = []
    if len(selected_arr) > 0:
        for i in selected_arr:
            temp_list = []
            arr = Arrangement.objects.get(arrange_id=str(i))
            temp_list.append(li.__len__() + 1)
            temp_list.append(str(arr.arrange_title))
            temp_list.append("Y")
            temp_list.append(arr.arrange_cost)
            li.append(temp_list)

    if len(unselected_arr) > 0:
        for i in unselected_arr:
            temp_list = []
            arr = Arrangement.objects.get(arrange_id=str(i))
            temp_list.append(li.__len__() + 1)
            temp_list.append(str(arr.arrange_title))
            temp_list.append("")
            temp_list.append("")
            li.append(temp_list)

    special_a=Special_Arrangement.objects.all()
    print(special_a)
    for k in special_a:
        ev_sp=Event_Special_Arrangement.objects.filter(event_special_arrange_id=k.special_arrange_id,event_arrangement_event_id=event_id)
        temp_list=[]
        print("specialllllllllll", ev_sp)
        if len(ev_sp) > 0:

            print("for s in ev_sp:")
            for s in ev_sp:
                print("if len(ev_sp)>0:")
                temp_list.append(li.__len__()+1)
                temp_list.append(str(k.special_arrange_title))
                temp_list.append(str(s.event_arrange_quantity))
                temp_list.append(str(int(s.event_arrange_cost*s.event_arrange_quantity)))
                li.append(temp_list)
                print("temp",temp_list)
                print(li)
        else:
            print("else")
            temp_list.append(li.__len__() + 1)
            temp_list.append(str(k.special_arrange_title))
            temp_list.append(str(""))
            temp_list.append("")
            li.append(temp_list)
            print("temp",temp_list)

    print("list of printing arrangements", li)

    # li = [[1, "sofa sitting", "yes", 200], [2, "dj system and setup", "no", 2000], [3, "party", "yes", 1500],
    #       [4, "drugs", "yes", 50000]
    #     , [5, "ecstacy", "yes", 5000], [6, "lsd", "yes", 4000], [7, "bhung", "no", 500],
    #       [8, "jack daniels", "yes", 55000]
    #     , [9, "cocaine", "yes", 500000], [10, "hashish", "yes", 5000], [11, "heroine", "yes", 50000],
    #       [12, "drugs", "yes", 50000]
    #     , [13, "drugs", "yes", 50000]]

    # p=Print(print_details="")
    # p.save()
    # generate_booking_voucher(li, e_no, date, e_cust_name, e_date, str(slot), hall, "", int(e_guests),"",
                            #  e_cust_contact, price,term, account_list,p.print_id)
    # except:
    #     print("it's handled")

    p = Print(print_details="")
    p.save()
    # try:
    #generate_booking_voucher(li, e_no, date, e_cust_name, e_date, str(slot), hall, "", int(e_guests), "",
                             #e_cust_contact, price,term, account_list,p.print_id)
   # fs = FileSystemStorage("")
    #name_of_pdf = "Salary_Voucher" + str(p.print_id) + ".pdf"
    #with fs.open(name_of_pdf) as pdf:
    #    response = HttpResponse(pdf, content_type='application/pdf')
    #    response['Content-Disposition'] = 'attachment; filename=Salary Voucher.pdf'
    #    return response
    return render(request,'realapp/index.html')

def add_event(request):
    obj1 = Arrangement.objects.all()
    # all menu objects

    obj = Menu.objects.all()

    arrange_list = []
    menu_list = []

    for arrange in obj1:
        arrange_list.append({'arrange_title': arrange.arrange_title, 'arrange_cost': arrange.arrange_cost,
                             'arrange_id': arrange.arrange_id, 'arrange_details': arrange.arrange_details})

    for menu in obj:
        menu_list.append(
            {'menu_details': menu.menu_details, 'menu_cost_perhead': menu.menu_cost_perhead, 'menu_id': menu.menu_id})

    e_date = request.POST.get('event_date', default="")
    date = request.POST.get('event_booking_date', default="")
    hall = request.POST.get('event_hall', default="")
    slot1 = request.POST.get('event_slot', default="")
    e_no = request.POST.get('event_no', default="")
    e_cust_name = request.POST.get('event_cust_name', default="")
    e_cust_email = request.POST.get('event_cust_email', default="")
    e_cust_nic = request.POST.get('event_cust_nic', default="")
    e_cust_contact = request.POST.get('event_cust_contactno', default="")
    e_cust_contact2 = request.POST.get('event_cust_contactno2', default="")
    e_guests = request.POST.get('event_total_guests', default="")
    e_expense = request.POST.get('event_total_expense', default="")
    e_total_amount = request.POST.get('payable_amount', default="")
    e_advance = request.POST.get('event_advance', default="")
    additional_cost_perhead=request.POST.get('additional_cost',default=0)
    additional_overall_cost = request.POST.get('additional_overall_cost', default=0)
    discount_percent=request.POST.get('discount_percent',default=0)
    total_discount=request.POST.get('total_discount',default=0)
    other_time = request.POST.get('other_time', default=0)
    quantity = request.POST.get('quantity', default=0)
    q = request.POST.get('calculate', default=0)

    if additional_cost_perhead=="":
        additional_cost_perhead=0
    if additional_overall_cost=="":
        additional_overall_cost=0
    if total_discount=="":
        total_discount=0
    if discount_percent=="":
        discount_percent=0

    print("quantity        ",quantity,type(quantity))
    if quantity=="":
        quantity=0
    else:
        quantity=int(quantity)

    print("quantity",quantity)

    print(additional_cost_perhead)
    print(additional_overall_cost)
    print(discount_percent)
    print(total_discount)
    print(e_total_amount)


    slot=str(slot1)

    print("info")
    print(slot,type(slot))

    if slot=="3":
        slot=other_time

    print("other time",slot)

    currentDT = datetime.datetime.now()
    date1 = (currentDT.strftime("%Y-%m-%d"))
    e_payment = e_advance+";"+date1+";"

    details = request.POST.get('event_other_details', default="")
    value=request.POST.get('submit',default="")
    dt = parse(date)
    date = dt.strftime('%Y-%m-%d')
    dt1 = parse(str(e_date))
    e_date = dt1.strftime('%Y-%m-%d')
    obj = Booked_Slot.objects.filter(booked_date=e_date)
    # checking if an event is booked on this date
    event_list=[]

    menu_items = request.POST.getlist('menu_list1[]')
    checkboxes = request.POST.getlist('checkbox[]')

    # if len(menu_items)==0:
    #     messages.warning(request, 'Choose a Menu')
    #     return HttpResponse('choose a menu.')
    print(checkboxes)
    print("entered safely here.")
    # form.save(commit=True)
    print()
    if value=="SUBMIT":
        if quantity>0:
            os=Special_Arrangement.objects.get(special_arrange_id=1)
            e_total_amount=int(e_total_amount)+quantity*int(os.special_arrange_cost)
        obj2 = Event(event_no=e_no, event_date=e_date, event_booking_date=date, event_hall=hall, event_slot=str(slot),
                     event_cust_name=e_cust_name, event_cust_email=e_cust_email, event_cust_nic=e_cust_nic,
                     event_cust_contactno=e_cust_contact, event_cust_contactno2=e_cust_contact2,
                     event_total_guests=e_guests, event_total_expense=0, event_total_amount=e_total_amount,
                     event_advance=e_advance, event_payments_details=e_payment, event_details=details,additional_cost_perhead=int(additional_cost_perhead),
                     additional_overall_cost=int(additional_overall_cost),discount=int(total_discount))
        print("about to save")
        obj2.save()
        # getting the arrangements
        if len(checkboxes)>0:

            for i in checkboxes:
                cost = Arrangement.objects.get(arrange_id=i)
                event_arrange = Event_Arrangement(event_arrangement_event_id=Event(obj2.event_id),
                                                  event_arrangement_arrange_id=Arrangement(i),
                                                  event_arrange_cost=cost.arrange_cost,
                                                  event_arrange_details=cost.arrange_details)
                event_arrange.save()
        if quantity>0:
            o=Special_Arrangement.objects.get(special_arrange_id=1)
            e_ar=Event_Special_Arrangement(event_arrangement_event_id=Event(obj2.event_id),
                                           event_special_arrange_id=Special_Arrangement(1),
                                           event_arrange_quantity=quantity,
                                           event_arrange_cost=o.special_arrange_cost,
                                           event_arrange_title=o.special_arrange_title)
            e_ar.save()
        # getting the menu selected
        if len(menu_items)!=0:
            menu_vaganza = Menu.objects.get(menu_id=menu_items[0])
            event_menu = Event_Menu(event_menu_event_id=Event(obj2.event_id), event_menu_menu_id=Menu(menu_items[0]),
                                    menu_cost_perhead=menu_vaganza.menu_cost_perhead,
                                    menu_details=menu_vaganza.menu_details)
            # saving menu
            event_menu.save()

        e = Booked_Slot(booked_slot_event_id=Event(obj2.event_id), booked_date=e_date, booked_hall=hall,
                        booked_slot=slot)

        # saving booked slot

        e.save(force_insert=True)
        messages.info(request,'Event Created.')
        term=[]

        term_obj=Terms.objects.all()
        for i in term_obj:
            term.append(i.term_statement)


        # term = ["non refundable", "conditions apply", "yeah baby my rules"]
        price=""
        if len(menu_items)>0:
            for j in menu_items:
                m=Menu.objects.get(menu_id=str(j))
                price=str(m.menu_cost_perhead)


        account_list = [["", ""], ["Total Guests", int(e_guests)], ["Extra Tables/Chairs", ""],
                        ["Special Arrangements", ""],
                        ["Total Amount", int(e_total_amount)], ["Advance Paid", int(e_advance)], ["Part Payment", int(int(e_total_amount)-int(e_advance))],
                        ["", ""], ["", ""], ["", ""], ["", ""], ["Total Receipts", int(e_advance)]]

        selected_arr = []
        unselected_arr = []
        for i in checkboxes:
            selected_arr.append(int(i))

        all_arr = Arrangement.objects.all()

        for j in all_arr:
            unselected_arr.append(int(j.arrange_id))

        unselected_arr = set(unselected_arr) - set(selected_arr)
        li = []
        if len(selected_arr) > 0:
            for i in selected_arr:
                temp_list = []
                arr = Arrangement.objects.get(arrange_id=str(i))
                temp_list.append(li.__len__() + 1)
                temp_list.append(str(arr.arrange_title))
                temp_list.append("Y")
                temp_list.append(arr.arrange_cost)
                li.append(temp_list)

        if len(unselected_arr) > 0:
            for i in unselected_arr:
                temp_list = []
                arr = Arrangement.objects.get(arrange_id=str(i))
                temp_list.append(li.__len__() + 1)
                temp_list.append(str(arr.arrange_title))
                temp_list.append("")
                temp_list.append("")
                li.append(temp_list)

        special_a = Special_Arrangement.objects.all()
        for k in special_a:
            ev_sp = Event_Special_Arrangement.objects.filter(event_special_arrange_id=k.special_arrange_id,
                                                             event_arrangement_event_id=Event(obj2.event_id))
            temp_list = []
            print("specialllllllllll", ev_sp)
            for s in ev_sp:
                if len(ev_sp) > 0:
                    temp_list.append(li.__len__() + 1)
                    temp_list.append(str(k.special_arrange_title))
                    temp_list.append(str(s.event_arrange_quantity))
                    temp_list.append(str(int(s.event_arrange_cost * s.event_arrange_quantity)))
                    li.append(temp_list)

                else:
                    temp_list.append(li.__len__() + 1)
                    temp_list.append(str(k.special_arrange_title))
                    temp_list.append(str(""))
                    temp_list.append("")
                    li.append(temp_list)

        print("list of printing arrangements", li)


        # li = [[1, "sofa sitting", "yes", 200], [2, "dj system and setup", "no", 2000], [3, "party", "yes", 1500],
        #       [4, "drugs", "yes", 50000]
        #     , [5, "ecstacy", "yes", 5000], [6, "lsd", "yes", 4000], [7, "bhung", "no", 500],
        #       [8, "jack daniels", "yes", 55000]
        #     , [9, "cocaine", "yes", 500000], [10, "hashish", "yes", 5000], [11, "heroine", "yes", 50000],
        #       [12, "drugs", "yes", 50000]
        #     , [13, "drugs", "yes", 50000]]

        # p = Print(print_details="")
        # p.save()
        # generate_booking_voucher(li,e_no,date,e_cust_name,e_date,str(slot),hall,"",int(e_guests),0,
                                #  e_cust_contact,price, term, account_list,p.print_id)
        # ex=Expense(expense_event_id=Event(obj2.event_id),expense_title=" ",expense_date=e_date,expense_details=" ",expense_amount=e_expense)

        # ex.save()
        # return index(request)
    if q=="CALCULATE":
        # messages.info(request, 'CALCULATING')
        print(q)
        return HttpResponse("Calculating")
    currentDT = datetime.datetime.now()
    date = (currentDT.strftime("%Y-%m-%d"))
    object = Event.objects.filter(event_date__gte=date,conclude_event=False)


    for event in object:
        event_list.append(
            {'event_id': event.event_id,
             'event_name': event.event_cust_name + " " + " " + event.event_cust_contactno,
             'event_date': event.event_date})

    return render(request,'realapp/index.html', {'arrange_list': arrange_list, 'menu_list': menu_list,'event_list':event_list})

def about(request):
    obj1 = Arrangement.objects.all()
    # all menu objects

    obj = Menu.objects.all()

    arrange_list = []
    menu_list = []

    for arrange in obj1:
        arrange_list.append({'arrange_title': arrange.arrange_title, 'arrange_cost': arrange.arrange_cost,
                             'arrange_id': arrange.arrange_id, 'arrange_details': arrange.arrange_details})

    print(arrange_list)

    for menu in obj:
        menu_list.append(
            {'menu_details': menu.menu_details, 'menu_cost_perhead': menu.menu_cost_perhead, 'menu_id': menu.menu_id})


    # json for calendar

    currentDT = datetime.datetime.now()
    date = (currentDT.strftime("%Y-%m-%d"))
    object = Event.objects.filter(event_date__gte=date, conclude_event=False)
    count=0
    prev_count=0

    my_list=[]
    for j in object:
        dt = parse(str(j.event_date))
        e_date = dt.strftime('%m/%d/%Y')
        date1=e_date

        if date1==e_date:
            count+=1
        print(e_date)
        my_list.append({'event_date':str(e_date),'event_slot':str(j.event_slot),'event_hall':j.event_hall})
    my_list = json.dumps(my_list)
    print(my_list)

    special_arrangement=[]
    ob1=Special_Arrangement.objects.all()

    print(ob1)

    for i in ob1:
        special_arrangement.append({'title':i.special_arrange_title,'cost':i.special_arrange_cost,'id':i.special_arrange_id})

    print(special_arrangement)

    my_list1=[]
    list1=[]
    o=Booked_Slot.objects.filter(booked_date__gte=date)

    print(o)
    for j in o:
        list1.append(j)

    sorted_list = sorted(list1, key = attrgetter('booked_date'))
    print("list", sorted_list)


    # count=0
    # hall=""
    # slot=""
    # date=""
    # new_date=""
    # consec_date=False
    # not_consec_date=True
    # for k in sorted_list:
    #     print(k.booked_date)
    #     count+=1
    #     print(count)
    #
    #     if count==1:
    #         prev_date = k.booked_date
    #         hall1=k.booked_hall
    #         slot1=k.booked_slot
    #         date1=k.booked_date
    #     print("previous date",prev_date)
    #     print("new date",new_date)
    #     if count!=1:
    #
    #         print("checking")
    #         new_date=k.booked_date
    #         print("new date",new_date)
    #         if prev_date==new_date:
    #             consec_date=True
    #             print(consec_date)
    #             print("date set true")
    #             hall = str(hall)+str(k.booked_hall)
    #             slot = str(slot) + str(k.booked_slot)
    #             date =str(k.booked_date)
    #         if prev_date!=new_date and new_date!="":
    #             print("here")
    #             not_consec_date=False
    #
    #     elif count!=1 or not_consec_date==False:
    #         count=0
    #         prev_date
    #         if date!="":
    #             dt = parse(str(date))
    #             e_date = dt.strftime('%m/%d/%Y')
    #         if date1!="":
    #             dt = parse(str(date1))
    #             e_date1 = dt.strftime('%m/%d/%Y')
    #         dt = parse(str(k.booked_date))
    #         e_date2 = dt.strftime('%m/%d/%Y')
    #         if consec_date==False:
    #             my_list.append({'event_date':str(e_date2),'event_slot':str(k.booked_slot),'event_hall':k.booked_hall}) and my_list.append({'event_date':str(e_date1),'event_slot':str(slot1),'event_hall':hall1})
    #             hall1=""
    #             slot1=""
    #             date1=""
    #         if consec_date==True:
    #             my_list.append({'event_date': str(e_date2), 'event_slot': str(k.booked_slot),
    #                             'event_hall': k.booked_hall}) and my_list.append(
    #                 {'event_date': str(e_date), 'event_slot': str(slot), 'event_hall': hall})
    #             hall1 = ""
    #             slot1 = ""
    #             date1 = ""
    #             hall = ""
    #             slot = ""
    #             date = ""
    #
    # print("list          ",my_list)


    return render(request, 'realapp/about.html', {'arrange_list': arrange_list, 'menu_list': menu_list,'my_list':my_list,'special_arrangement':special_arrangement})

def add_daily_expense(request):
    currentDT = datetime.datetime.now()
    print("Entered")
    # expense_id=request.POST.get('expense_id',default=None)
    date=request.POST.get('date',default="")
    expense_title = request.POST.get('expense_title', default=None)
    expense_amount = request.POST.get('expense_amount', default=None)
    expense_details = request.POST.get('details', default="")
    print(expense_title)
    print(expense_amount)
    dt = parse(date)
    date = dt.strftime('%Y-%m-%d')
    # print(expense_id)
    # date = (currentDT.strftime("%Y-%m-%d"))
    if request.method == 'POST':
        obj = Expense(expense_event_id=None, expense_title=expense_title, expense_date=date, expense_details=expense_details,
                      expense_amount=expense_amount)
        obj.save()

        messages.info(request,'Daily Expense Added.')
        id = obj.expense_id

        expense_list = []
        obj = realapp.models.Expense.objects.filter(expense_date__month=str(datetime.datetime.today().month),
                                                    expense_event_id__isnull=True)
        if obj.count() > 0:
            print(obj)

        if obj.count() > 0:
            for expense in obj:
                expense_list.append({'expense_id': expense.expense_id, 'expense_event_id': expense.expense_event_id,
                                     'expense_title': expense.expense_title, 'expense_date': expense.expense_date,
                                     'expense_details': expense.expense_details,
                                     'expense_amount': expense.expense_amount})

        return render(request, 'realapp/Gen_Expense.html',{'expense_list':expense_list})

    return render(request, 'realapp/Gen_Expense.html')

def Expenses_info(request, event_id):
    print(event_id)
    obj = realapp.models.Expense.objects.filter(expense_event_id=event_id)
    print(obj)

    expense_list = []
    if obj.count() > 0:
        for expense in obj:
            expense_list.append({'expense_id': expense.expense_id, 'expense_event_id': expense.expense_event_id,
                                 'expense_title': expense.expense_title, 'expense_date': expense.expense_date,
                                 'expense_details': expense.expense_details, 'expense_amount': expense.expense_amount})

    return render(request, 'realapp/Expenses.html', {'expense_list': expense_list})

def Gen_Expense_gen_expense(request):
    return render(request, 'realapp/Gen_Expense.html')

def add_salary(request):
    object = Employee.objects.all()

    emp_list = []

    obj = Salary.objects.filter(salary_month__year=str(datetime.datetime.today().year),
                                salary_month__month=str(datetime.datetime.today().month))

    emp_list1 = []
    for emp in obj:
        obj1 = Employee.objects.get(emp_id=str(emp.salary_emp_id))
        name = obj1.emp_name
        emp_list1.append({'emp_id': emp.salary_emp_id, 'emp_name': name, 'emp_salary': emp.salary_amount_paid,
                          'salary_month': emp.salary_month, 'paid_status': emp.paid_status})

    print(obj)
    emp_list1 = []

    print(emp_list1)
    for emp in object:
        emp_list.append({'emp_id': emp.emp_id, 'emp_name': emp.emp_name, 'emp_joindate': emp.emp_joindate,
                         'emp_salary': emp.emp_salary, 'emp_status': emp.emp_status,
                         'emp_designation': emp.emp_designation})

    currentDT = datetime.datetime.now()
    emp_id1 = request.POST.get('emp_id', default="")
    date1 = request.POST.get('date', default=None)
    dt = parse(date1)
    date2 = dt.strftime('%Y-%m-%d')
    date = date2

    year=""
    month=""
    count=0

    for i in date:
        if i=="-":
            count=count+1
        if count==0:
            year=year+i
        if count==1 and i!="-":
            month=month+i

    print("date data type", type(date))

    paid_amount = request.POST.get('salary_amount', default="")
    details = request.POST.get('details', default="")

    e = Employee.objects.get(emp_id=str(emp_id1))
    print(emp_id1)

    print("year",year)
    print("month",month)
    obj1 = Salary.objects.filter(salary_emp_id=str(emp_id1),salary_month__year=year, salary_month__month=month)
    if obj1.count() == 0:
        obj = Salary(salary_emp_id=Employee(emp_id1), salary_month=date, salary_amount_paid=paid_amount,
                     salary_total_amount=e.emp_salary, paid_status="paid", salary_remarks=details)
        obj.save()

        emp_list1 = []
        obj = Salary.objects.filter(salary_month__year=str(datetime.datetime.today().year),
                                    salary_month__month=str(datetime.datetime.today().month))

        for emp in obj:
            obj1 = Employee.objects.get(emp_id=str(emp.salary_emp_id))
            name = obj1.emp_name
            emp_list1.append({'emp_id': obj1.emp_id, 'emp_name': name, 'emp_salary': emp.salary_amount_paid,
                              'salary_month': emp.salary_month, 'paid_status': emp.paid_status,'salary_id':emp.salary_id})

        print("emp_list1",emp_list1)
        messages.info(request, 'Salary Paid.', {'emp_list': emp_list, 'emp_list1': emp_list1})

    else:
        emp_list1 = []
        obj = Salary.objects.filter(salary_month__year=str(datetime.datetime.today().year),
                                    salary_month__month=str(datetime.datetime.today().month))

        for emp in obj:
            obj1 = Employee.objects.get(emp_id=str(emp.salary_emp_id))
            name = obj1.emp_name
            emp_list1.append({'emp_id': obj1.emp_id, 'emp_name': name, 'emp_salary': emp.salary_amount_paid,
                              'salary_month': emp.salary_month, 'paid_status': emp.paid_status,
                              'salary_id': emp.salary_id})
        messages.info(request,'Salary Already Paid.',{'emp_list': emp_list, 'emp_list1': emp_list1})
        # return HttpResponse("Employee already paid")
    print("here 2")
    return render(request, 'realapp/salary.html', {'emp_list': emp_list, 'emp_list1': emp_list1})

def filter_gen_expense(request):
    expense_list = []
    year1 = request.POST.get('year1', default="")
    month1 = request.POST.get('month1', default="")
    day1 = request.POST.get('day1', default="")
    year2 = request.POST.get('year2', default="")
    month2 = request.POST.get('month2', default="")
    day2 = request.POST.get('day2', default="")
    data = datetime.datetime.today().strftime('%Y-%m-%d')

    print(year1)
    print(month1)
    print(day1)

    print(year2)
    print(month2)
    print(day2)
    # filtering of general/daily expenses


    try:
        if year1!="":
            print("here")
            object = Expense.objects.filter(expense_date__year=year1,expense_event_id__isnull=True)

        if year1 !="" and month1!="":
            print("here2")
            object = Expense.objects.filter(expense_date__year=year1, expense_date__month=month1,expense_event_id__isnull=True)

        if year1 !="" and month1!="" and day1!="":
            print("her3")
            object = Expense.objects.filter(expense_date__year=year1,expense_date__month=month1,expense_date__day=day1,expense_event_id__isnull=True)

        if year1 !="" and month1!="" and day1!="" and year2!="":
            print("here4")
            date=year1+"-"+month1+"-"+day1
            object = Expense.objects.exclude(expense_date__year__gte=year2,expense_event_id__isnull=True).filter(expense_date__gte=date,expense_event_id__isnull=True)

        if year1!="" and year2!="":
            print("here5")
            object = Expense.objects.exclude(expense_date__year__gte=year2,expense_event_id__isnull=True).filter(expense_date__year__gte=year1,expense_event_id__isnull=True)

        if year1 !="" and month1!="" and day1!="" and year2!="" and month2!="":
            print("here6")
            date=year1+"-"+month1+"-"+day1
            object = Expense.objects.exclude(expense_date__year__gte=year2,expense_date__month__gte=month2,expense_event_id__isnull=True).filter(expense_date__gte=date,expense_event_id__isnull=True)

        if year1 !="" and month1!="" and day1!="" and year2!="" and month2!="" and day2!="":
            print("here7")
            date=year1+"-"+month1+"-"+day1
            date2 = year2 + "-" + month2 + "-" + day2
            object = Expense.objects.exclude(expense_date__gte=date2,expense_event_id__isnull=True).filter(expense_date__gte=date,expense_event_id__isnull=True)

        if year1 == "" and month1 == "" and day1 == "" and year2 == "" and month2 == "" and day2 == "":
            print("here8")
            currentDT = datetime.datetime.now()
            date = (currentDT.strftime("%Y-%m-%d"))
            object = Expense.objects.filter(expense_date__gte=date,expense_event_id__isnull=True)

        if year1 !="" and month1!="" and year2!="" and month2!="":
            print("here9")
            object = Expense.objects.exclude(expense_date__year__gte=year2,expense_date__month__gte=month2,expense_event_id__isnull=True).filter(expense_date__year__gte=year1,expense_date__month__gte=month1,expense_event_id__isnull=True)

        if year1 =="" and month1!="" and day1!="" and year2=="" and month2!="" and day2!="":
            print("here10")
            date=datetime.now().year+"-"+month1+"-"+day1
            object = Expense.objects.exclude(expense_date__year__gte=str(datetime.datetime.today().year),expense_date__month__gte=month2,expense_event_id__isnull=True).filter(expense_date__gte=date,expense_event_id__isnull=True)

        if year1=="" and year2=="" and month1!="" and month2!="":
            print("here11")
            object = Expense.objects.exclude(expense_date__year__gte=str(datetime.datetime.today().year), expense_date__month__gte=month2,expense_event_id__isnull=True).filter(expense_date__year__gte=str(datetime.datetime.today().year),
                                                                                                                                                  expense_date__month__gte=month1,expense_event_id__isnull=True)

        if month1!="" and year1=="" and year2=="" and month2=="" and day1=="" and day2=="":
            print("here12")
            object = Expense.objects.filter(expense_date__month=month1,expense_event_id__isnull=True)

        if month2!="" and year1=="" and year2=="" and month1=="" and day1=="" and day2=="":
            print("here13")
            object = Expense.objects.exclude(expense_date__year__gte=str(datetime.datetime.today().year),
                                             expense_date__month__gte=month2,expense_event_id__isnull=True).filter(
                expense_date__year__gte=str(datetime.datetime.today().year),expense_event_id__isnull=True)

        count=0
        t_expense=0
        if object.count()==0:
                return render(request,'realapp/Gen_expense.html')
        # obj=object.filter(expense_event_id__isnull=True)
        if object.count() > 0:
            print("here14")
            object1=object.order_by('-expense_date')
            for expense in object1:
                count=count+1
                t_expense=t_expense+expense.expense_amount
                expense_list.append({'expense_id': expense.expense_id, 'expense_event_id': expense.expense_event_id,
                                     'expense_title': expense.expense_title, 'expense_date': expense.expense_date,
                                     'expense_details': expense.expense_details,
                                     'expense_amount': expense.expense_amount})

        report_list = []

        report_list.append({'count': count, 't_expense': t_expense})

        return render(request, 'realapp/Gen_Expense.html', {'expense_list': expense_list, 'report_list': report_list})
    except:
        print("can't filter")
    return render(request, 'realapp/Gen_Expense.html', {'expense_list': expense_list})

def Gen_Expense(request):
    expense_list = []
    count=0
    t_expense=0
    obj = realapp.models.Expense.objects.filter(expense_date__month=str(datetime.datetime.today().month),
                                                expense_event_id__isnull=True).order_by('-expense_date')
    if obj.count() > 0:
        print(obj)

    if obj.count() > 0:
        for expense in obj:
            count=count+1
            t_expense=t_expense+expense.expense_amount
            expense_list.append({'expense_id': expense.expense_id, 'expense_event_id': expense.expense_event_id,
                                 'expense_title': expense.expense_title, 'expense_date': expense.expense_date,
                                 'expense_details': expense.expense_details, 'expense_amount': expense.expense_amount})

    report_list=[]

    report_list.append({'count':count,'t_expense':t_expense})

    return render(request, 'realapp/Gen_Expense.html', {'expense_list': expense_list,'report_list':report_list})

def filter(request):
    object = Employee.objects.all()

    emp_list = []
    emp_id = []

    for emp in object:
        emp_list.append({'emp_id': emp.emp_id, 'emp_name': emp.emp_name, 'emp_joindate': emp.emp_joindate,
                         'emp_salary': emp.emp_salary, 'emp_status': emp.emp_status,
                         'emp_designation': emp.emp_designation})
    for e in object:
        emp_id.append(e.emp_id)

    year = request.POST.get('year', default="")
    if year == "":
        year = str(datetime.datetime.today().year)
    month = request.POST.get('month', default="")

    print("month data type",type(month))
    id = request.POST.get('emp_id', default="")
    status = "paid"
    emp_sal = Salary.objects.filter(salary_month__year=year, salary_month__month=month)
    salary_emp_id = []

    salary_emp_id.append(p.salary_emp_id for p in emp_sal)

    # print("emp id",emp_id)
    # print("salary emp id",salary_emp_id)
    if id !="":
        print(id)
        print(month)
        print(year)
        # if status=="paid":
        print("with id")
        obj = Salary.objects.filter(salary_emp_id=id, salary_month__year=year, salary_month__month=month)
        # obj = Salary.objects.filter(salary_month__year=year, salary_month__month=month)
        print(obj)
        emp_list1 = []
        for emp in obj:
            obj1 = Employee.objects.get(emp_id=id)
            name = obj1.emp_name
            print(name)
            emp_list1.append({'salary_id':emp.salary_id,'emp_id': emp.salary_emp_id, 'emp_name': name, 'emp_salary': emp.salary_amount_paid,
                              'salary_month': emp.salary_month, 'paid_status': emp.paid_status})
        print(emp_list1)
    # else:

    else:
        print(id)
        print(month)
        print(year)
        emp_list1 = []
        ob = Salary.objects.filter(salary_month__year=year,salary_month__month=month)
        print(ob)
        if len(ob) >= 1:
            for i in ob:
                print("here ", i)
                try:
                    obj = realapp.models.Salary.objects.get(salary_emp_id=str(i.salary_emp_id),salary_month__year=year,salary_month__month=month)
                    print(obj.salary_emp_id)
                    obj1 = Employee.objects.get(emp_id=str(obj.salary_emp_id))
                    name = obj1.emp_name
                    print(name)
                    emp_list1.append({'salary_id':obj.salary_id,'emp_id': obj.salary_emp_id, 'emp_name': name,
                                      'emp_salary': obj.salary_amount_paid,
                                      'salary_month': obj.salary_month,
                                      'paid_status': obj.paid_status})
                except Salary.DoesNotExist:
                    print("none")

    return render(request, 'realapp/salary.html', {'emp_list': emp_list, 'emp_list1': emp_list1})

def get_events(request):
    year = request.POST.get('year', default="")

    month = request.POST.get('month', default="")

    no = request.POST.get('phone_no', default="")

    print(month)
    if year == "" and month == "None" and no == "":
        currentDT = datetime.datetime.now()
        date = (currentDT.strftime("%Y-%m-%d"))
        obj = Event.objects.filter(event_date__gte=date,conclude_event=False)

    if year == "" and month=="None" and no != "":
        obj = realapp.models.Event.objects.filter(Q(event_cust_contactno=no) | Q(event_cust_contactno2=no),conclude_event=False)

    if year != "" and month=="None" and no=="":
        obj = realapp.models.Event.objects.filter(event_date__year=year,conclude_event=False)

    if year!="" and month!="None" and no=="":
        obj = realapp.models.Event.objects.filter(event_date__year=year,event_date__month=month,conclude_event=False)

    if year !="" and month!="None" and no != "" or year=="" and month!="None" and no!="" or year!="" and month=="None" and no!="":
        obj = realapp.models.Event.objects.filter(Q(event_cust_contactno=no) | Q(event_cust_contactno2=no),conclude_event=False)


    if year == "" and month!="None":
        obj = realapp.models.Event.objects.filter(event_date__year=str(datetime.datetime.today().year),event_date__month=month,conclude_event=False)

    if year=="" and month!="" and no!="":
        obj = realapp.models.Event.objects.filter(Q(event_cust_contactno=no) | Q(event_cust_contactno2=no),conclude_event=False)

    event_list = []

    for event in obj:
        event_list.append({'event_id': event.event_id,
                           'event_name': event.event_cust_name + " " + " " + event.event_cust_contactno,
                           'event_date': event.event_date})


    return render(request, 'realapp/Events.html', {'event_list': event_list})

def Events(request):
    currentDT = datetime.datetime.now()
    date = (currentDT.strftime("%Y-%m-%d"))
    object = Event.objects.filter(event_date__gte=date,conclude_event=False)

    event_list = []

    for event in object:
        event_list.append(
            {'event_id': event.event_id, 'event_name': event.event_cust_name + " " + " " + event.event_cust_contactno,
             'event_date': event.event_date})

    return render(request, 'realapp/Events.html', {'event_list': event_list})

def Info(request, event_id):
    object = Event.objects.filter(event_id=event_id)
    print(object)

    concat=" "
    count=0
    # print(object1)
    object1 = Event.objects.get(event_id=event_id)

    print(object1.event_payments_details)
    for k in object1.event_payments_details:
        # semi_colon_count=0
        if k==";":
            count=count+1
            concat=concat+" "


        if count==2:
            # semi_colon_count=semi_colon_count+1
            concat=concat+", "
            count=0
        if k!=";":
            concat = concat + k

    print("concat",concat)

    print(object)
    print(event_id)

    event_list = []
    special_arrangement=[]

    ob1 = Expense.objects.filter(expense_event_id=str(event_id))
    j = 0
    if ob1.count() > 0:
        for i in ob1:
            j = j + i.expense_amount

    for event in object:
        print("event slot",type(str(event.event_slot)))
        event_list.append({'event_id': event.event_id, 'event_id2': event.event_id, 'event_no': event.event_no,
                           'event_cust_name': event.event_cust_name, 'event_cust_email': event.event_cust_email,
                           'event_cust_nic': event.event_cust_nic, 'event_cust_contactno': event.event_cust_contactno,
                           'event_cust_contactno2': event.event_cust_contactno2,
                           'event_total_guests': event.event_total_guests, 'event_advance': event.event_advance,
                           'event_total_amount': event.event_total_amount,
                           'event_total_expense': j, 'event_payments_details': concat,
                           'event_date': event.event_date,
                           'event_hall': event.event_hall, 'event_slot': str(event.event_slot),
                           'event_booking_date': event.event_booking_date,'event_details':event.event_details,
                           'remaining':event.event_total_amount-event.event_advance})

        # all arrangement objects
        event_arrange_ids_list=[]
        arrange_ids_list=[]

        obj1 = Arrangement.objects.all()
        # all menu objects

        obj = Menu.objects.all()

        event_arrangement_list = []

        event_arrangement_list1 = []
        event_arrangements = Event_Arrangement.objects.filter(event_arrangement_event_id=event_id)

        if len(event_arrangements) != 0:

            for event in event_arrangements:
                ob = Arrangement.objects.get(arrange_id=str(event.event_arrangement_arrange_id))
                event_arrange_ids_list.append(int(ob.arrange_id))
                event_arrangement_list1.append({'arrange_cost': event.event_arrange_cost,
                                                'arrange_id': ob.arrange_id,'arrange_details': ob.arrange_details
                                                ,'arrange_title': ob.arrange_title})

        for arrange in obj1:
            arrange_ids_list.append(int(arrange.arrange_id))

        list1=list(set(arrange_ids_list) - set(event_arrange_ids_list))

        print("event_arrangement ids list",event_arrange_ids_list)
        print("arrange ids",arrange_ids_list)
        print("list1",list1)
        for i in list1:
            ob2=Arrangement.objects.get(arrange_id=str(i))
            event_arrangement_list.append({'arrange_title': ob2.arrange_title, 'arrange_cost': ob2.arrange_cost,
                                           'arrange_id': ob2.arrange_id,
                                           'arrange_details': ob2.arrange_details})


        print("event_arrangement list",event_arrangement_list)
        print("event arrangement list1",event_arrangement_list1)



        ob2 = Event_Special_Arrangement.objects.filter(event_arrangement_event_id=event_id)
        print("ob2 ob2 ob2",ob2)
        # print(ob2.event_arrange_quantity)
        if len(ob2)>0:
            for i in ob2:
                special_arrangement.append({'quantity': i.event_arrange_quantity,'cost':i.event_arrange_cost})

        event_menu_list = []
        event_menu_list1 = []
        for menu in obj:
            event_menu_list.append({'menu_details': menu.menu_details, 'menu_cost_perhead': menu.menu_cost_perhead,
                                    'menu_id': menu.menu_id})

        event_menu = Event_Menu.objects.filter(event_menu_event_id=event_id)
        print(event_menu)
        if len(event_menu) != 0:
            for event in event_menu:
                objj = Menu.objects.get(menu_id=str(event.event_menu_menu_id))
                event_menu_list1.append({'menu_cost_perhead': event.menu_cost_perhead, 'event_menu_id': objj.menu_id})

        # messages.success(request, 'Profile details updated.')
    my_list = []
    currentDT = datetime.datetime.now()
    date = (currentDT.strftime("%Y-%m-%d"))
    object = Event.objects.filter(event_date__gte=date, conclude_event=False)
    for j in object:
        dt = parse(str(j.event_date))
        e_date = dt.strftime('%m/%d/%Y')

        print(e_date)
        my_list.append({'event_date': str(e_date), 'event_slot': str(j.event_slot), 'event_hall': j.event_hall})
    my_list = json.dumps(my_list)

    return render(request, 'realapp/Info.html',
                  {'event_arrangement_list1': event_arrangement_list1, 'event_list': event_list,
                   'event_arrangement_list': event_arrangement_list, 'event_menu_list': event_menu_list,
                   'event_menu_list1': event_menu_list1,'my_list':my_list,'special_arrangement':special_arrangement})

def generate_salary_voucher(ddate,amount,details,paid_to,paid_by,v_id):
    d = canvas.Canvas("Salary_Voucher"+str(v_id)+".pdf", pagesize=portrait(A4))
    d.drawImage("D:/rafi banquet hall/realproject/static/images/v1.jpg", 170, 770, 285, 50)
    d.setFont("Helvetica", 18)
    d.drawString(30, 730, "Dated As:")
    d.drawString(115,730,"____________")
    d.drawString(120,728,str(ddate))
    d.drawString(30, 670, "Amount of Voucher:")
    d.drawString(200, 670, "______________________________")
    d.drawString(215,668,str(amount))
    d.drawString(30,640,"Details:")
    d.drawString(100, 640, "___________________________________________")
    d.drawString(105, 638, str(details))
    d.drawString(30,610,"Paid to:")
    d.drawString(100, 610, "___________________________________________")
    d.drawString(105, 608, str(paid_to))
    d.drawString(30, 580,"Paid by:")
    d.drawString(100, 580, "___________________________________________")
    d.drawString(105, 578, str(paid_by))
    d.drawString(160, 510, "_____________")
    d.drawString(170, 490, "Approved By")
    d.drawString(390, 510, "____________")
    d.drawString(410,490,"Signed By")

    d.drawImage("D:/rafi banquet hall/realproject/static/images/v1.jpg", 170, 390, 285, 50)
    d.drawString(30, 350, "Dated As:")  # write your text
    d.drawString(115, 350, "____________")
    d.drawString(120, 348, str(ddate))
    d.drawString(30, 290, "Amount of Voucher:")
    d.drawString(200, 290, "______________________________")
    d.drawString(205, 288, str(amount))
    d.drawString(30, 260, "Details:")
    d.drawString(100, 260, "___________________________________________")
    d.drawString(105, 258, str(details))
    d.drawString(30, 230, "Paid to:")
    d.drawString(100, 230, "___________________________________________")
    d.drawString(105, 228, str(paid_to))
    d.drawString(30, 200, "Paid by:")
    d.drawString(100, 200, "___________________________________________")
    d.drawString(105, 198, str(paid_by))
    d.drawString(160, 130, "_____________")
    d.drawString(170, 110, "Approved By")
    d.drawString(390, 130, "____________")
    d.drawString(410, 110, "Signed By")

    d.showPage()
    d.save()

def sform(request,salary_id):
    obj = realapp.models.Salary.objects.get(salary_id=salary_id)

    obj2 = realapp.models.Salary.objects.filter(salary_id=salary_id)

    salary_list=[]

    obj1 = Employee.objects.get(emp_id=str(obj.salary_emp_id))
    name = obj1.emp_name

    print(name)

    for i in obj2:
        salary_list.append({'salary_date':i.salary_month,'emp_name':name,'salary_id':i.salary_id,'salary_amount_paid':i.salary_amount_paid,'salary_remarks':i.salary_remarks})
    #generate_salary_voucher(obj.salary_month,obj.salary_amount_paid,obj.salary_remarks,name," ",1)
    return render(request,'realapp/sform.html',{'salary_list':salary_list})

def update_salary(request,salary_id):
    amount=request.POST.get('amount',default="")
    details = request.POST.get('details',default="")
    date = request.POST.get('date',default="")
    emp_name=request.POST.get('name',default="")

    update_value=request.POST.get('update',default="")
    delete_value=request.POST.get('delete',default="")

    dt = parse(date)
    date = dt.strftime('%Y-%m-%d')

    print("date data type",type(date))

    if delete_value=="DELETE":

        print("deleted")
        obj=Salary.objects.get(salary_id=salary_id)
        obj.delete()

        messages.info(request, 'Salary Deleted.')

    if update_value=="UPDATE":
        obj = Salary.objects.filter(salary_id=salary_id)
        obj.update(salary_amount_paid=amount,salary_remarks=details,salary_month=date)
        p = Print(print_details="")
        p.save()
        # try:
        generate_salary_voucher(date,amount,details,emp_name,"",p.print_id)
        GHOSTSCRIPT_PATH = "C:\\Program Files\\gs\\gs9.23\\bin\\gswin64.exe"
        GSPRINT_PATH = "C:\\Program Files\\Ghostgum\\gsview\\gsprint.exe"

        # YOU CAN PUT HERE THE NAME OF YOUR SPECIFIC PRINTER INSTEAD OF DEFAULT
        currentprinter = win32print.GetDefaultPrinter()

        win32api.ShellExecute(0, 'open', GSPRINT_PATH,
                              '-ghostscript "' + GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" "D:\\rafi banquet hall\\realproject\\Salary_Voucher"'+str(p.print_id)+"'.pdf"'"',
                              '.', 0)
        # win32api.ShellExecute(0, "print", '"D:\\rafi banquet hall\\realproject\\Salary_Voucher"'+str(p.print_id)+'.pdf', '/d:"%s"' % currentprinter, ".", 0)
        # except:
        #     print("nothing")

    # salary view listing
    object = Employee.objects.all()

    emp_list = []
    obj = Salary.objects.filter(salary_month__year=str(datetime.datetime.today().year),
                                salary_month__month=str(datetime.datetime.today().month))

    messages.info(request, 'Salary Updated.')
    emp_list1 = []
    for emp in obj:
        obj1 = Employee.objects.get(emp_id=str(emp.salary_emp_id))
        name = obj1.emp_name
        emp_list1.append({'salary_id': emp.salary_id, 'emp_id': emp.salary_emp_id, 'emp_name': name,
                          'emp_salary': emp.salary_amount_paid,
                          'salary_month': emp.salary_month, 'paid_status': emp.paid_status})

    print(emp_list1)

    for emp in object:
        emp_list.append({'emp_id': emp.emp_id, 'emp_name': emp.emp_name, 'emp_joindate': emp.emp_joindate,
                         'emp_salary': emp.emp_salary, 'emp_status': emp.emp_status,
                         'emp_designation': emp.emp_designation})

    return render(request,'realapp/salary.html',{'emp_list':emp_list,'emp_list1':emp_list1})

def add_event_expense(request, event_id):
    # event_id=request.POST.get('event_id',default=None)
    title=request.POST.get('title',default="")
    amount = request.POST.get('amount', default=None)
    details = request.POST.get('details', default=None)
    currentDT = datetime.datetime.now()
    date = (currentDT.strftime("%Y-%m-%d"))
    print("event id", event_id)
    print("amount", amount)
    print("details", details)

    obj2=Expense.objects.filter(expense_title=title,expense_amount=amount,expense_details=details,expense_date=date)
    if obj2.count()==0:
        expense = Expense(expense_event_id=Event(event_id), expense_details=details, expense_amount=amount,
                          expense_date=date, expense_title=title)
        expense.save()

    return Info(request, event_id)
    # return render(request,'realapp/Info.html')

def update_event_expense(request, expense_event_id, expense_id):
    # event_id=request.POST.get('expense_event_id',default="")
    # expense_id = request.POST.get('expense_id', default="")
    title=request.POST.get('title',default="")
    expense_amount = request.POST.get('expense_amount', default="")
    expense_details = request.POST.get('expense_details', default="")

    u_value = request.POST.get('update', default="")
    d_value= request.POST.get('delete', default="")
    print(expense_event_id)
    print(expense_id)
    print(expense_amount)
    print(expense_details)
    currentDT = datetime.datetime.now()
    date = (currentDT.strftime("%Y-%m-%d"))

    obj2 = realapp.models.Expense.objects.filter(expense_id=str(expense_id))

    try:

        if u_value=="UPDATE":
            obj2.update(expense_amount=expense_amount, expense_details=expense_details, expense_date=date,expense_title=title)

        if d_value=="DELETE":
            obj2.delete()
    except:
        print("none")
    obj = realapp.models.Expense.objects.filter(expense_event_id=str(expense_event_id))
    print(obj)

    expense_list = []
    if obj.count() > 0:
        for expense in obj:
            expense_list.append({'expense_id': expense.expense_id, 'expense_event_id': expense.expense_event_id,
                                 'expense_title': expense.expense_title, 'expense_date': expense.expense_date,
                                 'expense_details': expense.expense_details, 'expense_amount': expense.expense_amount})

    return render(request, 'realapp/Expenses.html', {'expense_list': expense_list})

def update_daily_expense(request, expense_id):
    title = request.POST.get('title', default="")
    amount = request.POST.get('amount', default="")
    details = request.POST.get("details", default="")
    date=request.POST.get('date', default="")
    dt = parse(date)
    date = dt.strftime('%Y-%m-%d')

    u_value=request.POST.get('update',default="")
    d_value=request.POST.get('delete',default="")


    obj2 = realapp.models.Expense.objects.filter(expense_id=str(expense_id))


    if u_value == "UPDATE":
        obj2.update(expense_amount=str(amount), expense_details=str(details), expense_date = date,expense_title=str(title))
        messages.info(request, 'Daily Expense Updated.')

    if d_value=="DELETE":
        obj2.delete()
        messages.info(request, 'Daily Expense Deleted.')

    expense_list = []

    count=0
    t_expense=0
    obj = realapp.models.Expense.objects.filter(expense_date__month=str(datetime.datetime.today().month),
                                                expense_event_id__isnull=True)
    if obj.count() > 0:
        print(obj)

    if obj.count() > 0:
        for expense in obj:
            count=count+1
            t_expense=t_expense+expense.expense_amount
            expense_list.append({'expense_id': expense.expense_id, 'expense_event_id': expense.expense_event_id,
                                 'expense_title': expense.expense_title, 'expense_date': expense.expense_date,
                                 'expense_details': expense.expense_details, 'expense_amount': expense.expense_amount})

    report_list = []

    report_list.append({'count': count, 't_expense': t_expense})

    return render(request, 'realapp/Gen_Expense.html', {'expense_list': expense_list,'report_list':report_list})

def eform(request, expense_id, expense_event_id):
    obj = Expense.objects.get(expense_id=expense_id)
    expense_list = []
    # for i in obj:
    expense_list.append(
        {'expense_event_id': expense_event_id, 'expense_id': expense_id, 'expense_event_id': obj.expense_event_id,
         'expense_amount': obj.expense_amount,
         'expense_details': obj.expense_details,'expense_title':obj.expense_title})

    return render(request, 'realapp/eform.html', {'expense_list': expense_list})

def gen_form(request, expense_id):
    obj = Expense.objects.get(expense_id=expense_id)
    expense_list = []
    # for i in obj:
    expense_list.append(
        {'expense_id': expense_id,
         'expense_amount': obj.expense_amount,
         'expense_title':obj.expense_title,
         'expense_details': obj.expense_details,'expense_date':obj.expense_date})

    print(expense_list)

    return render(request, 'realapp/genform.html', {'expense_list': expense_list})

def userprofile(request):
    return render(request, 'realapp/index.html')

def genform(request):
    return render(request,'realapp/genform.html')

def login1(request):
    request.session.set_test_cookie()
    return render(request,'realapp/login1.html')

def generate_booking_voucher(arrangements,serial_no,booking_date,name,f_date,f_time,hall_no,f_type,guest,per_head,contact_no,menu_cost,terms,aclist,v_id):
    d = canvas.Canvas("Booking_Voucher"+str(v_id)+".pdf", pagesize=portrait(A4))
    d.drawImage("rafibanquet.pythonanywhere.com/images/elogo.jpg", 20, 725, 90, 90)
    d.setFillColorRGB(1, 0, 0)
    d.setFont("Times-BoldItalic", 25)
    d.drawString(185, 790, "Rafi Banquet & Event Organizer")
    d.setFont("Times-BoldItalic", 10)
    d.drawString(130, 775, "Klarak Abad Road near Govt.Hospital Kot Radha Klshen email:rafibanquet16@gmail.com tel:0492 385471-2")

    d.drawImage("{% static 'images/elogo.jpg' %}",240,730,190,20)
    d.setFont("Times-BoldItalic", 11)
    d.drawString(20,700, "Serial No.  ____________")
    d.drawString(70,700,str(serial_no))
    d.drawString(420,700,"Booking Date  ____________")
    d.drawString(500, 700, str(booking_date))

    d.drawString(20,675,"Name _____________________________________________")
    d.drawString(60, 675, str(name))
    d.drawString(320,675, "Function Date _____________")
    d.drawString(400, 675, str(f_date))
    d.drawString(480, 675, "Time ____________")
    d.drawString(530, 675, str(f_time))

    d.drawString(20, 650, "Hall # ____________")
    d.drawString(80, 650, str(hall_no))
    d.drawString(120, 650, "Type of Function ________________________")
    d.drawString(220, 650, str(f_type))
    d.drawString(340, 650, "No of Guest ____________")
    d.drawString(440, 650, str(guest))
    d.drawString(470, 650, "Per Head __________")
    d.drawString(530, 650, str(per_head))


    d.drawString(20, 625, "Contact Nos ____________________________________________________")
    d.drawString(100, 625, str(contact_no))
    d.drawString(380, 625, "Menu Per Head ________________")
    d.drawString(480, 625, str(menu_cost))


    build_accounts_table(accounts_style_sheet(),aclist,d)
    #d.drawImage("account.jpg",350,350,220,220)
    build_flowables(stylesheet(),arrangements,d,len(arrangements))
    d.drawImage("D:/rafi banquet hall/realproject/static/images/terms.jpg", 20, 260, 160, 16)
    print_terms(d, terms)
    # d.drawString(240,380,"yes")
    print(d.getAvailableFonts())
    d.showPage()
    d.save()

def accounts_style_sheet():
    return {
        'table_default': TableStyle(
            [
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.red),
                # ('TEXTFONT', (0, 0), (2, 2),'Helvetica'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.red),
                # ('INNERGRID', (1, 1), (2, 2), 0.5, colors.red),
                ('BOX', (0, 0), (1, -1), 0.25, colors.red),

            ]
        ),
    }

def stylesheet():
    return {
        'table_default': TableStyle(
            [
                ('TEXTCOLOR', (0,0),(-1,-1),colors.red),
                #('TEXTFONT', (0, 0), (2, 2),'Helvetica'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.red),
                #('INNERGRID', (1, 1), (2, 2), 0.5, colors.red),
                ('BOX', (0, 0), (3, -1), 0.25, colors.red),

            ]
        ),
    }

def build_accounts_table(stylesheet,list,d):
    table1 = Table(
        list
        , colWidths=[4 * cm, 4 * cm],
        style=stylesheet['table_default'],
    )
    d.drawImage("D:/rafi banquet hall/realproject/static/images/adpic.jpg",350,545,228,25)
    table1.wrapOn(d, 1000, 500)
    table1.drawOn(d,350,329)

def build_flowables(stylesheet, li,d, length):
    d.setFillColorRGB(1, 0, 0)
    table=Table(
        li
        ,colWidths=[0.95 * cm, 6.01 * cm, 1.46 * cm,1.39 * cm],
        style=stylesheet['table_default'],
    )
    d.drawImage("D:/rafi banquet hall/realproject/static/images/title.jpg",20,522,280,50)
    table.wrapOn(d,1000,500)
    if length==1:
        table.drawOn(d,20,505)
    if length==2:
        table.drawOn(d,20,488)
    if length==3:
        table.drawOn(d,20,470)
    if length==4:
        table.drawOn(d,20,452)
    if length==5:
        table.drawOn(d,20,434)
    if length==6:
        table.drawOn(d,20,416)
    if length==7:
        table.drawOn(d,20,398)
    if length==8:
        table.drawOn(d,20,380)
    if length==9:
        table.drawOn(d,20,362)
    if length==10:
        table.drawOn(d,20,344)
    if length==11:
        table.drawOn(d,20,326)
    if length==12:
        table.drawOn(d,20,308)
    if length==13:
        table.drawOn(d,20,290)

def print_terms(d, list):
    if len(list) != 0:
        d.setFont("Times-BoldItalic", 11)
        d.setFillColorRGB(1, 0, 0)
        count = 0
        height = 240
        num=1
        while count < len(list):
            term = str(num) + ": "  +list[count]
            d.drawString(20,height,term)
            count+=1
            height-=15
            num+=1

def user_login(request):
    username = request.POST.get('username',default="")
    password = request.POST.get('password',default="")

    user = authenticate(username=username, password=password)

    if user:
        login(request,user)
        return HttpResponseRedirect("/index/")
    else:
        print("Invalid login details: {0}, {1}".format(username, password))
        return HttpResponse("Invalid login details supplied.")
    return render(request, 'realapp/login.html')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/index/')