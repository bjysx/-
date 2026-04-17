<template>
  <div class="relative flex min-h-screen overflow-hidden bg-slate-950">
    <div class="absolute inset-0 bg-hero"></div>
    <div class="absolute -left-16 top-0 h-80 w-80 rounded-full bg-primary-500/30 blur-3xl"></div>
    <div class="absolute bottom-0 right-0 h-96 w-96 rounded-full bg-violet-500/20 blur-3xl"></div>
    <div class="relative z-10 grid w-full lg:grid-cols-[1.2fr,0.8fr]">
      <div class="hidden px-10 py-12 lg:flex lg:flex-col lg:justify-between">
        <div>
          <div class="inline-flex items-center gap-3 rounded-full border border-white/10 bg-white/10 px-4 py-2 text-sm text-white/80 backdrop-blur">
            <span class="flex h-8 w-8 items-center justify-center rounded-full bg-white/15 font-semibold">锦</span>
            ERP 企业级数智管理平台
          </div>
          <div class="mt-12 max-w-xl">
            <h1 class="text-5xl font-semibold leading-tight text-white">锦世源系统</h1>
            <p class="mt-6 text-lg leading-8 text-white/70">连接销售、运营、商品、供应链、财务与组织管理，打造统一、专业、可持续扩展的企业后台工作台。</p>
          </div>
        </div>
        <div class="grid max-w-2xl gap-4 md:grid-cols-3">
          <div class="rounded-3xl border border-white/10 bg-white/10 p-5 text-white backdrop-blur">
            <p class="text-sm text-white/60">模块中心</p>
            <p class="mt-3 text-3xl font-semibold">10</p>
            <p class="mt-2 text-sm text-white/70">完整覆盖企业运营链路</p>
          </div>
          <div class="rounded-3xl border border-white/10 bg-white/10 p-5 text-white backdrop-blur">
            <p class="text-sm text-white/60">业务页面</p>
            <p class="mt-3 text-3xl font-semibold">48</p>
            <p class="mt-2 text-sm text-white/70">标准化路由与页面骨架</p>
          </div>
          <div class="rounded-3xl border border-white/10 bg-white/10 p-5 text-white backdrop-blur">
            <p class="text-sm text-white/60">认证方案</p>
            <p class="mt-3 text-3xl font-semibold">JWT</p>
            <p class="mt-2 text-sm text-white/70">前后端分离安全登录</p>
          </div>
        </div>
      </div>
      <div class="flex items-center justify-center px-6 py-10 md:px-10">
        <div class="w-full max-w-md rounded-[32px] border border-white/10 bg-white/95 p-8 shadow-2xl backdrop-blur dark:bg-slate-900/90">
          <div class="text-center">
            <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-3xl brand-gradient text-2xl font-semibold text-white">锦</div>
            <h2 class="mt-5 text-3xl font-semibold text-slate-900 dark:text-slate-50">欢迎登录</h2>
            <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">请输入账号密码进入锦世源系统</p>
          </div>
          <el-form ref="formRef" :model="form" :rules="rules" label-position="top" class="mt-8">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="form.username" size="large" placeholder="请输入用户名" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="form.password" size="large" show-password placeholder="请输入密码" @keyup.enter="handleSubmit" />
            </el-form-item>
            <div class="mb-6 flex items-center justify-between">
              <el-checkbox v-model="form.remember">记住我</el-checkbox>

            </div>
            <el-button class="w-full !h-12 !rounded-2xl" type="primary" :loading="submitting" @click="handleSubmit">登录系统</el-button>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { ElMessage } from "element-plus"
import { login } from "@/api/auth"
import { getMenuTree } from "@/api/system"
import { useAuthStore } from "@/store/auth"

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const formRef = ref()
const submitting = ref(false)
const form = reactive({
  username: "",
  password: "",
  remember: true
})
const rules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }]
}

async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  submitting.value = true
  try {
    const response = await login(form)
    auth.setSession({ ...response, remember: form.remember })
    const menus = await getMenuTree()
    auth.setMenus(menus)
    ElMessage.success("登录成功")
    router.push((route.query.redirect || "/dashboard/home").toString())
  } finally {
    submitting.value = false
  }
}
</script>
