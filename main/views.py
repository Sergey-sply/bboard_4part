from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy


from .models import AdvUser, SubRubric, Bb
from .forms import ProfileEditForm, RegisterForm, SearchForm
from .utilities import signer

# Create your views here.


def index(request):
    """Display of the first 10 bbs."""
    bbs = Bb.objects.filter(is_active=True).select_related('rubric')[:10]   # get related bbs
    context = {'bbs': bbs}
    return render(request, 'main/index.html', context)


def other_page(request, page):

    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404

    return HttpResponse(template.render(request=request))


@login_required
def profile(request):
    return render(request, 'main/profile.html')


# activate profile via mail
def user_activate(request, sign):

    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/activation_failed.html')

    user = get_object_or_404(AdvUser, username=username)

    if user.is_activated:
        template = 'main/activation_done_earlier.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()

    return render(request, template)


class BBLoginView(LoginView):
    template_name = 'main/login.html'


class BBLogoutView(LogoutView):
    pass


# class for register
class RegisterView(CreateView):
    model = AdvUser
    template_name = 'main/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('main:register_done')


# class for success reg
class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


# class for edit profile
class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/profile_edit.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# class for delete user
class ProfileDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/profile_delete.html'
    success_url = reverse_lazy('main:index')
    success_message = 'Пользователь удален'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# for edit password
class PasswordEditView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_edit.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль успешно изменен'

# for reset password
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'main/password_reset.html'
    email_template_name = 'main/password_reset_email.html'
    success_url = reverse_lazy('main:password_reset_done')


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'main/password_reset_complete.html'


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'
    success_url = reverse_lazy('main:password_reset_complete')


def rubric_bbs(request, pk):
    """Form for searching bbs by keyword."""
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})

    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET('page')
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'bbs': page.object_list, 'form': form}

    return render(request, 'main/rubric_bbs.html', context)


def bb_detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'main/bb_detail.html', context)






