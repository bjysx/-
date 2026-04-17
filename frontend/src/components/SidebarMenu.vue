<template>
  <div class="flex h-full flex-col bg-slate-950/95 px-4 py-5 text-white">
    <div class="flex items-center gap-3 px-3">
      <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/10 text-xl font-semibold">锦</div>
      <div v-show="!app.state.sidebarCollapsed || app.state.isMobile" class="min-w-0">
        <p class="truncate text-lg font-semibold">锦世源系统</p>
        <p class="truncate text-xs text-white/60">Enterprise Management Suite</p>
      </div>
    </div>
    <div v-show="!app.state.sidebarCollapsed || app.state.isMobile" class="mt-5">
      <UserInfoCard />
    </div>
    <div class="mt-5 flex-1 overflow-y-auto">
      <el-menu
        :default-active="route.path"
        :collapse="app.state.sidebarCollapsed && !app.state.isMobile"
        :unique-opened="true"
        router
        class="border-none bg-transparent"
        background-color="transparent"
        text-color="rgba(255,255,255,0.7)"
        active-text-color="#ffffff"
      >
        <SidebarMenuItem v-for="item in menus" :key="item.key" :item="item" />
      </el-menu>
    </div>
  </div>
</template>

<style>
.el-menu--collapse .el-sub-menu__title span {
  display: none;
}

.el-sub-menu .el-menu {
  background-color: rgba(0, 0, 0, 0.2) !important;
}

.el-menu-item:hover, .el-sub-menu__title:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
  color: #fff !important;
}

.el-menu-item.is-active {
  background: var(--brand-gradient) !important;
  color: #fff !important;
  border-radius: 12px;
  margin: 4px 8px;
  height: 44px !important;
  line-height: 44px !important;
}

.el-menu--popup {
  background-color: #0f172a !important;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 5px;
}

.el-menu--popup .el-menu-item {
  color: rgba(255,255,255,0.7) !important;
}

.el-menu--popup .el-menu-item:hover {
  color: #fff !important;
  background-color: rgba(255,255,255,0.1) !important;
}
</style>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import SidebarMenuItem from "./SidebarMenuItem.vue"
import UserInfoCard from "./UserInfoCard.vue"
import { useAppStore } from "@/store/app"

const app = useAppStore()
const route = useRoute()
const menus = computed(() => app.availableMenus())
</script>
