"""Defines URL patterns for learning logs app"""

from django.urls import path
from . import views


app_name = 'learning_logs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # topics
    path('topics/', views.topics, name='topics'),

    # Detail page for a single topic.
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # new topic
    path('create_topic/', views.create_topic, name='create_topic'),

    # new entry
    path('create_entry/<int:topic_id>/', views.create_entry, name='create_entry'),

    # edit entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]