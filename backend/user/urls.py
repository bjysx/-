from django.urls import path
from .views import (
    LoginView, UserInfoView, LogoutView, ChangePasswordView, AvatarUploadView, UserListView, HRUserListView,
    EmployeeRelationView, EmployeeRosterView, ResignedEmployeeView, EmployeeOtherView,
    RecruitmentRequirementView, RecruitmentProgressView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('avatar/', AvatarUploadView.as_view(), name='avatar_upload'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('hr-users/', HRUserListView.as_view(), name='hr_user_list'),
    # 员工关系管理 - 花名册
    path('employee-relations/', EmployeeRelationView.as_view(), name='employee_relation_list'),
    path('employee-relations/<int:pk>/', EmployeeRelationView.as_view(), name='employee_relation_detail'),
    # 员工关系管理 - 子菜单路由
    path('employee-roster/', EmployeeRosterView.as_view(), name='employee_roster'),
    path('resigned-employees/', ResignedEmployeeView.as_view(), name='resigned_employees'),
    path('employee-other/', EmployeeOtherView.as_view(), name='employee_other'),
    # 招聘管理 - 需求汇总
    path('recruitment-requirements/', RecruitmentRequirementView.as_view(), name='recruitment_requirements'),
    path('recruitment-requirements/<int:pk>/', RecruitmentRequirementView.as_view(), name='recruitment_requirement_detail'),
    # 招聘管理 - 招聘进度
    path('recruitment-progress/', RecruitmentProgressView.as_view(), name='recruitment_progress'),
    path('recruitment-progress/<int:pk>/', RecruitmentProgressView.as_view(), name='recruitment_progress_detail'),
]
