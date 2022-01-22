from accounts.models import User

class PhoneNumberConfirmationPermission():
    def has_permission(self, request, view):
        user = User.objects.filter(email=request.data['email']).first()
        if user:
            if user.phone_number_confirmation:
                return True
            else:
                return False
        else:
            return False