from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, RedirectView

from .models import Course, Chapter, SubChapter, Media
from .forms import CourseForm, ChapterForm, SubChapterForm, MediaForm

# Course Detail View
class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "courses/course_detail.html"

course_detail_view = CourseDetailView.as_view()

# Course Create View
class CourseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_message = _("Course successfully created")

    def get_success_url(self):
        return reverse("courses:detail", kwargs={"slug": self.object.slug})

course_create_view = CourseCreateView.as_view()

# Course Update View
class CourseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_message = _("Course successfully updated")

    def get_success_url(self):
        return reverse("courses:detail", kwargs={"slug": self.object.slug})

course_update_view = CourseUpdateView.as_view()

# Course Delete View
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/course_confirm_delete.html"

    def get_success_url(self):
        return reverse("courses:list")

course_delete_view = CourseDeleteView.as_view()

# Chapter Detail View
class ChapterDetailView(LoginRequiredMixin, DetailView):
    model = Chapter
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "chapters/chapter_detail.html"

chapter_detail_view = ChapterDetailView.as_view()

# Chapter Create View
class ChapterCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = "chapters/chapter_form.html"
    success_message = _("Chapter successfully created")

    def get_success_url(self):
        return reverse("chapters:detail", kwargs={"slug": self.object.slug})

chapter_create_view = ChapterCreateView.as_view()

# Chapter Update View
class ChapterUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Chapter
    form_class = ChapterForm
    template_name = "chapters/chapter_form.html"
    success_message = _("Chapter successfully updated")

    def get_success_url(self):
        return reverse("chapters:detail", kwargs={"slug": self.object.slug})

chapter_update_view = ChapterUpdateView.as_view()

# Chapter Delete View
class ChapterDeleteView(LoginRequiredMixin, DeleteView):
    model = Chapter
    template_name = "chapters/chapter_confirm_delete.html"

    def get_success_url(self):
        return reverse("courses:detail", kwargs={"slug": self.object.course.slug})

chapter_delete_view = ChapterDeleteView.as_view()

# SubChapter Detail View
class SubChapterDetailView(LoginRequiredMixin, DetailView):
    model = SubChapter
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "subchapters/subchapter_detail.html"

subchapter_detail_view = SubChapterDetailView.as_view()

# SubChapter Create View
class SubChapterCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SubChapter
    form_class = SubChapterForm
    template_name = "subchapters/subchapter_form.html"
    success_message = _("SubChapter successfully created")

    def get_success_url(self):
        return reverse("subchapters:detail", kwargs={"slug": self.object.slug})

subchapter_create_view = SubChapterCreateView.as_view()

# SubChapter Update View
class SubChapterUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SubChapter
    form_class = SubChapterForm
    template_name = "subchapters/subchapter_form.html"
    success_message = _("SubChapter successfully updated")

    def get_success_url(self):
        return reverse("subchapters:detail", kwargs={"slug": self.object.slug})

subchapter_update_view = SubChapterUpdateView.as_view()

# SubChapter Delete View
class SubChapterDeleteView(LoginRequiredMixin, DeleteView):
    model = SubChapter
    template_name = "subchapters/subchapter_confirm_delete.html"

    def get_success_url(self):
        return reverse("chapters:detail", kwargs={"slug": self.object.chapter.slug})

subchapter_delete_view = SubChapterDeleteView.as_view()

# Media Create View
class MediaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Media
    form_class = MediaForm
    template_name = "media/media_form.html"
    success_message = _("Media successfully uploaded")

    def get_success_url(self):
        if self.object.chapter:
            return reverse("chapters:detail", kwargs={"slug": self.object.chapter.slug})
        return reverse("subchapters:detail", kwargs={"slug": self.object.subchapter.slug})

media_create_view = MediaCreateView.as_view()

# Media Update View
class MediaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Media
    form_class = MediaForm
    template_name = "media/media_form.html"
    success_message = _("Media successfully updated")

    def get_success_url(self):
        if self.object.chapter:
            return reverse("chapters:detail", kwargs={"slug": self.object.chapter.slug})
        return reverse("subchapters:detail", kwargs={"slug": self.object.subchapter.slug})

media_update_view = MediaUpdateView.as_view()

# Media Delete View
class MediaDeleteView(LoginRequiredMixin, DeleteView):
    model = Media
    template_name = "media/media_confirm_delete.html"

    def get_success_url(self):
        if self.object.chapter:
            return reverse("chapters:detail", kwargs={"slug": self.object.chapter.slug})
        return reverse("subchapters:detail", kwargs={"slug": self.object.subchapter.slug})

media_delete_view = MediaDeleteView.as_view()
