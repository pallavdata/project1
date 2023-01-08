from django.contrib import admin
from .models import Apply,Job,Login_Accounts,Mcq,role,skill,InterviewTemp
# Register your models here.
admin.site.register(Login_Accounts)
admin.site.register(Apply)
admin.site.register(Job)
admin.site.register(Mcq)
admin.site.register(role)
admin.site.register(skill)
admin.site.register(InterviewTemp)
# admin.site.register(Interview)
# admin.site.register(Assignment)