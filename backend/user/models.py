from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model for Jinsyiyuan System
    """
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="昵称")
    avatar = models.URLField(max_length=500, blank=True, null=True, verbose_name="头像")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="手机号")
    role = models.CharField(max_length=20, default='staff', verbose_name="角色")
    department = models.CharField(max_length=50, blank=True, null=True, verbose_name="部门")
    position = models.CharField(max_length=50, blank=True, null=True, verbose_name="职位")
    current_token = models.CharField(max_length=255, blank=True, null=True, verbose_name="当前token")

    class Meta:
        db_table = 'sys_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmployeeRelation(models.Model):
    """
    员工关系管理表
    """
    # 基本信息
    employee_name = models.CharField(max_length=50, verbose_name="员工姓名")
    phone = models.CharField(max_length=11, verbose_name="手机号")
    
    # 部门岗位信息
    department = models.CharField(max_length=50, verbose_name="部门")
    position = models.CharField(max_length=50, verbose_name="岗位")
    employee_status = models.CharField(max_length=20, verbose_name="员工状态")  # 正式、试用期、试岗期
    job_level = models.CharField(max_length=20, blank=True, null=True, verbose_name="职级")
    
    # 个人信息
    household_registration = models.CharField(max_length=100, blank=True, null=True, verbose_name="户籍地")
    birth_date = models.DateField(blank=True, null=True, verbose_name="出生年月日")
    gender = models.CharField(max_length=10, verbose_name="性别")  # 男、女
    age = models.IntegerField(blank=True, null=True, verbose_name="年龄")
    education = models.CharField(max_length=20, blank=True, null=True, verbose_name="学历")
    
    # 入职信息
    entry_date = models.DateField(verbose_name="入司日期")
    regularization_date = models.DateField(blank=True, null=True, verbose_name="转正时间")
    work_years = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="工龄")
    
    # 详细信息（详情中显示）
    birthplace = models.CharField(max_length=100, blank=True, null=True, verbose_name="籍贯")
    id_card_number = models.CharField(max_length=18, blank=True, null=True, verbose_name="身份证号")
    home_address = models.CharField(max_length=200, blank=True, null=True, verbose_name="家庭住址")
    graduation_school = models.CharField(max_length=100, blank=True, null=True, verbose_name="毕业院校")
    major = models.CharField(max_length=50, blank=True, null=True, verbose_name="专业")
    marital_status = models.CharField(max_length=20, blank=True, null=True, verbose_name="婚姻状态")  # 未婚/已婚/离异/丧偶
    family_member_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="家庭成员姓名")
    family_member_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="家庭成员电话")
    emergency_contact_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="紧急联系人姓名")
    emergency_contact_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="紧急联系人电话")
    bank_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="银行卡开户银行名称")
    bank_branch = models.CharField(max_length=100, blank=True, null=True, verbose_name="银行卡开户行")
    bank_account = models.CharField(max_length=30, blank=True, null=True, verbose_name="银行卡号")
    contract_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="合同签订编号")
    social_security_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="社保缴纳基数")
    position_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="岗位工资")
    social_security_status = models.CharField(max_length=10, blank=True, null=True, verbose_name="是否缴纳社保")  # 是、否
    social_security_date = models.DateField(blank=True, null=True, verbose_name="社保缴纳时间")
    
    # 合同信息
    contract_start_date = models.DateField(verbose_name="合同签订日期")
    contract_end_date = models.DateField(verbose_name="合同到期日期")
    
    # 薪资信息
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="薪资")
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="基本工资")
    performance_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="绩效工资")
    commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="提成")
    allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="补助")
    
    # 系统字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'employee_relation'
        verbose_name = '员工关系'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.employee_name


class RecruitmentRequirement(models.Model):
    """
    招聘管理-需求汇总表
    """
    # 需求信息
    department = models.CharField(max_length=50, verbose_name="需求部门")
    requester = models.CharField(max_length=50, verbose_name="需求提出人")
    position = models.CharField(max_length=100, verbose_name="需求岗位")
    application_date = models.DateField(verbose_name="申请日期")
    
    # 紧急程度
    urgency_level = models.CharField(max_length=20, verbose_name="紧急程度")  # 紧急、正常、低优先级
    
    # 人数信息
    required_count = models.IntegerField(verbose_name="需求人数")
    hired_count = models.IntegerField(default=0, verbose_name="已入职人数")
    remaining_count = models.IntegerField(verbose_name="剩余人数")
    
    # 人员类别和状态
    personnel_type = models.CharField(max_length=50, verbose_name="人员类别")  # 全职、兼职、实习等
    recruitment_status = models.CharField(max_length=50, verbose_name="招聘状态")  # 招聘中、已暂停、已完成
    
    # HR信息
    responsible_hr = models.CharField(max_length=50, verbose_name="负责HR")
    work_location = models.CharField(max_length=100, verbose_name="工作地")
    
    # 薪资和要求
    salary_range = models.CharField(max_length=100, blank=True, null=True, verbose_name="建议薪资范围")
    job_requirements = models.TextField(blank=True, null=True, verbose_name="岗位要求")
    remarks = models.TextField(blank=True, null=True, verbose_name="备注")
    
    # 系统字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'recruitment_requirement'
        verbose_name = '招聘需求汇总'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.department}-{self.position}"
    
    def save(self, *args, **kwargs):
        # 自动计算剩余人数
        self.remaining_count = self.required_count - self.hired_count
        super().save(*args, **kwargs)


class RecruitmentProgress(models.Model):
    """
    招聘管理-招聘进度表
    """
    # 候选人信息
    candidate_name = models.CharField(max_length=50, verbose_name="候选人")
    recommendation_date = models.DateField(verbose_name="推荐日期")
    
    # 应聘信息
    department = models.CharField(max_length=50, verbose_name="应聘部门")
    position = models.CharField(max_length=100, verbose_name="应聘岗位")
    source_channel = models.CharField(max_length=50, verbose_name="来源渠道")
    
    # 简历文件
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True, verbose_name="候选人简历")
    resume_file_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="简历文件名")
    
    # 个人信息
    gender = models.CharField(max_length=10, verbose_name="性别")
    education = models.CharField(max_length=20, verbose_name="学历")
    
    # HR信息
    inviting_hr = models.CharField(max_length=50, verbose_name="邀约HR")
    
    # 一面信息
    first_interview_time = models.DateTimeField(blank=True, null=True, verbose_name="一面面试时间")
    first_interviewer = models.CharField(max_length=50, blank=True, null=True, verbose_name="一面面试官")
    
    # 二面信息
    second_interview_time = models.DateTimeField(blank=True, null=True, verbose_name="二面面试时间")
    second_interviewer = models.CharField(max_length=50, blank=True, null=True, verbose_name="二面面试官")
    
    # 面试结果
    interview_result = models.CharField(max_length=50, verbose_name="面试结果")
    
    # 到岗时间
    expected_arrival_time = models.DateField(blank=True, null=True, verbose_name="预计到岗时间")
    
    # === 储备阶段 ===
    reserve_status = models.CharField(max_length=20, blank=True, null=True, verbose_name="储备状态")
    # created_at 自动作为新增时间
    
    # === 待面试阶段 ===
    expected_interview_time = models.DateTimeField(blank=True, null=True, verbose_name="预计面试时间")
    actual_interview_time = models.DateTimeField(blank=True, null=True, verbose_name="实际面试时间")
    
    # === 初试阶段 ===
    is_attended = models.CharField(max_length=10, blank=True, null=True, verbose_name="是否到面")  # 是/否
    is_video_interview = models.CharField(max_length=10, blank=True, null=True, verbose_name="是否视频面试")  # 是/否
    first_interview_actual_time = models.DateTimeField(blank=True, null=True, verbose_name="初试时间")
    first_interview_actual_interviewer = models.CharField(max_length=50, blank=True, null=True, verbose_name="初试面试官")
    first_interview_result = models.CharField(max_length=20, blank=True, null=True, verbose_name="初试结果")  # 通过/未通过
    first_interview_fail_reason = models.TextField(blank=True, null=True, verbose_name="初试未通过原因")
    
    # === 复试阶段 ===
    second_interview_actual_time = models.DateTimeField(blank=True, null=True, verbose_name="复试时间")
    second_interview_actual_interviewer = models.CharField(max_length=50, blank=True, null=True, verbose_name="复试面试官")
    second_interview_result = models.CharField(max_length=20, blank=True, null=True, verbose_name="复试结果")  # 通过/未通过
    second_interview_fail_reason = models.TextField(blank=True, null=True, verbose_name="复试未通过原因")
    
    # === 确认OFFER阶段 ===
    expected_salary = models.CharField(max_length=50, blank=True, null=True, verbose_name="期待薪资")
    salary_confirm_standard = models.CharField(max_length=100, blank=True, null=True, verbose_name="谈薪确认标准")
    probation_period = models.CharField(max_length=20, blank=True, null=True, verbose_name="转正期限")
    social_security_remarks = models.TextField(blank=True, null=True, verbose_name="社保备注")
    onboard_department = models.CharField(max_length=50, blank=True, null=True, verbose_name="入职部门")
    onboard_position = models.CharField(max_length=100, blank=True, null=True, verbose_name="入职岗位")
    job_level = models.CharField(max_length=20, blank=True, null=True, verbose_name="职级")
    expected_onboard_date = models.DateField(blank=True, null=True, verbose_name="预计入职日期")
    
    # === 发OFFER阶段 ===
    offer_status = models.CharField(max_length=20, blank=True, null=True, verbose_name="OFFER状态")  # 已发/未发/已接受/已拒绝
    offer_reply = models.TextField(blank=True, null=True, verbose_name="OFFER回复")
    
    # 系统字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'recruitment_progress'
        verbose_name = '招聘进度'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.candidate_name
