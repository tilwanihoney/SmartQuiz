from django.contrib import admin
from .models import Subject, Question, QuizResult

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'subject', 'correct_option')
    list_filter = ('subject',)

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'score', 'total_questions', 'created_at')
    list_filter = ('subject', 'created_at')
