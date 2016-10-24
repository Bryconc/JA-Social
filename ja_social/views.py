from django.views.generic import CreateView, DetailView, UpdateView, ListView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.db.models import Sum

from .forms import UserForm
from .models import VolunteerRecord, UserProfile, PhotoRecord



class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class UserRegisterView(CreateView):
    template_name = "user_register.html"
    model = User
    success_url = reverse_lazy('ja_social:home_page')
    form_class = UserForm


class UserProfileView(DetailView):
    model = UserProfile
    template_name = "user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['hours'] = VolunteerRecord.objects.all()
        context['photos'] = PhotoRecord.objects.filter(user_profile=self.request.user.profile)
        context['hours_total'] = VolunteerRecord.objects.filter(user_profile=self.request.user.profile, verified= True).aggregate(Sum('hours'))
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = "user_profile_edit.html"
    model = UserProfile
    fields = ['company']

    def get_context_data(self, **kwargs):
        context = super(ProfileEditView, self).get_context_data(**kwargs)
        context['hours'] = VolunteerRecord.objects.all()
        context['photos'] = PhotoRecord.objects.filter(user_profile=self.request.user.profile);
        context['hours_total'] = VolunteerRecord.objects.filter(user_profile=self.request.user.profile, verified= True).aggregate(Sum('hours'))
        return context


class VolunteerRecordLogView(CreateView):
    template_name = "volunteer_log.html"
    model = VolunteerRecord
    fields = ['county', 'school_name', 'JA_program', 'hours']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_profile = self.request.user.profile
        obj.save()
        return HttpResponseRedirect(reverse_lazy('ja_social:user_view', args=(self.request.user.pk,)))


class PhotoUploadView(CreateView):
    template_name = "photo_upload.html"
    model = PhotoRecord
    fields = ['photo']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_profile = self.request.user.profile
        obj.save()
        return HttpResponseRedirect(reverse_lazy('ja_social:user_view', args=(self.request.user.pk,)))


class PhotoGalleryView(ListView):
    template_name = "photo_gallery.html"
    model = PhotoRecord


class HomePageTemplate(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super(HomePageTemplate, self).get_context_data(**kwargs)
        context['photos'] = PhotoRecord.objects.all()
        return context


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('ja_social:home_page'))


def profile_redirect(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('ja_social:user_view', args=(request.user.pk,)))
    return HttpResponseRedirect(reverse('ja_social:home_page'))
