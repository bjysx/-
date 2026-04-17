from django.db import models
from user.models import User
import uuid

class BusinessRecord(models.Model):
    id = models.AutoField(primary_key=True)
    page_code = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    owner = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    priority = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    progress = models.IntegerField(default=0)
    target_date = models.CharField(max_length=20, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'business_record'

class ProductInfo(models.Model):
    id = models.AutoField(primary_key=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    style_code = models.CharField(max_length=100, blank=True, null=True)
    product_code = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=200, blank=True, null=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    color_spec = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    spec = models.CharField(max_length=50, blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    market_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    virtual_category = models.CharField(max_length=100, blank=True, null=True)
    product_tags = models.CharField(max_length=200, blank=True, null=True)
    gb_code = models.CharField(max_length=50, blank=True, null=True)
    supplier_name = models.CharField(max_length=100, blank=True, null=True)
    purchase_features = models.CharField(max_length=200, blank=True, null=True)
    suggested_purchase_qty = models.IntegerField(blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    product_status = models.CharField(max_length=20, blank=True, null=True)
    stock_sync = models.IntegerField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    order_message_remark = models.TextField(blank=True, null=True)
    storage_lower_limit = models.IntegerField(blank=True, null=True)
    storage_upper_limit = models.IntegerField(blank=True, null=True)
    overflow_qty = models.IntegerField(blank=True, null=True)
    standard_carton_qty = models.IntegerField(blank=True, null=True)
    standard_carton_volume = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    main_location = models.CharField(max_length=100, blank=True, null=True)
    actual_weight = models.CharField(max_length=50, blank=True, null=True)
    color_pinyin = models.CharField(max_length=100, blank=True, null=True)
    product_property = models.CharField(max_length=100, blank=True, null=True)
    lining_material = models.CharField(max_length=100, blank=True, null=True)
    upper_material = models.CharField(max_length=100, blank=True, null=True)
    package_volume = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    closure_type = models.CharField(max_length=50, blank=True, null=True)
    warehouse_party = models.CharField(max_length=100, blank=True, null=True)
    origin_place = models.CharField(max_length=100, blank=True, null=True)
    occasion = models.CharField(max_length=100, blank=True, null=True)
    ingredient = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    matching_scene = models.CharField(max_length=100, blank=True, null=True)
    sole_material = models.CharField(max_length=100, blank=True, null=True)
    style = models.CharField(max_length=100, blank=True, null=True)
    craft = models.CharField(max_length=100, blank=True, null=True)
    function = models.CharField(max_length=100, blank=True, null=True)
    heel_height = models.CharField(max_length=50, blank=True, null=True)
    item_name = models.CharField(max_length=100, blank=True, null=True)
    brand_secondary = models.CharField(max_length=100, blank=True, null=True)
    crowd = models.CharField(max_length=100, blank=True, null=True)
    target_object = models.CharField(max_length=100, blank=True, null=True)
    season = models.CharField(max_length=50, blank=True, null=True)
    age_group = models.CharField(max_length=50, blank=True, null=True)
    use_scene = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_info'

class ProductWorkflow(models.Model):
    """
    产品工作流表
    """
    # 工作流基本信息
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    product_name = models.CharField(max_length=200, blank=True, null=True)
    brand = models.CharField(max_length=50, default='white_label')  # white_label: 白牌, double_star: 双星
    workflow_type = models.CharField(max_length=50, default='sample')  # sample: 样品对接, order: 订单处理, production: 大货生产
    status = models.CharField(max_length=50, default='pending')  # pending: 待处理, in_progress: 进行中, completed: 已完成, rejected: 已拒绝
    current_stage = models.CharField(max_length=50, default='1')  # 存储阶段数字或'eliminated'
    total_stages = models.IntegerField(default=9)
    progress = models.IntegerField(default=0)
    
    # 淘汰信息
    eliminate_reason = models.TextField(blank=True, null=True)  # 淘汰原因
    eliminate_time = models.DateTimeField(blank=True, null=True)  # 淘汰时间
    eliminator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_eliminators')  # 淘汰人
    
    # 申请人信息
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_applicants')
    application_time = models.DateTimeField(auto_now_add=True)
    
    # 产品信息
    demand_time = models.DateField(blank=True, null=True)
    images = models.JSONField(blank=True, null=True)  # 存储图片URL列表
    hot_sales_data = models.TextField(blank=True, null=True)
    product_link = models.URLField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    launch_date = models.DateField(blank=True, null=True)  # 上市时间
    sales_volume = models.IntegerField(blank=True, null=True)  # 销售量
    platform_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # 平台价格
    demand_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # 需求价格
    sole_material = models.CharField(max_length=100, blank=True, null=True)  # 底材
    size_range = models.CharField(max_length=100, blank=True, null=True)  # 码段
    planning_requirements = models.TextField(blank=True, null=True)  # 企划需求
    required_days = models.IntegerField(blank=True, null=True)
    countdown = models.IntegerField(blank=True, null=True)
    full_color_demand_time = models.DateField(blank=True, null=True)
    development_rhythm = models.CharField(max_length=50, blank=True, null=True)
    season = models.CharField(max_length=50, blank=True, null=True)
    operation = models.CharField(max_length=100, blank=True, null=True)
    platform = models.CharField(max_length=50, blank=True, null=True)  # 平台
    product_selling_points = models.TextField(blank=True, null=True)
    product_improvement_points = models.TextField(blank=True, null=True)
    meeting_suggestions = models.TextField(blank=True, null=True)
    
    # 审批信息
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_approvers')
    approval_time = models.DateTimeField(blank=True, null=True)
    approval_comments = models.TextField(blank=True, null=True)
    
    # 供应商信息
    supplier = models.CharField(max_length=200, blank=True, null=True)
    merchandiser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_merchandisers')
    
    # 样品单信息
    sample_order_number = models.CharField(max_length=100, blank=True, null=True)
    sample_order_time = models.DateTimeField(blank=True, null=True)
    sample_delivery_comments = models.TextField(blank=True, null=True)  # 样品送至业务备注
    
    # 业务人员信息
    salesperson = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_salespersons')
    salesperson_approval_time = models.DateTimeField(blank=True, null=True)
    salesperson_comments = models.TextField(blank=True, null=True)
    
    # 运营人员信息
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_operators')
    operator_approval_time = models.DateTimeField(blank=True, null=True)
    operator_comments = models.TextField(blank=True, null=True)
    # 运营部门领导信息
    operator_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_operator_leaders')
    
    # 摄影师信息
    photographer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_photographers')
    photographer_approval_time = models.DateTimeField(blank=True, null=True)
    photographer_comments = models.TextField(blank=True, null=True)
    white_background_images = models.JSONField(blank=True, null=True)  # 存储白底图片URL列表
    
    # 文员信息
    clerk = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_clerks')
    clerk_approval_time = models.DateTimeField(blank=True, null=True)
    clerk_comments = models.TextField(blank=True, null=True)
    
    # 订单处理信息
    order_stage = models.IntegerField(default=0)  # 订单处理阶段
    order_created = models.BooleanField(default=False)  # 是否已创建订单
    order_warehouse = models.CharField(max_length=200, blank=True, null=True)  # 仓储方
    order_items = models.JSONField(blank=True, null=True)  # 电子订单条目
    order_created_time = models.DateTimeField(blank=True, null=True)  # 下单日期
    requested_ship_date = models.DateField(blank=True, null=True)  # 要求出货日期
    merchandiser_images = models.JSONField(blank=True, null=True)  # 跟单上传图片
    
    # 大货生产信息
    production_stage = models.IntegerField(default=0)  # 生产阶段：0-待入库，1-已入库
    inbound_time = models.DateTimeField(blank=True, null=True)  # 入库时间
    inbound_operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_inbound_operators')  # 入库操作人
    
    # 双星工作流 - 发起流程字段
    report_id = models.CharField(max_length=100, blank=True, null=True)  # 报备ID
    article_number = models.CharField(max_length=100, blank=True, null=True)  # 货号
    ds_system_approval = models.CharField(max_length=50, blank=True, null=True)  # 双星系统提报是否通过
    ds_brand = models.CharField(max_length=100, blank=True, null=True)  # 品牌(双星)
    order_color = models.CharField(max_length=100, blank=True, null=True)  # 下单颜色
    quantity = models.IntegerField(blank=True, null=True)  # 数量
    selected_platform = models.CharField(max_length=100, blank=True, null=True)  # 选中平台
    applicable_season = models.CharField(max_length=50, blank=True, null=True)  # 适用季节
    shoe_category = models.CharField(max_length=50, blank=True, null=True)  # 鞋子分类：单/网/棉
    shoe_insole = models.CharField(max_length=100, blank=True, null=True)  # 鞋垫（跟单）
    style_source = models.CharField(max_length=100, blank=True, null=True)  # 款式来源（跟单）
    
    # 双星工作流 - 跟单员下样品单字段
    expected_completion_time = models.DateField(blank=True, null=True)  # 预计完成时间
    futures_spot_season = models.CharField(max_length=100, blank=True, null=True)  # 适配期货/现货-季节
    sample_order_remarks = models.TextField(blank=True, null=True)  # 样品单备注
    
    # 双星工作流 - 填写初价字段
    initial_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # 初期报价（跟单）
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # 最终价格
    price_details = models.TextField(blank=True, null=True)  # 价格明细
    price_submitted = models.CharField(max_length=50, blank=True, null=True)  # 价格是否提交
    price_submit_date = models.DateField(blank=True, null=True)  # 价格提交日期
    price_approval_completed = models.CharField(max_length=50, blank=True, null=True)  # 价格审批是否完成
    unordered_reason = models.TextField(blank=True, null=True)  # 未下单原因
    ds_six_images_uploaded = models.CharField(max_length=50, blank=True, null=True)  # 双星6张图是否上传
    ds_six_images_qualified = models.CharField(max_length=50, blank=True, null=True)  # 双星6张图是否合格
    price_calculator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_price_calculators')  # 价格核算人员
    
    # 双星工作流 - 核算价格字段
    price_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflow_price_leaders')  # 价格核算人员直属领导
    
    # 双星工作流 - 上传试穿报告字段
    try_on_report = models.JSONField(blank=True, null=True)  # 试穿报告文件列表
    
    # 双星工作流 - 确认寄拍字段
    need_white_bg_photo = models.CharField(max_length=50, blank=True, null=True)  # 是否拍白底图
    white_bg_passed = models.CharField(max_length=50, blank=True, null=True)  # 白底图是否通过
    white_bg_fail_reason = models.TextField(blank=True, null=True)  # 白底图未过说明
    has_try_on_report = models.CharField(max_length=50, blank=True, null=True)  # 是否有试穿报告
    accessory_material = models.CharField(max_length=100, blank=True, null=True)  # 辅料材质
    is_ordered = models.CharField(max_length=50, blank=True, null=True)  # 是否下单
    ds_order_date = models.DateField(blank=True, null=True)  # 下单日期
    need_photo_shoot = models.CharField(max_length=50, blank=True, null=True)  # 是否寄拍
    photo_shoot_date = models.DateField(blank=True, null=True)  # 寄拍日期
    photo_shoot_remarks = models.TextField(blank=True, null=True)  # 寄拍备注
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_workflow'
        verbose_name = '产品工作流'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.product_name or '未命名产品'} - {self.status}"

class SupplierMerchandiser(models.Model):
    """
    供应商跟单员表
    """
    id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=200, unique=True, verbose_name='供应商名称')
    brand_name = models.CharField(max_length=200, default='', verbose_name='品牌名称')
    merchandiser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='跟单员')
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name='地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'supplier_merchandiser'
        verbose_name = '供应商跟单员'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.supplier_name} - {self.merchandiser.username if self.merchandiser else '无'}"


