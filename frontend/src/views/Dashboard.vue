<template>
  <div class="dashboard-container">
    <h1>欢迎使用权限管理系统</h1>
    <p>这是仪表盘页面</p>
    <el-button type="primary" @click="handleLogout">退出登录</el-button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const handleLogout = () => {
  ElMessage.success('退出登录成功')
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
  color: #303133;
}

p {
  margin-bottom: 30px;
  color: #606266;
}
</style>
