from .models import ParentCategory


def categories(request):
    context = {
        'categories': ParentCategory.objects.all(),
        }
    return context

