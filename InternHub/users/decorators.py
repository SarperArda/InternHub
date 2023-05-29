from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs, ):
            role = None
            if request.user.role is not None:
                role = request.user.role

            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page.')

        return wrapper_func

    return decorator


def decorate_get_all(model_cls):
    def get_all(*args, **kwargs):
        return model_cls.objects.all()

    return get_all
