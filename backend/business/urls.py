from django.urls import path
from .views import (
    DashboardView,
    PageSummaryView,
    PageRecordListView,
    PageRecordDetailView,
    PageExportView,
    ProductFieldsView,
    ProductListCreateView,
    ProductDetailView,
    ProductBatchDeleteView,
    ProductImageProxyView,
    ProductExportView,
    WorkflowListView,
    WorkflowDetailView,
    WorkflowStatusView,
    WorkflowImageUploadView,
    SupplierMerchandiserView,
)

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('pages/<str:page_code>/summary/', PageSummaryView.as_view(), name='page_summary'),
    path('pages/<str:page_code>/records/', PageRecordListView.as_view(), name='page_records'),
    path('pages/<str:page_code>/records/<int:record_id>/', PageRecordDetailView.as_view(), name='page_record_detail'),
    path('pages/<str:page_code>/export/', PageExportView.as_view(), name='page_export'),
    path('products/fields/', ProductFieldsView.as_view(), name='product_fields'),
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('products/image-proxy/', ProductImageProxyView.as_view(), name='product_image_proxy'),
    path('products/export/', ProductExportView.as_view(), name='product_export'),
    path('products/batch-delete/', ProductBatchDeleteView.as_view(), name='product_batch_delete'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    # 工作流相关路由
    path('workflows/', WorkflowListView.as_view(), name='workflow_list'),
    path('workflows/upload-image/', WorkflowImageUploadView.as_view(), name='workflow_upload_image'),
    path('workflows/<str:workflow_id>/', WorkflowDetailView.as_view(), name='workflow_detail'),
    path('workflows/<str:workflow_id>/status/', WorkflowStatusView.as_view(), name='workflow_status'),
    path('supplier-merchandisers/', SupplierMerchandiserView.as_view(), name='supplier_merchandiser'),
]
