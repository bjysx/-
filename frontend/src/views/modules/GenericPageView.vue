<template>
  <GenericBusinessPage
    :section-title="currentPage.sectionTitle"
    :page-title="currentPage.title"
    :page-code="currentPage.pageCode"
  />
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import GenericBusinessPage from "@/components/GenericBusinessPage.vue"
import { flatPageMap } from "@/config/menu"

const route = useRoute()
const currentPage = computed(() => flatPageMap[route.meta.pageCode] || { title: "业务页面", sectionTitle: "工作台", pageCode: "" })
</script>
