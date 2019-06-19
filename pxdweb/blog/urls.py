from django.urls import path
from. import views
urlpatterns = [
    path('<int:blog_pk>',views.blog_detail, name='blog_detail'),
    path('', views.blog_list, name='blog_list'),
    path('type/<int:blog_with_type>',views.blog_with_type,name = 'blog_with_type'),
    path('date/<int:year>/<int:month>',views.blog_with_date, name = 'blog_with_date'),

]