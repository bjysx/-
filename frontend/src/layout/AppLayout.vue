<template>
  <div class="flex min-h-screen bg-slate-100 text-slate-900 transition-colors dark:bg-slate-950 dark:text-slate-100">
    <transition name="fade">
      <div v-if="showMask" class="fixed inset-0 z-40 bg-slate-950/50 lg:hidden" @click="app.toggleSidebar(true)" />
    </transition>
    <aside
      class="fixed inset-y-0 left-0 z-50 w-[290px] flex-shrink-0 transform transition-all duration-300 overflow-x-hidden"
      :class="[collapsedClass, app.state.isMobile && app.state.sidebarCollapsed ? '-translate-x-full' : 'translate-x-0']"
    >
      <SidebarMenu />
    </aside>
    <!-- 右侧内容区域 -->
    <div class="flex flex-1 flex-col" :style="{ marginLeft: mainContentMarginLeft }">
      <!-- 顶部导航栏 -->
      <div class="sticky top-0 z-30">
        <AppHeader />
      </div>
      <!-- 主内容区域 -->
      <main class="flex-1 p-4 md:p-6 overflow-auto">
        <router-view v-slot="{ Component, route }">
          <transition name="slide-fade" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import SidebarMenu from "@/components/SidebarMenu.vue"
import AppHeader from "@/components/AppHeader.vue"
import { useAppStore } from "@/store/app"

const app = useAppStore()
const collapsedClass = computed(() => (app.state.sidebarCollapsed && !app.state.isMobile ? "lg:w-[88px]" : "lg:w-[290px]"))
const showMask = computed(() => app.state.isMobile && !app.state.sidebarCollapsed)

const mainContentMarginLeft = computed(() => {
  if (app.state.isMobile) {
    return "0px"
  }
  return app.state.sidebarCollapsed ? "88px" : "290px"
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active,
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.25s ease;
}

.fade-enter-from,
.fade-leave-to,
.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
