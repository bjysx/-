<template>
  <div class="page-shell">
    <section class="page-card">
      <!-- 品牌选择 -->
      <div class="mb-5">
        <div class="flex items-center gap-3">
          <span class="text-base font-semibold text-gray-700">品牌：</span>
          <div class="flex gap-2">
            <el-button :type="currentBrand === '全部' ? 'primary' : 'default'" round @click="selectBrand('全部')">全部</el-button>
            <el-button :type="currentBrand === '白牌' ? 'primary' : 'default'" round @click="selectBrand('白牌')">白牌</el-button>
            <el-button :type="currentBrand === '双星' ? 'primary' : 'default'" round @click="selectBrand('双星')">双星</el-button>
            <el-button :type="currentBrand === '雅鹿' ? 'primary' : 'default'" round @click="selectBrand('雅鹿')">雅鹿</el-button>
          </div>
        </div>
      </div>

      <!-- 双星品牌工作流 -->
      <DoubleStarWorkflow v-if="currentBrand === '双星'" />

      <!-- 雅鹿品牌待开发 -->
      <div v-else-if="currentBrand === '雅鹿'" class="flex flex-col items-center justify-center py-20 text-gray-400">
        <el-icon :size="64" class="mb-4"><Collection /></el-icon>
        <span class="text-lg">待开发</span>
      </div>

      <!-- 白牌和全部品牌的工作流 -->
      <template v-else>
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
              <el-select v-model="filters.status" clearable placeholder="状态筛选" class="w-[140px]">
                <el-option label="待处理" value="pending" />
                <el-option label="进行中" value="in_progress" />
                <el-option label="已完成" value="completed" />
                <el-option label="已拒绝" value="rejected" />
              </el-select>
            </el-form-item>
            <el-form-item class="!mb-2 md:!mb-0">
              <el-select v-model="filters.merchandiser" clearable placeholder="跟单员" class="w-[140px]">
                <el-option v-for="user in users" :key="user.id" :label="user.nickname" :value="user.id" />
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
              <el-button v-if="filters.workflow_type === 'sample'" type="primary" :icon="Plus" @click="openCreateWorkflowDialog">发起流程</el-button>
              <el-button type="success" @click="loadWorkflows(1)">查询</el-button>
              <el-button @click="resetFilters">重置</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 全部品牌时的待开发提示 -->
        <div v-if="currentBrand === '全部'" class="flex flex-col items-center justify-center py-20 text-gray-400">
          <el-icon :size="64" class="mb-4"><Collection /></el-icon>
          <span class="text-lg">待开发</span>
        </div>

        <!-- 白牌工作流表格 -->
        <el-table v-else v-loading="loading" :data="workflows" stripe row-key="id">
          <!-- 表格内容保持原有逻辑 -->
          <el-table-column type="expand">
            <template #default="{ row }">
              <div class="p-4 bg-gray-50">
                <!-- 流程进度 -->
                <div class="mt-4 border-t pt-4">
                  <h5 class="text-sm font-semibold mb-3">流程进度</h5>
                  <div class="flex items-center justify-between bg-white p-3 rounded-lg shadow-sm">
                    <div v-for="(stage, index) in getWorkflowStages(row)" :key="index" 
                         :class="['flex flex-col items-center flex-1', index < getWorkflowStages(row).length - 1 ? 'relative' : '']">
                      <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium z-10',
                        stage.status === 'completed' ? 'bg-green-500 text-white' :
                        stage.status === 'current' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-500']">
                        {{ stage.status === 'completed' ? '✓' : stage.status === 'current' ? '●' : index + 1 }}
                      </div>
                      <span :class="['text-xs mt-1 text-center', stage.status === 'current' ? 'text-blue-600 font-medium' : 'text-slate-600']">
                        {{ stage.name }}
                      </span>
                      <span v-if="stage.handler" class="text-xs text-slate-400 mt-0.5">{{ stage.handler }}</span>
                      <!-- 连接线 -->
                      <div v-if="index < getWorkflowStages(row).length - 1"
                           :class="['absolute top-4 left-1/2 w-full h-0.5 -z-0',
                            stage.status === 'completed' && getWorkflowStages(row)[index + 1].status !== 'pending' ? 'bg-green-400' : 'bg-gray-200']"
                           style="width: calc(100% - 2rem); left: calc(50% + 1rem);"></div>
                    </div>
                  </div>
                </div>

                <!-- 图片预览 -->
                <div v-if="row.images && row.images.length > 0" class="mt-4 border-t pt-4">
                  <h5 class="text-sm font-semibold mb-2">产品图片</h5>
                  <div class="flex flex-wrap gap-2">
                    <el-image
                      v-for="(image, imgIndex) in row.images.slice(0, 6)"
                      :key="imgIndex"
                      :src="image.startsWith('http') ? image : `/api${image}`"
                      fit="cover"
                      class="w-16 h-16 object-cover rounded cursor-pointer hover:opacity-80 transition-opacity"
                      :preview-src-list="row.images.map(img => img.startsWith('http') ? img : `/api${img}`)"
                      :initial-index="imgIndex"
                      preview-teleported
                    />
                    <span v-if="row.images.length > 6" class="w-16 h-16 flex items-center justify-center bg-gray-100 rounded text-xs text-slate-500">
                      +{{ row.images.length - 6 }}
                    </span>
                  </div>
                </div>
              </div>
            </template>
          </el-table-column>

          <!-- 大货生产界面字段 -->
          <template v-if="filters.workflow_type === 'production'">
            <el-table-column label="产品名称" prop="product_name" width="100" show-overflow-tooltip />
            <el-table-column label="跟单" width="80">
              <template #default="{ row }">
                <span class="text-sm">{{ row.merchandiser_name || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="下单日期" width="120">
              <template #default="{ row }">
                <span class="text-xs text-slate-500">{{ formatDateTime(row.order_created_time) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="要求出货日期" width="120">
              <template #default="{ row }">
                <span class="text-xs text-slate-500">{{ formatDateTime(row.requested_ship_date) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="供应商" width="100">
              <template #default="{ row }">
                <span class="text-sm">{{ row.supplier_name || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="仓储方" width="100">
              <template #default="{ row }">
                <span class="text-sm">{{ row.order_warehouse || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="工厂款号" width="100">
              <template #default="{ row }">
                <span class="text-sm">{{ row.order_items && row.order_items.length > 0 ? row.order_items[0].factory_style_number : '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="跟单上传图片" width="120">
              <template #default="{ row }">
                <div class="flex items-center gap-2">
                  <div v-if="row.merchandiser_images && row.merchandiser_images.length > 0" class="flex gap-1">
                    <el-image
                      v-for="(img, index) in row.merchandiser_images.slice(0, 2)"
                      :key="index"
                      :src="img"
                      :preview-src-list="row.merchandiser_images"
                      :initial-index="index"
                      fit="cover"
                      class="w-10 h-10 rounded border cursor-pointer"
                    />
                  </div>
                  <span v-else class="text-xs text-slate-400">无</span>
                </div>
              </template>
            </el-table-column>
          </template>

          <!-- 样品对接和订单处理字段 -->
          <template v-else>
            <el-table-column label="产品名称" prop="product_name" min-width="150" show-overflow-tooltip />
            <el-table-column label="当前阶段" width="120">
              <template #default="{ row }">
                <el-tag :type="getStageType(row.current_stage)" size="small">
                  {{ getStageName(row.current_stage) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="申请人" width="100">
              <template #default="{ row }">
                <span class="text-sm">{{ row.applicant_name || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="申请时间" width="150">
              <template #default="{ row }">
                <span class="text-xs text-slate-500">{{ formatDateTime(row.created_at) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="viewDetail(row)">详情</el-button>
                <el-button v-if="canApprove(row)" type="success" link size="small" @click="handleApprove(row)">审批</el-button>
              </template>
            </el-table-column>
          </template>
        </el-table>

        <!-- 分页 -->
        <div class="mt-4 flex justify-end">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :total="pagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </template>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Collection } from '@element-plus/icons-vue'
import { formatDateTime } from '@/utils/formatters'
import { getWorkflows } from '@/api/business'
import { getUsers } from '@/api/system'
import DoubleStarWorkflow from './DoubleStarWorkflow.vue'

// 当前品牌
const currentBrand = ref('白牌')

// 筛选条件
const filters = reactive({
  q: '',
  status: '',
  merchandiser: '',
  platform: '',
  development_rhythm: '',
  workflow_type: 'sample'
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 数据
const workflows = ref([])
const users = ref([])
const loading = ref(false)

// 选择品牌
function selectBrand(brand) {
  currentBrand.value = brand
  if (brand === '白牌') {
    loadWorkflows(1)
  }
}

// 选择工作流类型
function selectWorkflowType(type) {
  filters.workflow_type = type
  if (currentBrand.value === '白牌') {
    loadWorkflows(1)
  }
}

// 加载工作流数据
async function loadWorkflows(page = 1) {
  if (currentBrand.value !== '白牌') return
  
  loading.value = true
  try {
    const params = {
      page,
      page_size: pagination.pageSize,
      brand: 'white_label',
      workflow_type: filters.workflow_type,
      q: filters.q,
      status: filters.status,
      merchandiser: filters.merchandiser,
      platform: filters.platform,
      development_rhythm: filters.development_rhythm
    }
    const res = await getWorkflows(params)
    workflows.value = res.results || []
    pagination.total = res.total || 0
    pagination.page = page
  } catch (error) {
    ElMessage.error('加载工作流数据失败')
  } finally {
    loading.value = false
  }
}

// 加载用户列表
async function loadUsers() {
  try {
    const res = await getUsers()
    users.value = res.results || res || []
  } catch (error) {
    console.error('加载用户列表失败:', error)
  }
}

// 获取阶段名称
function getStageName(stage) {
  const stageMap = {
    1: '部门审批',
    2: '选择供应商',
    3: '确认LOGO',
    4: '样品送达',
    5: '首色审核',
    6: '运营审核',
    7: '全色审核',
    8: '运营审核',
    9: '摄影师上传',
    10: '文员审核',
    11: '已完成'
  }
  return stageMap[stage] || '未知阶段'
}

// 获取阶段类型
function getStageType(stage) {
  if (stage === 11) return 'success'
  if (stage === 1) return 'info'
  return 'warning'
}

// 获取工作流阶段
function getWorkflowStages(row) {
  const stages = [
    { name: '提交', status: 'completed', handler: row.applicant_name },
    { name: '审批', status: row.current_stage >= 2 ? 'completed' : row.current_stage === 1 ? 'current' : 'pending', handler: row.approver_name },
    { name: '选供应商', status: row.current_stage >= 3 ? 'completed' : row.current_stage === 2 ? 'current' : 'pending', handler: row.supplier },
    { name: '确认LOGO', status: row.current_stage >= 4 ? 'completed' : row.current_stage === 3 ? 'current' : 'pending', handler: row.merchandiser_name },
    { name: '样品送达', status: row.current_stage >= 5 ? 'completed' : row.current_stage === 4 ? 'current' : 'pending', handler: row.merchandiser_name },
    { name: '首色审核', status: row.current_stage >= 6 ? 'completed' : row.current_stage === 5 ? 'current' : 'pending', handler: row.salesperson_name },
    { name: '运营审核', status: row.current_stage >= 7 ? 'completed' : row.current_stage === 6 ? 'current' : 'pending', handler: row.operator_name },
    { name: '全色审核', status: row.current_stage >= 8 ? 'completed' : row.current_stage === 7 ? 'current' : 'pending', handler: row.salesperson_name },
    { name: '运营审核', status: row.current_stage >= 9 ? 'completed' : row.current_stage === 8 ? 'current' : 'pending', handler: row.operator_name },
    { name: '摄影师上传', status: row.current_stage >= 10 ? 'completed' : row.current_stage === 9 ? 'current' : 'pending', handler: row.photographer_name },
    { name: '文员审核', status: row.current_stage >= 11 ? 'completed' : row.current_stage === 10 ? 'current' : 'pending', handler: row.clerk_name }
  ]
  return stages
}

// 是否可以审批
function canApprove(row) {
  return row.status === 'pending' || row.status === 'in_progress'
}

// 查看详情
function viewDetail(row) {
  ElMessage.info('查看详情: ' + row.product_name)
}

// 处理审批
function handleApprove(row) {
  ElMessage.info('审批: ' + row.product_name)
}

// 打开创建工作流对话框
function openCreateWorkflowDialog() {
  ElMessage.info('发起流程')
}

// 重置筛选
function resetFilters() {
  filters.q = ''
  filters.status = ''
  filters.merchandiser = ''
  filters.platform = ''
  filters.development_rhythm = ''
  loadWorkflows(1)
}

// 分页大小变化
function handleSizeChange(size) {
  pagination.pageSize = size
  loadWorkflows(1)
}

// 页码变化
function handlePageChange(page) {
  loadWorkflows(page)
}

onMounted(() => {
  loadUsers()
  loadWorkflows(1)
})
</script>

<style scoped>
.page-shell {
  @apply p-5;
}

.page-card {
  @apply bg-white rounded-lg shadow-sm p-5;
}
</style>
