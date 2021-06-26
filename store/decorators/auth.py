from django.shortcuts import redirect

def unauthenticated_user(get_response):
    # One-time configuration and initialization.
    def middleware(request):
        # print("middleware")
        # print(request.path)
        # print(request.META['PATH_INFO'])

        # re_path = request.META['PATH_INFO']
        re_path = request.path
        if not request.session.get('customer_id'):
            return redirect(f'/login?redirect={re_path}')

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    return middleware


def stop_login_signup(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# to get to admin panel
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == "customer":
            return redirect('homepage')
        if group == "admin":
            return view_func(request, *args, **kwargs)
    return wrapper_func
