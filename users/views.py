from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from .models import GalleryImage
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator





def home(request):
    return render(request, 'index.html')

def projects(request):
    return render(request, 'projects.html')

def gallery_view(request):
    choutuppal_images = GalleryImage.objects.filter(site='Choutuppal')
    yacharam_images = GalleryImage.objects.filter(site='Yacharam')
    kothur_images = GalleryImage.objects.filter(site='Kothur')
    other_images = GalleryImage.objects.exclude(site__in=['Choutuppal', 'Yacharam', 'Kothur'])

    context = {
        'choutuppal_images': choutuppal_images,
        'yacharam_images': yacharam_images,
        'kothur_images': kothur_images,
        'other_images': other_images,
    }
    return render(request, 'gallery.html', context)

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        requirements = request.POST.get('requirements')

        Contact.objects.create(
            name = name,
            email = email,
            subject = subject,
            requirements = requirements
        )
        messages.success(request, "Your message has been submitted successfully!")


    return render(request, 'contact.html')

def chotepalle_view(request):
    return render(request, 'choteppall.html')

def kothur_view(request):
    return render(request, 'kothur.html')

def yacharam_view(request):
    return render(request, 'yacharam.html')

def contact_list(request):
    contacts = Contact.objects.all().order_by('-id')  
    return render(request, 'contact_list.html', {'contacts': contacts})

def is_superadmin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superadmin)
@login_required
def super_admin_dashboard_view(request):
    return render(request, 'dashboard/super_admin_dashboard.html')

def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('/contact-list/')

def superadmin_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')  
        password = request.POST.get('password')

        try:
            user = User.objects.get(Q(username=identifier) | Q(email=identifier))
        except User.DoesNotExist:
            user = None

        if user:
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user is not None and auth_user.is_superuser:
                login(request, auth_user)
                return redirect('/super-admin-dashboard/')
            else:
                messages.error(request, "Invalid credentials or not authorized as Superadmin.")
        else:
            messages.error(request, "User not found.")

    return render(request, 'login.html')

def superadmin_logout_view(request):
    logout(request)
    return redirect('/') 


@require_http_methods(["GET", "POST"])
def upload_gallery_image(request):
    if request.method == 'POST':
        site = request.POST.get('site')
        title = request.POST.get('title', '')
        images = request.FILES.getlist('images')  

        for img in images:
            GalleryImage.objects.create(site=site, title=title, image=img)

        return redirect('/images-list/')  

    return render(request, 'dashboard/upload_images.html') 

def update_gallery_image(request, pk):
    image_obj = get_object_or_404(GalleryImage, pk=pk)

    if request.method == 'POST':
        image_obj.site = request.POST.get('site', image_obj.site)
        image_obj.title = request.POST.get('title', image_obj.title)

        if 'image' in request.FILES:
            image_obj.image = request.FILES['image']

        image_obj.save()
        return redirect('/images-list/') 

    return render(request, 'dashboard/update_image.html', {'image_obj': image_obj})

@require_POST
def delete_gallery_image(request, pk):
    image_obj = get_object_or_404(GalleryImage, pk=pk)
    image_obj.delete()
    return redirect('/images-list/') 

def image_list(request):
    image_list = GalleryImage.objects.all().order_by('-id') 
    paginator = Paginator(image_list, 5)  
    page_number = request.GET.get('page')
    images = paginator.get_page(page_number)

    return render(request, 'dashboard/upload_images_list.html', {'images': images})