from django import forms
from django.contrib import admin
from news.models import NewsPost


class NewsPostForm(forms.ModelForm):
    model = NewsPost
    fields = '__all__'


class NewsPostAdmin(admin.ModelAdmin):
    form = NewsPostForm
    list_display = ['title', 'source_divesite', 'is_cover_story', 'active']
    list_editable = ['is_cover_story', 'active']


admin.site.register(NewsPost, NewsPostAdmin)
