from django.contrib import admin
from .models import *
@admin.register(Brands)
class ScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(Cars)
class SubjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Clips)
class SubjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Reviews)
class SubjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Feedback)
class SubjectAdmin(admin.ModelAdmin):
    pass