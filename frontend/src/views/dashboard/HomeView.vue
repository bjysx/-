<template>
  <div class="page-shell">
    <section class="grid gap-4 xl:grid-cols-[1.6fr,1fr]">
      <div class="page-card brand-gradient text-white">
        <p class="text-sm text-white/70">企业数智驾驶舱</p>
        <div class="mt-4 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 class="text-3xl font-semibold">欢迎回来，{{ auth.state.user?.display_name || auth.state.user?.username }}</h2>
            <p class="mt-3 max-w-2xl text-sm leading-7 text-white/75">当前工作台已接入销售、运营、商品、供应链、财务、人力、行政、预警、设计与工作中心，支持实时经营数据查看与业务台账管理。</p>
          </div>
          <el-button size="large" class="!rounded-2xl !border-white/20 !bg-white/10 !text-white" @click="loadDashboard">刷新概览</el-button>
        </div>
      </div>
      <div class="page-card">
        <h3 class="text-lg font-semibold">个人工作卡片</h3>
        <div class="mt-4">
          <UserInfoCard />
        </div>
      </div>
    </section>

    <section class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      <div v-for="card in dashboard.overview_cards" :key="card.label" class="page-card">
        <p class="text-sm text-slate-500 dark:text-slate-400">{{ card.label }}</p>
        <p class="mt-3 text-3xl font-semibold">{{ card.formatted || card.value }}</p>
        <p class="mt-3 text-xs text-emerald-500">{{ card.trend }}</p>
      </div>
    </section>

    <section class="grid gap-4 xl:grid-cols-3">
      <div class="page-card xl:col-span-2">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold">营收趋势</h3>
          <el-tag type="primary" effect="plain">近7日</el-tag>
        </div>
        <DashboardChart :option="dashboard.trend_option" />
      </div>
      <div class="page-card">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold">模块占比</h3>
          <el-tag effect="plain">实时统计</el-tag>
        </div>
        <DashboardChart :option="dashboard.module_option" />
      </div>
    </section>

    <section class="page-card">
      <div class="mb-4 flex items-center justify-between">
        <h3 class="text-lg font-semibold">经营雷达</h3>
        <el-tag type="success" effect="plain">待开发</el-tag>
      </div>
      <DashboardChart :option="dashboard.radar_option" />
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive } from "vue"
import { getDashboardData } from "@/api/system"
import DashboardChart from "@/components/DashboardChart.vue"
import UserInfoCard from "@/components/UserInfoCard.vue"
import { useAuthStore } from "@/store/auth"

const auth = useAuthStore()
const dashboard = reactive({
  overview_cards: [],
  trend_option: {},
  module_option: {},
  radar_option: {}
})

async function loadDashboard() {
  const response = await getDashboardData()
  Object.assign(dashboard, response.data)
}

onMounted(() => {
  loadDashboard()
})
</script>
