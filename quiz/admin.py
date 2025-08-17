from django.contrib import admin
from .models import Quiz, Question, Result

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of empty forms to display

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_limit', 'question_count')
    inlines = [QuestionInline]
    
    def question_count(self, obj):
        return obj.question_set.count()
    question_count.short_description = 'Questions'

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'correct_answer')
    list_filter = ('quiz',)
    search_fields = ('text', 'correct_answer')

class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'time_taken', 'percentage')
    list_filter = ('quiz', 'user')
    search_fields = ('user__username', 'quiz__title')
    
    def percentage(self, obj):
        return f"{(obj.score / 5) * 100:.1f}%"
    percentage.short_description = 'Percentage'

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result, ResultAdmin)