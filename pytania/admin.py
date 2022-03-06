from django.contrib import admin
from .models import Question, TextToQuestion, ExamsInfo

# Register your models here.

admin.site.register(Question)
admin.site.register(ExamsInfo)
admin.site.register(TextToQuestion)