<template>
  <header class="sticky top-0 z-30 p-4 md:p-6">
    <div class="glass-panel flex flex-wrap items-center justify-between gap-4 rounded-[28px] px-5 py-4">
      <div class="flex min-w-0 items-center gap-3">
        <el-button circle text @click="app.toggleSidebar()">
          <el-icon><Fold /></el-icon>
        </el-button>
        <div class="min-w-0">
          <h1 class="truncate text-lg font-semibold text-slate-900 dark:text-slate-50">锦世源系统</h1>
          <BreadcrumbNav class="mt-1 text-xs text-slate-500 dark:text-slate-400" />
        </div>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <el-dropdown trigger="click">
          <el-button circle text>
            <el-icon><Bell /></el-icon>
            <el-badge v-if="pendingTasks.length > 0" :value="pendingTasks.length" class="badge" />
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-for="task in pendingTasks" :key="task.id" @click="navigateToTask(task)">
                <div class="flex flex-col items-start">
                  <span class="font-medium">{{ task.title }}</span>
                  <span class="text-xs text-slate-500">{{ task.description }}</span>
                </div>
              </el-dropdown-item>
              <el-dropdown-item v-if="pendingTasks.length === 0">暂无待处理任务</el-dropdown-item>
              <el-dropdown-item divided @click="router.push('/warning/warning-history')">所有预警历史</el-dropdown-item>
              <el-dropdown-item @click="router.push('/warning/warning-rules')">预警规则配置</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button circle text @click="toggleFullscreen">
          <el-icon><FullScreen /></el-icon>
        </el-button>
        <el-button circle text @click="app.toggleTheme()">
          <el-icon><component :is="themeIcon" /></el-icon>
        </el-button>
        <el-dropdown trigger="click">
          <div class="flex cursor-pointer items-center gap-3 rounded-2xl bg-slate-100 px-3 py-2 dark:bg-slate-900">
            <el-avatar :size="36" :src="auth.state.user?.avatar || undefined">{{ avatarText }}</el-avatar>
            <div class="hidden text-left md:block">
              <p class="text-sm font-medium text-slate-800 dark:text-slate-100">{{ auth.state.user?.display_name || auth.state.user?.username }}</p>
              <p class="text-xs text-slate-500 dark:text-slate-400">{{ auth.state.user?.department || "" }} - {{ auth.state.user?.position || "" }}</p>
            </div>
            <el-icon><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="avatarVisible = true">更换头像</el-dropdown-item>
              <el-dropdown-item @click="passwordVisible = true">修改密码</el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </header>

  <el-dialog v-model="passwordVisible" title="修改密码" width="460px">
    <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-position="top">
      <el-form-item label="原密码" prop="old_password">
        <el-input v-model="passwordForm.old_password" show-password />
      </el-form-item>
      <el-form-item label="新密码" prop="new_password">
        <el-input v-model="passwordForm.new_password" show-password />
      </el-form-item>
      <el-form-item label="确认密码" prop="confirm_password">
        <el-input v-model="passwordForm.confirm_password" show-password />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="flex justify-end gap-3">
        <el-button @click="passwordVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitPassword">确认修改</el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog v-model="avatarVisible" title="更换头像" width="400px">
    <div class="flex flex-col items-center gap-4">
      <el-avatar :size="120" :src="auth.state.user?.avatar || undefined">{{ avatarText }}</el-avatar>
      <el-upload
        class="avatar-uploader"
        action="/api/user/avatar/"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
        :headers="{ Authorization: `Bearer ${auth.state.accessToken}` }"
      >
        <el-button type="primary">选择图片</el-button>
      </el-upload>
      <p class="text-sm text-slate-500">请选择 200x200 像素的图片，大小不超过 2MB</p>
    </div>
  </el-dialog>
</template>

<script setup>
import { computed, reactive, ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"
import { Bell, FullScreen, Fold, ArrowDown, Sunny, Moon } from "@element-plus/icons-vue"
import { changePassword, logout } from "@/api/auth"
import { getWorkflows } from "@/api/business"
import BreadcrumbNav from "./BreadcrumbNav.vue"
import { useAppStore } from "@/store/app"
import { useAuthStore } from "@/store/auth"

const router = useRouter()
const auth = useAuthStore()
const app = useAppStore()
const passwordVisible = ref(false)
const avatarVisible = ref(false)
const passwordFormRef = ref()
const submitting = ref(false)
const pendingTasks = ref([])

// 加载待处理任务
async function loadPendingTasks() {
  if (!auth.state.user) {
    console.log('用户未登录，无法加载待处理任务')
    return
  }
  try {
    console.log('开始加载待处理任务，用户ID:', auth.state.user.id)
    const response = await getWorkflows({ page: 1, page_size: 10, status: 'in_progress' })
    console.log('获取到的工作流数据:', response.results)
    const tasks = []
    response.results.forEach(workflow => {
      console.log('处理工作流:', workflow.product_name, '当前阶段:', workflow.current_stage, '跟单员:', workflow.merchandiser, '用户ID:', auth.state.user.id)
      // 根据工作流当前阶段和用户角色生成任务
      if (workflow.current_stage === 1 && workflow.approver === auth.state.user.id) {
        tasks.push({
          id: workflow.id,
          title: `审批工作流: ${workflow.product_name}`,
          description: '等待审批人审批',
          type: 'workflow',
          workflow_id: workflow.id
        })
      } else if (workflow.current_stage === 2 && workflow.approver === auth.state.user.id) {
        tasks.push({
          id: workflow.id,
          title: `选择供应商: ${workflow.product_name}`,
          description: '请审批人选择供应商',
          type: 'workflow',
          workflow_id: workflow.id
        })
      } else if (workflow.current_stage === 3 && workflow.merchandiser === auth.state.user.id) {
        console.log('添加确认LOGO/高频任务:', workflow.product_name)
        tasks.push({
          id: workflow.id,
          title: `确认LOGO/高频: ${workflow.product_name}`,
          description: '请跟单员确认LOGO/高频',
          type: 'workflow',
          workflow_id: workflow.id
        })
      } else if (workflow.current_stage === 4 && workflow.merchandiser === auth.state.user.id) {
        tasks.push({
          id: workflow.id,
          title: `下样品单: ${workflow.product_name}`,
          description: '请跟单员下样品单',
          type: 'workflow',
          workflow_id: workflow.id
        })
      } else if (workflow.current_stage === 5 && workflow.salesperson === auth.state.user.id) {
        tasks.push({
          id: workflow.id,
          title: `业务员审核: ${workflow.product_name}`,
          description: '请业务员审核样品单',
          type: 'workflow',
          workflow_id: workflow.id
        })
      } else if (workflow.current_stage === 6 && workflow.operator === auth.state.user.id) {
        tasks.push({
          id: workflow.id,
          title: `运营人员审核: ${workflow.product_name}`,
          description: '请运营人员审核样品单',
          type: 'workflow',
          workflow_id: workflow.id
        })
      } else if (workflow.current_stage === 7 && workflow.salesperson === auth.state.user.id) {
        tasks.push({
          id: workflow.id,
          title: `业务员审核全色: ${workflow.product_name}`,
          description: '请业务员审核全色',
          type: 'workflow',
          workflow_id: workflow.id
        })
      } else if (workflow.current_stage === 8 && workflow.operator === auth.state.user.id) {
        tasks.push({
          id: workflow.id,
          title: `运营人员审核全色: ${workflow.product_name}`,
          description: '请运营人员审核全色',
          type: 'workflow',
          workflow_id: workflow.id
        })
      } else if (workflow.current_stage === 9 && workflow.photographer === auth.state.user.id) {
        tasks.push({
          id: workflow.id,
          title: `摄影师审核: ${workflow.product_name}`,
          description: '请摄影师审核',
          type: 'workflow',
          workflow_id: workflow.id
        })
      } else if (workflow.progress === 99 && workflow.clerk === auth.state.user.id) {
        tasks.push({
          id: workflow.id,
          title: `文员审核: ${workflow.product_name}`,
          description: '请文员审核',
          type: 'workflow',
          workflow_id: workflow.id
        })
      }
    })
    console.log('生成的待处理任务:', tasks)
    pendingTasks.value = tasks
  } catch (error) {
    console.error('加载待处理任务失败:', error)
  }
}

// 导航到任务
function navigateToTask(task) {
  if (task.type === 'workflow') {
    router.push(`/product/white-label?workflow_id=${task.workflow_id}`)
    // 导航后重新加载待办事项，确保列表正确更新
    setTimeout(() => {
      loadPendingTasks()
    }, 1000)
  }
}

// 组件挂载时加载待处理任务
onMounted(() => {
  loadPendingTasks()
})
const passwordForm = reactive({
  old_password: "",
  new_password: "",
  confirm_password: ""
})
const passwordRules = {
  old_password: [{ required: true, message: "请输入原密码", trigger: "blur" }],
  new_password: [{ required: true, message: "请输入新密码", trigger: "blur" }],
  confirm_password: [
    { required: true, message: "请再次输入新密码", trigger: "blur" },
    {
      validator: (_, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error("两次输入的新密码不一致"))
          return
        }
        callback()
      },
      trigger: "blur"
    }
  ]
}
const avatarText = computed(() => (auth.state.user?.display_name || auth.state.user?.username || "锦").slice(0, 1))
const themeIcon = computed(() => (app.state.theme === "dark" ? "Sunny" : "Moon"))

async function handleLogout() {
  try {
    await logout()
  } finally {
    auth.clear()
    router.push({ name: "login" })
  }
}

async function submitPassword() {
  const valid = await passwordFormRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  submitting.value = true
  try {
    await changePassword(passwordForm)
    ElMessage.success("密码修改成功，请重新登录")
    passwordVisible.value = false
    await handleLogout()
  } finally {
    submitting.value = false
  }
}

async function toggleFullscreen() {
  if (document.fullscreenElement) {
    await document.exitFullscreen()
    return
  }
  await document.documentElement.requestFullscreen()
}

function handleAvatarSuccess(response, uploadFile, uploadFileList) {
  console.log('头像上传成功回调:', response)
  if (response.success) {
    ElMessage.success("头像上传成功")
    // 更新用户信息
    auth.setUser({
      ...auth.state.user,
      avatar: response.data.avatar
    })
    avatarVisible.value = false
  } else {
    ElMessage.error("头像上传失败")
  }
}

function beforeAvatarUpload(file) {
  const isJPG = file.type === "image/jpeg" || file.type === "image/png"
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error("请选择 JPG 或 PNG 格式的图片")
    return false
  }
  if (!isLt2M) {
    ElMessage.error("图片大小不能超过 2MB")
    return false
  }
  return true
}
</script>
