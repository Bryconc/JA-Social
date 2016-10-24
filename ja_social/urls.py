from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.views import login

from .views import UserRegisterView, VolunteerRecordLogView, logout_view, UserProfileView, profile_redirect, ProfileEditView, PhotoUploadView, PhotoGalleryView, HomePageTemplate

urlpatterns = [
    url(r'^$', HomePageTemplate.as_view(), name="home_page"),

    url(r'^account/register$', UserRegisterView.as_view(), name="account_registration"),
    url(r'^account/success$', TemplateView.as_view(template_name="success.html"), name="account success page"),
    url(r'^account/profile/(?P<pk>[0-9]+)', UserProfileView.as_view(), name='user_view'),
    url(r'^account/update/(?P<pk>[0-9]+)', ProfileEditView.as_view(), name='user_update'),
    url(r'^account/login$', login, {'template_name': 'login.html'}, name='login_page'),
    url(r'^account/logout$', logout_view, name='logout_page'),
    url(r'^account/photo/upload$', PhotoUploadView.as_view(), name='photo_upload'),
    url(r'^account/photo/gallery$', PhotoGalleryView.as_view(), name='photo_gallery'),

    url(r'^profile/', profile_redirect, name='profile_redirect'),

    url(r'^volunteer/success$', TemplateView.as_view(template_name="success.html"), name="volunteer success page"),
    url(r'^volunteer/log$', VolunteerRecordLogView.as_view(), name="volunteer_record_log"),

    url(r'^profile_pics/(?P<pk>[0-9]+)', profile_redirect, name='profile_redirect'),

]
