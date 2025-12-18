from django.shortcuts import render

def page_not_found(request, exception):
    # Обработка ошибки 404: страница не найдена
    return render(request, "pages/404.html", status=404)

def csrf_failure(request, reason=""):
    # Обработка ошибки 403: CSRF токен недействителен
    return render(request, "pages/403csrf.html", status=403)

def internal_server_error(request):
    # Обработка ошибки 500: внутренняя ошибка сервера
    return render(request, "pages/500.html", status=500)
