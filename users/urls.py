from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('projects/', projects),
    path('gallery/', gallery_view),
    path('contact/', contact),
    path('chotepalle/', chotepalle_view),
    path('kothur/', kothur_view),
    path('yacharam/', yacharam_view),
    path('contact-list/', contact_list),
    path('contact-delete/<int:pk>/', delete_contact),
    path('super-admin-dashboard/', super_admin_dashboard_view),
    path('login/', superadmin_login, name='superadmin_login'),
    path('logout/', superadmin_logout_view, name='superadmin_logout'),
    path('upload-img/', upload_gallery_image, name='upload_page'),

    path('images-list/', image_list, name='image_list'),
    path('images-update/<int:pk>/', update_gallery_image, name='image_update'),
    path('images-delete/<int:pk>/', delete_gallery_image, name='image_delete'),



]