from django.urls import path
from .views import (
    course_detail_view, course_create_view, course_update_view, course_delete_view,
    chapter_detail_view, chapter_create_view, chapter_update_view, chapter_delete_view,
    subchapter_detail_view, subchapter_create_view, subchapter_update_view, subchapter_delete_view,
    media_create_view, media_update_view, media_delete_view
)

app_name = 'courses'

urlpatterns = [
    path('course/<slug:slug>/', course_detail_view, name='detail'),
    path('course/create/', course_create_view, name='create'),
    path('course/<slug:slug>/edit/', course_update_view, name='edit'),
    path('course/<slug:slug>/delete/', course_delete_view, name='delete'),

    path('chapter/<slug:slug>/', chapter_detail_view, name='chapter_detail'),
    path('chapter/create/', chapter_create_view, name='chapter_create'),
    path('chapter/<slug:slug>/edit/', chapter_update_view, name='chapter_edit'),
    path('chapter/<slug:slug>/delete/', chapter_delete_view, name='chapter_delete'),

    path('subchapter/<slug:slug>/', subchapter_detail_view, name='subchapter_detail'),
    path('subchapter/create/', subchapter_create_view, name='subchapter_create'),
    path('subchapter/<slug:slug>/edit/', subchapter_update_view, name='subchapter_edit'),
    path('subchapter/<slug:slug>/delete/', subchapter_delete_view, name='subchapter_delete'),

    path('media/create/', media_create_view, name='media_create'),
    path('media/<int:pk>/edit/', media_update_view, name='media_edit'),
    path('media/<int:pk>/delete/', media_delete_view, name='media_delete'),
]
