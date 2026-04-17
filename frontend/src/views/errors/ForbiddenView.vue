<template>
  <div class="flex min-h-[70vh] items-center justify-center">
    <div class="page-card max-w-lg text-center">
      <div class="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-amber-100 text-3xl text-amber-500 dark:bg-amber-500/10">!</div>
      <h2 class="mt-6 text-3xl font-semibold">暂无访问权限</h2>
      <p class="mt-3 text-sm text-slate-500 dark:text-slate-400">当前账号未获得该页面访问权限，请联系系统管理员开通。</p>
      <el-button class="mt-6" type="primary" @click="$router.push('/dashboard/home')">返回首页</el-button>
    </div>
  </div>
</template>
