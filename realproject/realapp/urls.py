from django.conf.urls import url
from realapp import views


app_name='realapp'

urlpatterns=[
    url(r'^gallery/$',views.gallery,name='gallery'),
    url(r'^employee/$',views.employee,name='employee'),
    url(r'^contact/$',views.contact,name='contact'),
    url(r'^about/$',views.about,name='about'),
    url(r'^index/$',views.index,name='index'),
    url(r'^salary/$',views.salary,name='salary'),
url(r'^salary2/$',views.salary2,name='salary2'),
url(r'^filter_salary2/$',views.filter_salary2,name='filter_salary2'),
url(r'^get_table_data/$',views.get_table_data,name='get_table_data'),
url(r'^salary/sform/$',views.sform,name='sform'),
url(r'^ereport/$',views.ereport,name='ereport'),
url(r'^ereport/Gen_Expense/$',views.Gen_Expense, name='Gen_Expense'),
url(r'^ereport/filter_event_reports/$',views.filter_event_reports,name='filter_event_reports'),
url(r'^userprofile/$',views.userprofile,name='userprofile'),
    url(r'^add_daily_expense/$', views.add_daily_expense, name='add_daily_expense'),
    url(r'^add_salary/$', views.add_salary, name='add_salary'),
    url(r'^filter/$', views.filter, name='filter'),
    url(r'^Events/$',views.Events,name='Events'),
    url(r'^Info/$',views.Info,name='Info'),
    url(r'^get_events/$', views.get_events, name='get_events'),
url(r'^add_event/$', views.add_event, name='add_event'),
url(r'^add_events/Info/(?P<event_id>\w+)/$', views.Info, name='Info'),
    url(r'^Events/Info/(?P<event_id>\w+)/$', views.Info, name='Info'),
url(r'^get_events/Info/(?P<event_id>\w+)/$', views.Info, name='Info'),
url(r'^update_form/', views.update_form, name='update_form'),
# url(r'^update_form/$', views.Info, name='Info'),
url(r'^Events/Gen_Expense/$', views.Gen_Expense, name='Gen_Expense'),
url(r'^Events/Gen_Expense/Gen_Expense/$', views.Gen_Expense, name='Gen_Expense'),
url(r'^Events/Gen_Expense/genform/$', views.genform, name='genform'),
# url(r'^Events/Gen_Expense/$', views.Gen_Expense, name='Gen_Expense'),
# url(r'^Events/Gen_Expense/Gen_Expense/$', views.Gen_Expense, name='Gen_Expense'),
url(r'^Gen_Expense/$', views.Gen_Expense_gen_expense, name='Gen_Expense_gen_expense'),
url(r'^filter_gen_expense/$', views.filter_gen_expense, name='filter_gen_expense'),
url(r'^login/$', views.login1, name='login1'),

]