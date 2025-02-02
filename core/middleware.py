from django.shortcuts import redirect

class AuthRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si el usuario está autenticado y está intentando acceder a login o registro
        if request.user.is_authenticated:
            if request.path in ['/login/', '/register/']:  # Si está en login o registro
                if request.user.tipo == 'usuario':
                    return redirect('dashboard_usuario')  # Redirige a su dashboard
                elif request.user.tipo == 'psicologo':
                    return redirect('dashboard_psicologo')  # Redirige al dashboard del psicólogo
        # Si el usuario no está autenticado, continúa con la solicitud
        return self.get_response(request)
