from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Content, Comment, Topic

admin.site.register(Content)
admin.site.register(Comment)
admin.site.register(Topic)
