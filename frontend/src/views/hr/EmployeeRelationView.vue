<template>
  <div class="employee-relation-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>员工档案信息</h2>
    </div>

    <!-- 搜索筛选区域 -->
    <div class="search-area">
      <div class="search-row">
        <el-select v-model="filters.department" placeholder="部门" clearable>
          <el-option label="销售中心" value="销售中心" />
          <el-option label="运营中心" value="运营中心" />
          <el-option label="商品中心" value="商品中心" />
          <el-option label="供应链中心" value="供应链中心" />
          <el-option label="财务中心" value="财务中心" />
          <el-option label="人力资源" value="人力资源" />
          <el-option label="行政中心" value="行政中心" />
          <el-option label="设计中心" value="设计中心" />
        </el-select>
        <el-select v-model="filters.position" placeholder="岗位" clearable>
          <el-option label="经理" value="经理" />
          <el-option label="主管" value="主管" />
          <el-option label="专员" value="专员" />
          <el-option label="助理" value="助理" />
        </el-select>
        <el-select v-model="filters.employee_status" placeholder="员工状态" clearable>
          <el-option label="正式" value="正式" />
          <el-option label="试用期" value="试用期" />
          <el-option label="试岗期" value="试岗期" />
        </el-select>
        <el-input v-model="filters.employee_name" placeholder="请输入姓名" clearable />
        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon>搜索
        </el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>
      <div class="search-row">
        <el-select v-model="filters.job_level" placeholder="职级" clearable>
          <el-option label="P1" value="P1" />
          <el-option label="P2" value="P2" />
          <el-option label="P3" value="P3" />
          <el-option label="P4" value="P4" />
          <el-option label="P5" value="P5" />
          <el-option label="M1" value="M1" />
          <el-option label="M2" value="M2" />
          <el-option label="M3" value="M3" />
        </el-select>
        <el-select v-model="filters.work_years" placeholder="工龄" clearable>
          <el-option label="1年以下" value="0-1" />
          <el-option label="1-3年" value="1-3" />
          <el-option label="3-5年" value="3-5" />
          <el-option label="5-10年" value="5-10" />
          <el-option label="10年以上" value="10+" />
        </el-select>
        <el-date-picker
          v-model="filters.contract_start_date"
          type="daterange"
          range-separator="至"
          start-placeholder="合同签订日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
        />
        <el-date-picker
          v-model="filters.birth_date"
          type="daterange"
          range-separator="至"
          start-placeholder="出生日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
        />
      </div>
    </div>

    <!-- 操作按钮区域 -->
    <div class="operation-area">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>新增
      </el-button>
      <el-button @click="handleBatchDelete" :disabled="!selectedRows.length">
        <el-icon><Delete /></el-icon>删除
      </el-button>
      <el-button @click="handleExport">
        <el-icon><Download /></el-icon>导出
      </el-button>
      <el-button @click="handleImport">
        <el-icon><Upload /></el-icon>导入
      </el-button>
    </div>

    <!-- 数据表格 -->
    <div class="table-container">
      <el-table
        :data="tableData"
        v-loading="loading"
        @selection-change="handleSelectionChange"
        border
        stripe
        highlight-current-row
      >
        <el-table-column type="selection" width="50" align="center" />
        <el-table-column prop="department" label="部门" width="100" show-overflow-tooltip />
        <el-table-column prop="position" label="岗位" width="100" show-overflow-tooltip />
        <el-table-column prop="employee_status" label="员工状态" width="90">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.employee_status)">
              {{ row.employee_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="job_level" label="职级" width="70" align="center" />
        <el-table-column prop="employee_name" label="员工姓名" width="100" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column prop="birthplace" label="户籍地" width="120" show-overflow-tooltip />
        <el-table-column prop="birth_date" label="出生年月日" width="110" />
        <el-table-column prop="gender" label="性别" width="70" align="center" />
        <el-table-column prop="age" label="年龄" width="70" align="center" />
        <el-table-column prop="education" label="学历" width="80" />
        <el-table-column prop="entry_date" label="入司日期" width="110" />
        <el-table-column prop="work_years" label="工龄" width="70" align="center" />
        <el-table-column prop="contract_start_date" label="合同签订时间" width="110" />
        <el-table-column prop="contract_end_date" label="合同结束时间" width="110" />
        <el-table-column prop="salary" label="薪资" width="100" align="right">
          <template #default="{ row }">
            {{ formatMoney(row.salary) }}
          </template>
        </el-table-column>
        <el-table-column prop="basic_salary" label="基本工资" width="100" align="right">
          <template #default="{ row }">
            {{ formatMoney(row.basic_salary) }}
          </template>
        </el-table-column>
        <el-table-column prop="performance_salary" label="绩效工资" width="100" align="right">
          <template #default="{ row }">
            {{ formatMoney(row.performance_salary) }}
          </template>
        </el-table-column>
        <el-table-column prop="commission" label="提成" width="80" align="right">
          <template #default="{ row }">
            {{ formatMoney(row.commission) }}
          </template>
        </el-table-column>
        <el-table-column prop="allowance" label="补助" width="80" align="right">
          <template #default="{ row }">
            {{ formatMoney(row.allowance) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">详情</el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">修改</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页 -->
    <div class="pagination-area">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="employee-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="员工姓名" prop="employee_name">
              <el-input v-model="form.employee_name" placeholder="请输入员工姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="出生日期" prop="birth_date">
              <el-date-picker
                v-model="form.birth_date"
                type="date"
                placeholder="选择出生日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="户籍地" prop="birthplace">
              <el-input v-model="form.birthplace" placeholder="请输入户籍地" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学历" prop="education">
              <el-select v-model="form.education" placeholder="请选择学历" style="width: 100%">
                <el-option label="博士" value="博士" />
                <el-option label="硕士" value="硕士" />
                <el-option label="本科" value="本科" />
                <el-option label="大专" value="大专" />
                <el-option label="高中" value="高中" />
                <el-option label="初中" value="初中" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="部门" prop="department">
              <el-select v-model="form.department" placeholder="请选择部门" style="width: 100%">
                <el-option label="销售中心" value="销售中心" />
                <el-option label="运营中心" value="运营中心" />
                <el-option label="商品中心" value="商品中心" />
                <el-option label="供应链中心" value="供应链中心" />
                <el-option label="财务中心" value="财务中心" />
                <el-option label="人力资源" value="人力资源" />
                <el-option label="行政中心" value="行政中心" />
                <el-option label="设计中心" value="设计中心" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="岗位" prop="position">
              <el-input v-model="form.position" placeholder="请输入岗位" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="职级" prop="job_level">
              <el-select v-model="form.job_level" placeholder="请选择职级" style="width: 100%">
                <el-option label="P1" value="P1" />
                <el-option label="P2" value="P2" />
                <el-option label="P3" value="P3" />
                <el-option label="P4" value="P4" />
                <el-option label="P5" value="P5" />
                <el-option label="M1" value="M1" />
                <el-option label="M2" value="M2" />
                <el-option label="M3" value="M3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="员工状态" prop="employee_status">
              <el-select v-model="form.employee_status" placeholder="请选择员工状态" style="width: 100%">
                <el-option label="正式" value="正式" />
                <el-option label="试用期" value="试用期" />
                <el-option label="试岗期" value="试岗期" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="入司日期" prop="entry_date">
              <el-date-picker
                v-model="form.entry_date"
                type="date"
                placeholder="选择入司日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="工龄" prop="work_years">
              <el-input-number v-model="form.work_years" :min="0" :precision="1" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="合同开始" prop="contract_start_date">
              <el-date-picker
                v-model="form.contract_start_date"
                type="date"
                placeholder="选择合同开始日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="合同结束" prop="contract_end_date">
              <el-date-picker
                v-model="form.contract_end_date"
                type="date"
                placeholder="选择合同结束日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="基本工资" prop="basic_salary">
              <el-input-number v-model="form.basic_salary" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="绩效工资" prop="performance_salary">
              <el-input-number v-model="form.performance_salary" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="提成" prop="commission">
              <el-input-number v-model="form.commission" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="补助" prop="allowance">
              <el-input-number v-model="form.allowance" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- 导入对话框 -->
    <el-dialog v-model="importDialogVisible" title="导入员工数据" width="500px">
      <el-upload
        drag
        action="/api/user/employee-relations/import/"
        :headers="uploadHeaders"
        :on-success="handleImportSuccess"
        :on-error="handleImportError"
        accept=".xlsx,.xls"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            请上传 Excel 文件，支持 .xlsx 或 .xls 格式
          </div>
        </template>
      </el-upload>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Delete, Download, Upload, UploadFilled } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import {
  getEmployeeRelations,
  createEmployeeRelation,
  updateEmployeeRelation,
  deleteEmployeeRelation,
  batchDeleteEmployeeRelations,
  exportEmployeeRelations,
  importEmployeeRelations
} from '@/api/hr'

const authStore = useAuthStore()

// 加载状态
const loading = ref(false)
const submitting = ref(false)

// 筛选条件
const filters = reactive({
  department: '',
  position: '',
  employee_status: '',
  job_level: '',
  employee_name: '',
  work_years: '',
  contract_start_date: '',
  birth_date: ''
})

// 表格数据
const tableData = ref([])
const selectedRows = ref([])

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('新增员工')
const isEdit = ref(false)
const currentId = ref(null)
const formRef = ref(null)

// 表单
const form = reactive({
  employee_name: '',
  gender: '男',
  phone: '',
  birth_date: '',
  birthplace: '',
  education: '',
  department: '',
  position: '',
  job_level: '',
  employee_status: '正式',
  entry_date: '',
  work_years: 0,
  contract_start_date: '',
  contract_end_date: '',
  basic_salary: 0,
  performance_salary: 0,
  commission: 0,
  allowance: 0
})

// 表单校验规则
const rules = {
  employee_name: [{ required: true, message: '请输入员工姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  department: [{ required: true, message: '请选择部门', trigger: 'change' }],
  position: [{ required: true, message: '请输入岗位', trigger: 'blur' }],
  employee_status: [{ required: true, message: '请选择员工状态', trigger: 'change' }]
}

// 导入对话框
const importDialogVisible = ref(false)
const uploadHeaders = computed(() => ({
  'Authorization': `Bearer ${authStore.state.accessToken}`
}))

// 获取状态标签类型
const getStatusType = (status) => {
  const map = {
    '正式': 'success',
    '试用期': 'warning',
    '试岗期': 'info'
  }
  return map[status] || 'info'
}

// 格式化金额
const formatMoney = (value) => {
  if (!value && value !== 0) return '-'
  return '¥' + Number(value).toFixed(2)
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...filters
    }
    const res = await getEmployeeRelations(params)
    tableData.value = res.results || []
    pagination.total = res.total || 0
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadData()
}

// 重置
const handleReset = () => {
  Object.keys(filters).forEach(key => {
    filters[key] = ''
  })
  pagination.page = 1
  loadData()
}

// 选择变化
const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  currentId.value = null
  dialogTitle.value = '新增员工'
  Object.keys(form).forEach(key => {
    form[key] = key === 'gender' ? '男' : key === 'work_years' ? 0 : ''
  })
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  isEdit.value = true
  currentId.value = row.id
  dialogTitle.value = '编辑员工'
  Object.keys(form).forEach(key => {
    form[key] = row[key] || (key === 'gender' ? '男' : key === 'work_years' ? 0 : '')
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row) => {
  ElMessage.info('查看功能开发中')
}

// 提交
const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    // 计算总薪资
    form.salary = (form.basic_salary || 0) + (form.performance_salary || 0) + (form.commission || 0) + (form.allowance || 0)
    
    if (isEdit.value) {
      await updateEmployeeRelation(currentId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createEmployeeRelation(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  } finally {
    submitting.value = false
  }
}

// 批量删除
const handleBatchDelete = async () => {
  if (!selectedRows.value.length) {
    ElMessage.warning('请选择要删除的记录')
    return
  }
  try {
    await ElMessageBox.confirm('确定删除选中的记录吗？', '提示', { type: 'warning' })
    const ids = selectedRows.value.map(row => row.id)
    await batchDeleteEmployeeRelations(ids)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 导出
const handleExport = async () => {
  try {
    const res = await exportEmployeeRelations(filters)
    const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `员工关系_${new Date().toISOString().split('T')[0]}.xlsx`
    link.click()
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

// 导入
const handleImport = () => {
  importDialogVisible.value = true
}

// 导入成功
const handleImportSuccess = () => {
  ElMessage.success('导入成功')
  importDialogVisible.value = false
  loadData()
}

// 导入失败
const handleImportError = () => {
  ElMessage.error('导入失败')
}

// 分页变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  loadData()
}

const handlePageChange = (page) => {
  pagination.page = page
  loadData()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.employee-relation-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.search-area {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.search-row {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.search-row:last-child {
  margin-bottom: 0;
}

.search-row .el-select,
.search-row .el-input {
  width: 180px;
}

.search-row .el-date-picker {
  width: 260px;
}

.operation-area {
  background: #fff;
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.table-container {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.pagination-area {
  background: #fff;
  padding: 15px 20px;
  border-radius: 8px;
  display: flex;
  justify-content: flex-end;
}

.employee-form {
  max-height: 500px;
  overflow-y: auto;
}
</style>
