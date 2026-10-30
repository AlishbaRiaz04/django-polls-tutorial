from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Question Information", {"fields": ["question_text"]}),
        ("Publication Details", {"fields": ["pub_date"]}),
    ]
    list_display = (
        "question_text",
        "pub_date",
        "was_published_recently",
    )
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

admin.site.site_url = "/polls/"
admin.site.site_header = "Polls Administration"
admin.site.site_title = "Polls Admin"
admin.site.index_title = "Welcome to the Polls Administration"
