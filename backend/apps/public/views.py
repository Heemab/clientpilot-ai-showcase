from django.shortcuts import render


def home(request):
    return render(request, "public/home.html")


def demo(request):
    """
    Public page shown for premium features that are
    demonstrated during a live consultation.
    """
    return render(request, "public/demo.html")


def contact(request):
    """
    Consultation / live demo page.
    """
    return render(request, "public/contact.html")