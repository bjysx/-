from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import BusinessRecord, ProductInfo, ProductWorkflow, SupplierMerchandiser
from django.db.models import Q
from urllib.parse import urlparse, unquote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from django.http import HttpResponse
from io import BytesIO
from datetime import datetime, date
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import random
import logging

logger = logging.getLogger(__name__)

PRODUCT_FIELDS_DEFINITION = [
    {"key": "id", "label": "ID"},
    {"key": "image_url", "label": "图片"},
    {"key": "style_code", "label": "款式编码"},
    {"key": "product_code", "label": "商品编码"},
    {"key": "product_name", "label": "商品名称"},
    {"key": "short_name", "label": "商品简称"},
    {"key": "color_spec", "label": "颜色及规格"},
    {"key": "color", "label": "颜色"},
    {"key": "spec", "label": "规格"},
    {"key": "base_price", "label": "基本售价"},
    {"key": "cost_price", "label": "成本价"},
    {"key": "purchase_price", "label": "采购价"},
    {"key": "market_price", "label": "市场/吊牌价"},
    {"key": "brand", "label": "品牌"},
    {"key": "category", "label": "分类"},
    {"key": "virtual_category", "label": "虚拟分类"},
    {"key": "product_tags", "label": "商品标签"},
    {"key": "gb_code", "label": "国标码"},
    {"key": "supplier_name", "label": "供应商名称"},
    {"key": "purchase_features", "label": "采购特征"},
    {"key": "suggested_purchase_qty", "label": "建议采购数"},
    {"key": "weight", "label": "重量"},
    {"key": "length", "label": "长"},
    {"key": "width", "label": "宽"},
    {"key": "height", "label": "高"},
    {"key": "volume", "label": "体积"},
    {"key": "unit", "label": "单位"},
    {"key": "product_status", "label": "商品状态"},
    {"key": "stock_sync", "label": "库存同步"},
    {"key": "remark", "label": "备注"},
    {"key": "order_message_remark", "label": "订单留言备注"},
    {"key": "storage_lower_limit", "label": "库容下限"},
    {"key": "storage_upper_limit", "label": "库容上限"},
    {"key": "overflow_qty", "label": "溢出数量"},
    {"key": "standard_carton_qty", "label": "标准装箱数量"},
    {"key": "standard_carton_volume", "label": "标准装箱体积"},
    {"key": "main_location", "label": "主仓位"},
    {"key": "actual_weight", "label": "实际重量"},
    {"key": "color_pinyin", "label": "颜色(拼音)"},
    {"key": "product_property", "label": "商品属性"},
    {"key": "lining_material", "label": "帮材"},
    {"key": "upper_material", "label": "帮面材质"},
    {"key": "package_volume", "label": "包装体积"},
    {"key": "closure_type", "label": "闭合方式"},
    {"key": "warehouse_party", "label": "仓储方"},
    {"key": "origin_place", "label": "产地"},
    {"key": "occasion", "label": "场合"},
    {"key": "ingredient", "label": "成份"},
    {"key": "size", "label": "尺码"},
    {"key": "matching_scene", "label": "搭配场景"},
    {"key": "sole_material", "label": "底材"},
    {"key": "style", "label": "风格"},
    {"key": "craft", "label": "工艺"},
    {"key": "function", "label": "功能"},
    {"key": "heel_height", "label": "后跟高"},
    {"key": "item_name", "label": "品名"},
    {"key": "brand_secondary", "label": "品牌(属性)"},
    {"key": "crowd", "label": "人群"},
    {"key": "target_object", "label": "适用对象"},
    {"key": "season", "label": "适用季节"},
    {"key": "age_group", "label": "适用年龄"},
    {"key": "use_scene", "label": "适用场景"},
    {"key": "created_at", "label": "创建时间"},
    {"key": "updated_at", "label": "更新时间"},
]

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "overview_cards": [
                {"label": "当日销售额", "value": 128430, "formatted": "¥128,430", "trend": "+12.5%"},
                {"label": "活跃用户数", "value": 1240, "trend": "+3.2%"},
                {"label": "待处理订单", "value": 45, "trend": "-2.1%"},
                {"label": "库存预警", "value": 12, "trend": "+5.0%"},
            ],
            "trend_option": {
                "xAxis": {"type": 'category', "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']},
                "yAxis": {"type": 'value'},
                "series": [{"data": [random.randint(1000, 5000) for _ in range(7)], "type": 'line', "smooth": True}]
            },
            "module_option": {
                "series": [{
                    "type": 'pie',
                    "radius": '50%',
                    "data": [
                        {"value": 40, "name": '国内电商'},
                        {"value": 30, "name": '跨境电商'},
                        {"value": 20, "name": 'B2B'},
                        {"value": 10, "name": '其他'}
                    ]
                }]
            },
            "radar_option": {
                "radar": {
                    "indicator": [
                        {"name": '销售', "max": 100},
                        {"name": '运营', "max": 100},
                        {"name": '商品', "max": 100},
                        {"name": '供应', "max": 100},
                        {"name": '财务', "max": 100}
                    ]
                },
                "series": [{
                    "type": 'radar',
                    "data": [{"value": [80, 70, 90, 60, 85], "name": '当前经营指数'}]
                }]
            }
        }
        return Response(data)

class PageSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, page_code):
        # Generate some random summary data for any page
        data = {
            "overview_cards": [
                {"label": "项目总数", "value": random.randint(50, 200), "trend": "+2.4%"},
                {"label": "已完成", "value": random.randint(10, 50), "trend": "+5.1%"},
                {"label": "异常项", "value": random.randint(0, 5), "trend": "-1.2%"},
                {"label": "金额汇总", "formatted": f"¥{random.randint(100, 999)}k", "trend": "+12.5%"},
            ],
            "trend_option": {
                "xAxis": {"type": 'category', "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']},
                "yAxis": {"type": 'value'},
                "series": [{"data": [random.randint(10, 100) for _ in range(7)], "type": 'line', "smooth": True}]
            },
            "status_option": {
                "series": [{
                    "type": 'pie',
                    "radius": '50%',
                    "data": [
                        {"value": 40, "name": '进行中'},
                        {"value": 30, "name": '已完成'},
                        {"value": 20, "name": '待审核'},
                        {"value": 10, "name": '规划中'}
                    ]
                }]
            }
        }
        return Response(data)

class PageRecordListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, page_code):
        q = request.query_params.get('q', '')
        status_filter = request.query_params.get('status', '')
        
        # Get or create some mock data if empty
        queryset = BusinessRecord.objects.filter(page_code=page_code)
        if not queryset.exists():
            # Seed mock data for new pages
            for i in range(1, 25):
                BusinessRecord.objects.create(
                    page_code=page_code,
                    title=f"示例任务 {i}",
                    owner=random.choice(["张三", "李四", "王五", "赵六"]),
                    department=random.choice(["销售部", "运营部", "财务部", "人力资源部"]),
                    status=random.choice(["规划中", "进行中", "待审核", "已完成"]),
                    priority=random.choice(["高", "中", "低"]),
                    amount=random.randint(1000, 100000),
                    progress=random.randint(0, 100),
                    target_date="2024-12-31"
                )
            queryset = BusinessRecord.objects.filter(page_code=page_code)

        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(owner__icontains=q))
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        total = queryset.count()
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        records = queryset.order_by('-id')[start:end]
        
        return Response({
            "total": total,
            "results": [
                {
                    "id": r.id,
                    "title": r.title,
                    "owner": r.owner,
                    "department": r.department,
                    "status": r.status,
                    "priority": r.priority,
                    "amount": float(r.amount),
                    "progress": r.progress,
                    "target_date": r.target_date,
                    "remark": r.remark
                } for r in records
            ]
        })

    def post(self, request, page_code):
        data = request.data
        record = BusinessRecord.objects.create(
            page_code=page_code,
            title=data.get('title'),
            owner=data.get('owner'),
            department=data.get('department'),
            status=data.get('status', '进行中'),
            priority=data.get('priority', '中'),
            amount=data.get('amount', 0),
            progress=data.get('progress', 0),
            target_date=data.get('target_date'),
            remark=data.get('remark', '')
        )
        return Response({"id": record.id}, status=status.HTTP_201_CREATED)

class PageRecordDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, page_code, record_id):
        try:
            record = BusinessRecord.objects.get(id=record_id, page_code=page_code)
            data = request.data
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            record.save()
            return Response({"message": "Updated"})
        except BusinessRecord.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, page_code, record_id):
        BusinessRecord.objects.filter(id=record_id, page_code=page_code).delete()
        return Response({"message": "Deleted"})

class PageExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, page_code):
        queryset = BusinessRecord.objects.filter(page_code=page_code)
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "业务导出"
        
        headers = ["ID", "标题", "负责人", "部门", "状态", "优先级", "金额", "进度", "目标日期"]
        ws.append(headers)
        
        for r in queryset:
            ws.append([r.id, r.title, r.owner, r.department, r.status, r.priority, r.amount, r.progress, r.target_date])
            
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = f'attachment; filename={page_code}_export.xlsx'
        return response


def _product_to_dict(product: ProductInfo):
    def as_float(value, default=0):
        if value is None:
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def as_int(value, default=0):
        if value is None:
            return default
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    return {
        "id": product.id,
        "image_url": product.image_url,
        "style_code": product.style_code,
        "product_code": product.product_code,
        "product_name": product.product_name,
        "short_name": product.short_name,
        "color_spec": product.color_spec,
        "color": product.color,
        "spec": product.spec,
        "base_price": as_float(product.base_price),
        "cost_price": as_float(product.cost_price),
        "purchase_price": as_float(product.purchase_price),
        "market_price": as_float(product.market_price),
        "brand": product.brand,
        "category": product.category,
        "virtual_category": product.virtual_category,
        "product_tags": product.product_tags,
        "gb_code": product.gb_code,
        "supplier_name": product.supplier_name,
        "purchase_features": product.purchase_features,
        "suggested_purchase_qty": as_int(product.suggested_purchase_qty),
        "weight": as_float(product.weight),
        "length": as_float(product.length),
        "width": as_float(product.width),
        "height": as_float(product.height),
        "volume": as_float(product.volume),
        "unit": product.unit,
        "product_status": product.product_status,
        "stock_sync": bool(as_int(product.stock_sync)),
        "remark": product.remark,
        "order_message_remark": product.order_message_remark,
        "storage_lower_limit": as_int(product.storage_lower_limit),
        "storage_upper_limit": as_int(product.storage_upper_limit),
        "overflow_qty": as_int(product.overflow_qty),
        "standard_carton_qty": as_int(product.standard_carton_qty),
        "standard_carton_volume": as_float(product.standard_carton_volume),
        "main_location": product.main_location,
        "actual_weight": as_float(product.actual_weight),
        "color_pinyin": product.color_pinyin,
        "product_property": product.product_property,
        "lining_material": product.lining_material,
        "upper_material": product.upper_material,
        "package_volume": as_float(product.package_volume),
        "closure_type": product.closure_type,
        "warehouse_party": product.warehouse_party,
        "origin_place": product.origin_place,
        "occasion": product.occasion,
        "ingredient": product.ingredient,
        "size": product.size,
        "matching_scene": product.matching_scene,
        "sole_material": product.sole_material,
        "style": product.style,
        "craft": product.craft,
        "function": product.function,
        "heel_height": product.heel_height,
        "item_name": product.item_name,
        "brand_secondary": product.brand_secondary,
        "crowd": product.crowd,
        "target_object": product.target_object,
        "season": product.season,
        "age_group": product.age_group,
        "use_scene": product.use_scene,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
    }


class ProductFieldsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        fields = PRODUCT_FIELDS_DEFINITION
        default_keys = [
            "image_url",
            "style_code",
            "product_code",
            "product_name",
            "short_name",
            "color_spec",
            "color",
            "spec",
            "base_price",
            "cost_price",
            "purchase_price",
            "market_price",
            "brand",
            "category",
            "virtual_category",
            "product_tags",
            "gb_code",
            "supplier_name",
            "purchase_features",
            "suggested_purchase_qty",
        ]
        return Response({"fields": fields, "default_keys": default_keys})


class ProductExportView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        export_type = request.query_params.get("export_type", "visible")  # 'visible' or 'all'
        columns_param = request.query_params.get("columns", "")
        
        # Apply filters from request
        style_code = request.query_params.get("style_code", "").strip()
        product_code = request.query_params.get("product_code", "").strip()
        product_name = request.query_params.get("product_name", "").strip()

        queryset = ProductInfo.objects.all().order_by("id")
        if style_code:
            queryset = queryset.filter(style_code__icontains=style_code)
        if product_code:
            queryset = queryset.filter(product_code__icontains=product_code)
        if product_name:
            queryset = queryset.filter(product_name__icontains=product_name)

        if export_type == "visible" and columns_param:
            requested_keys = columns_param.split(",")
            # Ensure 'id' is always included if not present
            if 'id' not in requested_keys:
                requested_keys.insert(0, 'id')
            export_fields = [f for f in PRODUCT_FIELDS_DEFINITION if f["key"] in requested_keys]
        else:  # export_type == 'all' or no columns specified for visible
            export_fields = PRODUCT_FIELDS_DEFINITION

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "商品信息表"

        # Write headers
        headers = [f["label"] for f in export_fields]
        ws.append(headers)

        # Write data
        for product in queryset:
            row_data = []
            product_dict = _product_to_dict(product)
            for field in export_fields:
                value = product_dict.get(field["key"])
                # Handle boolean values for stock_sync
                if field["key"] == "stock_sync":
                    row_data.append("是" if value else "否")
                elif isinstance(value, (datetime, date)):
                    row_data.append(value.strftime("%Y-%m-%d %H:%M:%S") if isinstance(value, datetime) else value.strftime("%Y-%m-%d"))
                else:
                    row_data.append(value)
            ws.append(row_data)

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        filename = f"商品信息表_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class ProductListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        style_code = request.query_params.get("style_code", "").strip()
        product_code = request.query_params.get("product_code", "").strip()
        product_name = request.query_params.get("product_name", "").strip()

        queryset = ProductInfo.objects.all()
        if style_code:
            queryset = queryset.filter(style_code__icontains=style_code)
        if product_code:
            queryset = queryset.filter(product_code__icontains=product_code)
        if product_name:
            queryset = queryset.filter(product_name__icontains=product_name)

        total = queryset.count()
        try:
            page = int(request.query_params.get("page", 1) or 1)
        except ValueError:
            page = 1
        try:
            page_size = int(request.query_params.get("page_size", 10) or 10)
        except ValueError:
            page_size = 10
        start = (page - 1) * page_size
        end = start + page_size
        items = queryset.order_by("id")[start:end]
        return Response({"total": total, "results": [_product_to_dict(item) for item in items]})

    def post(self, request):
        payload = request.data or {}
        allowed = {
            "image_url",
            "style_code",
            "product_code",
            "product_name",
            "short_name",
            "color_spec",
            "color",
            "spec",
            "base_price",
            "cost_price",
            "purchase_price",
            "market_price",
            "brand",
            "category",
            "virtual_category",
            "product_tags",
            "gb_code",
            "supplier_name",
            "purchase_features",
            "suggested_purchase_qty",
            "weight",
            "length",
            "width",
            "height",
            "volume",
            "unit",
            "product_status",
            "stock_sync",
            "remark",
            "order_message_remark",
            "storage_lower_limit",
            "storage_upper_limit",
            "overflow_qty",
            "standard_carton_qty",
            "standard_carton_volume",
            "main_location",
            "actual_weight",
            "color_pinyin",
            "product_property",
            "lining_material",
            "upper_material",
            "package_volume",
            "closure_type",
            "warehouse_party",
            "origin_place",
            "occasion",
            "ingredient",
            "size",
            "matching_scene",
            "sole_material",
            "style",
            "craft",
            "function",
            "heel_height",
            "item_name",
            "brand_secondary",
            "crowd",
            "target_object",
            "season",
            "age_group",
            "use_scene",
        }
        data = {k: v for k, v in payload.items() if k in allowed}

        if not data.get("style_code") or not data.get("product_code") or not data.get("product_name"):
            return Response({"message": "款式编码、商品编码、商品名称为必填项"}, status=status.HTTP_400_BAD_REQUEST)

        product = ProductInfo.objects.create(**data)
        return Response({"id": product.id}, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, product_id):
        try:
            product = ProductInfo.objects.get(id=product_id)
        except ProductInfo.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        payload = request.data or {}
        mutable_fields = {
            "image_url",
            "style_code",
            "product_code",
            "product_name",
            "short_name",
            "color_spec",
            "color",
            "spec",
            "base_price",
            "cost_price",
            "purchase_price",
            "market_price",
            "brand",
            "category",
            "virtual_category",
            "product_tags",
            "gb_code",
            "supplier_name",
            "purchase_features",
            "suggested_purchase_qty",
            "weight",
            "length",
            "width",
            "height",
            "volume",
            "unit",
            "product_status",
            "stock_sync",
            "remark",
            "order_message_remark",
            "storage_lower_limit",
            "storage_upper_limit",
            "overflow_qty",
            "standard_carton_qty",
            "standard_carton_volume",
            "main_location",
            "actual_weight",
            "color_pinyin",
            "product_property",
            "lining_material",
            "upper_material",
            "package_volume",
            "closure_type",
            "warehouse_party",
            "origin_place",
            "occasion",
            "ingredient",
            "size",
            "matching_scene",
            "sole_material",
            "style",
            "craft",
            "function",
            "heel_height",
            "item_name",
            "brand_secondary",
            "crowd",
            "target_object",
            "season",
            "age_group",
            "use_scene",
        }
        for key, value in payload.items():
            if key in mutable_fields:
                setattr(product, key, value)

        if not product.style_code or not product.product_code or not product.product_name:
            return Response({"message": "款式编码、商品编码、商品名称为必填项"}, status=status.HTTP_400_BAD_REQUEST)

        product.save()
        return Response({"message": "Updated"})

    def delete(self, request, product_id):
        ProductInfo.objects.filter(id=product_id).delete()
        return Response({"message": "Deleted"})


class ProductBatchDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ids = request.data.get("ids") or []
        if not isinstance(ids, list) or not ids:
            return Response({"message": "ids 不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        ProductInfo.objects.filter(id__in=ids).delete()
        return Response({"message": "Deleted", "deleted": len(ids)})


class ProductImageProxyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        raw_url = request.query_params.get("url", "")
        if not raw_url:
            return Response({"message": "url 不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        url = unquote(str(raw_url)).strip().replace("`", "")
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            return Response({"message": "url 不合法"}, status=status.HTTP_400_BAD_REQUEST)

        allowed_hosts = {
            "images.sursung.com",
            "images-erp.sursung.com",
            "images.sursung.com:443",
            "images-erp.sursung.com:443",
        }
        if parsed.netloc not in allowed_hosts:
            return Response({"message": "url host 不允许"}, status=status.HTTP_403_FORBIDDEN)

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://erp.sursung.com/",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        }
        try:
            req = Request(url, headers=headers, method="GET")
            with urlopen(req, timeout=15) as resp:
                content_type = resp.headers.get("Content-Type", "application/octet-stream")
                data = resp.read()
                return HttpResponse(data, content_type=content_type)
        except HTTPError as err:
            return Response({"message": "图片访问被拒绝", "status": err.code}, status=err.code)
        except URLError:
            return Response({"message": "图片代理失败"}, status=status.HTTP_502_BAD_GATEWAY)


def _get_user_display_name(user):
    if user is None:
        return None
    return user.nickname if user.nickname else user.username


def _workflow_to_dict(workflow: ProductWorkflow):
    return {
        "id": workflow.id,
        "product_id": workflow.product_id,
        "product_name": workflow.product_name,
        "brand": workflow.brand,
        "workflow_type": workflow.workflow_type,
        "status": workflow.status,
        "current_stage": workflow.current_stage,
        "total_stages": workflow.total_stages,
        "progress": workflow.progress,
        "applicant": workflow.applicant.id if workflow.applicant else None,
        "applicant_name": _get_user_display_name(workflow.applicant),
        "application_time": workflow.application_time,
        "demand_time": workflow.demand_time,
        "images": workflow.images,
        "hot_sales_data": workflow.hot_sales_data,
        "product_link": workflow.product_link,
        "gender": workflow.gender,
        "launch_date": workflow.launch_date,
        "sales_volume": workflow.sales_volume,
        "platform_price": float(workflow.platform_price) if workflow.platform_price else None,
        "demand_price": float(workflow.demand_price) if workflow.demand_price else None,
        "sole_material": workflow.sole_material,
        "size_range": workflow.size_range,
        "planning_requirements": workflow.planning_requirements,
        "required_days": workflow.required_days,
        "countdown": workflow.countdown,
        "full_color_demand_time": workflow.full_color_demand_time,
        "development_rhythm": workflow.development_rhythm,
        "season": workflow.season,
        "operation": workflow.operation,
        "platform": workflow.platform,
        "product_selling_points": workflow.product_selling_points,
        "product_improvement_points": workflow.product_improvement_points,
        "meeting_suggestions": workflow.meeting_suggestions,
        "approver": workflow.approver.id if workflow.approver else None,
        "approver_name": _get_user_display_name(workflow.approver),
        "approval_time": workflow.approval_time,
        "approval_comments": workflow.approval_comments,
        "supplier": workflow.supplier,
        "merchandiser": workflow.merchandiser.id if workflow.merchandiser else None,
        "merchandiser_name": _get_user_display_name(workflow.merchandiser),
        "sample_order_number": workflow.sample_order_number,
        "sample_order_time": workflow.sample_order_time,
        "sample_delivery_comments": workflow.sample_delivery_comments,
        "salesperson": workflow.salesperson.id if workflow.salesperson else None,
        "salesperson_name": _get_user_display_name(workflow.salesperson),
        "salesperson_approval_time": workflow.salesperson_approval_time,
        "salesperson_comments": workflow.salesperson_comments,
        "operator": workflow.operator.id if workflow.operator else None,
        "operator_name": _get_user_display_name(workflow.operator),
        "operator_approval_time": workflow.operator_approval_time,
        "operator_comments": workflow.operator_comments,
        "operator_leader": workflow.operator_leader.id if workflow.operator_leader else None,
        "operator_leader_name": _get_user_display_name(workflow.operator_leader),
        "photographer": workflow.photographer.id if workflow.photographer else None,
        "photographer_name": _get_user_display_name(workflow.photographer),
        "photographer_approval_time": workflow.photographer_approval_time,
        "photographer_comments": workflow.photographer_comments,
        "clerk": workflow.clerk.id if workflow.clerk else None,
        "clerk_name": _get_user_display_name(workflow.clerk),
        "clerk_approval_time": workflow.clerk_approval_time,
        "clerk_comments": workflow.clerk_comments,
        "eliminate_reason": workflow.eliminate_reason,
        "eliminate_time": workflow.eliminate_time,
        "eliminator": workflow.eliminator.id if workflow.eliminator else None,
        "eliminator_name": _get_user_display_name(workflow.eliminator),
        "order_stage": workflow.order_stage,
        "order_created": workflow.order_created,
        "order_warehouse": workflow.order_warehouse,
        "order_items": workflow.order_items,
        "order_created_time": workflow.order_created_time,
        "requested_ship_date": workflow.requested_ship_date,
        "merchandiser_images": workflow.merchandiser_images,
        "production_stage": workflow.production_stage,
        "report_id": workflow.report_id,
        "article_number": workflow.article_number,
        "ds_system_approval": workflow.ds_system_approval,
        "ds_brand": workflow.ds_brand,
        "order_color": workflow.order_color,
        "quantity": workflow.quantity,
        "selected_platform": workflow.selected_platform,
        "applicable_season": workflow.applicable_season,
        "shoe_category": workflow.shoe_category,
        "shoe_insole": workflow.shoe_insole,
        "style_source": workflow.style_source,
        "expected_completion_time": workflow.expected_completion_time,
        "futures_spot_season": workflow.futures_spot_season,
        "sample_order_remarks": workflow.sample_order_remarks,
        "initial_price": float(workflow.initial_price) if workflow.initial_price else None,
        "final_price": float(workflow.final_price) if workflow.final_price else None,
        "price_details": workflow.price_details,
        "price_submitted": workflow.price_submitted,
        "price_submit_date": workflow.price_submit_date,
        "price_approval_completed": workflow.price_approval_completed,
        "unordered_reason": workflow.unordered_reason,
        "ds_six_images_uploaded": workflow.ds_six_images_uploaded,
        "ds_six_images_qualified": workflow.ds_six_images_qualified,
        "price_calculator": workflow.price_calculator.id if workflow.price_calculator else None,
        "price_calculator_name": _get_user_display_name(workflow.price_calculator),
        "price_leader": workflow.price_leader.id if workflow.price_leader else None,
        "price_leader_name": _get_user_display_name(workflow.price_leader),
        "try_on_report": workflow.try_on_report,
        "need_white_bg_photo": workflow.need_white_bg_photo,
        "white_bg_passed": workflow.white_bg_passed,
        "white_bg_fail_reason": workflow.white_bg_fail_reason,
        "has_try_on_report": workflow.has_try_on_report,
        "accessory_material": workflow.accessory_material,
        "is_ordered": workflow.is_ordered,
        "ds_order_date": workflow.ds_order_date,
        "need_photo_shoot": workflow.need_photo_shoot,
        "photo_shoot_date": workflow.photo_shoot_date,
        "photo_shoot_remarks": workflow.photo_shoot_remarks,
        "created_at": workflow.created_at,
        "updated_at": workflow.updated_at,
    }


class WorkflowListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        workflow_type = request.query_params.get("workflow_type", "")
        brand = request.query_params.get("brand", "")
        status = request.query_params.get("status", "")
        applicant = request.query_params.get("applicant", "")
        merchandiser = request.query_params.get("merchandiser", "")
        platform = request.query_params.get("platform", "")
        development_rhythm = request.query_params.get("development_rhythm", "")

        queryset = ProductWorkflow.objects.all()
        
        if brand:
            queryset = queryset.filter(brand=brand)
        
        is_admin = user.is_superuser
        is_manager = user.position and "主管" in user.position
        
        if not is_admin and not is_manager:
            queryset = queryset.filter(
                Q(applicant=user) |
                Q(approver=user) |
                Q(merchandiser=user) |
                Q(salesperson=user) |
                Q(operator=user) |
                Q(operator_leader=user) |
                Q(photographer=user) |
                Q(clerk=user) |
                Q(price_calculator=user) |
                Q(price_leader=user)
            )

        if workflow_type:
            if workflow_type == "order":
                queryset = queryset.filter(
                    Q(workflow_type="order") |
                    Q(workflow_type="sample", current_stage="12")  # 样品对接完成的流程也显示在订单处理中
                )
            elif workflow_type == "production":
                queryset = queryset.filter(
                    Q(workflow_type="production") |
                    Q(workflow_type="order", order_stage__gte=1) |
                    Q(workflow_type="sample", order_stage__gte=1)
                )
            else:
                queryset = queryset.filter(workflow_type=workflow_type)
        if status:
            queryset = queryset.filter(status=status)
        if applicant:
            queryset = queryset.filter(applicant_id=applicant)
        if merchandiser:
            queryset = queryset.filter(merchandiser_id=merchandiser)
        if platform:
            queryset = queryset.filter(platform=platform)
        if development_rhythm:
            queryset = queryset.filter(development_rhythm=development_rhythm)

        total = queryset.count()
        try:
            page = int(request.query_params.get("page", 1) or 1)
        except ValueError:
            page = 1
        try:
            page_size = int(request.query_params.get("page_size", 10) or 10)
        except ValueError:
            page_size = 10
        start = (page - 1) * page_size
        end = start + page_size
        items = queryset.order_by("-id")[start:end]
        return Response({"total": total, "results": [_workflow_to_dict(item) for item in items]})

    def post(self, request):
        payload = request.data or {}
        user = request.user

        # 创建工作流，自动获取当前时间作为提出需求的时间
        workflow = ProductWorkflow.objects.create(
            product_name=payload.get("product_name"),
            brand=payload.get("brand", "white_label"),
            workflow_type=payload.get("workflow_type", "sample"),
            applicant=user,
            demand_time=timezone.now().date(),  # 自动获取当前时间作为提出需求的时间
            images=payload.get("images"),
            hot_sales_data=payload.get("hot_sales_data"),
            product_link=payload.get("product_link"),
            gender=payload.get("gender"),
            launch_date=payload.get("launch_date"),
            sales_volume=payload.get("sales_volume"),
            platform_price=payload.get("platform_price"),
            demand_price=payload.get("demand_price"),
            sole_material=payload.get("sole_material"),
            size_range=payload.get("size_range"),
            planning_requirements=payload.get("planning_requirements"),
            season=payload.get("season"),
            operation=payload.get("operation"),
            platform=payload.get("platform"),
            approver_id=payload.get("approver"),
            report_id=payload.get("report_id"),
            article_number=payload.get("article_number"),
            ds_system_approval=payload.get("ds_system_approval"),
            ds_brand=payload.get("ds_brand"),
            order_color=payload.get("order_color"),
            quantity=payload.get("quantity"),
            selected_platform=payload.get("selected_platform"),
            applicable_season=payload.get("applicable_season"),
            shoe_category=payload.get("shoe_category"),
            shoe_insole=payload.get("shoe_insole"),
            style_source=payload.get("style_source"),
        )

        return Response({"id": workflow.id}, status=status.HTTP_201_CREATED)


class WorkflowDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, workflow_id):
        try:
            workflow = ProductWorkflow.objects.get(id=workflow_id)
            return Response(_workflow_to_dict(workflow))
        except ProductWorkflow.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, workflow_id):
        try:
            workflow = ProductWorkflow.objects.get(id=workflow_id)
        except ProductWorkflow.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        payload = request.data or {}
        allowed_fields = [
            "product_name",
            "demand_time",
            "images",
            "hot_sales_data",
            "product_link",
            "gender",
            "required_days",
            "countdown",
            "full_color_demand_time",
            "development_rhythm",
            "season",
            "operation",
            "product_selling_points",
            "product_improvement_points",
            "meeting_suggestions",
            "approver",
        ]

        for key, value in payload.items():
            if key in allowed_fields:
                if key == "approver":
                    setattr(workflow, key, value)
                else:
                    setattr(workflow, key, value)

        workflow.save()
        return Response({"message": "Updated"})

    def delete(self, request, workflow_id):
        ProductWorkflow.objects.filter(id=workflow_id).delete()
        return Response({"message": "Deleted"})


class WorkflowStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, workflow_id):
        try:
            workflow = ProductWorkflow.objects.get(id=workflow_id)
        except ProductWorkflow.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        payload = request.data or {}
        action = payload.get("action")
        user = request.user

        # 处理工作流状态变更
        if action == "submit":
            # 申请人提交工作流
            if workflow.applicant != user:
                return Response({"message": "你没有这个权限"})
            workflow.status = "in_progress"
            workflow.save()
            # 发送通知给审批人
            if workflow.approver:
                logger.info(f"发送通知给审批人 {workflow.approver.username}：工作流 {workflow.product_name or '未命名产品'} 已提交，请审批")
        elif action == "approve":
            # 领导审批
            if workflow.approver != user:
                return Response({"message": "你没有这个权限"})
            workflow.approver = user
            workflow.approval_time = datetime.now()
            workflow.approval_comments = payload.get("comments")
            workflow.current_stage = "2"
            workflow.progress = 11
            workflow.save()
            # 发送通知给申请人
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 已审批通过")
        elif action == "select_supplier":
            # 选择供应商
            if workflow.approver != user:
                return Response({"message": "你没有这个权限"})
            workflow.supplier = payload.get("supplier")
            # 自动获取供应商对应的跟单员
            merchandiser = None
            try:
                supplier_merchandiser = SupplierMerchandiser.objects.get(supplier_name=workflow.supplier)
                workflow.merchandiser = supplier_merchandiser.merchandiser
                merchandiser = supplier_merchandiser.merchandiser
            except SupplierMerchandiser.DoesNotExist:
                pass
            workflow.current_stage = "3"
            workflow.progress = 22
            workflow.save()
            # 发送通知给跟单员
            if merchandiser:
                logger.info(f"发送通知给跟单员 {merchandiser.username}：工作流 {workflow.product_name or '未命名产品'} 已选择供应商，请确认LOGO/高频")
            # 发送通知给申请人
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 已选择供应商")
        elif action == "confirm_logo":
            # 跟单员确认LOGO/高频
            if workflow.merchandiser != user:
                return Response({"message": "你没有这个权限"})
            workflow.current_stage = "4"
            workflow.progress = 33
            workflow.save()
            # 发送通知给跟单员（下样品单）
            if workflow.merchandiser:
                logger.info(f"发送通知给跟单员 {workflow.merchandiser.username}：工作流 {workflow.product_name or '未命名产品'} LOGO/高频已确认，请下样品单")
        elif action == "place_sample_order":
            # 样品送至业务
            if workflow.merchandiser != user:
                return Response({"message": "你没有这个权限"})
            workflow.sample_order_number = payload.get("sample_order_number")
            workflow.sample_order_time = datetime.now()
            workflow.sample_delivery_comments = payload.get("comments")  # 保存备注
            workflow.salesperson_id = payload.get("salesperson")
            salesperson_id = payload.get("salesperson")
            workflow.current_stage = "5"
            workflow.progress = 44
            workflow.save()
            # 发送通知给业务人员
            from user.models import User
            try:
                salesperson = User.objects.get(id=salesperson_id)
                logger.info(f"发送通知给业务人员 {salesperson.username}：工作流 {workflow.product_name or '未命名产品'} 样品已送达，请审核")
            except User.DoesNotExist:
                pass
        elif action == "salesperson_approve":
            # 首色对接-审核材质
            if workflow.salesperson != user:
                return Response({"message": "你没有这个权限"})
            workflow.salesperson = user
            workflow.salesperson_approval_time = datetime.now()
            workflow.salesperson_comments = payload.get("comments")
            workflow.operator_id = payload.get("operator")
            operator_id = payload.get("operator")
            workflow.current_stage = "6"
            workflow.progress = 55
            workflow.save()
            # 发送通知给运营人员
            from user.models import User
            try:
                operator = User.objects.get(id=operator_id)
                logger.info(f"发送通知给运营人员 {operator.username}：工作流 {workflow.product_name or '未命名产品'} 材质已审核，请审核数据价格")
            except User.DoesNotExist:
                pass
        elif action == "operator_approve":
            # 首色对接-运营审核数据价格
            if workflow.operator != user:
                return Response({"message": "你没有这个权限"})
            workflow.operator = user
            workflow.operator_approval_time = datetime.now()
            workflow.operator_comments = payload.get("comments")
            workflow.current_stage = "7"
            workflow.progress = 66
            workflow.save()
            # 发送通知给业务人员（审核全色）
            if workflow.salesperson:
                logger.info(f"发送通知给业务人员 {workflow.salesperson.username}：工作流 {workflow.product_name or '未命名产品'} 数据价格已确认，请审核全色")
        elif action == "salesperson_approve_full_color":
            # 全色对接-业务审核材质
            if workflow.salesperson != user:
                return Response({"message": "你没有这个权限"})
            workflow.salesperson_approval_time = datetime.now()
            workflow.salesperson_comments = payload.get("comments")
            workflow.current_stage = "8"
            workflow.progress = 77
            workflow.save()
            # 发送通知给运营人员（审核全色）
            if workflow.operator:
                logger.info(f"发送通知给运营人员 {workflow.operator.username}：工作流 {workflow.product_name or '未命名产品'} 全色材质已确认，请审核数据价格")
        elif action == "operator_approve_full_color":
            # 全色对接-运营审核数据价格并选择摄影师
            if workflow.operator != user:
                return Response({"message": "你没有这个权限"})
            workflow.operator_approval_time = datetime.now()
            workflow.operator_comments = payload.get("comments")
            workflow.photographer_id = payload.get("photographer")
            photographer_id = payload.get("photographer")
            workflow.current_stage = "9"
            workflow.progress = 88
            workflow.save()
            # 发送通知给摄影师
            from user.models import User
            try:
                photographer = User.objects.get(id=photographer_id)
                logger.info(f"发送通知给摄影师 {photographer.username}：工作流 {workflow.product_name or '未命名产品'} 全色数据价格已确认，请上传白底")
            except User.DoesNotExist:
                pass
        elif action == "photographer_approve":
            # 摄影师上传白底
            if workflow.photographer != user:
                return Response({"message": "你没有这个权限"})
            workflow.photographer = user
            workflow.photographer_approval_time = datetime.now()
            workflow.photographer_comments = payload.get("comments")
            workflow.white_background_images = payload.get("white_background_images", [])
            workflow.clerk_id = payload.get("clerk")
            clerk_id = payload.get("clerk")
            workflow.current_stage = "10"
            workflow.progress = 99
            workflow.save()
            # 发送通知给文员
            from user.models import User
            try:
                clerk = User.objects.get(id=clerk_id)
                logger.info(f"发送通知给文员 {clerk.username}：工作流 {workflow.product_name or '未命名产品'} 白底已上传，请审核")
            except User.DoesNotExist:
                pass
        elif action == "clerk_approve":
            # 文员审核白底
            if workflow.clerk != user:
                return Response({"message": "你没有这个权限"})
            workflow.clerk = user
            workflow.clerk_approval_time = datetime.now()
            workflow.clerk_comments = payload.get("comments")
            workflow.status = "completed"
            workflow.progress = 100
            workflow.current_stage = "样品对接完成"
            workflow.workflow_type = "order"  # 样品对接完成，进入订单处理流程
            workflow.save()
            # 发送通知给申请人
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 样品对接已完成，进入订单处理流程")
        elif action == "reject":
            # 拒绝工作流，返回上一步
            workflow.status = "in_progress"
            previous_stage = workflow.current_stage
            try:
                current_stage_int = int(workflow.current_stage)
                if current_stage_int > 1:
                    # 返回上一步
                    new_stage = current_stage_int - 1
                    workflow.current_stage = str(new_stage)
                    # 更新进度
                    if new_stage == 1:
                        workflow.progress = 0
                    elif new_stage == 2:
                        workflow.progress = 11
                    elif new_stage == 3:
                        workflow.progress = 22
                    elif new_stage == 4:
                        workflow.progress = 33
                    elif new_stage == 5:
                        workflow.progress = 44
                    elif new_stage == 6:
                        workflow.progress = 55
                    elif new_stage == 7:
                        workflow.progress = 66
                    elif new_stage == 8:
                        workflow.progress = 77
                    elif new_stage == 9:
                        workflow.progress = 88
            except ValueError:
                # 如果current_stage不是数字（例如'eliminated'），则不做处理
                pass
            workflow.save()
            
            # 发送通知给上一步的负责人
            try:
                current_stage_int = int(workflow.current_stage)
                if current_stage_int == 1:
                    # 返回到申请人
                    if workflow.applicant:
                        logger.info(f"发送通知给申请人 {workflow.applicant.username}")
                elif current_stage_int == 2:
                    # 返回到审批人
                    if workflow.approver:
                        logger.info(f"发送通知给审批人 {workflow.approver.username}")
                elif current_stage_int == 3:
                    # 返回到审批人（选择供应商）
                    if workflow.approver:
                        logger.info(f"发送通知给审批人 {workflow.approver.username}")
                elif current_stage_int == 4:
                    # 返回到跟单员（确认LOGO/高频）
                    if workflow.merchandiser:
                        logger.info(f"发送通知给跟单员 {workflow.merchandiser.username}")
                elif current_stage_int == 5:
                    # 返回到跟单员（下样品单）
                    if workflow.merchandiser:
                        logger.info(f"发送通知给跟单员 {workflow.merchandiser.username}")
                elif current_stage_int == 6:
                    # 返回到业务人员（审核样品单）
                    if workflow.salesperson:
                        logger.info(f"发送通知给业务人员 {workflow.salesperson.username}")
                elif current_stage_int == 7:
                    # 返回到运营人员（审核样品单）
                    if workflow.operator:
                        logger.info(f"发送通知给运营人员 {workflow.operator.username}")
                elif current_stage_int == 8:
                    # 返回到业务员（审核全色）
                    if workflow.salesperson:
                        logger.info(f"发送通知给业务人员 {workflow.salesperson.username}")
                elif current_stage_int == 9:
                    # 返回到运营人员（审核全色）
                    if workflow.operator:
                        logger.info(f"发送通知给运营人员 {workflow.operator.username}")
            except ValueError:
                # 如果current_stage不是数字（例如'eliminated'），则不做处理
                pass
        elif action == "eliminate":
            # 淘汰工作流
            if workflow.merchandiser != user:
                return Response({"message": "你没有这个权限"})
            workflow.current_stage = "eliminated"
            workflow.eliminate_reason = payload.get("eliminate_reason")
            workflow.eliminate_time = datetime.now()
            workflow.eliminator = user
            workflow.save()
            # 发送通知给申请人
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 已被淘汰")
        elif action == "create_electronic_order":
            # 制作或修改电子订单
            if workflow.clerk != user:
                return Response({"message": "你没有这个权限"})
            # 保存订单信息
            order_items = payload.get("order_items", [])
            warehouse = payload.get("warehouse", "")
            # 无论是否是第一次创建订单，都设置order_stage为1，这样业务人员可以重新审核
            workflow.order_stage = 1
            workflow.order_created = True
            workflow.order_warehouse = warehouse
            workflow.order_items = order_items
            # 如果是第一次创建订单，设置下单日期
            if not workflow.order_created_time:
                workflow.order_created_time = datetime.now()
            workflow.save()
            # 发送通知给相关人员
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 电子订单已{'制作' if not workflow.order_created else '修改'}完成")
        elif action == "approve_order_material":
            # 业务审核材质
            if workflow.salesperson != user:
                return Response({"message": "你没有这个权限"})
            workflow.order_stage = 2
            workflow.save()
            # 发送通知给相关人员
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 业务审核材质已完成")
        elif action == "approve_order_data_price":
            # 运营审核数据价格
            if workflow.operator != user:
                return Response({"message": "你没有这个权限"})
            workflow.order_stage = 3
            # 保存部门领导人信息
            operator_leader_id = payload.get("operator_leader")
            if operator_leader_id:
                workflow.operator_leader_id = operator_leader_id
            workflow.save()
            # 发送通知给相关人员
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 运营审核数据价格已完成")
        elif action == "approve_order_data_price_by_leader":
            # 运营部门领导审核数据价格
            # 这里可以根据实际情况添加权限检查
            workflow.order_stage = 4
            workflow.current_stage = "production"
            workflow.workflow_type = "production"
            workflow.save()
            # 发送通知给相关人员
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 运营部门领导审核数据价格已完成，已进入大货生产阶段")
        elif action == "reject_order_material":
            # 业务审核材质拒绝
            if workflow.salesperson != user:
                return Response({"message": "你没有这个权限"})
            workflow.order_stage = 0
            workflow.save()
            # 发送通知给相关人员
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 业务审核材质已拒绝")
        elif action == "reject_order_data_price":
            # 运营审核数据价格拒绝
            if workflow.operator != user:
                return Response({"message": "你没有这个权限"})
            workflow.order_stage = 1
            workflow.save()
            # 发送通知给相关人员
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 运营审核数据价格已拒绝")
        elif action == "reject_order_data_price_by_leader":
            # 运营部门领导审核数据价格拒绝
            # 这里可以根据实际情况添加权限检查
            workflow.order_stage = 2
            workflow.save()
            # 发送通知给相关人员
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 运营部门领导审核数据价格已拒绝")
        elif action == "stock_in":
            # 入库操作
            workflow.current_stage = "stocked"
            workflow.save()
            if workflow.applicant:
                logger.info(f"发送通知给申请人 {workflow.applicant.username}：工作流 {workflow.product_name or '未命名产品'} 已入库")

        # ========== 双星工作流状态变更 ==========
        elif action == "ds_approve":
            # 双星 - 部门审批人审核
            logger.info(f'[WorkflowStatusView] 部门审批人审核 - 工作流ID: {workflow.id}, 用户: {user.username}, 当前阶段: {workflow.current_stage}')
            if workflow.approver != user:
                logger.warning(f'[WorkflowStatusView] 权限验证失败 - 用户 {user.username} 不是该工作流的审批人')
                return Response({"message": "你没有这个权限"}, status=403)

            supplier = payload.get("supplier")
            if not supplier:
                logger.error('[WorkflowStatusView] 缺少必填字段: supplier')
                return Response({"message": "请选择供应商"}, status=400)

            workflow.approval_time = datetime.now()
            workflow.approval_comments = payload.get("comments")
            workflow.supplier = supplier
            try:
                supplier_merchandiser = SupplierMerchandiser.objects.get(supplier_name=workflow.supplier)
                workflow.merchandiser = supplier_merchandiser.merchandiser
            except SupplierMerchandiser.DoesNotExist:
                logger.warning(f'[WorkflowStatusView] 未找到供应商: {workflow.supplier}')
            workflow.current_stage = "2"
            workflow.progress = 8
            workflow.status = "in_progress"
            workflow.save()
            logger.info(f'[WorkflowStatusView] 部门审批人审核成功 - 新阶段: {workflow.current_stage}, 进度: {workflow.progress}%')
            return Response({
                "message": "审批通过，流程已推进到跟单员下样品单",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_place_sample_order":
            # 双星 - 跟单员下样品单
            if workflow.merchandiser != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.expected_completion_time = payload.get("expected_completion_time")
            workflow.futures_spot_season = payload.get("futures_spot_season")
            workflow.sample_order_remarks = payload.get("comments")
            workflow.photographer_id = payload.get("photographer")
            workflow.sample_order_time = datetime.now()
            workflow.current_stage = "3"
            workflow.progress = 16
            workflow.save()
            return Response({
                "message": "样品单已下单，流程已推进到样品会确认",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_sample_confirm":
            # 双星 - 样品会确认
            if workflow.merchandiser != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.current_stage = "4"
            workflow.progress = 25
            workflow.save()
            return Response({
                "message": "样品会确认通过，流程已推进到摄影部过白底",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_photographer_white_bg":
            # 双星 - 摄影部过白底
            if workflow.photographer != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.photographer_approval_time = datetime.now()
            workflow.photographer_comments = payload.get("comments")
            workflow.white_background_images = payload.get("white_background_images", [])
            workflow.current_stage = "5"
            workflow.progress = 33
            workflow.save()
            return Response({
                "message": "白底图已上传，流程已推进到填写初价",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_fill_initial_price":
            # 双星 - 填写初价
            if workflow.merchandiser != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.initial_price = payload.get("initial_price")
            workflow.final_price = payload.get("final_price")
            workflow.price_details = payload.get("price_details")
            workflow.price_submitted = payload.get("price_submitted")
            workflow.price_submit_date = payload.get("price_submit_date")
            workflow.price_approval_completed = payload.get("price_approval_completed")
            workflow.unordered_reason = payload.get("unordered_reason")
            workflow.ds_six_images_uploaded = payload.get("ds_six_images_uploaded")
            workflow.ds_six_images_qualified = payload.get("ds_six_images_qualified")
            workflow.price_calculator_id = payload.get("price_calculator")
            workflow.current_stage = "6"
            workflow.progress = 42
            workflow.save()
            return Response({
                "message": "初价已填写，流程已推进到核算价格",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_calculate_price":
            # 双星 - 核算价格
            if workflow.price_calculator != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.clerk_id = payload.get("clerk")
            workflow.price_leader_id = payload.get("price_leader")
            workflow.current_stage = "7"
            workflow.progress = 50
            workflow.save()
            return Response({
                "message": "价格已核算，流程已推进到审批核算价格",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_approve_calculated_price":
            # 双星 - 审批核算价格
            if workflow.price_leader != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.current_stage = "8"
            workflow.progress = 58
            workflow.save()
            return Response({
                "message": "核算价格已审批，流程已推进到钉钉价格审批",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_dingtalk_price_approval":
            # 双星 - 钉钉价格审批
            if workflow.clerk != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.clerk_approval_time = datetime.now()
            workflow.current_stage = "9"
            workflow.progress = 67
            workflow.save()
            return Response({
                "message": "钉钉价格审批已完成，流程已推进到上传试穿报告",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_upload_try_on_report":
            # 双星 - 上传试穿报告
            if workflow.merchandiser != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.try_on_report = payload.get("try_on_report", [])
            workflow.current_stage = "10"
            workflow.progress = 75
            workflow.save()
            return Response({
                "message": "试穿报告已上传，流程已推进到确认寄拍",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_confirm_photo_shoot":
            # 双星 - 确认寄拍（不需要寄拍）
            if workflow.photographer != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.need_photo_shoot = "否"
            workflow.current_stage = "11"
            workflow.progress = 83
            workflow.save()
            return Response({
                "message": "确认不需要寄拍，流程已推进到文员审核",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_need_photo_shoot":
            # 双星 - 确认寄拍（需要寄拍）
            if workflow.photographer != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.need_photo_shoot = "是"
            workflow.need_white_bg_photo = payload.get("need_white_bg_photo")
            workflow.white_bg_passed = payload.get("white_bg_passed")
            workflow.white_bg_fail_reason = payload.get("white_bg_fail_reason")
            workflow.has_try_on_report = payload.get("has_try_on_report")
            workflow.accessory_material = payload.get("accessory_material")
            workflow.is_ordered = payload.get("is_ordered")
            workflow.ds_order_date = payload.get("ds_order_date")
            workflow.photo_shoot_date = payload.get("photo_shoot_date")
            workflow.photo_shoot_remarks = payload.get("photo_shoot_remarks")
            workflow.current_stage = "11"
            workflow.progress = 83
            workflow.save()
            return Response({
                "message": "确认需要寄拍，流程已推进到文员审核",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_clerk_review":
            # 双星 - 文员审核
            if workflow.clerk != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.clerk_approval_time = datetime.now()
            workflow.clerk_comments = payload.get("comments")
            # 样品对接完成，自动进入订单处理流程
            workflow.workflow_type = "order"
            # 设置订单处理的阶段为1（电子订单制作）
            workflow.order_stage = 1
            # 订单处理流程状态保持进行中
            workflow.status = "in_progress"
            workflow.progress = 0  # 订单处理从0%开始
            workflow.current_stage = "1"  # 订单处理的current_stage与order_stage对应
            workflow.save()
            return Response({
                "message": "文员审核通过，样品对接已完成，已自动进入订单处理流程",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage,
                "workflow_type": workflow.workflow_type,
                "order_stage": workflow.order_stage
            })

        elif action == "ds_reject":
            # 双星 - 拒绝，返回上一个流程
            workflow.status = "in_progress"
            try:
                current_stage_int = int(workflow.current_stage)
                if current_stage_int > 1:
                    new_stage = current_stage_int - 1
                    workflow.current_stage = str(new_stage)
                    progress_map = {1: 0, 2: 8, 3: 16, 4: 25, 5: 33, 6: 42, 7: 50, 8: 58, 9: 67, 10: 75, 11: 83}
                    workflow.progress = progress_map.get(new_stage, 0)
            except ValueError:
                pass
            workflow.save()
            return Response({
                "message": "已拒绝，流程已退回上一步",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        elif action == "ds_eliminate":
            # 双星 - 样品会确认拒绝（淘汰流程）
            if workflow.merchandiser != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.current_stage = "eliminated"
            workflow.status = "rejected"
            workflow.eliminate_reason = payload.get("eliminate_reason", "样品会确认不通过，流程淘汰")
            workflow.eliminate_time = datetime.now()
            workflow.eliminator = user
            workflow.save()
            return Response({
                "message": "流程已淘汰",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage
            })

        # 双星 - 订单处理流程
        elif action == "create_ds_electronic_order":
            # 双星 - 制作电子订单
            if workflow.clerk != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.order_stage = 2  # 推进到下一阶段：业务审核材质
            workflow.order_created = True
            workflow.order_created_time = datetime.now()
            workflow.order_items = payload.get("order_items", [])
            workflow.order_warehouse = payload.get("warehouse", "")
            workflow.current_stage = "2"
            workflow.progress = 25
            workflow.save()
            return Response({
                "message": "电子订单制作完成，流程已推进到业务审核材质",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage,
                "order_stage": workflow.order_stage
            })

        elif action == "ds_approve_order_material":
            # 双星 - 业务审核材质
            if workflow.clerk != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.order_stage = 3  # 推进到下一阶段：运营审核数据价格
            workflow.order_material_comments = payload.get("comments", "")
            workflow.order_material_approval_time = datetime.now()
            workflow.current_stage = "3"
            workflow.progress = 50
            workflow.save()
            return Response({
                "message": "业务审核材质通过，流程已推进到运营审核数据价格",
                "status": workflow.status,
                "order_stage": workflow.order_stage
            })

        elif action == "ds_approve_data_price":
            # 双星 - 运营审核数据价格
            if workflow.clerk != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.order_stage = 4  # 推进到下一阶段：运营部门领导审核
            workflow.order_data_comments = payload.get("comments", "")
            workflow.order_data_approval_time = datetime.now()
            workflow.current_stage = "4"
            workflow.progress = 75
            workflow.save()
            return Response({
                "message": "运营审核数据价格通过，流程已推进到运营部门领导审核",
                "status": workflow.status,
                "order_stage": workflow.order_stage
            })

        elif action == "ds_approve_data_price_leader":
            # 双星 - 运营部门领导审核数据价格
            if workflow.clerk != user:
                return Response({"message": "你没有这个权限"}, status=403)
            workflow.order_stage = 5  # 订单处理完成
            workflow.order_leader_comments = payload.get("comments", "")
            workflow.order_leader_approval_time = datetime.now()
            # 订单处理流程完成，自动进入大货生产流程
            workflow.workflow_type = "production"
            workflow.production_stage = 0  # 待入库
            workflow.status = "in_progress"
            workflow.progress = 0
            workflow.current_stage = "0"
            workflow.save()
            return Response({
                "message": "运营部门领导审核通过，订单处理流程已完成，已进入大货生产流程",
                "status": workflow.status,
                "progress": workflow.progress,
                "current_stage": workflow.current_stage,
                "order_stage": workflow.order_stage,
                "workflow_type": workflow.workflow_type,
                "production_stage": workflow.production_stage
            })

        # 双星 - 订单处理拒绝（退回上一步）
        elif action == "ds_order_reject":
            if workflow.clerk != user:
                return Response({"message": "你没有这个权限"}, status=403)

            # 将订单处理阶段退回上一步
            orderStage = workflow.order_stage
            if orderStage is None:
                return Response({"message": "订单尚未开始，无法拒绝"}, status=400)
            if orderStage <= 1:
                return Response({"message": "第一阶段无法拒绝"}, status=400)

            new_orderStage = orderStage - 1
            progress_map = {1: 0, 2: 25, 3: 50, 4: 75}

            workflow.order_stage = new_orderStage
            workflow.current_stage = str(new_orderStage)
            workflow.progress = progress_map.get(new_orderStage, 0)
            workflow.save()

            return Response({
                "message": "已拒绝，订单处理流程退回上一步",
                "status": "in_progress",
                "order_stage": workflow.order_stage
            })

        # 大货生产流程 - 入库
        elif action == "production_inbound":
            # 允许生产流程或订单处理完成后的工作流进行入库
            if workflow.workflow_type != 'production' and not (workflow.workflow_type == 'order' and workflow.order_stage == 5):
                return Response({"message": f"当前工作流不能入库，当前类型：{workflow.workflow_type}，订单阶段：{workflow.order_stage}"}, status=400)
            
            # 如果已经是已入库状态，返回提示
            if workflow.production_stage == 1:
                return Response({"message": "该商品已经入库"}, status=400)
            
            # 如果是订单处理完成后的工作流，先切换到生产流程
            if workflow.workflow_type == 'order' and workflow.order_stage == 5:
                workflow.workflow_type = 'production'
                workflow.production_stage = 0
            
            workflow.production_stage = 1  # 已入库
            workflow.inbound_time = datetime.now()
            workflow.inbound_operator = user
            workflow.save()

            return Response({
                "message": "入库成功",
                "production_stage": workflow.production_stage,
                "inbound_time": workflow.inbound_time
            })

        # 如果action不匹配任何已知操作
        return Response({"message": "未知的操作类型"}, status=400)


class SupplierMerchandiserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        suppliers = SupplierMerchandiser.objects.all()
        return Response([
            {
                "id": s.id,
                "supplier_name": s.supplier_name,
                "merchandiser": s.merchandiser.id if s.merchandiser else None,
                "merchandiser_name": _get_user_display_name(s.merchandiser),
            }
            for s in suppliers
        ])

    def post(self, request):
        payload = request.data or {}
        supplier = SupplierMerchandiser.objects.create(
            supplier_name=payload.get("supplier_name"),
            merchandiser_id=payload.get("merchandiser"),
        )
        return Response({"id": supplier.id}, status=status.HTTP_201_CREATED)


class WorkflowImageUploadView(APIView):
    """
    Upload workflow images
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            file = request.FILES.get('file')

            if not file:
                logger.warning('[WorkflowImageUploadView] 未接收到文件')
                return Response({"success": False, "message": "请选择文件"}, status=400)

            logger.info(f'[WorkflowImageUploadView] 开始上传图片: {file.name}, 大小: {file.size} bytes')

            # 生成唯一文件名
            ext = file.name.split('.')[-1] if '.' in file.name else 'jpg'
            filename = f"workflow_images/{uuid.uuid4()}.{ext}"

            logger.info(f'[WorkflowImageUploadView] 生成文件名: {filename}')

            # 保存文件
            file_path = default_storage.save(filename, ContentFile(file.read()))

            logger.info(f'[WorkflowImageUploadView] 文件保存成功: {file_path}')

            # 构建文件URL
            image_url = f"/media/{file_path}"

            logger.info(f'[WorkflowImageUploadView] 图片上传成功: {image_url}')

            return Response({"success": True, "data": {"url": image_url}})

        except Exception as e:
            logger.error(f'[WorkflowImageUploadView] 图片上传失败: {str(e)}', exc_info=True)
            return Response({"success": False, "message": f"上传失败: {str(e)}"}, status=500)
