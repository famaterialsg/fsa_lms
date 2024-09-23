from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'question' 
urlpatterns = [
    path('questions/', views.question_list, name='question_list'),
    path('questions/<int:pk>/', views.question_detail, name='question_detail'),
    path('questions/create/', views.question_add, name='question_add'),
    path('questions/edit/<int:pk>/', views.question_edit, name='question_edit'),
    path('questions/<int:question_pk>/answers/add/', views.answer_add, name='answer_add'),
    path('questions/delete/<int:pk>/', views.question_delete, name='question_delete'),
    path('subject/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),

]
