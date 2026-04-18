from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64
import uuid
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginView(TokenObtainPairView):
    """
    Login and get JWT token
    """
    serializer_class = CustomTokenObtainPairSerializer

class UserInfoView(APIView):
    """
    Get current user information
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LogoutView(APIView):
    """
    Logout (usually handled by client clearing the token)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({"message": "Successfully logged out"})

class ChangePasswordView(APIView):
    """
    Change user password
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        
        if not user.check_password(old_password):
            return Response({"error": "原密码错误"}, status=400)
            
        user.set_password(new_password)
        user.save()
        return Response({"message": "密码修改成功"})

class AvatarUploadView(APIView):
    """
    Upload user avatar
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        file = request.FILES.get('file')
        
        if not file:
            return Response({"success": False, "message": "请选择文件"}, status=400)
        
        # 生成唯一文件名
        ext = file.name.split('.')[-1]
        filename = f"avatars/{uuid.uuid4()}.{ext}"
        
        # 保存文件
        file_path = default_storage.save(filename, ContentFile(file.read()))
        
        # 构建文件URL
        avatar_url = f"/media/{file_path}"
        
        # 更新用户头像
        user.avatar = avatar_url
        user.save()
        
        return Response({"success": True, "data": {"avatar": avatar_url}})

class UserListView(APIView):
    """
    Get all users information
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 支持按部门筛选
        department = request.query_params.get('department', '')
        users = User.objects.all()
        if department:
            users = users.filter(department=department)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class HRUserListView(APIView):
    """
    获取人事部用户列表（用于指派HR）
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 获取人事部用户
        hr_users = User.objects.filter(department='人力资源部')
        data = []
        for user in hr_users:
            data.append({
                'id': user.id,
                'username': user.username,
                'nickname': user.nickname,
                'department': user.department,
                'position': user.position
            })
        return Response(data)


from .models import EmployeeRelation
from django.db.models import Q


class EmployeeRelationView(APIView):
    """
    员工关系管理
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取员工关系列表"""
        queryset = EmployeeRelation.objects.all()
        
        # 筛选条件
        department = request.query_params.get('department', '')
        position = request.query_params.get('position', '')
        employee_status = request.query_params.get('employee_status', '')
        keyword = request.query_params.get('keyword', '')
        
        if department:
            queryset = queryset.filter(department=department)
        if position:
            queryset = queryset.filter(position=position)
        if employee_status:
            queryset = queryset.filter(employee_status=employee_status)
        if keyword:
            queryset = queryset.filter(
                Q(employee_name__icontains=keyword) |
                Q(phone__icontains=keyword)
            )
        
        # 转正时间范围筛选
        regularization_date_start = request.query_params.get('regularization_date_start', '')
        regularization_date_end = request.query_params.get('regularization_date_end', '')
        if regularization_date_start and regularization_date_end:
            queryset = queryset.filter(
                regularization_date__gte=regularization_date_start,
                regularization_date__lte=regularization_date_end
            )
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        total = queryset.count()
        
        start = (page - 1) * page_size
        end = start + page_size
        results = queryset[start:end]
        
        data = []
        for item in results:
            data.append({
                'id': item.id,
                'department': item.department,
                'position': item.position,
                'employee_status': item.employee_status,
                'job_level': item.job_level,
                'employee_name': item.employee_name,
                'phone': item.phone,
                'household_registration': item.household_registration,
                'birth_date': item.birth_date.strftime('%Y-%m-%d') if item.birth_date else None,
                'gender': item.gender,
                'age': item.age,
                'education': item.education,
                'entry_date': item.entry_date.strftime('%Y-%m-%d') if item.entry_date else None,
                'regularization_date': item.regularization_date.strftime('%Y-%m-%d') if item.regularization_date else None,
                'work_years': item.work_years,
                'contract_start_date': item.contract_start_date.strftime('%Y-%m-%d') if item.contract_start_date else None,
                'contract_end_date': item.contract_end_date.strftime('%Y-%m-%d') if item.contract_end_date else None,
                'salary': float(item.salary) if item.salary else 0,
                'base_salary': float(item.base_salary) if item.base_salary else 0,
                'performance_salary': float(item.performance_salary) if item.performance_salary else 0,
                'commission': float(item.commission) if item.commission else 0,
                'allowance': float(item.allowance) if item.allowance else 0,
                # 详细信息字段
                'birthplace': item.birthplace,
                'id_card_number': item.id_card_number,
                'home_address': item.home_address,
                'graduation_school': item.graduation_school,
                'major': item.major,
                'marital_status': item.marital_status,
                'family_member_name': item.family_member_name,
                'family_member_phone': item.family_member_phone,
                'emergency_contact_name': item.emergency_contact_name,
                'emergency_contact_phone': item.emergency_contact_phone,
                'bank_name': item.bank_name,
                'bank_branch': item.bank_branch,
                'bank_account': item.bank_account,
                'contract_number': item.contract_number,
                'social_security_base': float(item.social_security_base) if item.social_security_base else 0,
                'position_salary': float(item.position_salary) if item.position_salary else 0,
                'social_security_status': item.social_security_status,
                'social_security_date': item.social_security_date.strftime('%Y-%m-%d') if item.social_security_date else None,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': item.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return Response({
            'results': data,
            'total': total,
            'page': page,
            'page_size': page_size
        })

    def post(self, request):
        """创建员工关系记录"""
        data = request.data
        
        employee = EmployeeRelation.objects.create(
            department=data.get('department', ''),
            position=data.get('position', ''),
            employee_status=data.get('employee_status', '正式'),
            job_level=data.get('job_level', ''),
            employee_name=data.get('employee_name', ''),
            phone=data.get('phone', ''),
            household_registration=data.get('household_registration', ''),
            birth_date=data.get('birth_date'),
            gender=data.get('gender', '男'),
            age=data.get('age', 0),
            education=data.get('education', ''),
            entry_date=data.get('entry_date'),
            regularization_date=data.get('regularization_date'),
            work_years=data.get('work_years', 0),
            contract_start_date=data.get('contract_start_date'),
            contract_end_date=data.get('contract_end_date'),
            salary=data.get('salary', 0),
            base_salary=data.get('base_salary', 0),
            performance_salary=data.get('performance_salary', 0),
            commission=data.get('commission', 0),
            allowance=data.get('allowance', 0),
            # 详细信息字段
            birthplace=data.get('birthplace', ''),
            id_card_number=data.get('id_card_number', ''),
            home_address=data.get('home_address', ''),
            graduation_school=data.get('graduation_school', ''),
            major=data.get('major', ''),
            marital_status=data.get('marital_status', ''),
            family_member_name=data.get('family_member_name', ''),
            family_member_phone=data.get('family_member_phone', ''),
            emergency_contact_name=data.get('emergency_contact_name', ''),
            emergency_contact_phone=data.get('emergency_contact_phone', ''),
            bank_name=data.get('bank_name', ''),
            bank_branch=data.get('bank_branch', ''),
            bank_account=data.get('bank_account', ''),
            contract_number=data.get('contract_number', ''),
            social_security_base=data.get('social_security_base', 0),
            position_salary=data.get('position_salary', 0),
            # 社保信息
            social_security_status=data.get('social_security_status', ''),
            social_security_date=data.get('social_security_date'),
        )
        
        return Response({'id': employee.id, 'message': '创建成功'}, status=201)

    def put(self, request, pk):
        """更新员工关系记录"""
        try:
            employee = EmployeeRelation.objects.get(pk=pk)
        except EmployeeRelation.DoesNotExist:
            return Response({'message': '记录不存在'}, status=404)
        
        data = request.data
        for key, value in data.items():
            if hasattr(employee, key):
                setattr(employee, key, value)
        employee.save()
        
        return Response({'message': '更新成功'})

    def delete(self, request, pk):
        """删除员工关系记录"""
        try:
            employee = EmployeeRelation.objects.get(pk=pk)
            employee.delete()
            return Response({'message': '删除成功'})
        except EmployeeRelation.DoesNotExist:
            return Response({'message': '记录不存在'}, status=404)


class EmployeeRosterView(APIView):
    """
    花名册 - 在职员工列表
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取在职员工花名册列表"""
        queryset = EmployeeRelation.objects.filter(employee_status='正式')
        
        # 筛选条件
        department = request.query_params.get('department', '')
        position = request.query_params.get('position', '')
        keyword = request.query_params.get('keyword', '')
        
        if department:
            queryset = queryset.filter(department=department)
        if position:
            queryset = queryset.filter(position=position)
        if keyword:
            queryset = queryset.filter(
                Q(employee_name__icontains=keyword) |
                Q(phone__icontains=keyword)
            )
        
        # 转正时间范围筛选
        regularization_date_start = request.query_params.get('regularization_date_start', '')
        regularization_date_end = request.query_params.get('regularization_date_end', '')
        if regularization_date_start and regularization_date_end:
            queryset = queryset.filter(
                regularization_date__gte=regularization_date_start,
                regularization_date__lte=regularization_date_end
            )
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        total = queryset.count()
        
        start = (page - 1) * page_size
        end = start + page_size
        results = queryset[start:end]
        
        data = []
        for item in results:
            data.append({
                'id': item.id,
                'department': item.department,
                'position': item.position,
                'employee_status': item.employee_status,
                'job_level': item.job_level,
                'employee_name': item.employee_name,
                'phone': item.phone,
                'household_registration': item.household_registration,
                'birth_date': item.birth_date.strftime('%Y-%m-%d') if item.birth_date else None,
                'gender': item.gender,
                'age': item.age,
                'education': item.education,
                'entry_date': item.entry_date.strftime('%Y-%m-%d') if item.entry_date else None,
                'regularization_date': item.regularization_date.strftime('%Y-%m-%d') if item.regularization_date else None,
                'work_years': item.work_years,
                'contract_start_date': item.contract_start_date.strftime('%Y-%m-%d') if item.contract_start_date else None,
                'contract_end_date': item.contract_end_date.strftime('%Y-%m-%d') if item.contract_end_date else None,
                'salary': float(item.salary) if item.salary else 0,
                'base_salary': float(item.base_salary) if item.base_salary else 0,
                'performance_salary': float(item.performance_salary) if item.performance_salary else 0,
                'commission': float(item.commission) if item.commission else 0,
                'allowance': float(item.allowance) if item.allowance else 0,
                # 详细信息字段
                'birthplace': item.birthplace,
                'id_card_number': item.id_card_number,
                'home_address': item.home_address,
                'graduation_school': item.graduation_school,
                'major': item.major,
                'marital_status': item.marital_status,
                'family_member_name': item.family_member_name,
                'family_member_phone': item.family_member_phone,
                'emergency_contact_name': item.emergency_contact_name,
                'emergency_contact_phone': item.emergency_contact_phone,
                'bank_name': item.bank_name,
                'bank_branch': item.bank_branch,
                'bank_account': item.bank_account,
                'contract_number': item.contract_number,
                'social_security_base': float(item.social_security_base) if item.social_security_base else 0,
                'position_salary': float(item.position_salary) if item.position_salary else 0,
                'social_security_status': item.social_security_status,
                'social_security_date': item.social_security_date.strftime('%Y-%m-%d') if item.social_security_date else None,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': item.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return Response({
            'results': data,
            'total': total,
            'page': page,
            'page_size': page_size
        })


class ResignedEmployeeView(APIView):
    """
    离职员工
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取离职员工列表"""
        queryset = EmployeeRelation.objects.filter(employee_status='离职')
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        total = queryset.count()
        
        start = (page - 1) * page_size
        end = start + page_size
        results = queryset[start:end]
        
        data = []
        for item in results:
            data.append({
                'id': item.id,
                'department': item.department,
                'position': item.position,
                'employee_status': item.employee_status,
                'employee_name': item.employee_name,
                'phone': item.phone,
            })
        
        return Response({
            'results': data,
            'total': total,
            'page': page,
            'page_size': page_size
        })


class EmployeeOtherView(APIView):
    """
    其他员工
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取其他员工列表"""
        queryset = EmployeeRelation.objects.exclude(employee_status__in=['正式', '离职'])
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        total = queryset.count()
        
        start = (page - 1) * page_size
        end = start + page_size
        results = queryset[start:end]
        
        data = []
        for item in results:
            data.append({
                'id': item.id,
                'department': item.department,
                'position': item.position,
                'employee_status': item.employee_status,
                'employee_name': item.employee_name,
                'phone': item.phone,
            })
        
        return Response({
            'results': data,
            'total': total,
            'page': page,
            'page_size': page_size
        })


# 招聘管理相关导入
from .models import RecruitmentRequirement, RecruitmentProgress


class RecruitmentRequirementView(APIView):
    """
    招聘管理 - 需求汇总
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取招聘需求列表"""
        queryset = RecruitmentRequirement.objects.all()
        
        # 筛选条件
        department = request.query_params.get('department', '')
        position = request.query_params.get('position', '')
        status = request.query_params.get('status', '')
        hr = request.query_params.get('hr', '')
        urgency = request.query_params.get('urgency', '')
        
        if department:
            queryset = queryset.filter(department=department)
        if position:
            queryset = queryset.filter(position__icontains=position)
        if status:
            queryset = queryset.filter(recruitment_status=status)
        if hr:
            queryset = queryset.filter(responsible_hr=hr)
        if urgency:
            queryset = queryset.filter(urgency_level=urgency)
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        total = queryset.count()
        
        start = (page - 1) * page_size
        end = start + page_size
        results = queryset[start:end]
        
        data = []
        for item in results:
            data.append({
                'id': item.id,
                'department': item.department,
                'requester': item.requester,
                'position': item.position,
                'application_date': item.application_date.strftime('%Y-%m-%d') if item.application_date else None,
                'urgency_level': item.urgency_level,
                'required_count': item.required_count,
                'hired_count': item.hired_count,
                'remaining_count': item.remaining_count,
                'personnel_type': item.personnel_type,
                'recruitment_status': item.recruitment_status,
                'responsible_hr': item.responsible_hr,
                'work_location': item.work_location,
                'salary_range': item.salary_range,
                'job_requirements': item.job_requirements,
                'remarks': item.remarks,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': item.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return Response({
            'results': data,
            'total': total,
            'page': page,
            'page_size': page_size
        })

    def post(self, request):
        """创建招聘需求"""
        data = request.data
        
        requirement = RecruitmentRequirement.objects.create(
            department=data.get('department', ''),
            requester=data.get('requester', ''),
            position=data.get('position', ''),
            application_date=data.get('application_date'),
            urgency_level=data.get('urgency_level', '普通'),
            required_count=data.get('required_count', 1),
            hired_count=data.get('hired_count', 0),
            remaining_count=data.get('remaining_count', 1),
            personnel_type=data.get('personnel_type', ''),
            recruitment_status=data.get('recruitment_status', '招聘中'),
            responsible_hr=data.get('responsible_hr', ''),
            work_location=data.get('work_location', ''),
            salary_range=data.get('salary_range', ''),
            job_requirements=data.get('job_requirements', ''),
            remarks=data.get('remarks', ''),
        )
        
        return Response({'id': requirement.id, 'message': '创建成功'}, status=201)

    def put(self, request, pk):
        """更新招聘需求"""
        try:
            requirement = RecruitmentRequirement.objects.get(pk=pk)
        except RecruitmentRequirement.DoesNotExist:
            return Response({'message': '记录不存在'}, status=404)
        
        data = request.data
        for key, value in data.items():
            if hasattr(requirement, key):
                setattr(requirement, key, value)
        
        # 重新计算剩余人数
        requirement.remaining_count = requirement.required_count - requirement.hired_count
        requirement.save()
        
        return Response({'message': '更新成功'})

    def delete(self, request, pk):
        """删除招聘需求"""
        try:
            requirement = RecruitmentRequirement.objects.get(pk=pk)
            requirement.delete()
            return Response({'message': '删除成功'})
        except RecruitmentRequirement.DoesNotExist:
            return Response({'message': '记录不存在'}, status=404)


class RecruitmentProgressView(APIView):
    """
    招聘管理-招聘进度
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取招聘进度列表"""
        queryset = RecruitmentProgress.objects.all()
        
        # 筛选条件
        department = request.query_params.get('department', '')
        position = request.query_params.get('position', '')
        interview_result = request.query_params.get('interview_result', '')
        hr = request.query_params.get('hr', '')
        keyword = request.query_params.get('keyword', '')
        
        if department:
            queryset = queryset.filter(department=department)
        if position:
            queryset = queryset.filter(position=position)
        if interview_result:
            queryset = queryset.filter(interview_result=interview_result)
        if hr:
            queryset = queryset.filter(inviting_hr=hr)
        if keyword:
            queryset = queryset.filter(candidate_name__icontains=keyword)
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        total = queryset.count()
        
        start = (page - 1) * page_size
        end = start + page_size
        results = queryset[start:end]
        
        data = []
        for item in results:
            try:
                # 处理日期字段，确保它们是日期对象
                recommend_date = item.recommendation_date
                if recommend_date and hasattr(recommend_date, 'strftime'):
                    recommend_date = recommend_date.strftime('%Y-%m-%d')
                
                first_interview_time = item.first_interview_time
                if first_interview_time and hasattr(first_interview_time, 'strftime'):
                    first_interview_time = first_interview_time.strftime('%Y-%m-%d %H:%M')
                
                second_interview_time = item.second_interview_time
                if second_interview_time and hasattr(second_interview_time, 'strftime'):
                    second_interview_time = second_interview_time.strftime('%Y-%m-%d %H:%M')
                
                expected_arrival = item.expected_arrival_time
                if expected_arrival and hasattr(expected_arrival, 'strftime'):
                    expected_arrival = expected_arrival.strftime('%Y-%m-%d')
                
                created_at = item.created_at
                if created_at and hasattr(created_at, 'strftime'):
                    created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
                
                # 处理简历文件 URL
                resume_url = None
                if item.resume_file and hasattr(item.resume_file, 'url'):
                    try:
                        resume_url = item.resume_file.url
                    except:
                        resume_url = None
                
                # 处理新字段的日期格式
                expected_interview_time = item.expected_interview_time
                if expected_interview_time and hasattr(expected_interview_time, 'strftime'):
                    expected_interview_time = expected_interview_time.strftime('%Y-%m-%d %H:%M')
                
                actual_interview_time = item.actual_interview_time
                if actual_interview_time and hasattr(actual_interview_time, 'strftime'):
                    actual_interview_time = actual_interview_time.strftime('%Y-%m-%d %H:%M')
                
                first_interview_actual_time = item.first_interview_actual_time
                if first_interview_actual_time and hasattr(first_interview_actual_time, 'strftime'):
                    first_interview_actual_time = first_interview_actual_time.strftime('%Y-%m-%d %H:%M')
                
                second_interview_actual_time = item.second_interview_actual_time
                if second_interview_actual_time and hasattr(second_interview_actual_time, 'strftime'):
                    second_interview_actual_time = second_interview_actual_time.strftime('%Y-%m-%d %H:%M')
                
                expected_onboard_date = item.expected_onboard_date
                if expected_onboard_date and hasattr(expected_onboard_date, 'strftime'):
                    expected_onboard_date = expected_onboard_date.strftime('%Y-%m-%d')
                
                data.append({
                    'id': item.id,
                    'candidate_name': item.candidate_name,
                    'recommend_date': recommend_date,
                    'department': item.department,
                    'position': item.position,
                    'source_channel': item.source_channel,
                    'resume_url': resume_url,
                    'gender': item.gender,
                    'education': item.education,
                    'invite_hr': item.inviting_hr,
                    'first_interview_time': first_interview_time,
                    'first_interviewer': item.first_interviewer,
                    'second_interview_time': second_interview_time,
                    'second_interviewer': item.second_interviewer,
                    'interview_result': item.interview_result,
                    'expected_arrival': expected_arrival,
                    'created_at': created_at,
                    # 储备阶段字段
                    'reserve_status': item.reserve_status,
                    'add_time': created_at,
                    # 待面试阶段字段
                    'expected_interview_time': expected_interview_time,
                    'actual_interview_time': actual_interview_time,
                    # 初试阶段字段
                    'is_attended': item.is_attended,
                    'is_video_interview': item.is_video_interview,
                    'first_interview_actual_time': first_interview_actual_time,
                    'first_interview_actual_interviewer': item.first_interview_actual_interviewer,
                    'first_interview_result': item.first_interview_result,
                    'first_interview_fail_reason': item.first_interview_fail_reason,
                    # 复试阶段字段
                    'second_interview_actual_time': second_interview_actual_time,
                    'second_interview_actual_interviewer': item.second_interview_actual_interviewer,
                    'second_interview_result': item.second_interview_result,
                    'second_interview_fail_reason': item.second_interview_fail_reason,
                    # 确认offer阶段字段
                    'expected_salary': item.expected_salary,
                    'salary_confirm_standard': item.salary_confirm_standard,
                    'probation_period': item.probation_period,
                    'social_security_remarks': item.social_security_remarks,
                    'onboard_department': item.onboard_department,
                    'onboard_position': item.onboard_position,
                    'job_level': item.job_level,
                    'expected_onboard_date': expected_onboard_date,
                    # 发offer阶段字段
                    'offer_status': item.offer_status,
                    'offer_reply': item.offer_reply,
                })
            except Exception as e:
                # 如果单条记录处理失败，跳过该记录
                print(f"处理招聘进度记录 {item.id} 时出错: {str(e)}")
                continue
        
        return Response({
            'results': data,
            'total': total,
            'page': page,
            'page_size': page_size
        })

    def post(self, request):
        """创建招聘进度记录"""
        data = request.data
        
        progress = RecruitmentProgress.objects.create(
            candidate_name=data.get('candidate_name', ''),
            recommendation_date=data.get('recommend_date'),
            department=data.get('department', ''),
            position=data.get('position', ''),
            source_channel=data.get('source_channel', ''),
            resume_file_name=data.get('resume_url', ''),
            gender=data.get('gender', ''),
            education=data.get('education', ''),
            inviting_hr=data.get('invite_hr', ''),
            first_interview_time=data.get('first_interview_time'),
            first_interviewer=data.get('first_interviewer', ''),
            second_interview_time=data.get('second_interview_time'),
            second_interviewer=data.get('second_interviewer', ''),
            interview_result=data.get('interview_result', '待面试'),
            expected_arrival_time=data.get('expected_arrival'),
            # 新增字段
            reserve_status=data.get('reserve_status', ''),
            expected_interview_time=data.get('expected_interview_time'),
            actual_interview_time=data.get('actual_interview_time'),
            is_attended=data.get('is_attended', False),
            is_video_interview=data.get('is_video_interview', False),
            first_interview_actual_time=data.get('first_interview_actual_time'),
            first_interview_actual_interviewer=data.get('first_interview_actual_interviewer', ''),
            first_interview_result=data.get('first_interview_result', ''),
            first_interview_fail_reason=data.get('first_interview_fail_reason', ''),
            second_interview_actual_time=data.get('second_interview_actual_time'),
            second_interview_actual_interviewer=data.get('second_interview_actual_interviewer', ''),
            second_interview_result=data.get('second_interview_result', ''),
            second_interview_fail_reason=data.get('second_interview_fail_reason', ''),
            expected_salary=data.get('expected_salary', ''),
            salary_confirm_standard=data.get('salary_confirm_standard', ''),
            probation_period=data.get('probation_period', ''),
            social_security_remarks=data.get('social_security_remarks', ''),
            onboard_department=data.get('onboard_department', ''),
            onboard_position=data.get('onboard_position', ''),
            job_level=data.get('job_level', ''),
            expected_onboard_date=data.get('expected_onboard_date'),
            offer_status=data.get('offer_status', ''),
            offer_reply=data.get('offer_reply', ''),
        )
        
        return Response({'id': progress.id, 'message': '创建成功'}, status=201)

    def put(self, request, pk):
        """更新招聘进度记录"""
        try:
            progress = RecruitmentProgress.objects.get(pk=pk)
        except RecruitmentProgress.DoesNotExist:
            return Response({'message': '记录不存在'}, status=404)
        
        data = request.data
        for key, value in data.items():
            if hasattr(progress, key):
                setattr(progress, key, value)
        progress.save()
        
        return Response({'message': '更新成功'})

    def delete(self, request, pk):
        """删除招聘进度记录"""
        try:
            progress = RecruitmentProgress.objects.get(pk=pk)
            progress.delete()
            return Response({'message': '删除成功'})
        except RecruitmentProgress.DoesNotExist:
            return Response({'message': '记录不存在'}, status=404)

