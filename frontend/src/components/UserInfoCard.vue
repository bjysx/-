<template>
  <div class="rounded-[28px] p-4 text-white shadow-panel brand-gradient">
    <div class="flex items-center gap-3">
      <el-avatar :size="50" :src="user.avatar || undefined">{{ avatarText }}</el-avatar>
      <div class="min-w-0">
        <p class="truncate text-base font-semibold">{{ user.display_name || user.username || "管理员" }}</p>
        <p class="truncate text-xs text-white/70">{{ user.role_label || "系统管理员" }}</p>
      </div>
    </div>
    <div class="mt-4 grid grid-cols-2 gap-3 text-xs text-white/80">
      <div class="rounded-2xl bg-white/10 p-3">
        <p>在线状态</p>
        <p class="mt-1 text-sm font-semibold text-white">正常</p>
      </div>
      <div class="rounded-2xl bg-white/10 p-3">
        <p>主题模式</p>
        <p class="mt-1 text-sm font-semibold text-white">{{ themeText }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useAuthStore } from "@/store/auth"
import { useAppStore } from "@/store/app"

const auth = useAuthStore()
const app = useAppStore()
const user = computed(() => auth.state.user || {})
const avatarText = computed(() => (user.value.display_name || user.value.username || "锦").slice(0, 1))
const themeText = computed(() => (app.state.theme === "dark" ? "深色" : "浅色"))
</script>
