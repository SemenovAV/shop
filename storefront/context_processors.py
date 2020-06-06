from .models import ParentCategory, SubCategory


def categories(request):

    context = {
        'categories': ParentCategory.objects.all(),
        'subcategories': SubCategory.objects.all()
        }
    return context

