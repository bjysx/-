<template>
  <div class="flex min-h-[70vh] items-center justify-center">
    <div class="page-card max-w-lg text-center">
      <div class="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-slate-100 text-3xl font-bold text-slate-500 dark:bg-slate-800 dark:text-slate-400">404</div>
      <h2 class="mt-6 text-3xl font-semibold">页面找不到了</h2>
      <p class="mt-3 text-sm text-slate-500 dark:text-slate-400">抱歉，您访问的页面不存在或已被移除。请检查输入的网址是否正确。</p>
      <div class="mt-8 flex justify-center gap-3">
        <el-button type="primary" @click="$router.push('/dashboard/home')">返回首页</el-button>
        <el-button @click="$router.back()">返回上一页</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
