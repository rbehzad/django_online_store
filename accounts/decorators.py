from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# how to use it?
# @unauthenticated_user


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator

# how to use it?
# @allowed_users(allowed_roles=[admin])


def seller_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'seller':
            return redirect('dashboard')

        if group == 'customer':
            return redirect('home')
    return wrapper_func
# how to use it?
# @seller_only


# if we use group then you we should wrote our reister like this?
# def registerUser(request):
#     page = 'register'
#     form = CustomUserCreationForm()
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             group = Group.objects.get(name='seller')
#             user.groups.add()

#             if user is not None:
#                 login(request, user)
#                 return redirect('dashboard')
        
#     context = {'form': form, 'page': page}
#     return render(request, 'post/login_register.html', context)
