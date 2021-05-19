from rest_framework.permissions import BasePermission,SAFE_METHODS

class DossierPostMethod(BasePermission):

    def has_permission(self,request,view):
        if request.method != 'POST':
            return True