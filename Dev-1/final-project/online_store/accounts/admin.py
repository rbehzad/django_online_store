from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	list_display = ('fullname', 'username', 'email', 'is_admin', 'is_seller')
	list_filter = ('is_admin', 'is_seller')
	fieldsets = (
		('Main', {'fields':('fullname', 'username', 'email', 'phone_number', 'password')}),
		('Personal info', {'fields':('is_active', 'is_seller')}),
		('Permissions', {'fields':('is_admin',)})
	)
	add_fieldsets = (
		(None, {
			'fields':('fullname', 'username', 'email', 'phone_number', 'password1', 'password2', 'is_seller')
		}),
	)
	search_fields = ('email', 'username')
	ordering = ('email', 'username')
	filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)













# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin


# class CustomUserAdmin(UserAdmin):
#     list_display = (
#         'username', 'email', 'first_name', 'last_name', 'is_staff',
#         'is_seller'
#         )

#     fieldsets = (
#         (None, {
#             'fields': ('username', 'password')
#         }),
#         ('Personal info', {
#             'fields': ('full_name', 'email')
#         }),
#         ('Permissions', {
#             'fields': (
#                 'is_active',
#                 'groups', 'user_permissions'
#                 )
#         }),
#         ('Important dates', {
#             'fields': ('last_login')
#         }),
#         ('Additional info', {
#             'fields': ('is_seller',)
#         })
#     )

#     add_fieldsets = (
#         (None, {
#             'fields': ('username', 'password1', 'password2')
#         }),
#         ('Personal info', {
#             'fields': ('first_name', 'last_name', 'email')
#         }),
#         ('Permissions', {
#             'fields': (
#                 'is_active',
#                 'groups', 'user_permissions'
#                 )
#         }),
#         ('Important dates', {
#             'fields': ('last_login')
#         }),
#         ('Additional info', {
#             'fields': ('is_student',)
#         })
#     )

# admin.site.register(User, CustomUserAdmin)