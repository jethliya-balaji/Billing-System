from django.conf import settings

def business_name_settings(request):
    return {
        'business_name': settings.BUSINESS_NAME,
    }
