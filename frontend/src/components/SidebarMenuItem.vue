<template>
  <el-sub-menu v-if="item.children?.length" :index="item.key">
    <template #title>
      <el-icon><component :is="item.icon || 'Tickets'" /></el-icon>
      <span>{{ item.title }}</span>
    </template>
    <SidebarMenuItem v-for="child in item.children" :key="child.key" :item="child" />
  </el-sub-menu>
  <el-menu-item v-else :index="item.path">
    <el-icon><component :is="item.icon || 'Tickets'" /></el-icon>
    <template #title>{{ item.title }}</template>
  </el-menu-item>
</template>

<script setup>
import { useRouter } from "vue-router"

defineProps({
  item: {
    type: Object,
    required: true
  }
})

const router = useRouter()
</script>
