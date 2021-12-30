from django.urls import path

from .views import *

urlpatterns = [
    path('home/', HomeListView.as_view(), name='home'),

    path('post-detail/<slug:slug_text>', post_detail, name='post_detail'),
    path('category/<slug:slug_text>', class_category, name='category_reverse'),
    path('dashboard/', dashboard, name='dashboard'),

    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerUser, name='register'),

    path('add-post/', addPost, name='add_post'),
    path('add-category/', addCategory, name='add_category'),
    path('add-tag/', addTag, name='add_tag'),
    path('delete-post/<slug:slug>', deletePost, name='delete_post'),
    path('update-post/<slug:slug>', updatePost, name='update_post'),
    
    path('categories/', categoryList, name='categories'),
    path('tags/', tagList, name='tags'),

    path('delete-category/<slug:slug>', deleteCategory, name='delete_category'),
    path('update-category/<slug:slug>', updateCategory, name='update_category'),
    
    path('delete-tag/<slug:slug>', deleteTag, name='delete_tag'),
    path('update-tag/<slug:slug>', updateTag, name='update_tag'),

    path('add-comment/<slug:slug>', addComment, name='add_comment'),
    path('search-post/', searchPost, name='search_post'),

    path('contact/', contact, name='contact'),
]
