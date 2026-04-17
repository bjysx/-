<template>
  <div class="page-shell flex flex-col h-full">
    <!-- 顶部部分 -->
    <section class="page-card mb-4">
      <div class="flex flex-wrap items-start justify-between gap-4">
        <div class="flex flex-wrap gap-2 items-center"> <!-- Combined button group -->
          <el-button :icon="Setting" @click="drawerVisible = true">列设置</el-button>
          <el-button type="primary" :icon="Plus" @click="openCreate">新增商品</el-button>
          <el-button type="danger" :icon="Delete" :disabled="selectedIds.length === 0" @click="confirmDelete">
            删除
          </el-button>
          <el-dropdown trigger="click">
            <el-button :icon="Download">导出</el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="exportData('visible')">导出可见列</el-dropdown-item>
                <el-dropdown-item @click="exportData('all')">导出所有列</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        <div> <!-- Title group -->
          <h2 class="page-title">商品列表</h2>
          <p class="page-subtitle">商品中心 · 商品信息管理与库存策略配置</p>
        </div>
      </div>

      <div class="mt-6">
        <el-form :inline="true" :model="filters" class="w-full">
          <el-form-item class="!mb-2 md:!mb-0" label="款式编码">
            <el-input v-model="filters.style_code" clearable placeholder="请输入款式编码" @keyup.enter="loadProducts(1)" />
          </el-form-item>
          <el-form-item class="!mb-2 md:!mb-0" label="商品编码">
            <el-input v-model="filters.product_code" clearable placeholder="请输入商品编码" @keyup.enter="loadProducts(1)" />
          </el-form-item>
          <el-form-item class="!mb-2 md:!mb-0" label="商品名称">
            <el-input v-model="filters.product_name" clearable placeholder="请输入商品名称" @keyup.enter="loadProducts(1)" />
          </el-form-item>
          <el-form-item class="!mb-2 md:!mb-0">
            <el-button type="primary" :icon="Search" @click="loadProducts(1)">查询</el-button>
            <el-button @click="resetFilters">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </section>

    <!-- 数据列表部分 -->
    <section class="page-card flex-1 flex flex-col overflow-hidden">
      <div class="product-table-scroll flex-1 overflow-x-auto">
        <el-table v-loading="loading" class="product-table" :data="rows" stripe @selection-change="handleSelectionChange" :style="{ minWidth: totalTableWidth + 'px' }">
          <el-table-column type="selection" width="48" fixed="left" />
          <el-table-column
            v-if="visibleKeys.includes('image_url')"
            prop="image_url"
            label="图片"
            width="92"
            align="center"
            fixed="left"
          >
            <template #default="{ row }">
              <el-image
                v-if="resolveImageSrc(row.image_url)"
                :src="resolveImageSrc(row.image_url)"
                fit="cover"
                class="h-12 w-12 rounded-xl border border-slate-200/60 dark:border-slate-700/60"
                :preview-src-list="[resolveImageSrc(row.image_url)]"
                preview-teleported
              />
              <div
                v-else
                class="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 text-xs text-slate-500 dark:bg-slate-800 dark:text-slate-400"
              >
                无图
              </div>
            </template>
          </el-table-column>

          <!-- 固定列按照visibleKeys的顺序显示 -->
          <el-table-column
            v-for="key in visibleKeys.filter(k => ['style_code', 'product_code', 'product_name'].includes(k))"
            :key="key"
            :prop="key"
            :label="fields.find(f => f.key === key)?.label"
            :min-width="colMinWidth(key)"
            fixed="left"
            show-overflow-tooltip
          />

          <el-table-column
            v-for="key in visibleKeys.filter(k => k !== 'image_url' && !['style_code', 'product_code', 'product_name'].includes(k))"
            :key="key"
            :prop="key"
            :label="fields.find(f => f.key === key)?.label"
            :min-width="colMinWidth(key)"
            :fixed="fixedColumnPosition(key)"
            show-overflow-tooltip
          >
            <template v-if="key === 'stock_sync'" #default="{ row }">
              <el-tag :type="row.stock_sync ? 'success' : 'info'" effect="light">{{ row.stock_sync ? "同步" : "不同步" }}</el-tag>
            </template>
            <template v-else-if="isPriceField(key)" #default="{ row }">
              {{ formatMoney(row[key]) }}
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="mt-4 flex justify-end">
        <div class="rounded-2xl border border-slate-200/60 bg-white/90 px-3 py-2 shadow-lg backdrop-blur dark:border-slate-700/60 dark:bg-slate-950/80">
          <el-pagination
            background
            layout="total, prev, pager, next, sizes"
            :current-page="pagination.page"
            :page-size="pagination.page_size"
            :page-sizes="[10, 20, 50, 100]"
            :total="pagination.total"
            @current-change="loadProducts"
            @size-change="handleSizeChange"
          />
        </div>
      </div>
    </section>

    <el-drawer v-model="drawerVisible" title="列设置" size="420px">
      <div class="space-y-4">
        <div class="rounded-2xl border border-slate-200/60 p-4 dark:border-slate-700/60">
          <div class="flex items-center justify-between">
            <div class="text-sm font-semibold">显示字段</div>
            <div class="text-xs text-slate-500 dark:text-slate-400">{{ visibleKeys.length }}/{{ fields.length }}</div>
          </div>
          <el-divider class="!my-4" />
          <div class="mb-4">
            <div class="text-xs text-slate-500 dark:text-slate-400 mb-2">拖拽调整字段顺序</div>
            <draggable v-model="visibleKeys" item-key="key" class="space-y-2">
              <template #item="{ element }">
                <div class="flex items-center justify-between gap-2 p-2 hover:bg-slate-50 dark:hover:bg-slate-800/50 rounded">
                  <div class="flex items-center gap-2">
                    <el-icon class="cursor-move text-slate-400"><Menu /></el-icon>
                    <span>{{ fields.find(f => f.key === element)?.label }}</span>
                  </div>
                  <el-button 
                    type="text" 
                    size="small" 
                    @click.stop="removeField(element)"
                    class="text-red-500"
                  >
                    删除
                  </el-button>
                </div>
              </template>
            </draggable>
          </div>
          <div>
            <div class="text-xs text-slate-500 dark:text-slate-400 mb-2">可选字段</div>
            <el-checkbox-group v-model="visibleKeys" class="grid grid-cols-2 gap-2">
              <el-checkbox v-for="f in fields.filter(f => !visibleKeys.includes(f.key))" :key="f.key" :label="f.key">{{ f.label }}</el-checkbox>
            </el-checkbox-group>
          </div>
        </div>
        <div class="flex justify-end gap-3">
          <el-button @click="restoreDefaultColumns">恢复默认</el-button>
          <el-button type="primary" @click="saveColumns">保存</el-button>
        </div>
      </div>
    </el-drawer>

    <el-dialog v-model="createVisible" title="新增商品" width="780px">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-position="top">
        <div class="grid gap-4 md:grid-cols-2">
          <el-form-item label="图片" prop="image_url">
            <el-input v-model="createForm.image_url" placeholder="图片 URL（可选）" />
          </el-form-item>
          <el-form-item label="款式编码" prop="style_code">
            <el-input v-model="createForm.style_code" placeholder="必填" />
          </el-form-item>
          <el-form-item label="商品编码" prop="product_code">
            <el-input v-model="createForm.product_code" placeholder="必填" />
          </el-form-item>
          <el-form-item label="商品名称" prop="product_name" class="md:col-span-2">
            <el-input v-model="createForm.product_name" placeholder="必填" />
          </el-form-item>
          <el-form-item label="商品简称" prop="short_name">
            <el-input v-model="createForm.short_name" />
          </el-form-item>
          <el-form-item label="颜色及规格" prop="color_spec">
            <el-input v-model="createForm.color_spec" />
          </el-form-item>
          <el-form-item label="颜色" prop="color">
            <el-input v-model="createForm.color" />
          </el-form-item>
          <el-form-item label="规格" prop="spec">
            <el-input v-model="createForm.spec" />
          </el-form-item>
          <el-form-item label="基本售价" prop="base_price">
            <el-input-number v-model="createForm.base_price" class="w-full" :min="0" :precision="2" />
          </el-form-item>
          <el-form-item label="成本价" prop="cost_price">
            <el-input-number v-model="createForm.cost_price" class="w-full" :min="0" :precision="2" />
          </el-form-item>
          <el-form-item label="采购价" prop="purchase_price">
            <el-input-number v-model="createForm.purchase_price" class="w-full" :min="0" :precision="2" />
          </el-form-item>
          <el-form-item label="市场/吊牌价" prop="market_price">
            <el-input-number v-model="createForm.market_price" class="w-full" :min="0" :precision="2" />
          </el-form-item>
          <el-form-item label="品牌" prop="brand">
            <el-input v-model="createForm.brand" />
          </el-form-item>
          <el-form-item label="分类" prop="category">
            <el-input v-model="createForm.category" />
          </el-form-item>
          <el-form-item label="虚拟分类" prop="virtual_category">
            <el-input v-model="createForm.virtual_category" />
          </el-form-item>
          <el-form-item label="商品标签" prop="product_tags">
            <el-input v-model="createForm.product_tags" />
          </el-form-item>
          <el-form-item label="国标码" prop="gb_code">
            <el-input v-model="createForm.gb_code" />
          </el-form-item>
          <el-form-item label="供应商名称" prop="supplier_name">
            <el-input v-model="createForm.supplier_name" />
          </el-form-item>
          <el-form-item label="采购特征" prop="purchase_features">
            <el-input v-model="createForm.purchase_features" />
          </el-form-item>
          <el-form-item label="建议采购数" prop="suggested_purchase_qty">
            <el-input-number v-model="createForm.suggested_purchase_qty" class="w-full" :min="0" :precision="0" />
          </el-form-item>
          <el-form-item label="单位" prop="unit">
            <el-input v-model="createForm.unit" />
          </el-form-item>
          <el-form-item label="商品状态" prop="product_status">
            <el-select v-model="createForm.product_status" class="w-full">
              <el-option label="上架" value="上架" />
              <el-option label="下架" value="下架" />
              <el-option label="停用" value="停用" />
            </el-select>
          </el-form-item>
          <el-form-item label="库存同步" prop="stock_sync">
            <el-switch v-model="createForm.stock_sync" />
          </el-form-item>
          <el-form-item label="备注" prop="remark" class="md:col-span-2">
            <el-input v-model="createForm.remark" type="textarea" :rows="3" maxlength="500" show-word-limit />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <div class="flex justify-end gap-3">
          <el-button @click="createVisible = false">取消</el-button>
          <el-button type="primary" :loading="creating" @click="submitCreate">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { ElMessage, ElMessageBox } from "element-plus"
import { Delete, Download, Plus, Search, Setting, Menu } from "@element-plus/icons-vue"
import { batchDeleteProducts, createProduct, getProductFields, getProducts } from "@/api/business"
import draggable from "vuedraggable"

const loading = ref(false)
const rows = ref([])
const fields = ref([])
const defaultKeys = ref([])
const drawerVisible = ref(false)

const filters = reactive({
  style_code: "",
  product_code: "",
  product_name: ""
})

const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})

const STORAGE_KEY = "jinsyiyuan-product-list-columns"
const visibleKeys = ref([])

const dynamicColumns = computed(() =>
  visibleKeys.value
    .filter(key => key !== "image_url")
    .map(key => fields.value.find(f => f.key === key))
    .filter(Boolean)
)

const totalTableWidth = computed(() => {
  const selectionColWidth = 48 // el-table-column type="selection" width
  const imageColWidth = visibleKeys.value.includes("image_url") ? 92 : 0 // el-table-column for image_url width
  
  // 计算固定在左侧的列宽度
  const fixedLeftColsWidth = selectionColWidth + imageColWidth +
    (visibleKeys.value.includes("style_code") ? colMinWidth("style_code") : 0) +
    (visibleKeys.value.includes("product_code") ? colMinWidth("product_code") : 0) +
    (visibleKeys.value.includes("product_name") ? colMinWidth("product_name") : 0)

  // 计算动态列宽度，按照visibleKeys的顺序
  const dynamicColsWidth = visibleKeys.value
    .filter(key => key !== "image_url" && !['style_code', 'product_code', 'product_name'].includes(key))
    .reduce((sum, key) => sum + colMinWidth(key), 0)

  // Add a buffer for potential padding/borders/scrollbars
  return fixedLeftColsWidth + dynamicColsWidth + 20 // 20px buffer
})

const selectedIds = ref([])

function handleSelectionChange(selection) {
  selectedIds.value = selection.map((row) => row.id)
}

function normalizeImageUrl(value) {
  if (!value) {
    return ""
  }
  const raw = String(value).trim().replace(/^[`'"]+|[`'"]+$/g, "")
  if (!raw) {
    return ""
  }
  const candidates = raw.split(/[,\s|;]+/).map((item) => item.trim()).filter(Boolean)
  const firstUrl = candidates.find((item) => /^https?:\/\//i.test(item)) || candidates[0]
  if (!firstUrl) {
    return ""
  }
  if (firstUrl.startsWith("//")) {
    return `https:${firstUrl}`
  }
  return firstUrl
}

function resolveImageSrc(value) {
  const raw = normalizeImageUrl(value)
  if (!raw) {
    return ""
  }
  try {
    const url = new URL(raw)
    if (["images.sursung.com", "images-erp.sursung.com"].includes(url.host)) {
      return `/api/business/products/image-proxy/?url=${encodeURIComponent(raw)}`
    }
    return raw
  } catch {
    return raw
  }
}

function isPriceField(key) {
  return ["base_price", "cost_price", "purchase_price", "market_price"].includes(key)
}

function formatMoney(value) {
  const number = Number(value || 0)
  return `¥${number.toFixed(2)}`
}

function colMinWidth(key) {
  if (key === "product_name") {
    return 180
  }
  if (["style_code", "product_code", "short_name", "supplier_name"].includes(key)) {
    return 120
  }
  return 100
}

function fixedColumnPosition(key) {
  if (["style_code", "product_code", "product_name"].includes(key)) {
    return "left"
  }
  return undefined
}

async function loadFields() {
  const res = await getProductFields()
  fields.value = res.fields || []
  defaultKeys.value = res.default_keys || []

  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      if (Array.isArray(parsed) && parsed.length) {
        visibleKeys.value = parsed
        return
      }
    } catch (error) {
      localStorage.removeItem(STORAGE_KEY)
    }
  }
  visibleKeys.value = defaultKeys.value
}

async function loadProducts(page = pagination.page) {
  loading.value = true
  try {
    pagination.page = page
    const res = await getProducts({
      page: pagination.page,
      page_size: pagination.page_size,
      style_code: filters.style_code,
      product_code: filters.product_code,
      product_name: filters.product_name
    })
    rows.value = res.results || []
    pagination.total = res.total || 0
  } finally {
    loading.value = false
  }
}

function handleSizeChange(size) {
  pagination.page_size = size
  loadProducts(1)
}

function resetFilters() {
  filters.style_code = ""
  filters.product_code = ""
  filters.product_name = ""
  loadProducts(1)
}

function restoreDefaultColumns() {
  visibleKeys.value = defaultKeys.value
}

function removeField(key) {
  const index = visibleKeys.value.indexOf(key)
  if (index > -1) {
    visibleKeys.value.splice(index, 1)
  }
}

function saveColumns() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(visibleKeys.value))
  ElMessage.success("列设置已保存")
  drawerVisible.value = false
}

async function confirmDelete() {
  if (!selectedIds.value.length) {
    return
  }
  await ElMessageBox.confirm(`确认删除选中的 ${selectedIds.value.length} 条商品数据？`, "删除确认", {
    confirmButtonText: "删除",
    cancelButtonText: "取消",
    type: "warning"
  })
  await batchDeleteProducts(selectedIds.value)
  ElMessage.success("删除成功")
  selectedIds.value = []
  await loadProducts(1)
}

async function exportData(type) {
  ElMessage.info("正在生成导出文件，请稍候...")
  try {
    const params = {
      ...filters,
      export_type: type,
      columns: type === "visible" ? visibleKeys.value.join(",") : undefined
    }
    const response = await fetch(`/api/business/products/export/?${new URLSearchParams(params).toString()}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      }
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const blob = await response.blob()
    const contentDisposition = response.headers.get("Content-Disposition")
    let filename = `商品信息表_${new Date().getTime()}.xlsx`
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename\*?=['"]?(?:UTF-8''|.*?['"])([^"']+)$/i)
      if (filenameMatch && filenameMatch[1]) {
        filename = decodeURIComponent(filenameMatch[1])
      }
    }

    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
    ElMessage.success("导出成功")
  } catch (error) {
    console.error("导出失败:", error)
    ElMessage.error("导出失败，请稍后再试")
  }
}

const createVisible = ref(false)
const createFormRef = ref()
const creating = ref(false)
const createForm = reactive({
  image_url: "",
  style_code: "",
  product_code: "",
  product_name: "",
  short_name: "",
  color_spec: "",
  color: "",
  spec: "",
  base_price: 0,
  cost_price: 0,
  purchase_price: 0,
  market_price: 0,
  brand: "",
  category: "",
  virtual_category: "",
  product_tags: "",
  gb_code: "",
  supplier_name: "",
  purchase_features: "",
  suggested_purchase_qty: 0,
  unit: "",
  product_status: "上架",
  stock_sync: true,
  remark: ""
})

const createRules = {
  style_code: [{ required: true, message: "请输入款式编码", trigger: "blur" }],
  product_code: [{ required: true, message: "请输入商品编码", trigger: "blur" }],
  product_name: [{ required: true, message: "请输入商品名称", trigger: "blur" }]
}

function openCreate() {
  Object.assign(createForm, {
    image_url: "",
    style_code: "",
    product_code: "",
    product_name: "",
    short_name: "",
    color_spec: "",
    color: "",
    spec: "",
    base_price: 0,
    cost_price: 0,
    purchase_price: 0,
    market_price: 0,
    brand: "",
    category: "",
    virtual_category: "",
    product_tags: "",
    gb_code: "",
    supplier_name: "",
    purchase_features: "",
    suggested_purchase_qty: 0,
    unit: "",
    product_status: "上架",
    stock_sync: true,
    remark: ""
  })
  createVisible.value = true
}

async function submitCreate() {
  const valid = await createFormRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  creating.value = true
  try {
    await createProduct(createForm)
    ElMessage.success("新增成功")
    createVisible.value = false
    await loadProducts(1)
  } finally {
    creating.value = false
  }
}

onMounted(async () => {
  await loadFields()
  await loadProducts(1)
})
</script>

<style scoped>


.product-table-scroll {
  overflow-y: hidden;
  overscroll-behavior-x: contain;
}


</style>
