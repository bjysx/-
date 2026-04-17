<template>
  <div class="page-shell">
    <section class="page-card">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 class="page-title">{{ pageTitle }}</h2>
          <p class="page-subtitle">{{ sectionTitle }} · 聚焦经营分析、过程跟踪与数据驱动决策</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <el-button :icon="Refresh" @click="reloadAll">刷新数据</el-button>
          <el-button v-if="canExport" type="success" :icon="Download" :loading="exporting" @click="handleExport">导出Excel</el-button>
          <el-button v-if="canCreate" type="primary" :icon="Plus" @click="openCreateDialog">新增记录</el-button>
        </div>
      </div>
      <div class="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div v-for="card in summary.overview_cards" :key="card.label" class="rounded-3xl border border-slate-200/60 p-4 dark:border-slate-700/60">
          <p class="text-sm text-slate-500 dark:text-slate-400">{{ card.label }}</p>
          <p class="mt-3 text-2xl font-semibold text-slate-900 dark:text-slate-50">{{ card.formatted || card.value }}</p>
          <p class="mt-2 text-xs text-emerald-500">{{ card.trend }}</p>
        </div>
      </div>
    </section>

    <section class="grid gap-4 xl:grid-cols-3">
      <div class="page-card xl:col-span-2">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold">趋势分析</h3>
          <el-tag type="primary" effect="plain">ECharts</el-tag>
        </div>
        <DashboardChart :option="summary.trend_option" />
      </div>
      <div class="page-card">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold">状态分布</h3>
          <el-tag effect="plain">实时汇总</el-tag>
        </div>
        <DashboardChart :option="summary.status_option" />
      </div>
    </section>

    <section class="page-card">
      <div class="mb-5 flex flex-wrap items-center justify-between gap-3">
        <h3 class="text-lg font-semibold">业务台账</h3>
        <el-form :inline="true" :model="filters" class="w-full xl:w-auto">
          <el-form-item class="!mb-2 md:!mb-0">
            <el-input v-model="filters.q" clearable placeholder="搜索标题/负责人/备注" @keyup.enter="loadRecords(1)" />
          </el-form-item>
          <el-form-item class="!mb-2 md:!mb-0">
            <el-select v-model="filters.status" clearable placeholder="状态筛选" class="w-[160px]">
              <el-option label="规划中" value="规划中" />
              <el-option label="进行中" value="进行中" />
              <el-option label="待审核" value="待审核" />
              <el-option label="已完成" value="已完成" />
            </el-select>
          </el-form-item>
          <el-form-item class="!mb-2 md:!mb-0">
            <el-button type="primary" @click="loadRecords(1)">查询</el-button>
            <el-button @click="resetFilters">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table v-loading="loading" :data="records" stripe>
        <el-table-column label="标题" prop="title" min-width="220" />
        <el-table-column label="负责人" prop="owner" min-width="120" />
        <el-table-column label="部门" prop="department" min-width="140" />
        <el-table-column label="状态" prop="status" min-width="110">
          <template #default="{ row }">
            <el-tag :type="statusTypeMap[row.status] || 'info'" effect="light">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="优先级" prop="priority" min-width="110" />
        <el-table-column label="金额" prop="amount" min-width="130">
          <template #default="{ row }">{{ formatCurrency(row.amount) }}</template>
        </el-table-column>
        <el-table-column label="进度" prop="progress" min-width="140">
          <template #default="{ row }">
            <el-progress :percentage="Number(row.progress)" :stroke-width="10" />
          </template>
        </el-table-column>
        <el-table-column label="目标日期" prop="target_date" min-width="140">
          <template #default="{ row }">{{ formatDate(row.target_date) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="170" fixed="right">
          <template #default="{ row }">
            <el-button v-if="canEdit" type="primary" text @click="openEditDialog(row)">编辑</el-button>
            <el-button v-if="canDelete" type="danger" text @click="removeRecord(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="mt-5 flex justify-end">
        <el-pagination
          background
          layout="total, prev, pager, next, sizes"
          :current-page="pagination.page"
          :page-size="pagination.page_size"
          :page-sizes="[8, 12, 20, 30]"
          :total="pagination.total"
          @current-change="loadRecords"
          @size-change="handleSizeChange"
        />
      </div>
    </section>

    <el-dialog v-model="dialogVisible" :title="editingRecord?.id ? '编辑记录' : '新增记录'" width="560px">
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <div class="grid gap-4 md:grid-cols-2">
          <el-form-item label="标题" prop="title">
            <el-input v-model="form.title" maxlength="100" show-word-limit />
          </el-form-item>
          <el-form-item label="负责人" prop="owner">
            <el-input v-model="form.owner" />
          </el-form-item>
          <el-form-item label="部门" prop="department">
            <el-input v-model="form.department" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="form.status" class="w-full">
              <el-option label="规划中" value="规划中" />
              <el-option label="进行中" value="进行中" />
              <el-option label="待审核" value="待审核" />
              <el-option label="已完成" value="已完成" />
            </el-select>
          </el-form-item>
          <el-form-item label="优先级" prop="priority">
            <el-select v-model="form.priority" class="w-full">
              <el-option label="高" value="高" />
              <el-option label="中" value="中" />
              <el-option label="低" value="低" />
            </el-select>
          </el-form-item>
          <el-form-item label="金额" prop="amount">
            <el-input-number v-model="form.amount" class="w-full" :min="0" :step="1000" :precision="2" />
          </el-form-item>
          <el-form-item label="进度" prop="progress">
            <el-slider v-model="form.progress" :step="5" show-input />
          </el-form-item>
          <el-form-item label="目标日期" prop="target_date">
            <el-date-picker v-model="form.target_date" class="w-full" type="date" value-format="YYYY-MM-DD" />
          </el-form-item>
        </div>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="4" maxlength="300" show-word-limit />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="flex justify-end gap-3">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitting" @click="submitForm">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { ElMessage, ElMessageBox } from "element-plus"
import { Download, Plus, Refresh } from "@element-plus/icons-vue"
import { createRecord, deleteRecord, exportRecords, getPageRecords, getPageSummary, updateRecord } from "@/api/business"
import { useAuthStore } from "@/store/auth"
import { downloadBlob } from "@/utils/download"
import { formatCurrency, formatDate } from "@/utils/formatters"
import DashboardChart from "./DashboardChart.vue"

const props = defineProps({
  sectionTitle: { type: String, required: true },
  pageTitle: { type: String, required: true },
  pageCode: { type: String, required: true }
})

const auth = useAuthStore()
const formRef = ref()
const dialogVisible = ref(false)
const editingRecord = ref(null)
const loading = ref(false)
const submitting = ref(false)
const exporting = ref(false)
const records = ref([])
const summary = reactive({
  overview_cards: [],
  trend_option: {},
  status_option: {}
})
const filters = reactive({ q: "", status: "" })
const pagination = reactive({ page: 1, page_size: 8, total: 0 })
const form = reactive({
  title: "",
  owner: "",
  department: "",
  status: "规划中",
  priority: "中",
  amount: 0,
  progress: 0,
  target_date: "",
  remark: ""
})
const rules = {
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
  owner: [{ required: true, message: "请输入负责人", trigger: "blur" }],
  department: [{ required: true, message: "请输入部门", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "change" }],
  priority: [{ required: true, message: "请选择优先级", trigger: "change" }],
  target_date: [{ required: true, message: "请选择目标日期", trigger: "change" }]
}
const statusTypeMap = { 规划中: "info", 进行中: "warning", 待审核: "primary", 已完成: "success" }
const allowedButtons = computed(() => auth.allowedButtons(props.pageCode))
const canCreate = computed(() => allowedButtons.value.includes("create"))
const canEdit = computed(() => allowedButtons.value.includes("update"))
const canDelete = computed(() => allowedButtons.value.includes("delete"))
const canExport = computed(() => allowedButtons.value.includes("export"))

function resetForm() {
  Object.assign(form, {
    title: "",
    owner: "",
    department: "",
    status: "规划中",
    priority: "中",
    amount: 0,
    progress: 0,
    target_date: "",
    remark: ""
  })
}

async function loadSummary() {
  const response = await getPageSummary(props.pageCode)
  Object.assign(summary, response.data)
}

async function loadRecords(page = pagination.page) {
  loading.value = true
  try {
    pagination.page = page
    const response = await getPageRecords(props.pageCode, {
      page: pagination.page,
      page_size: pagination.page_size,
      q: filters.q,
      status: filters.status
    })
    records.value = response.data.results
    pagination.total = response.data.total
  } finally {
    loading.value = false
  }
}

function resetFilters() {
  filters.q = ""
  filters.status = ""
  loadRecords(1)
}

function handleSizeChange(size) {
  pagination.page_size = size
  loadRecords(1)
}

function openCreateDialog() {
  editingRecord.value = null
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(row) {
  editingRecord.value = row
  Object.assign(form, {
    title: row.title,
    owner: row.owner,
    department: row.department,
    status: row.status,
    priority: row.priority,
    amount: Number(row.amount),
    progress: Number(row.progress),
    target_date: row.target_date,
    remark: row.remark
  })
  dialogVisible.value = true
}

async function submitForm() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  submitting.value = true
  try {
    if (editingRecord.value?.id) {
      await updateRecord(props.pageCode, editingRecord.value.id, form)
      ElMessage.success("记录更新成功")
    } else {
      await createRecord(props.pageCode, form)
      ElMessage.success("记录新增成功")
    }
    dialogVisible.value = false
    await reloadAll()
  } finally {
    submitting.value = false
  }
}

async function removeRecord(row) {
  await ElMessageBox.confirm(`确认删除“${row.title}”吗？`, "删除确认", { type: "warning" })
  await deleteRecord(props.pageCode, row.id)
  ElMessage.success("记录已删除")
  await reloadAll()
}

async function handleExport() {
  exporting.value = true
  try {
    const blob = await exportRecords(props.pageCode, {
      q: filters.q,
      status: filters.status
    })
    downloadBlob(blob, `${props.pageTitle}.xlsx`)
    ElMessage.success("导出成功")
  } finally {
    exporting.value = false
  }
}

async function reloadAll() {
  await Promise.all([loadSummary(), loadRecords(pagination.page)])
}

onMounted(() => {
  reloadAll()
})
</script>
