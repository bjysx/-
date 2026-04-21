<template>
  <div class="page-shell">
    <section class="page-card">
      <!-- 版本标记: v2-使用DoubleStarWorkflow组件 -->
      <!-- 品牌选择 -->
      <div class="mb-5">
        <div class="flex items-center gap-3">
          <span class="text-base font-semibold text-gray-700">品牌：</span>
          <div class="flex gap-1">
            <el-button :type="currentBrand === '全部' ? 'primary' : 'default'" round @click="selectBrand('全部')">全部</el-button>
            <el-button :type="currentBrand === '白牌' ? 'primary' : 'default'" round @click="selectBrand('白牌')">白牌</el-button>
            <el-button :type="currentBrand === '双星' ? 'primary' : 'default'" round @click="selectBrand('双星')">双星</el-button>
            <el-button :type="currentBrand === '雅鹿' ? 'primary' : 'default'" round @click="selectBrand('雅鹿')">雅鹿</el-button>
            <el-button :type="currentBrand === 'FKO' ? 'primary' : 'default'" round @click="selectBrand('FKO')">FKO</el-button>
          </div>
        </div>
      </div>

      <!-- 进度选择 - 对所有品牌显示 -->
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

      <!-- 筛选条件 - 对所有品牌显示 -->
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

      <!-- 全部待开发提示 -->
      <div v-if="currentBrand === '全部'" class="flex flex-col items-center justify-center py-20 text-gray-400">
        <el-icon :size="64" class="mb-4"><Collection /></el-icon>
        <span class="text-lg">待开发</span>
      </div>

      <!-- 所有品牌都使用白牌工作流内容 -->
      <div v-else>
        <el-table v-loading="loading" :data="workflows" stripe row-key="id">
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
                  <span v-if="row.merchandiser_images.length > 2" class="text-xs text-slate-400 flex items-center">+{{ row.merchandiser_images.length - 2 }}</span>
                </div>
                <span v-else class="text-xs text-slate-400">无图片</span>
                <el-button v-if="userInfo && userInfo.id && row.merchandiser === userInfo.id" type="primary" link size="small" @click="uploadMerchandiserImages(row)">上传</el-button>
              </div>
            </template>
          </el-table-column>
        </template>
        
        <!-- 样品对接和订单处理界面字段 -->
        <template v-if="filters.workflow_type !== 'production'">
          <!-- 图片 -->
          <el-table-column label="图片" width="100">
            <template #default="{ row }">
              <div v-if="row.images && row.images.length > 0" class="flex gap-1">
                <el-image
                  v-for="(img, index) in row.images.slice(0, 2)"
                  :key="index"
                  :src="img"
                  :preview-src-list="row.images"
                  :initial-index="index"
                  fit="cover"
                  class="w-10 h-10 rounded border cursor-pointer"
                />
                <span v-if="row.images.length > 2" class="text-xs text-slate-400 flex items-center">+{{ row.images.length - 2 }}</span>
              </div>
              <span v-else class="text-xs text-slate-400">无图片</span>
            </template>
          </el-table-column>
          <!-- 平台 -->
          <el-table-column label="平台" width="70">
            <template #default="{ row }">
              <span class="text-sm">{{ row.platform || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 性别 -->
          <el-table-column label="性别" width="50">
            <template #default="{ row }">
              <span class="text-sm">{{ row.gender || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 爆款数据展示 -->
          <el-table-column label="爆款数据" width="100">
            <template #default="{ row }">
              <span class="text-sm text-blue-600 truncate" :title="row.hot_sales_data">{{ row.hot_sales_data || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 爆款链接 -->
          <el-table-column label="爆款链接" width="120">
            <template #default="{ row }">
              <a v-if="row.product_link" :href="row.product_link" target="_blank" class="text-sm text-blue-500 hover:text-blue-700 underline truncate block" :title="row.product_link">链接</a>
              <span v-else class="text-sm text-slate-400">-</span>
            </template>
          </el-table-column>
          <!-- 销售量 -->
          <el-table-column label="销售量" width="70">
            <template #default="{ row }">
              <span class="text-sm">{{ row.sales_volume || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 上市时间 -->
          <el-table-column label="上市时间" width="90">
            <template #default="{ row }">
              <span class="text-sm">{{ row.launch_date || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 平台价格 -->
          <el-table-column label="平台价格" width="85">
            <template #default="{ row }">
              <span class="text-sm font-semibold text-orange-600">¥{{ row.platform_price || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 需求价格 -->
          <el-table-column label="需求价格" width="85">
            <template #default="{ row }">
              <span class="text-sm text-green-600">¥{{ row.demand_price || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 企划需求 -->
          <el-table-column label="企划需求" width="100">
            <template #default="{ row }">
              <span class="text-sm text-purple-600 truncate" :title="row.planning_requirements">{{ row.planning_requirements || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 底材 -->
          <el-table-column label="底材" width="70">
            <template #default="{ row }">
              <span class="text-sm">{{ row.sole_material || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 码段 -->
          <el-table-column label="码段" width="80">
            <template #default="{ row }">
              <span class="text-sm">{{ row.size_range || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 开发季节 -->
          <el-table-column label="开发季节" width="80">
            <template #default="{ row }">
              <span class="text-sm">{{ row.season || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 当前阶段 -->
          <el-table-column v-if="filters.workflow_type !== 'order'" label="当前阶段" width="90">
            <template #default="{ row }">
              <span class="text-sm font-medium text-blue-600">{{ getStageName(row.current_stage) }}</span>
            </template>
          </el-table-column>
          <!-- 申请人 -->
          <el-table-column v-if="filters.workflow_type !== 'order'" label="申请人" width="70">
            <template #default="{ row }">
              <span class="text-sm">{{ row.applicant_name || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 部门审批人 -->
          <el-table-column v-if="filters.workflow_type !== 'order'" label="部门审批人" width="90">
            <template #default="{ row }">
              <span class="text-sm">{{ row.approver_name || '-' }}</span>
            </template>
          </el-table-column>
          <!-- 申请时间 -->
          <el-table-column v-if="filters.workflow_type !== 'order'" label="申请时间" prop="application_time" width="130">
            <template #default="{ row }">
              <span class="text-xs text-slate-500">{{ formatDateTime(row.application_time) }}</span>
            </template>
          </el-table-column>
        </template>
        <el-table-column label="操作" width="160" fixed="right" align="center">
          <template #default="{ row }">
            <div class="flex items-center justify-center gap-1">
              <el-button type="primary" link size="small" @click="viewWorkflowDetail(row)">
                <el-icon><View /></el-icon>详情
              </el-button>
              <el-button v-if="row.status === 'pending'" type="success" link size="small" @click="submitWorkflow(row)">提交</el-button>
              <el-button v-if="userInfo && userInfo.id && row.merchandiser === userInfo.id" type="warning" link size="small" @click="openEliminateDialog(row)">淘汰</el-button>
              <el-button v-if="row.current_stage === '0'" type="danger" link size="small" @click="viewEliminateReason(row)">淘汰</el-button>
              <el-button v-if="filters.workflow_type === 'production'" type="success" link size="small" @click="stockIn(row)">入库</el-button>
              <el-popconfirm title="确定删除此工作流？" @confirm="deleteWorkflowItem(row)" confirm-button-text="确定" cancel-button-text="取消">
                <template #reference>
                  <el-button type="danger" link size="small">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 上传跟单图片对话框 -->
      <el-dialog v-model="merchandiserImageDialogVisible" title="上传跟单图片" width="500px">
        <div class="p-4">
          <el-upload
            action="#"
            :auto-upload="false"
            :multiple="true"
            :on-change="handleMerchandiserImageChange"
            :file-list="merchandiserImageFileList"
            :limit="6"
            :on-exceed="handleExceed"
            list-type="picture-card"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
          <p class="text-xs text-slate-500 mt-2">最多可上传6张图片</p>
        </div>
        <template #footer>
          <div class="flex justify-end gap-2">
            <el-button @click="merchandiserImageDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitMerchandiserImages">确认上传</el-button>
          </div>
        </template>
      </el-dialog>

      <div class="mt-5 flex justify-end">
        <el-pagination
          background
          layout="total, prev, pager, next, sizes"
          :current-page="pagination.page"
          :page-size="pagination.page_size"
          :page-sizes="[8, 12, 20, 30]"
          :total="pagination.total"
          @current-change="loadWorkflows"
          @size-change="handleSizeChange"
        />
      </div>
      </div>
    </section>

    <!-- 发起工作流对话框 -->
    <el-dialog v-model="createDialogVisible" title="发起工作流" width="800px">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-position="top">
        <div class="grid gap-4 md:grid-cols-2">
          <el-form-item label="性别" prop="gender">
            <el-select v-model="createForm.gender" class="w-full" placeholder="请选择性别">
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
              <el-option label="中性" value="中性" />
            </el-select>
          </el-form-item>
          <el-form-item label="上市时间" prop="launch_date">
            <el-date-picker v-model="createForm.launch_date" class="w-full" type="date" value-format="YYYY-MM-DD" placeholder="请选择上市时间" />
          </el-form-item>
          <el-form-item label="销售量" prop="sales_volume">
            <el-input-number v-model="createForm.sales_volume" class="w-full" :min="0" placeholder="请输入销售量" />
          </el-form-item>
          <el-form-item label="平台价格" prop="platform_price">
            <el-input-number v-model="createForm.platform_price" class="w-full" :precision="2" :min="0" placeholder="请输入平台价格" />
          </el-form-item>
          <el-form-item label="需求价格" prop="demand_price">
            <el-input-number v-model="createForm.demand_price" class="w-full" :precision="2" :min="0" placeholder="请输入需求价格" />
          </el-form-item>
          <el-form-item label="开发季节" prop="season">
            <el-select v-model="createForm.season" class="w-full" placeholder="请选择开发季节">
              <el-option label="春季" value="春季" />
              <el-option label="夏季" value="夏季" />
              <el-option label="秋季" value="秋季" />
              <el-option label="冬季" value="冬季" />
            </el-select>
          </el-form-item>
          <el-form-item label="运营姓名" prop="operation">
            <el-input v-model="createForm.operation" maxlength="100" placeholder="请输入运营姓名" />
          </el-form-item>
          <el-form-item label="平台（选填）" prop="platform">
            <el-select v-model="createForm.platform" class="w-full" clearable placeholder="请选择平台">
              <el-option label="淘宝" value="淘宝" />
              <el-option label="京东" value="京东" />
              <el-option label="拼多多" value="拼多多" />
              <el-option label="抖音" value="抖音" />
            </el-select>
          </el-form-item>
          <el-form-item label="底材（选填）" prop="sole_material">
            <el-input v-model="createForm.sole_material" maxlength="100" placeholder="请输入底材" />
          </el-form-item>
          <el-form-item label="码段（选填）" prop="size_range">
            <el-input v-model="createForm.size_range" maxlength="100" placeholder="请输入码段" />
          </el-form-item>
        </div>
        <el-form-item label="上传图片" prop="images">
          <el-upload
            class="upload-demo"
            action="/api/business/workflows/upload-image/"
            :headers="{ 'Authorization': `Bearer ${authStore.state.accessToken}` }"
            :on-success="handleImageSuccess"
            :on-error="handleImageError"
            :on-remove="handleImageRemove"
            :file-list="imageFileList"
            list-type="picture-card"
            multiple
            name="file"
          >
            <el-icon><Plus /></el-icon>
            <template #tip>
              <div class="el-upload__tip">支持上传多张图片</div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="爆款数据展示" prop="hot_sales_data">
          <el-input v-model="createForm.hot_sales_data" type="textarea" :rows="3" maxlength="500" show-word-limit placeholder="请输入爆款数据展示" />
        </el-form-item>
        <el-form-item label="爆款链接" prop="product_link">
          <el-input v-model="createForm.product_link" placeholder="请输入爆款链接" />
        </el-form-item>
        <el-form-item label="企划需求" prop="planning_requirements">
          <el-input v-model="createForm.planning_requirements" type="textarea" :rows="3" maxlength="500" show-word-limit placeholder="请输入企划需求" />
        </el-form-item>
        <el-form-item label="选择审批人" prop="approver">
          <el-select v-model="createForm.approver" class="w-full" placeholder="请选择审批人">
            <el-option v-for="user in users" :key="user.id" :label="user.nickname" :value="user.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitCreateForm">确定</el-button>
      </template>
    </el-dialog>

    <!-- 工作流详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="`工作流详情 - ${currentWorkflow?.product_name}`" width="800px">
      <div v-if="currentWorkflow" class="space-y-4">
        <div class="border-b pb-4">
          <h4 class="text-lg font-semibold mb-3">基本信息</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-slate-500">产品名称</p>
              <p class="font-medium">{{ currentWorkflow.product_name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">工作流类型</p>
              <p class="font-medium">{{ currentWorkflow.workflow_type === 'sample' ? '样品对接' : currentWorkflow.workflow_type }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">状态</p>
              <el-tag :type="currentWorkflow.current_stage === '0' ? statusTypeMap.eliminated : (statusTypeMap[currentWorkflow.status] || 'info')" effect="light">
                {{ currentWorkflow.current_stage === '0' ? statusTextMap.eliminated : (statusTextMap[currentWorkflow.status] || currentWorkflow.status) }}
              </el-tag>
            </div>
            <div>
              <p class="text-sm text-slate-500">当前阶段</p>
              <p class="font-medium">{{ getStageName(currentWorkflow.current_stage) }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">进度</p>
              <el-progress :percentage="currentWorkflow.progress" :stroke-width="8" />
            </div>
            <div>
              <p class="text-sm text-slate-500">申请时间</p>
              <p class="font-medium">{{ formatDateTime(currentWorkflow.application_time) }}</p>
            </div>
          </div>
        </div>

        <div v-if="currentWorkflow.workflow_type !== 'order'" class="border-b pb-4">
          <h4 class="text-lg font-semibold mb-3">产品信息</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-slate-500">产品名称</p>
              <p class="font-medium">{{ currentWorkflow.product_name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">性别</p>
              <p class="font-medium">{{ currentWorkflow.gender || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">开发季节</p>
              <p class="font-medium">{{ currentWorkflow.season || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">上市时间</p>
              <p class="font-medium">{{ currentWorkflow.launch_date || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">平台价格</p>
              <p class="font-medium">¥{{ currentWorkflow.platform_price || '0.00' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">需求价格</p>
              <p class="font-medium">¥{{ currentWorkflow.demand_price || '0.00' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">销售量</p>
              <p class="font-medium">{{ currentWorkflow.sales_volume || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">运营姓名</p>
              <p class="font-medium">{{ currentWorkflow.operation || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">平台</p>
              <p class="font-medium">{{ currentWorkflow.platform || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">底材</p>
              <p class="font-medium">{{ currentWorkflow.sole_material || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">码段</p>
              <p class="font-medium">{{ currentWorkflow.size_range || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">提出需求时间</p>
              <p class="font-medium">{{ formatDate(currentWorkflow.demand_time) }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">爆款数据展示</p>
              <p class="font-medium">{{ currentWorkflow.hot_sales_data || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">爆款链接</p>
              <a v-if="currentWorkflow.product_link" :href="currentWorkflow.product_link" target="_blank" class="text-blue-500 hover:underline">
                {{ currentWorkflow.product_link }}
              </a>
              <span v-else>-</span>
            </div>
            <div>
              <p class="text-sm text-slate-500">企划需求</p>
              <p class="font-medium">{{ currentWorkflow.planning_requirements || '-' }}</p>
            </div>
          </div>
          <div class="mt-4">
            <p class="text-sm text-slate-500">上传图片</p>
            <div class="flex flex-wrap gap-2 mt-2">
              <el-image
                v-for="(image, index) in currentWorkflow.images || []"
                :key="index"
                :src="image.startsWith('http') ? image : `/api${image}`"
                fit="cover"
                class="w-24 h-24 object-cover rounded"
                :preview-src-list="(currentWorkflow.images || []).map(img => img.startsWith('http') ? img : `/api${img}`)"
                :initial-index="index"
                preview-teleported
              />
              <span v-if="!currentWorkflow.images || currentWorkflow.images.length === 0">-</span>
            </div>
          </div>
        </div>

        <!-- ========== 以下部分已注释，工作流进度可以代替 ==========
        审批信息 -->
        <!-- <div v-if="currentWorkflow.current_stage >= 2" class="border-b pb-4">
          <h4 class="text-lg font-semibold mb-3">审批信息</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-slate-500">审批人</p>
              <p class="font-medium">{{ currentWorkflow.approver_name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">审批时间</p>
              <p class="font-medium">{{ formatDate(currentWorkflow.approval_time) }}</p>
            </div>
            <div class="col-span-2">
              <p class="text-sm text-slate-500">审批意见</p>
              <p class="font-medium">{{ currentWorkflow.approval_comments || '-' }}</p>
            </div>
          </div>
        </div>

        <div v-if="currentWorkflow.current_stage >= 3" class="border-b pb-4">
          <h4 class="text-lg font-semibold mb-3">供应商信息</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-slate-500">供应商</p>
              <p class="font-medium">{{ currentWorkflow.supplier || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">跟单员</p>
              <p class="font-medium">{{ currentWorkflow.merchandiser_name || '-' }}</p>
            </div>
          </div>
        </div>

        <div v-if="currentWorkflow.current_stage >= 5" class="border-b pb-4">
          <h4 class="text-lg font-semibold mb-3">样品单信息</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-slate-500">样品单号</p>
              <p class="font-medium">{{ currentWorkflow.sample_order_number || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">下单时间</p>
              <p class="font-medium">{{ formatDate(currentWorkflow.sample_order_time) }}</p>
            </div>
          </div>
        </div>

        <div v-if="currentWorkflow.current_stage >= 6" class="border-b pb-4">
          <h4 class="text-lg font-semibold mb-3">业务人员审核</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-slate-500">业务人员</p>
              <p class="font-medium">{{ currentWorkflow.salesperson_name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">审核时间</p>
              <p class="font-medium">{{ formatDate(currentWorkflow.salesperson_approval_time) }}</p>
            </div>
            <div class="col-span-2">
              <p class="text-sm text-slate-500">审核意见</p>
              <p class="font-medium">{{ currentWorkflow.salesperson_comments || '-' }}</p>
            </div>
          </div>
        </div>

        <div v-if="currentWorkflow.current_stage >= 7" class="border-b pb-4">
          <h4 class="text-lg font-semibold mb-3">运营人员审核</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-slate-500">运营人员</p>
              <p class="font-medium">{{ currentWorkflow.operator_name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">审核时间</p>
              <p class="font-medium">{{ formatDate(currentWorkflow.operator_approval_time) }}</p>
            </div>
            <div class="col-span-2">
              <p class="text-sm text-slate-500">审核意见</p>
              <p class="font-medium">{{ currentWorkflow.operator_comments || '-' }}</p>
            </div>
          </div>
        </div>

        <div v-if="currentWorkflow.current_stage >= 9 || currentWorkflow.photographer_approval_time" class="border-b pb-4">
          <h4 class="text-lg font-semibold mb-3">摄影师审核</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-slate-500">摄影师</p>
              <p class="font-medium">{{ currentWorkflow.photographer_name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">审核时间</p>
              <p class="font-medium">{{ formatDate(currentWorkflow.photographer_approval_time) }}</p>
            </div>
            <div class="col-span-2">
              <p class="text-sm text-slate-500">审核意见</p>
              <p class="font-medium">{{ currentWorkflow.photographer_comments || '-' }}</p>
            </div>
          </div>
        </div>

        <div v-if="currentWorkflow.current_stage >= 10 || currentWorkflow.clerk_approval_time" class="border-b pb-4">
          <h4 class="text-lg font-semibold mb-3">文员审核</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-slate-500">文员</p>
              <p class="font-medium">{{ currentWorkflow.clerk_name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-500">审核时间</p>
              <p class="font-medium">{{ formatDate(currentWorkflow.clerk_approval_time) }}</p>
            </div>
            <div class="col-span-2">
              <p class="text-sm text-slate-500">审核意见</p>
              <p class="font-medium">{{ currentWorkflow.clerk_comments || '-' }}</p>
            </div>
          </div>
        </div>
        ========== 以上部分已注释 ========== -->



        <div class="mt-6">
          <h4 class="text-lg font-semibold mb-4">工作流进度</h4>
          
          <!-- 进度时间线 -->
          <div class="relative">
            <!-- 订单处理工作流 -->
            <template v-if="currentWorkflow.workflow_type === 'order'">
              <!-- 步骤1: 电子订单制作 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.order_stage >= 1 || currentWorkflow.order_created ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.order_stage >= 1 || currentWorkflow.order_created ? '✓' : '1' }}
                  </div>
                  <div v-if="currentWorkflow.order_stage >= 1" class="w-0.5 h-12 bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-12 bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">电子订单制作</span>
                    <el-tag :type="currentWorkflow.order_stage >= 1 || currentWorkflow.order_created ? 'success' : 'info'" size="small">
                      {{ currentWorkflow.order_stage >= 1 || currentWorkflow.order_created ? '已完成' : '待文员处理' }}
                    </el-tag>
                  </div>
                  <p class="text-sm text-slate-500">文员：{{ currentWorkflow.clerk_name || '-' }}</p>
                  <div v-if="currentWorkflow && userInfo && userInfo.id && currentWorkflow.clerk === userInfo.id && (currentWorkflow.order_stage === 0 || !currentWorkflow.order_created)" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="createElectronicOrder(currentWorkflow)">
                      {{ currentWorkflow.order_created ? '修改订单' : '制作订单' }}
                    </el-button>
                  </div>
                  <!-- 显示电子订单数据 -->
                  <div v-if="currentWorkflow.order_stage >= 1 || currentWorkflow.order_created" class="mt-4">
                    <div class="bg-gray-50 p-4 rounded-lg">
                      <h5 class="text-sm font-semibold mb-2">电子订单详情</h5>
                      <div class="grid grid-cols-2 gap-2 mb-2">
                        <div>
                          <p class="text-xs text-slate-500">仓储方</p>
                          <p class="text-sm">{{ currentWorkflow.order_warehouse || '-' }}</p>
                        </div>
                        <div>
                          <p class="text-xs text-slate-500">跟单</p>
                          <p class="text-sm">{{ currentWorkflow.merchandiser_name || '-' }}</p>
                        </div>
                      </div>
                      <div v-if="currentWorkflow.order_items && currentWorkflow.order_items.length > 0" class="overflow-x-auto">
                        <table class="w-full border-collapse text-sm">
                          <thead>
                            <tr class="bg-gray-100">
                              <th class="border p-1 text-center">工厂款号</th>
                              <th class="border p-1 text-center">颜色</th>
                              <th class="border p-1 text-center">侧标</th>
                              <th class="border p-1 text-center">后柱织带</th>
                              <th class="border p-1 text-center">里子布</th>
                              <th class="border p-1 text-center">底材</th>
                              <th class="border p-1 text-center">商品编码</th>
                              <th class="border p-1 text-center">尺码</th>
                              <th class="border p-1 text-center">箱数</th>
                              <th class="border p-1 text-center">双数</th>
                              <th class="border p-1 text-center">总数</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(item, index) in currentWorkflow.order_items" :key="index" class="hover:bg-gray-50">
                              <td class="border p-1 text-center">{{ item.factory_style_number || '-' }}</td>
                              <td class="border p-1 text-center">{{ item.color || '-' }}</td>
                              <td class="border p-1 text-center">{{ item.side_label || '-' }}</td>
                              <td class="border p-1 text-center">{{ item.back_column_webbing || '-' }}</td>
                              <td class="border p-1 text-center">{{ item.lining_cloth || '-' }}</td>
                              <td class="border p-1 text-center">{{ item.bottom_material || '-' }}</td>
                              <td class="border p-1 text-center">{{ item.product_code || '-' }}</td>
                              <td class="border p-1 text-center">{{ item.size || '-' }}</td>
                              <td class="border p-1 text-center">{{ item.box_count || '-' }}</td>
                              <td class="border p-1 text-center">{{ item.pair_count || '-' }}</td>
                              <td class="border p-1 text-center">{{ item.total_count || '-' }}</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 步骤2: 业务审核材质 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.order_stage >= 2 ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.order_stage >= 2 ? '✓' : '2' }}
                  </div>
                  <div v-if="currentWorkflow.order_stage >= 2" class="w-0.5 h-12 bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-12 bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">业务审核材质</span>
                    <el-tag :type="currentWorkflow.order_stage >= 2 ? 'success' : 'info'" size="small">
                      {{ currentWorkflow.order_stage >= 2 ? '已完成' : '待业务处理' }}
                    </el-tag>
                  </div>
                  <p class="text-sm text-slate-500">业务人员：{{ currentWorkflow.salesperson_name || '-' }}</p>
                  <div v-if="currentWorkflow && userInfo && userInfo.id && currentWorkflow.salesperson === userInfo.id && currentWorkflow.order_stage === 1" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="approveOrderMaterial(currentWorkflow)">审核材质</el-button>
                    <el-button type="danger" size="small" @click="rejectOrderMaterial(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤3: 运营审核数据价格 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.order_stage >= 3 ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.order_stage >= 3 ? '✓' : '3' }}
                  </div>
                  <div v-if="currentWorkflow.order_stage >= 3" class="w-0.5 h-12 bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-12 bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">运营审核数据价格</span>
                    <el-tag :type="currentWorkflow.order_stage >= 3 ? 'success' : 'info'" size="small">
                      {{ currentWorkflow.order_stage >= 3 ? '已完成' : '待运营处理' }}
                    </el-tag>
                  </div>
                  <p class="text-sm text-slate-500">运营人员：{{ currentWorkflow.operator_name || '-' }}</p>
                  <div v-if="currentWorkflow && userInfo && userInfo.id && currentWorkflow.operator === userInfo.id && currentWorkflow.order_stage === 2" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="approveOrderDataPrice(currentWorkflow)">审核数据价格</el-button>
                    <el-button type="danger" size="small" @click="rejectOrderDataPrice(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤4: 运营部门领导审核数据价格 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.order_stage >= 4 ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.order_stage >= 4 ? '✓' : '4' }}
                  </div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">运营部门领导审核数据价格</span>
                    <el-tag :type="currentWorkflow.order_stage >= 4 ? 'success' : 'info'" size="small">
                      {{ currentWorkflow.order_stage >= 4 ? '已完成' : '待运营部门领导处理' }}
                    </el-tag>
                  </div>
                  <p class="text-sm text-slate-500">运营部门领导：{{ currentWorkflow.operator_leader_name || '-' }}</p>
                  <div v-if="currentWorkflow && userInfo && userInfo.id && currentWorkflow.operator_leader === userInfo.id && currentWorkflow.order_stage === 3" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="approveOrderDataPriceByLeader(currentWorkflow)">审核数据价格</el-button>
                    <el-button type="danger" size="small" @click="rejectOrderDataPriceByLeader(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>
            </template>
            
            <!-- 样品对接工作流 -->
            <template v-else>
              <!-- 步骤1: 提交申请 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.status !== 'pending' ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.status !== 'pending' ? '✓' : '1' }}
                  </div>
                  <div v-if="currentWorkflow.current_stage > 0" class="w-0.5 h-full bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-full bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">提交申请</span>
                    <el-tag :type="currentWorkflow.status !== 'pending' ? 'success' : 'info'" size="small">
                      {{ currentWorkflow.status !== 'pending' ? '已完成' : '待申请人处理' }}
                    </el-tag>
                  </div>
                  <p class="text-sm text-slate-500">申请人：{{ currentWorkflow.applicant_name || '-' }}</p>
                  <p v-if="currentWorkflow.application_time" class="text-xs text-slate-400 mt-1">{{ formatDateTime(currentWorkflow.application_time) }}</p>
                  <div v-if="currentWorkflow && currentWorkflow.status === 'pending' && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.applicant === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="submitWorkflow(currentWorkflow)">提交</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤2: 审批 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.current_stage >= 2 ? 'bg-green-500 text-white' : currentWorkflow.current_stage === 1 ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.current_stage >= 2 ? '✓' : currentWorkflow.current_stage === 1 ? '●' : '2' }}
                  </div>
                  <div v-if="currentWorkflow.current_stage > 2 || currentWorkflow.progress === 100" class="w-0.5 h-full bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-full bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">部门领导审批</span>
                    <el-tag :type="getStageStatusType(1)" size="small">{{ getStageStatusText(1) }}</el-tag>
                  </div>
                  <p class="text-sm text-slate-500">审批人：{{ currentWorkflow.approver_name || (currentWorkflow.current_stage >= 1 ? currentWorkflow.approver_name : '-') }}</p>
                  <p v-if="currentWorkflow.approval_time" class="text-xs text-slate-400 mt-1">{{ formatDateTime(currentWorkflow.approval_time) }}</p>
                  <div v-if="currentWorkflow && currentWorkflow.status === 'in_progress' && currentWorkflow.current_stage === 1 && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.approver === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="approveWorkflow(currentWorkflow)">部门领导审批</el-button>
                    <el-button type="danger" size="small" @click="rejectWorkflow(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤3: 选择供应商 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.current_stage >= 3 ? 'bg-green-500 text-white' : currentWorkflow.current_stage === 2 ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.current_stage >= 3 ? '✓' : currentWorkflow.current_stage === 2 ? '●' : '3' }}
                  </div>
                  <div v-if="currentWorkflow.current_stage > 3" class="w-0.5 h-full bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-full bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">选择供应商</span>
                    <el-tag :type="getStageStatusType(2)" size="small">{{ getStageStatusText(2) }}</el-tag>
                  </div>
                  <p class="text-sm text-slate-500">供应商：{{ currentWorkflow.supplier || '-' }}</p>
                  <p v-if="currentWorkflow.comments" class="text-sm text-slate-500 mt-1">跟单备注：{{ currentWorkflow.comments }}</p>
                  <div v-if="currentWorkflow && currentWorkflow.status === 'in_progress' && currentWorkflow.current_stage === 2 && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.approver === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="selectSupplier(currentWorkflow)">选择供应商</el-button>
                    <el-button type="danger" size="small" @click="rejectWorkflow(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤4: 确认跟单进度 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.current_stage >= 4 ? 'bg-green-500 text-white' : currentWorkflow.current_stage === 3 ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.current_stage >= 4 ? '✓' : currentWorkflow.current_stage === 3 ? '●' : '4' }}
                  </div>
                  <div v-if="currentWorkflow.current_stage > 4" class="w-0.5 h-full bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-full bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">确认跟单进度</span>
                    <el-tag :type="getStageStatusType(3)" size="small">{{ getStageStatusText(3) }}</el-tag>
                  </div>
                  <p class="text-sm text-slate-500">跟单员：{{ currentWorkflow.merchandiser_name || '-' }}</p>
                  <!-- 显示跟单进度记录（只显示有数据的行） -->
                  <div v-if="currentWorkflow.merchandiser_progress_records && currentWorkflow.merchandiser_progress_records.filter(r => r.progress || r.remark).length > 0" class="mt-2">
                    <p class="text-xs text-slate-400 mb-1">跟单进度记录：</p>
                    <div v-for="(record, idx) in currentWorkflow.merchandiser_progress_records.filter(r => r.progress || r.remark)" :key="idx" class="text-xs text-slate-500 mb-1">
                      {{ record.time }} - {{ record.progress }} - {{ record.remark }} - {{ record.completed ? '已完成' : '进行中' }}
                    </div>
                  </div>
                  <div v-if="currentWorkflow && currentWorkflow.status === 'in_progress' && currentWorkflow.current_stage === 3 && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.merchandiser === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="openMerchandiserProgressDialog(currentWorkflow)">更新跟单进度</el-button>
                    <el-button type="success" size="small" @click="openApproveDialog(currentWorkflow, 'confirm_logo', '完成跟单进度并选择业务员')">完成</el-button>
                    <el-button type="danger" size="small" @click="rejectWorkflow(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤5: 样品送至业务 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.current_stage >= 5 ? 'bg-green-500 text-white' : currentWorkflow.current_stage === 4 ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.current_stage >= 5 ? '✓' : currentWorkflow.current_stage === 4 ? '●' : '5' }}
                  </div>
                  <div v-if="currentWorkflow.current_stage > 5" class="w-0.5 h-full bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-full bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">样品送至业务</span>
                    <el-tag :type="getStageStatusType(4)" size="small">{{ getStageStatusText(4) }}</el-tag>
                  </div>
                  <p class="text-sm text-slate-500">跟单员：{{ currentWorkflow.merchandiser_name || '-' }}</p>
                  <p v-if="currentWorkflow.sample_delivery_comments" class="text-xs text-slate-400 mt-1">备注：{{ currentWorkflow.sample_delivery_comments }}</p>
                  <div v-if="currentWorkflow && currentWorkflow.status === 'in_progress' && currentWorkflow.current_stage === 4 && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.merchandiser === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="placeSampleOrder(currentWorkflow)">确认样品送达</el-button>
                    <el-button type="danger" size="small" @click="rejectWorkflow(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤6: 首色对接-审核材质 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.current_stage >= 6 ? 'bg-green-500 text-white' : currentWorkflow.current_stage === 5 ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.current_stage >= 6 ? '✓' : currentWorkflow.current_stage === 5 ? '●' : '6' }}
                  </div>
                  <div v-if="currentWorkflow.current_stage > 6" class="w-0.5 h-full bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-full bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">首色对接-审核材质</span>
                    <el-tag :type="getStageStatusType(5)" size="small">{{ getStageStatusText(5) }}</el-tag>
                  </div>
                  <p class="text-sm text-slate-500">业务员：{{ currentWorkflow.salesperson_name || '-' }}</p>
                  <p v-if="currentWorkflow.salesperson_approval_time" class="text-xs text-slate-400 mt-1">{{ formatDateTime(currentWorkflow.salesperson_approval_time) }}</p>
                  <p v-if="currentWorkflow.salesperson_comments" class="text-xs text-slate-400 mt-1">备注：{{ currentWorkflow.salesperson_comments }}</p>
                  <div v-if="currentWorkflow && currentWorkflow.status === 'in_progress' && currentWorkflow.current_stage === 5 && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.salesperson === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="salespersonApprove(currentWorkflow)">业务人员审核材质</el-button>
                    <el-button type="danger" size="small" @click="rejectWorkflow(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤7: 首色对接-运营审核数据价格 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.current_stage >= 7 ? 'bg-green-500 text-white' : currentWorkflow.current_stage === 6 ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.current_stage >= 7 ? '✓' : currentWorkflow.current_stage === 6 ? '●' : '7' }}
                  </div>
                  <div v-if="currentWorkflow.current_stage > 7" class="w-0.5 h-full bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-full bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">首色对接-运营审核数据价格</span>
                    <el-tag :type="getStageStatusType(6)" size="small">{{ getStageStatusText(6) }}</el-tag>
                  </div>
                  <p class="text-sm text-slate-500">运营人员：{{ currentWorkflow.operator_name || '-' }}</p>
                  <p v-if="currentWorkflow.operator_approval_time" class="text-xs text-slate-400 mt-1">{{ formatDateTime(currentWorkflow.operator_approval_time) }}</p>
                  <p v-if="currentWorkflow.operator_comments" class="text-xs text-slate-400 mt-1">备注：{{ currentWorkflow.operator_comments }}</p>
                  <div v-if="currentWorkflow && currentWorkflow.status === 'in_progress' && currentWorkflow.current_stage === 6 && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.operator === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="operatorApprove(currentWorkflow)">确认数据价格</el-button>
                    <el-button type="danger" size="small" @click="rejectWorkflow(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤8: 全色对接-业务审核材质 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.current_stage >= 8 ? 'bg-green-500 text-white' : currentWorkflow.current_stage === 7 ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.current_stage >= 8 ? '✓' : currentWorkflow.current_stage === 7 ? '●' : '8' }}
                  </div>
                  <div v-if="currentWorkflow.current_stage > 8" class="w-0.5 h-full bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-full bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">全色对接-业务审核材质</span>
                    <el-tag :type="getStageStatusType(7)" size="small">{{ getStageStatusText(7) }}</el-tag>
                  </div>
                  <p class="text-sm text-slate-500">业务员：{{ currentWorkflow.salesperson_name || '-' }}</p>
                  <p v-if="currentWorkflow.salesperson_comments" class="text-xs text-slate-400 mt-1">备注：{{ currentWorkflow.salesperson_comments }}</p>
                  <div v-if="currentWorkflow && currentWorkflow.status === 'in_progress' && currentWorkflow.current_stage === 7 && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.salesperson === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="salespersonApproveFullColor(currentWorkflow)">全色确认材质</el-button>
                    <el-button type="danger" size="small" @click="rejectWorkflow(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤9: 全色对接-运营审核数据价格 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.current_stage >= 9 ? 'bg-green-500 text-white' : currentWorkflow.current_stage === 8 ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.current_stage >= 9 ? '✓' : currentWorkflow.current_stage === 8 ? '●' : '9' }}
                  </div>
                  <div v-if="currentWorkflow.current_stage > 9" class="w-0.5 h-full bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-full bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">全色对接-运营审核数据价格</span>
                    <el-tag :type="getStageStatusType(8)" size="small">{{ getStageStatusText(8) }}</el-tag>
                  </div>
                  <p class="text-sm text-slate-500">运营人员：{{ currentWorkflow.operator_name || '-' }}</p>
                  <p v-if="currentWorkflow.operator_comments" class="text-xs text-slate-400 mt-1">备注：{{ currentWorkflow.operator_comments }}</p>
                  <div v-if="currentWorkflow && currentWorkflow.status === 'in_progress' && currentWorkflow.current_stage === 8 && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.operator === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="operatorApproveFullColor(currentWorkflow)">全色确认数据价格</el-button>
                    <el-button type="danger" size="small" @click="rejectWorkflow(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤10: 摄影师审核 -->
              <div class="flex gap-4 pb-6 border-b">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.current_stage >= 10 || currentWorkflow.photographer_approval_time ? 'bg-green-500 text-white' : currentWorkflow.current_stage === 9 ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.current_stage >= 10 || currentWorkflow.photographer_approval_time ? '✓' : currentWorkflow.current_stage === 9 ? '●' : '10' }}
                  </div>
                  <div v-if="currentWorkflow.progress === 99 || currentWorkflow.progress === 100" class="w-0.5 h-full bg-green-500 mt-2"></div>
                  <div v-else class="w-0.5 h-full bg-gray-200 mt-2"></div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">摄影师上传白底</span>
                    <el-tag :type="getStageStatusType(9)" size="small">{{ getStageStatusText(9) }}</el-tag>
                  </div>
                  <p class="text-sm text-slate-500">摄影师：{{ currentWorkflow.photographer_name || '-' }}</p>
                  <p v-if="currentWorkflow.photographer_approval_time" class="text-xs text-slate-400 mt-1">{{ formatDateTime(currentWorkflow.photographer_approval_time) }}</p>
                  <p v-if="currentWorkflow.photographer_comments" class="text-xs text-slate-400 mt-1">备注：{{ currentWorkflow.photographer_comments }}</p>
                  <div v-if="currentWorkflow.white_background_images && currentWorkflow.white_background_images.length > 0" class="mt-2">
                    <p class="text-xs text-slate-400 mb-1">白底图片：</p>
                    <div class="flex flex-wrap gap-2">
                      <el-image
                        v-for="(img, index) in currentWorkflow.white_background_images"
                        :key="index"
                        :src="img"
                        :preview-src-list="currentWorkflow.white_background_images"
                        :initial-index="index"
                        fit="cover"
                        class="w-16 h-16 rounded border"
                      />
                    </div>
                  </div>
                  <div v-if="currentWorkflow && currentWorkflow.status === 'in_progress' && currentWorkflow.current_stage === 9 && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.photographer === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="photographerApprove(currentWorkflow)">摄影师上传白底</el-button>
                    <el-button type="danger" size="small" @click="rejectWorkflow(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>

              <!-- 步骤11: 文员审核 -->
              <div class="flex gap-4 pb-6">
                <div class="flex flex-col items-center">
                  <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium', currentWorkflow.progress === 100 || currentWorkflow.clerk_approval_time ? 'bg-green-500 text-white' : currentWorkflow.progress === 99 ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500']">
                    {{ currentWorkflow.progress === 100 || currentWorkflow.clerk_approval_time ? '✓' : currentWorkflow.progress === 99 ? '●' : '11' }}
                  </div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium">文员审核白底</span>
                    <el-tag :type="currentWorkflow.progress === 100 || currentWorkflow.clerk_approval_time ? 'success' : currentWorkflow.progress === 99 ? 'warning' : 'info'" size="small">
                      {{ currentWorkflow.progress === 100 || currentWorkflow.clerk_approval_time ? '已完成' : currentWorkflow.progress === 99 ? '进行中' : '待文员处理' }}
                    </el-tag>
                  </div>
                  <p class="text-sm text-slate-500">文员：{{ currentWorkflow.clerk_name || '-' }}</p>
                  <p v-if="currentWorkflow.clerk_approval_time" class="text-xs text-slate-400 mt-1">{{ formatDateTime(currentWorkflow.clerk_approval_time) }}</p>
                  <div v-if="currentWorkflow && currentWorkflow.progress === 99 && currentWorkflow.current_stage !== 'eliminated' && userInfo && userInfo.id && currentWorkflow.clerk === userInfo.id" class="mt-3 flex gap-2">
                    <el-button type="primary" size="small" @click="clerkApprove(currentWorkflow)">文员审核白底</el-button>
                    <el-button type="danger" size="small" @click="rejectWorkflow(currentWorkflow)">拒绝</el-button>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>


      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 审批对话框 -->
    <el-dialog v-model="approveDialogVisible" :title="approveDialogTitle" width="500px">
      <el-form ref="approveFormRef" :model="approveForm" :rules="approveRules" label-position="top">
        <el-form-item v-if="approveDialogType === 'select_supplier'" label="选择供应商" prop="supplier">
          <el-select v-model="approveForm.supplier" class="w-full">
            <el-option v-for="supplier in suppliers" :key="supplier.id" :label="supplier.supplier_name" :value="supplier.supplier_name" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'place_sample_order'" label="选择业务人员" prop="salesperson">
          <el-select v-model="approveForm.salesperson" class="w-full">
            <el-option v-for="user in users" :key="user.id" :label="user.username" :value="user.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'place_sample_order'" label="备注（选填）">
          <el-input v-model="approveForm.comments" type="textarea" :rows="3" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'salesperson_approve'" label="请选择运营人员审核数据价格" prop="operator">
          <el-select v-model="approveForm.operator" class="w-full">
            <el-option v-for="user in users" :key="user.id" :label="user.username" :value="user.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'salesperson_approve'" label="备注（选填）">
          <el-input v-model="approveForm.comments" type="textarea" :rows="3" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'operator_approve'" label="确认样品数据价格无误">
          <p class="text-sm text-slate-600">请确认样品的数据价格信息是否正确</p>
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'operator_approve'" label="备注（选填）">
          <el-input v-model="approveForm.comments" type="textarea" :rows="3" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'salesperson_approve_full_color'" label="确认全色材质无误">
          <p class="text-sm text-slate-600">请确认全色材质信息是否正确</p>
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'salesperson_approve_full_color'" label="备注（选填）">
          <el-input v-model="approveForm.comments" type="textarea" :rows="3" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'operator_approve_full_color'" label="确认全色数据价格无误">
          <p class="text-sm text-slate-600">请确认全色的数据价格信息是否正确</p>
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'operator_approve_full_color'" label="备注（选填）">
          <el-input v-model="approveForm.comments" type="textarea" :rows="3" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'operator_approve_full_color'" label="选择摄影师" prop="photographer">
          <el-select v-model="approveForm.photographer" class="w-full">
            <el-option v-for="user in users" :key="user.id" :label="user.username" :value="user.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'photographer_approve'" label="上传白底图片">
          <el-upload
            :action="uploadUrl"
            :headers="uploadHeaders"
            :on-success="handleWhiteImageSuccess"
            :on-remove="handleWhiteImageRemove"
            :file-list="whiteImageFileList"
            list-type="picture-card"
            accept="image/*"
            multiple
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'photographer_approve'" label="选择文员" prop="clerk">
          <el-select v-model="approveForm.clerk" class="w-full">
            <el-option v-for="user in users" :key="user.id" :label="user.username" :value="user.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'photographer_approve'" label="备注（选填）">
          <el-input v-model="approveForm.comments" type="textarea" :rows="3" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'select_supplier'" label="跟单备注">
          <el-input v-model="approveForm.comments" type="textarea" :rows="3" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'confirm_logo'" label="选择业务人员" prop="salesperson">
          <el-select v-model="approveForm.salesperson" class="w-full">
            <el-option v-for="user in users" :key="user.id" :label="user.username" :value="user.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="approveDialogType === 'confirm_logo'" label="备注（选填）">
          <el-input v-model="approveForm.comments" type="textarea" :rows="3" maxlength="500" show-word-limit />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="flex justify-end gap-3">
          <el-button @click="approveDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitting" @click="submitApproveForm">确认</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 淘汰对话框 -->
    <el-dialog v-model="eliminateDialogVisible" title="淘汰产品" width="500px">
      <el-form ref="eliminateFormRef" :model="eliminateForm" :rules="eliminateRules" label-position="top">
        <el-form-item label="淘汰原因" prop="eliminate_reason">
          <el-input v-model="eliminateForm.eliminate_reason" type="textarea" :rows="4" maxlength="500" show-word-limit />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="flex justify-end gap-3">
          <el-button @click="eliminateDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitting" @click="submitEliminateForm">确认</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 淘汰原因查看对话框 -->
    <el-dialog v-model="eliminateReasonDialogVisible" title="淘汰原因" width="500px">
      <div class="p-4">
        <p class="text-sm text-slate-500">淘汰时间：{{ formatDateTime(eliminateForm.eliminate_time) }}</p>
        <p class="text-sm text-slate-500 mt-2">淘汰人：{{ eliminateForm.eliminator_name }}</p>
        <p class="text-sm text-slate-500 mt-2">淘汰原因：</p>
        <p class="mt-2 p-3 bg-gray-50 rounded">
          {{ eliminateForm.eliminate_reason }}
        </p>
      </div>
      <template #footer>
        <div class="flex justify-end">
          <el-button @click="eliminateReasonDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 跟单进度更新对话框 -->
    <el-dialog v-model="merchandiserProgressDialogVisible" title="更新跟单进度" width="700px">
      <div class="p-4">
        <el-table :data="merchandiserProgressForm.records" border>
          <el-table-column label="跟单进度" width="200">
            <template #default="{ row }">
              <el-input v-model="row.progress" placeholder="请输入进度" />
            </template>
          </el-table-column>
          <el-table-column label="备注" width="250">
            <template #default="{ row }">
              <el-input v-model="row.remark" placeholder="请输入备注" />
            </template>
          </el-table-column>
          <el-table-column label="是否完成" width="100" align="center">
            <template #default="{ row }">
              <el-checkbox v-model="row.completed" />
            </template>
          </el-table-column>
          <el-table-column label="更新时间" width="150">
            <template #default="{ row }">
              <span class="text-xs text-slate-500">{{ row.time || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80" align="center">
            <template #default="{ $index }">
              <el-button type="danger" link size="small" @click="removeProgressRecord($index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="mt-3">
          <el-button type="primary" size="small" @click="addProgressRecord">
            <el-icon><Plus /></el-icon>添加行
          </el-button>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <el-button @click="merchandiserProgressDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitting" @click="submitMerchandiserProgress">确认</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 电子订单制作对话框 -->
    <el-dialog v-model="electronicOrderDialogVisible" title="电子订单制作" width="800px">
      <div class="p-4">
        <div class="bg-green-50 p-4 rounded-lg mb-4">
          <h4 class="text-center font-semibold text-green-700">新款生产订单</h4>
          <p class="text-center text-sm text-slate-500 mt-1">图片仅做参考，细节与跟单确定</p>
        </div>
        
        <div class="grid grid-cols-4 gap-4 mb-4">
          <div>
            <p class="text-sm text-slate-500">跟单</p>
            <p class="font-medium">{{ currentWorkflow?.merchandiser_name || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-slate-500">下单日期</p>
            <p class="font-medium">{{ formatDate(new Date()) }}</p>
          </div>
          <div>
            <p class="text-sm text-slate-500">供应商</p>
            <p class="font-medium">{{ currentWorkflow?.supplier || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-slate-500">仓储方</p>
            <el-input v-model="warehouse" placeholder="请输入仓储方" class="w-full" />
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="border p-2 text-center">工厂款号/图片</th>
                <th class="border p-2 text-center">颜色</th>
                <th class="border p-2 text-center">侧标</th>
                <th class="border p-2 text-center">后柱织带</th>
                <th class="border p-2 text-center">里子布</th>
                <th class="border p-2 text-center">底材</th>
                <th class="border p-2 text-center">商品编码</th>
                <th class="border p-2 text-center">尺码</th>
                <th class="border p-2 text-center">箱数</th>
                <th class="border p-2 text-center">双数</th>
                <th class="border p-2 text-center">总数</th>
                <th class="border p-2 text-center">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in orderItems" :key="index" class="hover:bg-gray-50">
                <td class="border p-2">
                  <div class="flex items-center gap-2">
                    <el-upload
                      action="/api/business/workflows/upload-image/"
                      :headers="{ 'Authorization': `Bearer ${authStore.state.accessToken}` }"
                      :on-success="(response) => handleOrderImageSuccess(response, index)"
                      class="w-12 h-12 border-dashed border-2 border-slate-300 rounded flex items-center justify-center cursor-pointer"
                      accept="image/*"
                    >
                      <el-image v-if="item.image" :src="item.image" fit="cover" class="w-12 h-12 rounded" />
                      <el-icon v-else><Plus /></el-icon>
                    </el-upload>
                    <el-input v-model="item.factory_style_number" placeholder="工厂款号" class="w-32" />
                  </div>
                </td>
                <td class="border p-2">
                  <div class="w-full">
                    <el-input v-model="item.color" placeholder="颜色" class="w-full" :round="false" :clearable="true" />
                  </div>
                </td>
                <td class="border p-2">
                  <div class="w-full">
                    <el-input v-model="item.side_label" placeholder="侧标" class="w-full" :round="false" :clearable="true" />
                  </div>
                </td>
                <td class="border p-2">
                  <div class="w-full">
                    <el-input v-model="item.back_column_webbing" placeholder="后柱织带" class="w-full" :round="false" :clearable="true" />
                  </div>
                </td>
                <td class="border p-2">
                  <div class="w-full">
                    <el-input v-model="item.lining_cloth" placeholder="里子布" class="w-full" :round="false" :clearable="true" />
                  </div>
                </td>
                <td class="border p-2">
                  <div class="w-full">
                    <el-input v-model="item.bottom_material" placeholder="底材" class="w-full" :round="false" :clearable="true" />
                  </div>
                </td>
                <td class="border p-2">
                  <div class="w-full">
                    <el-input v-model="item.product_code" placeholder="商品编码" class="w-full" :round="false" :clearable="true" />
                  </div>
                </td>
                <td class="border p-2">
                  <div class="w-full">
                    <el-input v-model="item.size" placeholder="尺码" class="w-full" :round="false" :clearable="true" />
                  </div>
                </td>
                <td class="border p-2"><el-input-number v-model="item.box_count" :min="0" placeholder="箱数" /></td>
                <td class="border p-2"><el-input-number v-model="item.pair_count" :min="0" placeholder="双数" /></td>
                <td class="border p-2"><el-input-number v-model="item.total_count" :min="0" placeholder="总数" /></td>
                <td class="border p-2 text-center">
                  <el-button type="primary" link size="small" @click="copyOrderItem(index)">新增</el-button>
                  <el-button type="danger" link size="small" @click="removeOrderItem(index)">删除</el-button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="mt-4 flex justify-center">
          <el-button type="primary" @click="addOrderItem">
            <el-icon><Plus /></el-icon>增加工厂款号/图片
          </el-button>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <el-button @click="electronicOrderDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitting" @click="submitElectronicOrder">确认制作</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { ElMessage, ElMessageBox } from "element-plus"
import { Download, Plus, Refresh, View } from "@element-plus/icons-vue"
import { formatDate, formatDateTime } from "@/utils/formatters"
import { getUsers } from "@/api/system"
import { getWorkflows, getWorkflowDetail, createWorkflow, updateWorkflowStatus, deleteWorkflow, uploadWorkflowImage, getSupplierMerchandisers } from "@/api/business"
import { useAuthStore } from "@/store/auth"
import DoubleStarWorkflow from "./DoubleStarWorkflowView.vue"

const authStore = useAuthStore()
const userInfo = computed(() => authStore.state.user)

const props = defineProps({
  sectionTitle: { type: String, default: "商品中心" },
  pageTitle: { type: String, default: "白牌" }
})

const createFormRef = ref()
const approveFormRef = ref()
const createDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const approveDialogVisible = ref(false)
const loading = ref(false)
const submitting = ref(false)
const workflows = ref([])
const users = ref([])
const suppliers = ref([])
const currentWorkflow = ref(null)
const approveDialogTitle = ref("")
const approveDialogType = ref("")
const imageFileList = ref([])
const whiteImageFileList = ref([])
const uploadUrl = "/api/business/workflows/upload-image/"
const uploadHeaders = computed(() => ({ 'Authorization': `Bearer ${authStore.state.accessToken}` }))
const currentBrand = ref("白牌")
const filters = reactive({ q: "", status: "", workflow_type: "sample", merchandiser: null, platform: null, development_rhythm: null })
const pagination = reactive({ page: 1, page_size: 8, total: 0 })
const eliminateDialogVisible = ref(false)
const eliminateReasonDialogVisible = ref(false)
const eliminateFormRef = ref()
const eliminateForm = reactive({
  workflow_id: "",
  eliminate_reason: "",
  eliminate_time: null,
  eliminator_name: ""
})

// 跟单进度相关
const merchandiserProgressDialogVisible = ref(false)
const merchandiserProgressFormRef = ref()
const merchandiserProgressForm = reactive({
  records: [
    { progress: '', remark: '', completed: false, time: '' },
    { progress: '', remark: '', completed: false, time: '' }
  ]
})

// 电子订单相关
const electronicOrderDialogVisible = ref(false)
const warehouse = ref("")
const orderItems = ref([
  {
    factory_style_number: "",
    image: "",
    color: "",
    side_label: "",
    back_column_webbing: "",
    lining_cloth: "",
    bottom_material: "",
    product_code: "",
    size: "",
    box_count: 0,
    pair_count: 0,
    total_count: 0
  }
])

// 跟单上传图片相关
const merchandiserImageDialogVisible = ref(false)
const merchandiserImageFileList = ref([])
const currentMerchandiserWorkflow = ref(null)
const eliminateRules = reactive({
  eliminate_reason: [{ required: true, message: "请输入淘汰原因", trigger: "blur" }]
})
const createForm = reactive({
  product_name: "",
  images: [],
  hot_sales_data: "",
  product_link: "",
  gender: "",
  launch_date: "",
  sales_volume: null,
  platform_price: null,
  demand_price: null,
  season: "",
  operation: "",
  platform: "",
  sole_material: "",
  size_range: "",
  planning_requirements: "",
  approver: ""
})
const approveForm = reactive({
  supplier: "",
  sample_order_number: "",
  salesperson: "",
  operator: "",
  photographer: "",
  clerk: "",
  comments: "",
  white_background_images: []
})
const createRules = {
  product_name: [{ required: true, message: "请输入产品名称", trigger: "blur" }],
  gender: [{ required: true, message: "请选择性别", trigger: "change" }],
  launch_date: [{ required: true, message: "请选择上市时间", trigger: "change" }],
  sales_volume: [{ required: true, message: "请输入销售量", trigger: "blur" }],
  platform_price: [{ required: true, message: "请输入平台价格", trigger: "blur" }],
  demand_price: [{ required: true, message: "请输入需求价格", trigger: "blur" }],
  season: [{ required: true, message: "请选择开发季节", trigger: "change" }],
  operation: [{ required: true, message: "请输入运营姓名", trigger: "blur" }],
  hot_sales_data: [{ required: true, message: "请输入爆款数据展示", trigger: "blur" }],
  product_link: [{ required: true, message: "请输入爆款链接", trigger: "blur" }],
  planning_requirements: [{ required: true, message: "请输入企划需求", trigger: "blur" }],
  approver: [{ required: true, message: "请选择审批人", trigger: "change" }]
}
const approveRules = {
  supplier: [{ required: true, message: "请选择供应商", trigger: "change" }],
  salesperson: [{ required: true, message: "请选择业务人员", trigger: "change" }],
  operator: [{ required: true, message: "请选择运营人员", trigger: "change" }],
  photographer: [{ required: true, message: "请选择摄影师", trigger: "change" }],
  clerk: [{ required: true, message: "请选择文员", trigger: "change" }]
}
const statusTypeMap = { pending: "info", in_progress: "warning", completed: "success", rejected: "danger", eliminated: "danger" }
const statusTextMap = { pending: "待处理", in_progress: "进行中", completed: "已完成", rejected: "已拒绝", eliminated: "已淘汰" }

function handleImageSuccess(response, file, fileList) {
  if (response.success) {
    createForm.images.push(response.data.url)
    imageFileList.value = fileList
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error(response.message || '图片上传失败')
  }
}

function handleImageError(error) {
  ElMessage.error('图片上传失败')
  console.error('Upload error:', error)
}

function handleImageRemove(file, fileList) {
  if (file.response && file.response.success) {
    const url = file.response.data.url
    createForm.images = createForm.images.filter(img => img !== url)
  }
  imageFileList.value = fileList
}

function handleWhiteImageSuccess(response, file, fileList) {
  if (response.success) {
    if (!approveForm.white_background_images) {
      approveForm.white_background_images = []
    }
    approveForm.white_background_images.push(response.data.url)
    whiteImageFileList.value = fileList
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error(response.message || '图片上传失败')
  }
}

function handleWhiteImageRemove(file, fileList) {
  if (file.response && file.response.success) {
    const url = file.response.data.url
    if (approveForm.white_background_images) {
      approveForm.white_background_images = approveForm.white_background_images.filter(img => img !== url)
    }
  }
  whiteImageFileList.value = fileList
}

async function loadUsers() {
  try {
    const response = await getUsers()
    // 过滤出position包含"主管"的用户
    users.value = response.filter(user => user.position && user.position.includes("主管"))
  } catch (error) {
    ElMessage.error("获取用户列表失败")
  }
}

async function loadSuppliers() {
  try {
    const response = await getSupplierMerchandisers()
    suppliers.value = response
  } catch (error) {
    ElMessage.error("获取供应商列表失败")
  }
}

async function selectBrand(brand) {
  currentBrand.value = brand
  console.log('【调试】选择品牌:', brand, 'currentBrand:', currentBrand.value, '时间:', Date.now())
  
  // 全部品牌显示待开发
  if (brand === '全部') {
    ElMessage.info('待开发')
    workflows.value = []
    pagination.total = 0
    return
  }
  
  // 跨境品牌参数映射
  const brandMap = {
    '白牌': 'cross_border_white_label',
    '双星': 'cross_border_double_star',
    '雅鹿': 'cross_border_yalu',
    'FKO': 'cross_border_fko'
  }
  const brandParam = brandMap[brand] || 'cross_border_white_label'
  console.log('selectBrand - brandParam:', brandParam)
  
  loading.value = true
  try {
    const response = await getWorkflows({
      page: 1,
      page_size: pagination.page_size,
      q: filters.q,
      status: filters.status,
      brand: brandParam,
      workflow_type: filters.workflow_type,
      merchandiser: filters.merchandiser,
      platform: filters.platform,
      development_rhythm: filters.development_rhythm
    })
    console.log('工作流数据:', response.results)
    workflows.value = response.results
    pagination.total = response.total
    pagination.page = 1
  } finally {
    loading.value = false
  }
}

function selectWorkflowType(type) {
  filters.workflow_type = type
  loadWorkflows(1)
}

async function loadWorkflows(page = pagination.page) {
  loading.value = true
  try {
    pagination.page = page
    // 跨境品牌参数映射
    const brandMap = {
      '白牌': 'cross_border_white_label',
      '双星': 'cross_border_double_star',
      '雅鹿': 'cross_border_yalu',
      'FKO': 'cross_border_fko'
    }
    const brandParam = brandMap[currentBrand.value] || 'cross_border_white_label'
    console.log('loadWorkflows - currentBrand:', currentBrand.value, 'brandParam:', brandParam)
    const response = await getWorkflows({
      page: pagination.page,
      page_size: pagination.page_size,
      q: filters.q,
      status: filters.status,
      brand: brandParam,
      workflow_type: filters.workflow_type,
      merchandiser: filters.merchandiser,
      platform: filters.platform,
      development_rhythm: filters.development_rhythm
    })
    console.log('工作流数据:', response.results)
    workflows.value = response.results
    pagination.total = response.total
  } finally {
    loading.value = false
  }
}

function resetFilters() {
  filters.q = ""
  filters.status = ""
  filters.workflow_type = "sample"
  filters.merchandiser = null
  filters.platform = null
  filters.development_rhythm = null
  loadWorkflows(1)
}

function handleSizeChange(size) {
  pagination.page_size = size
  loadWorkflows(1)
}

function openCreateWorkflowDialog() {
  // 重置表单
  Object.assign(createForm, {
    product_name: "",
    demand_time: "",
    images: [],
    hot_sales_data: "",
    product_link: "",
    gender: "",
    required_days: null,
    countdown: null,
    full_color_demand_time: "",
    development_rhythm: "",
    season: "",
    operation: "",
    product_selling_points: "",
    product_improvement_points: "",
    meeting_suggestions: "",
    approver: ""
  })
  imageFileList.value = []
  createDialogVisible.value = true
}

async function submitCreateForm() {
  const valid = await createFormRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  submitting.value = true
  try {
    // 跨境品牌参数映射
    const brandMap = {
      '白牌': 'cross_border_white_label',
      '双星': 'cross_border_double_star',
      '雅鹿': 'cross_border_yalu',
      'FKO': 'cross_border_fko'
    }
    const brand = brandMap[currentBrand.value] || 'cross_border_white_label'
    await createWorkflow({ ...createForm, brand })
    ElMessage.success("工作流创建成功")
    createDialogVisible.value = false
    await loadWorkflows(1)
  } finally {
    submitting.value = false
  }
}

async function viewWorkflowDetail(row) {
  // 重新获取最新的工作流数据
  try {
    const response = await getWorkflowDetail(row.id)
    // 如果当前是订单处理界面，强制设置workflow_type为order
    if (filters.workflow_type === 'order') {
      response.workflow_type = 'order'
    }
    currentWorkflow.value = response
  } catch (error) {
    // 如果当前是订单处理界面，强制设置workflow_type为order
    if (filters.workflow_type === 'order') {
      row.workflow_type = 'order'
    }
    currentWorkflow.value = row
  }
  console.log('查看工作流详情:', currentWorkflow.value)
  console.log('当前用户信息:', userInfo.value)
  console.log('是否显示更新跟单进度按钮:', currentWorkflow.value && currentWorkflow.value.status === 'in_progress' && currentWorkflow.value.current_stage === 3 && userInfo.value && userInfo.value.id && currentWorkflow.value.merchandiser === userInfo.value.id)
  detailDialogVisible.value = true
}

async function submitWorkflow(workflow) {
  try {
    await updateWorkflowStatus(workflow.id, { action: "submit" })
    ElMessage.success("工作流提交成功")
    await loadWorkflows(pagination.page)
    if (detailDialogVisible.value) {
      currentWorkflow.value = { ...workflow, status: "in_progress" }
    }
  } catch (error) {
    ElMessage.error("工作流提交失败")
  }
}

async function deleteWorkflowItem(workflow) {
  try {
    await deleteWorkflow(workflow.id)
    ElMessage.success("工作流删除成功")
    await loadWorkflows(pagination.page)
  } catch (error) {
    ElMessage.error("工作流删除失败")
  }
}

function getStageStatusType(stage) {
  const workflow = currentWorkflow.value
  if (!workflow) return 'info'
  
  if (workflow.current_stage === 'eliminated') return 'danger'
  
  // 特殊处理某些阶段
  if (stage === 9 && workflow.photographer_approval_time) return 'success'
  if (stage === 9 && workflow.current_stage === 9) return 'warning'
  
  if (workflow.current_stage > stage + 1) return 'success'
  if (workflow.current_stage === stage + 1) return 'warning'
  return 'info'
}

function getStageStatusText(stage) {
  const workflow = currentWorkflow.value
  if (!workflow) return '待处理'
  
  if (workflow.current_stage === 'eliminated') return '已淘汰'
  
  // 特殊处理某些阶段
  if (stage === 9 && workflow.photographer_approval_time) return '已完成'
  if (stage === 9 && workflow.current_stage === 9) return '进行中'
  
  if (workflow.current_stage > stage + 1) return '已完成'
  if (workflow.current_stage === stage + 1) return '进行中'
  
  // 根据不同阶段显示待谁处理
  const stageHandlers = {
    0: '申请人',
    1: '部门领导',
    2: '部门领导',
    3: '跟单员',
    4: '跟单员',
    5: '业务员',
    6: '运营人员',
    7: '业务员',
    8: '运营人员',
    9: '摄影师',
    10: '文员'
  }
  
  return `待${stageHandlers[stage] || '处理人'}处理`
}

function getStageName(currentStage) {
  if (currentStage === '0') {
    return '淘汰'
  }
  const stageNames = {
    0: '待提交',
    1: '部门领导审批',
    2: '选择供应商',
    3: '确认跟单进度',
    4: '样品送至业务',
    5: '首色对接-审核材质',
    6: '首色对接-运营审核数据价格',
    7: '全色对接-业务审核材质',
    8: '全色对接-运营审核数据价格',
    9: '摄影师上传白底',
    10: '文员审核白底',
    11: '样品对接完成'
  }
  return stageNames[currentStage] || currentStage
}

function getProgressColor(percentage) {
  if (percentage >= 100) return '#67C23A'
  if (percentage >= 80) return '#E6A23C'
  if (percentage >= 50) return '#409EFF'
  if (percentage > 0) return '#909399'
  return '#F56C6C'
}

function getWorkflowStages(workflow) {
  const stages = [
    { name: '提交', status: workflow.status !== 'pending' ? 'completed' : 'pending', handler: workflow.applicant_name },
    { name: '部门领导审批', status: workflow.current_stage >= 2 ? 'completed' : workflow.current_stage === 1 ? 'current' : 'pending', handler: workflow.approver_name },
    { name: '选供应商', status: workflow.current_stage >= 3 ? 'completed' : workflow.current_stage === 2 ? 'current' : 'pending', handler: workflow.supplier || '-' },
    { name: '确认跟单进度', status: workflow.current_stage >= 4 ? 'completed' : workflow.current_stage === 3 ? 'current' : 'pending', handler: workflow.merchandiser_name },
    { name: '样品送至业务', status: workflow.current_stage >= 5 ? 'completed' : workflow.current_stage === 4 ? 'current' : 'pending', handler: workflow.merchandiser_name },
    { name: '首色对接-审核材质', status: workflow.current_stage >= 6 ? 'completed' : workflow.current_stage === 5 ? 'current' : 'pending', handler: workflow.salesperson_name },
    { name: '首色对接-运营审核数据价格', status: workflow.current_stage >= 7 ? 'completed' : workflow.current_stage === 6 ? 'current' : 'pending', handler: workflow.operator_name },
    { name: '全色对接-业务审核材质', status: workflow.current_stage >= 8 ? 'completed' : workflow.current_stage === 7 ? 'current' : 'pending', handler: workflow.salesperson_name },
    { name: '全色对接-运营审核数据价格', status: workflow.current_stage >= 9 ? 'completed' : workflow.current_stage === 8 ? 'current' : 'pending', handler: workflow.operator_name },
    { name: '摄影师上传白底', status: workflow.current_stage >= 10 || workflow.photographer_approval_time ? 'completed' : workflow.current_stage === 9 ? 'current' : 'pending', handler: workflow.photographer_name },
    { name: '文员审核白底', status: workflow.progress === 100 || workflow.clerk_approval_time ? 'completed' : workflow.progress === 99 ? 'current' : 'pending', handler: workflow.clerk_name }
  ]
  return stages
}

function openApproveDialog(workflow, type, title) {
  currentWorkflow.value = workflow
  approveDialogType.value = type
  approveDialogTitle.value = title
  // 重置表单
  Object.assign(approveForm, {
    supplier: "",
    sample_order_number: "",
    salesperson: "",
    operator: "",
    photographer: "",
    clerk: "",
    comments: "",
    white_background_images: []
  })
  whiteImageFileList.value = []
  approveDialogVisible.value = true
}

async function submitApproveForm() {
  const valid = await approveFormRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  submitting.value = true
  try {
    // 根据对话框类型确定 action
    let action = approveDialogType.value
    if (approveDialogType.value === "confirm_logo") {
      action = "complete_merchandiser_progress"
    }
    await updateWorkflowStatus(currentWorkflow.value.id, {
      action: action,
      ...approveForm
    })
    ElMessage.success("操作成功")
    approveDialogVisible.value = false
    await loadWorkflows(pagination.page)
    detailDialogVisible.value = false
  } finally {
    submitting.value = false
  }
}

function approveWorkflow(workflow) {
  openApproveDialog(workflow, "approve", "审批工作流")
}

function selectSupplier(workflow) {
  openApproveDialog(workflow, "select_supplier", "选择供应商")
}

function confirmLogo(workflow) {
  openApproveDialog(workflow, "confirm_logo", "完成跟单进度并选择业务员")
}

function placeSampleOrder(workflow) {
  openApproveDialog(workflow, "place_sample_order", "确认样品送达")
}

function salespersonApprove(workflow) {
  openApproveDialog(workflow, "salesperson_approve", "业务人员审核材质")
}

function operatorApprove(workflow) {
  openApproveDialog(workflow, "operator_approve", "确认数据价格")
}

function salespersonApproveFullColor(workflow) {
  openApproveDialog(workflow, "salesperson_approve_full_color", "全色确认材质")
}

function operatorApproveFullColor(workflow) {
  openApproveDialog(workflow, "operator_approve_full_color", "全色确认数据价格")
}

function photographerApprove(workflow) {
  openApproveDialog(workflow, "photographer_approve", "摄影师审核")
}

function clerkApprove(workflow) {
  openApproveDialog(workflow, "clerk_approve", "文员审核")
}

function openEliminateDialog(workflow) {
  eliminateForm.workflow_id = workflow.id
  eliminateForm.eliminate_reason = workflow.eliminate_reason || ''
  eliminateDialogVisible.value = true
}

async function submitEliminateForm() {
  const valid = await eliminateFormRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  submitting.value = true
  try {
    const response = await updateWorkflowStatus(eliminateForm.workflow_id, {
      action: 'eliminate',
      eliminate_reason: eliminateForm.eliminate_reason
    })
    console.log('淘汰接口返回:', response)
    ElMessage.success('淘汰成功')
    eliminateDialogVisible.value = false
    await loadWorkflows(pagination.page)
    detailDialogVisible.value = false
  } catch (error) {
    console.error('淘汰操作失败:', error)
    ElMessage.error('淘汰失败')
  } finally {
    submitting.value = false
  }
}

function viewEliminateReason(workflow) {
  eliminateForm.workflow_id = workflow.id
  eliminateForm.eliminate_reason = workflow.eliminate_reason || ''
  eliminateForm.eliminate_time = workflow.eliminate_time
  eliminateForm.eliminator_name = workflow.eliminator_name || ''
  eliminateReasonDialogVisible.value = true
}

// 电子订单相关方法
function createElectronicOrder(workflow) {
  currentWorkflow.value = workflow
  // 如果有现有订单数据，使用现有数据，否则使用空数据
  if (workflow.order_items && workflow.order_items.length > 0) {
    orderItems.value = [...workflow.order_items]
  } else {
    orderItems.value = [
      {
        factory_style_number: "",
        image: "",
        color: "",
        side_label: "",
        back_column_webbing: "",
        lining_cloth: "",
        bottom_material: "",
        product_code: "",
        size: "",
        box_count: 0,
        pair_count: 0,
        total_count: 0
      }
    ]
  }
  // 如果有现有仓储方数据，使用现有数据
  if (workflow.order_warehouse) {
    warehouse.value = workflow.order_warehouse
  } else {
    warehouse.value = ""
  }
  electronicOrderDialogVisible.value = true
}

function addOrderItem() {
  orderItems.value.push({
    factory_style_number: "",
    image: "",
    color: "",
    side_label: "",
    back_column_webbing: "",
    lining_cloth: "",
    bottom_material: "",
    product_code: "",
    size: "",
    box_count: 0,
    pair_count: 0,
    total_count: 0
  })
}

function removeOrderItem(index) {
  orderItems.value.splice(index, 1)
}

function copyOrderItem(index) {
  const item = orderItems.value[index]
  orderItems.value.splice(index + 1, 0, { ...item })
}

function handleOrderImageSuccess(response, index) {
  if (response.success) {
    orderItems.value[index].image = response.data.url
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error(response.message || '图片上传失败')
  }
}

async function submitElectronicOrder() {
  if (orderItems.value.length === 0) {
    ElMessage.error('请至少添加一个订单条目')
    return
  }
  
  submitting.value = true
  try {
    await updateWorkflowStatus(currentWorkflow.value.id, {
      action: 'create_electronic_order',
      warehouse: warehouse.value,
      order_items: orderItems.value
    })
    ElMessage.success('电子订单制作成功')
    electronicOrderDialogVisible.value = false
    await loadWorkflows(pagination.page)
    detailDialogVisible.value = false
  } catch (error) {
    ElMessage.error('电子订单制作失败')
  } finally {
    submitting.value = false
  }
}

async function rejectWorkflow(workflow) {
  await ElMessageBox.confirm("确认拒绝该工作流吗？", "拒绝确认", { type: "warning" })
  try {
    await updateWorkflowStatus(workflow.id, { action: "reject" })
    ElMessage.success("工作流已拒绝")
    await loadWorkflows(pagination.page)
    if (detailDialogVisible.value) {
      currentWorkflow.value = { ...workflow, status: "rejected" }
    }
  } catch (error) {
    ElMessage.error("拒绝失败")
  }
}

// 订单处理工作流相关方法
async function approveOrderMaterial(workflow) {
  try {
    await updateWorkflowStatus(workflow.id, { action: 'approve_order_material' })
    ElMessage.success('业务审核材质成功')
    await loadWorkflows(pagination.page)
    if (detailDialogVisible.value) {
      currentWorkflow.value = { ...workflow, order_stage: 2 }
    }
  } catch (error) {
    ElMessage.error('业务审核材质失败')
  }
}

async function approveOrderDataPrice(workflow) {
  // 弹出对话框选择部门领导人
  const { value: operatorLeaderId } = await ElMessageBox.prompt(
    '请选择部门领导人',
    '选择部门领导人',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      inputType: 'select',
      inputOptions: userOptions.value.map(user => ({
        label: user.username,
        value: user.id
      })),
      inputPlaceholder: '请选择部门领导人'
    }
  )
  
  if (!operatorLeaderId) {
    ElMessage.warning('请选择部门领导人')
    return
  }
  
  try {
    await updateWorkflowStatus(workflow.id, { 
      action: 'approve_order_data_price',
      operator_leader: operatorLeaderId
    })
    ElMessage.success('运营审核数据价格成功')
    await loadWorkflows(pagination.page)
    if (detailDialogVisible.value) {
      currentWorkflow.value = { ...workflow, order_stage: 3, operator_leader: operatorLeaderId }
    }
  } catch (error) {
    ElMessage.error('运营审核数据价格失败')
  }
}

async function approveOrderDataPriceByLeader(workflow) {
  try {
    await updateWorkflowStatus(workflow.id, { action: 'approve_order_data_price_by_leader' })
    ElMessage.success('运营部门领导审核数据价格成功')
    await loadWorkflows(pagination.page)
    if (detailDialogVisible.value) {
      currentWorkflow.value = { ...workflow, order_stage: 4 }
    }
  } catch (error) {
    ElMessage.error('运营部门领导审核数据价格失败')
  }
}

// 订单处理工作流拒绝方法
async function rejectOrderMaterial(workflow) {
  await ElMessageBox.confirm('确认拒绝该审核吗？', '拒绝确认', { type: 'warning' })
  try {
    await updateWorkflowStatus(workflow.id, { action: 'reject_order_material' })
    ElMessage.success('业务审核材质已拒绝')
    await loadWorkflows(pagination.page)
    if (detailDialogVisible.value) {
      currentWorkflow.value = { ...workflow, order_stage: 0 }
    }
  } catch (error) {
    ElMessage.error('拒绝失败')
  }
}

async function rejectOrderDataPrice(workflow) {
  await ElMessageBox.confirm('确认拒绝该审核吗？', '拒绝确认', { type: 'warning' })
  try {
    await updateWorkflowStatus(workflow.id, { action: 'reject_order_data_price' })
    ElMessage.success('运营审核数据价格已拒绝')
    await loadWorkflows(pagination.page)
    if (detailDialogVisible.value) {
      currentWorkflow.value = { ...workflow, order_stage: 1 }
    }
  } catch (error) {
    ElMessage.error('拒绝失败')
  }
}

async function rejectOrderDataPriceByLeader(workflow) {
  await ElMessageBox.confirm('确认拒绝该审核吗？', '拒绝确认', { type: 'warning' })
  try {
    await updateWorkflowStatus(workflow.id, { action: 'reject_order_data_price_by_leader' })
    ElMessage.success('运营部门领导审核数据价格已拒绝')
    await loadWorkflows(pagination.page)
    if (detailDialogVisible.value) {
      currentWorkflow.value = { ...workflow, order_stage: 2 }
    }
  } catch (error) {
    ElMessage.error('拒绝失败')
  }
}

// 跟单进度相关方法
function openMerchandiserProgressDialog(workflow) {
  currentWorkflow.value = workflow
  // 初始化默认两行
  merchandiserProgressForm.records = [
    { progress: '', remark: '', completed: false, time: '' },
    { progress: '', remark: '', completed: false, time: '' }
  ]
  merchandiserProgressDialogVisible.value = true
}

function addMerchandiserProgressRow() {
  merchandiserProgressForm.records.push({ progress: '', remark: '', completed: false, time: '' })
}

function removeMerchandiserProgressRow(index) {
  if (merchandiserProgressForm.records.length > 1) {
    merchandiserProgressForm.records.splice(index, 1)
  }
}

async function submitMerchandiserProgress() {
  // 过滤掉空行（进度和备注都为空），并为每一行添加当前时间
  const records = merchandiserProgressForm.records
    .filter(row => row.progress || row.remark)
    .map(row => ({
      ...row,
      time: new Date().toLocaleString()
    }))
  
  try {
    await updateWorkflowStatus(currentWorkflow.value.id, {
      action: 'update_merchandiser_progress',
      progress_records: records
    })
    ElMessage.success('跟单进度更新成功')
    merchandiserProgressDialogVisible.value = false
    await loadWorkflows(pagination.page)
    if (detailDialogVisible.value) {
      const response = await getWorkflowDetail(currentWorkflow.value.id)
      currentWorkflow.value = response
    }
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

async function completeMerchandiserProgress(workflow) {
  try {
    await updateWorkflowStatus(workflow.id, { action: 'complete_merchandiser_progress' })
    ElMessage.success('跟单进度已完成')
    await loadWorkflows(pagination.page)
    if (detailDialogVisible.value) {
      const response = await getWorkflowDetail(workflow.id)
      currentWorkflow.value = response
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 入库方法
async function stockIn(workflow) {
  try {
    await updateWorkflowStatus(workflow.id, { action: 'stock_in' })
    ElMessage.success('入库成功')
    await loadWorkflows(pagination.page)
  } catch (error) {
    ElMessage.error('入库失败')
  }
}

onMounted(async () => {
  await Promise.all([loadUsers(), loadSuppliers(), loadWorkflows()])
})
</script>
