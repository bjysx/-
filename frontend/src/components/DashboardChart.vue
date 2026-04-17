<template>
  <div ref="chartRef" class="h-[320px] w-full"></div>
</template>

<script setup>
import * as echarts from "echarts"
import { onBeforeUnmount, onMounted, ref, watch } from "vue"

const props = defineProps({
  option: {
    type: Object,
    default: () => ({})
  }
})

const chartRef = ref()
let chartInstance

function render() {
  if (!chartRef.value) {
    return
  }
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }
  chartInstance.setOption(props.option || {}, true)
  chartInstance.resize()
}

function handleResize() {
  chartInstance?.resize()
}

watch(() => props.option, render, { deep: true })

onMounted(() => {
  render()
  window.addEventListener("resize", handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize)
  chartInstance?.dispose()
})
</script>
