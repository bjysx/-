<template>
  <div>
    <!-- 进度选择 -->
    <div class="mb-5">
      <div class="flex items-center gap-3">
        <span class="text-base font-semibold text-gray-700">进度：</span>
        <div class="flex gap-2">
          <el-button :type="filters.workflow_type === 'sample' ? 'primary' : 'default'" round @click="selectWorkflowType('sample')">样品对接</el-button>
          <el-button :type="filters.workflow_type === 'order' ? 'primary' : 'default'" round @click="selectWorkflowType('order')">订单处理</el-button>
          <el-button :type="filters.workflow_type === 'production' ? 'primary' : 'default'" round @click="selectWorkflowType('production')">大货生产</el-button>
        </div>
      </div>
    </div>

    <!-- 筛选条件 -->
    <div class="mb-5 p-4 bg-gray-50 rounded-lg">
      <el-form :inline="true" :model="filters" class="w-full">
        <el-form-item class="!mb-2 md:!mb-0">
          <el-input v-model="filters.q" clearable placeholder="搜索产品名称" @keyup.enter="loadWorkflows(1)" class="w-[200px]" />
        </el-form-item>
        <el-form-item class="!mb-2 md:!mb-0">
          <el-select v-model="filters.merchandiser" clearable placeholder="跟单员" class="w-[140px]">
            <el-option v-for="u in users" :key="u.id" :label="u.nickname" :value="u.id" />
          </el-select>
        </el-form-item>
        <el-form-item class="!mb-2 md:!mb-0">
          <el-select v-model="filters.platform" clearable placeholder="平台" class="w-[140px]">
            <el-option label="淘宝" value="淘宝" />
            <el-option label="京东" value="京东" />
            <el-option label="拼多多" value="拼多多" />
            <el-option label="抖音" value="抖音" />
          </el-select>
        </el-form-item>
        <el-form-item class="!mb-2 md:!mb-0">
          <el-select v-model="filters.development_rhythm" clearable placeholder="开发节奏" class="w-[140px]">
            <el-option label="快速开发" value="快速开发" />
            <el-option label="常规开发" value="常规开发" />
            <el-option label="缓慢开发" value="缓慢开发" />
          </el-select>
        </el-form-item>
        <el-form-item class="!mb-2 md:!mb-0">
          <el-button v-if="filters.workflow_type === 'sample'" type="primary" :icon="Plus" @click="openCreateDialog">发起流程</el-button>
          <el-button type="success" @click="loadWorkflows(1)">查询</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 数据表格 -->
    <el-table v-loading="loading" :data="workflows" stripe row-key="id">
      <el-table-column type="expand">
        <template #default="{ row }">
          <div class="p-4 bg-gray-50">
            <div class="border-t pt-4">
              <h5 class="text-sm font-semibold mb-3">流程进度</h5>
              <div class="flex items-center justify-between bg-white p-3 rounded-lg shadow-sm overflow-x-auto">
                <div v-for="(stage, index) in getWorkflowStages(row)" :key="index"
                     :class="['flex flex-col items-center flex-1 min-w-[80px]', index < getWorkflowStages(row).length - 1 ? 'relative' : '']">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium z-10',
                    stage.status === 'completed' ? 'bg-green-500 text-white' :
                    stage.status === 'current' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-500']">
                    {{ stage.status === 'completed' ? '✓' : stage.status === 'current' ? '●' : index + 1 }}
                  </div>
                  <span :class="['text-xs mt-1 text-center', stage.status === 'current' ? 'text-blue-600 font-medium' : 'text-slate-600']">{{ stage.name }}</span>
                  <span v-if="stage.handler" class="text-xs text-slate-400 mt-0.5">{{ stage.handler }}</span>
                </div>
              </div>
            </div>
            <div v-if="row.images && row.images.length > 0" class="mt-4 border-t pt-4">
              <h5 class="text-sm font-semibold mb-2">产品图片</h5>
              <div class="flex flex-wrap gap-2">
                <el-image v-for="(image, imgIndex) in row.images.slice(0, 6)" :key="imgIndex"
                  :src="image.startsWith('http') ? image : image.startsWith('/media') ? image : `/api${image}`" fit="cover"
                  class="w-16 h-16 object-cover rounded cursor-pointer hover:opacity-80"
                  :preview-src-list="row.images.map(img => img.startsWith('http') ? img : img.startsWith('/media') ? img : `/api${img}`)"
                  :initial-index="imgIndex" preview-teleported @error="handleImageLoadError" />
              </div>
            </div>
          </div>
        </template>
      </el-table-column>

      <!-- 样品对接列 -->
      <template v-if="filters.workflow_type === 'sample'">
        <el-table-column label="报备ID" width="90">
          <template #default="{ row }">{{ row.report_id || '-' }}</template>
        </el-table-column>
        <el-table-column label="货号" width="90">
          <template #default="{ row }">{{ row.article_number || '-' }}</template>
        </el-table-column>
        <el-table-column label="当前阶段" width="120">
          <template #default="{ row }">
            <span :class="['text-sm font-medium', row.current_stage === 'eliminated' ? 'text-red-600' : 'text-blue-600']">{{ getStageName(row.current_stage) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="部门审批人" width="90">
          <template #default="{ row }">{{ row.approver_name || '-' }}</template>
        </el-table-column>
        <el-table-column label="申请人" width="70">
          <template #default="{ row }">{{ row.applicant_name || '-' }}</template>
        </el-table-column>
        <el-table-column label="申请时间" width="130">
          <template #default="{ row }">
            <span class="text-xs text-slate-500">{{ formatDateTime(row.application_time) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="图片" width="80">
          <template #default="{ row }">
            <div v-if="row.images && row.images.length > 0" class="flex gap-1">
              <el-image v-for="(img, index) in row.images.slice(0, 2)" :key="index"
                :src="img.startsWith('http') ? img : img.startsWith('/media') ? img : `/api${img}`"
                :preview-src-list="row.images.map(i => i.startsWith('http') ? i : i.startsWith('/media') ? i : `/api${i}`)"
                :initial-index="index" fit="cover" class="w-10 h-10 rounded border cursor-pointer" @error="handleImageLoadError" />
            </div>
            <span v-else class="text-xs text-slate-400">无</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)">详情</el-button>
            <el-popconfirm title="确定删除？" @confirm="deleteWorkflowItem(row)">
              <template #reference><el-button type="danger" link size="small">删除</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </template>

      <!-- 订单处理列 -->
      <template v-if="filters.workflow_type === 'order'">
        <el-table-column label="报备ID" width="90">
          <template #default="{ row }">{{ row.report_id || '-' }}</template>
        </el-table-column>
        <el-table-column label="货号" width="90">
          <template #default="{ row }">{{ row.article_number || '-' }}</template>
        </el-table-column>
        <el-table-column label="当前阶段" width="120">
          <template #default="{ row }">
            <span class="text-sm font-medium text-blue-600">{{ getOrderStageName(row.order_stage) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="跟单员" width="80">
          <template #default="{ row }">{{ row.merchandiser_name || '-' }}</template>
        </el-table-column>
        <el-table-column label="产品图片" width="80">
          <template #default="{ row }">
            <div v-if="row.images && row.images.length > 0" class="flex gap-1">
              <el-image v-for="(img, index) in row.images.slice(0, 2)" :key="index"
                :src="img.startsWith('http') ? img : img.startsWith('/media') ? img : `/api${img}`"
                :preview-src-list="row.images.map(i => i.startsWith('http') ? i : i.startsWith('/media') ? i : `/api${i}`)"
                :initial-index="index" fit="cover" class="w-10 h-10 rounded border cursor-pointer" />
            </div>
            <span v-else class="text-xs text-slate-400">无</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)">详情</el-button>
            <el-popconfirm title="确定删除？" @confirm="deleteWorkflowItem(row)">
              <template #reference><el-button type="danger" link size="small">删除</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </template>

      <!-- 大货生产列 -->
      <template v-if="filters.workflow_type === 'production'">
        <el-table-column label="报备ID" width="90">
          <template #default="{ row }">{{ row.report_id || '-' }}</template>
        </el-table-column>
        <el-table-column label="货号" width="90">
          <template #default="{ row }">{{ row.article_number || '-' }}</template>
        </el-table-column>
        <el-table-column label="当前阶段" width="120">
          <template #default="{ row }">
            <span class="text-sm font-medium text-blue-600">{{ getProductionStageName(row.production_stage) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="跟单" width="80">
          <template #default="{ row }">{{ row.merchandiser_name || '-' }}</template>
        </el-table-column>
        <el-table-column label="供应商" width="100">
          <template #default="{ row }">{{ row.supplier || '-' }}</template>
        </el-table-column>
        <el-table-column label="仓储方" width="100">
          <template #default="{ row }">{{ row.order_warehouse || '-' }}</template>
        </el-table-column>
        <el-table-column label="工厂款号" width="120">
          <template #default="{ row }">
            <span v-if="row.order_items && row.order_items.length > 0">
              {{ row.order_items.map(item => item.factory_style_number).filter(Boolean).join(', ') || '-' }}
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)">详情</el-button>
            <el-popconfirm title="确定删除？" @confirm="deleteWorkflowItem(row)">
              <template #reference><el-button type="danger" link size="small">删除</el-button></template>
            </el-popconfirm>
            <el-button type="success" link size="small" @click="handleProductionInbound(row)">入库</el-button>
          </template>
        </el-table-column>
      </template>
    </el-table>

    <!-- 分页 -->
    <div class="mt-5 flex justify-end">
      <el-pagination background layout="total, prev, pager, next, sizes"
        :current-page="pagination.page" :page-size="pagination.page_size"
        :page-sizes="[8, 12, 20, 30]" :total="pagination.total"
        @current-change="loadWorkflows" @size-change="handleSizeChange" />
    </div>

    <!-- 发起工作流对话框 -->
    <el-dialog v-model="createDialogVisible" title="发起工作流 - 双星" width="800px">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-position="top">
        <div class="grid gap-4 md:grid-cols-2">
          <el-form-item label="报备ID" prop="report_id">
            <el-input v-model="createForm.report_id" placeholder="请输入报备ID" />
          </el-form-item>
          <el-form-item label="货号" prop="article_number">
            <el-input v-model="createForm.article_number" placeholder="请输入货号" />
          </el-form-item>
          <el-form-item label="双星系统提报是否通过" prop="ds_system_approval">
            <el-select v-model="createForm.ds_system_approval" class="w-full" placeholder="请选择">
              <el-option label="是" value="是" />
              <el-option label="否" value="否" />
            </el-select>
          </el-form-item>
          <el-form-item label="品牌" prop="ds_brand">
            <el-input v-model="createForm.ds_brand" placeholder="请输入品牌" />
          </el-form-item>
          <el-form-item label="下单颜色" prop="order_color">
            <el-input v-model="createForm.order_color" placeholder="请输入下单颜色" />
          </el-form-item>
          <el-form-item label="数量" prop="quantity">
            <el-input-number v-model="createForm.quantity" class="w-full" :min="0" placeholder="请输入数量" />
          </el-form-item>
          <el-form-item label="选中平台" prop="selected_platform">
            <el-select v-model="createForm.selected_platform" class="w-full" placeholder="请选择平台">
              <el-option label="淘宝" value="淘宝" />
              <el-option label="京东" value="京东" />
              <el-option label="拼多多" value="拼多多" />
              <el-option label="抖音" value="抖音" />
            </el-select>
          </el-form-item>
          <el-form-item label="适用季节" prop="applicable_season">
            <el-select v-model="createForm.applicable_season" class="w-full" placeholder="请选择适用季节">
              <el-option label="春季" value="春季" />
              <el-option label="夏季" value="夏季" />
              <el-option label="秋季" value="秋季" />
              <el-option label="冬季" value="冬季" />
              <el-option label="全季" value="全季" />
            </el-select>
          </el-form-item>
          <el-form-item label="鞋子分类" prop="shoe_category">
            <el-select v-model="createForm.shoe_category" class="w-full" placeholder="请选择鞋子分类">
              <el-option label="单鞋" value="单鞋" />
              <el-option label="网鞋" value="网鞋" />
              <el-option label="棉鞋" value="棉鞋" />
            </el-select>
          </el-form-item>
          <el-form-item label="鞋底材质" prop="sole_material">
            <el-input v-model="createForm.sole_material" placeholder="请输入鞋底材质" />
          </el-form-item>
          <el-form-item label="鞋垫（跟单）" prop="shoe_insole">
            <el-input v-model="createForm.shoe_insole" placeholder="请输入鞋垫" />
          </el-form-item>
          <el-form-item label="款式来源（跟单）" prop="style_source">
            <el-input v-model="createForm.style_source" placeholder="请输入款式来源" />
          </el-form-item>
        </div>
        <el-form-item label="上传图片" prop="images">
          <el-upload action="/api/business/workflows/upload-image/"
            :headers="{ 'Authorization': `Bearer ${authStore.state.accessToken}` }"
            :on-success="handleImageSuccess" :on-error="handleImageError" :on-remove="handleImageRemove"
            :file-list="imageFileList" list-type="picture-card" multiple name="file">
            <el-icon><Plus /></el-icon>
            <template #tip><div class="el-upload__tip">支持上传多张图片</div></template>
          </el-upload>
        </el-form-item>
        <el-form-item label="选择部门审批人" prop="approver">
          <el-select v-model="createForm.approver" class="w-full" placeholder="请选择审批人">
            <el-option v-for="u in users" :key="u.id" :label="u.nickname" :value="u.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitCreateForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { ElMessage, ElMessageBox } from "element-plus"
import { Plus } from "@element-plus/icons-vue"
import { formatDateTime } from "@/utils/formatters"
import { getUsers } from "@/api/system"
import { getWorkflows, getWorkflowDetail, createWorkflow, deleteWorkflow, updateWorkflowStatus, getSupplierMerchandisers } from "@/api/business"
import { useAuthStore } from "@/store/auth"

const authStore = useAuthStore()
const userInfo = computed(() => authStore.state.user)

const createFormRef = ref()
const createDialogVisible = ref(false)
const loading = ref(false)
const submitting = ref(false)
const workflows = ref([])
const users = ref([])
const suppliers = ref([])
const imageFileList = ref([])

const filters = reactive({ q: "", workflow_type: "sample", merchandiser: null, platform: null, development_rhythm: null })
const pagination = reactive({ page: 1, page_size: 8, total: 0 })

const createForm = reactive({
  images: [], report_id: "", article_number: "",
  ds_system_approval: "", ds_brand: "", order_color: "", quantity: null,
  selected_platform: "", applicable_season: "", shoe_category: "",
  sole_material: "", shoe_insole: "", style_source: "", approver: ""
})

const createRules = {
  approver: [{ required: true, message: "请选择审批人", trigger: "change" }]
}

function selectWorkflowType(type) {
  filters.workflow_type = type
  loadWorkflows(1)
}

function handleSizeChange(size) {
  pagination.page_size = size
  loadWorkflows(1)
}

async function loadUsers() {
  try {
    const res = await getUsers()
    users.value = res.results || res
  } catch (error) {
    ElMessage.error('加载用户列表失败')
  }
}

async function loadWorkflows(page = pagination.page) {
  loading.value = true
  try {
    pagination.page = page
    const response = await getWorkflows({
      page: pagination.page,
      page_size: pagination.page_size,
      q: filters.q,
      brand: "double_star",
      workflow_type: filters.workflow_type,
      merchandiser: filters.merchandiser,
      platform: filters.platform,
      development_rhythm: filters.development_rhythm
    })
    workflows.value = response.results
    pagination.total = response.total
  } finally {
    loading.value = false
  }
}

function resetFilters() {
  filters.q = ""
  filters.workflow_type = "sample"
  filters.merchandiser = null
  filters.platform = null
  filters.development_rhythm = null
  loadWorkflows(1)
}

function openCreateDialog() {
  createDialogVisible.value = true
}

async function submitCreateForm() {
  try {
    await createFormRef.value.validate()
    submitting.value = true
    const formData = {
      ...createForm,
      workflow_type: 'sample',
      status: 'pending',
      current_stage: '1',
      progress: 0
    }
    await createWorkflow(formData)
    ElMessage.success("工作流创建成功")
    createDialogVisible.value = false
    createFormRef.value.resetFields()
    imageFileList.value = []
    await loadWorkflows(pagination.page)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('创建失败')
    }
  } finally {
    submitting.value = false
  }
}

async function viewDetail(row) {
  try {
    const detail = await getWorkflowDetail(row.id)
    // 这里可以触发详情事件给父组件处理
    emit('viewDetail', detail)
  } catch (error) {
    ElMessage.error('获取详情失败')
  }
}

async function deleteWorkflowItem(row) {
  try {
    await deleteWorkflow(row.id)
    ElMessage.success('删除成功')
    await loadWorkflows(pagination.page)
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

async function handleProductionInbound(row) {
  try {
    await ElMessageBox.confirm('确认入库？', '确认操作', { type: 'warning' })
    await updateWorkflowStatus(row.id, { action: 'production_inbound', production_stage: 1 })
    ElMessage.success('入库成功')
    await loadWorkflows(pagination.page)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('入库失败')
    }
  }
}

function handleImageSuccess(response) {
  if (response.success) {
    createForm.images.push(response.data.url)
    ElMessage.success('上传成功')
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

function handleImageError() {
  ElMessage.error('图片上传失败')
}

function handleImageRemove(file) {
  const index = createForm.images.indexOf(file.url)
  if (index > -1) {
    createForm.images.splice(index, 1)
  }
}

function handleImageLoadError(event) {
  console.error('图片加载失败:', event)
}

function getWorkflowStages(workflow) {
  // 简化版流程阶段
  const stages = [
    { name: '提交', status: 'completed', handler: workflow.applicant_name },
    { name: '审批', status: workflow.current_stage >= 2 ? 'completed' : 'current', handler: workflow.approver_name },
    { name: '处理', status: workflow.current_stage >= 3 ? 'completed' : 'pending', handler: workflow.merchandiser_name },
    { name: '完成', status: workflow.status === 'completed' ? 'completed' : 'pending', handler: '-' }
  ]
  return stages
}

function getStageName(stage) {
  const names = { 1: '待审批', 2: '处理中', 3: '已完成', eliminated: '已淘汰' }
  return names[stage] || stage
}

function getOrderStageName(stage) {
  const names = { 1: '电子订单', 2: '业务审核', 3: '运营审核', 4: '领导审核' }
  return names[stage] || stage
}

function getProductionStageName(stage) {
  const names = { 1: '待入库', 2: '已入库', 3: '已完成' }
  return names[stage] || stage
}

const emit = defineEmits(['viewDetail'])

onMounted(async () => {
  await Promise.all([loadUsers(), loadWorkflows()])
})
</script>
