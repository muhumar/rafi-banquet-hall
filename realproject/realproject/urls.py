"""realproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from realapp import views

urlpatterns = [
    url(r'^$',views.index,name="index"),
url(r'^index/$',views.index,name="index"),
    url(r'^admin/', admin.site.urls),
    url(r'^Expenses/(?P<event_id>\w+)/$', views.Expenses_info, name='Expenses_info'),
url(r'^sform/(?P<salary_id>\w+)/$', views.sform, name='sform'),
    url(r'^add_event_expense/(?P<event_id>\w+)/$', views.add_event_expense, name='add_event_expense'),
    url(r'^eform/(?P<expense_id>\w+)/(?P<expense_event_id>\w+)/$', views.eform, name='eform'),
url(r'^genform/(?P<expense_id>\w+)/$', views.gen_form, name='gen_form'),
    url(r'^update_event_expense/(?P<expense_event_id>\w+)/(?P<expense_id>\w+)/$', views.update_event_expense, name='update_event_expense'),
url(r'^update_daily_expense/(?P<expense_id>\w+)/$', views.update_daily_expense, name='update_daily_expense'),
url(r'^update_salary/(?P<salary_id>\w+)/$', views.update_salary, name='update_salary'),
url(r'^user_login/$', views.user_login, name='user_login'),
url(r'^restricted/', views.restricted, name='restricted'),
url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^realapp/',include('realapp.urls')),
]
