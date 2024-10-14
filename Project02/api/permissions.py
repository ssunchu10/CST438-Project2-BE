from rest_framework.permissions import BasePermission
from projectApp.models import User  # Make sure to import your User model

class IsCustomAdmin(BasePermission):
    # Permissions for admin
    def has_permission(self, request, view):
        # Check if user is logged in through session
        if 'user_id' not in request.session:
            return False

        user_id = request.session['user_id']

        # Check the is_admin field in the user object to see if they are an admin
        try:
            user = User.objects.get(id=user_id)
            return user.is_admin
        except User.DoesNotExist:
            return False