from django.contrib import admin
from realapp.models import Event
from realapp.models import Salary
from realapp.models import Employee
from realapp.models import Attendance
from realapp.models import Arrangement
from realapp.models import Business_Details
from realapp.models import Booked_Slot
from realapp.models import Expense
from realapp.models import Menu
from realapp.models import Event_Menu
from realapp.models import Terms
from realapp.models import Event_Arrangement,UserProfile,Event_Special_Arrangement,Special_Arrangement
# Register your models here.
admin.site.register(Event)
admin.site.register(Salary)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Arrangement)
admin.site.register(Business_Details)
admin.site.register(Booked_Slot)
admin.site.register(Expense)
admin.site.register(Menu)
admin.site.register(Event_Menu)
admin.site.register(Terms)
admin.site.register(Event_Arrangement)
admin.site.register(Event_Special_Arrangement)
admin.site.register(Special_Arrangement)
admin.site.register(UserProfile)