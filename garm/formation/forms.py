from django import forms
from .models import Course, Chapter, SubChapter, Media

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'duration', 'cover_image', 'skills', 'certification_exam']

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['name', 'content', 'order', 'estimated_time']

class SubChapterForm(forms.ModelForm):
    class Meta:
        model = SubChapter
        fields = ['name', 'content', 'order']

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['name', 'media_type', 'file', 'description']
