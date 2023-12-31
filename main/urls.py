from django.urls import path

from .views import (index, other_page, profile, user_activate, rubric_bbs, bb_detail, BBLoginView, BBLogoutView, ProfileEditView,
                    PasswordEditView, RegisterView, RegisterDoneView, ProfileDeleteView, ResetPasswordView,
                    ResetPasswordDoneView, ResetPasswordConfirmView, ResetPasswordCompleteView)

app_name = 'main'

urlpatterns = [
    path('accounts/activate/<str:sign>/', user_activate, name='activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/password/edit/', PasswordEditView.as_view(), name='password_edit'),
    path('accounts/password/reset/', ResetPasswordView.as_view(), name='reset_password'),
    path('accounts/password/reset/done/', ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password/reset/complete/', ResetPasswordCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/profile/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
    path('accounts/profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('<int:rubric_pk>/<int:pk>/', bb_detail, name='bb_detail'),
    path('<int:pk>/', rubric_bbs, name='rubric_bbs'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]

