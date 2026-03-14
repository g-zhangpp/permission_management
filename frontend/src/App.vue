<template>
  <div id="app">
    <template v-if="$route.meta.requiresAuth">
      <el-container class="container">
        <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
          <div class="logo">
            <h1 v-if="!isCollapse">权限管理系统</h1>
            <div v-else class="logo-icon">
              <el-icon><Setting /></el-icon>
            </div>
          </div>
          <el-menu
            :default-active="activeMenu"
            :collapse="isCollapse"
            class="el-menu-vertical-demo"
            @select="handleMenuSelect"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
          >
            <!-- 动态渲染菜单 -->
            <template v-for="menu in userMenus" :key="menu.id">
              <!-- 有子菜单的情况 -->
              <el-sub-menu v-if="menu.children && menu.children.length > 0" :index="menu.id.toString()">
                <template #title>
                  <el-icon :size="20"><component :is="getIcon(menu.icon)" /></el-icon>
                  <span>{{ menu.name }}</span>
                </template>
                <!-- 渲染子菜单 -->
                <el-menu-item
                  v-for="subMenu in menu.children"
                  :key="subMenu.id"
                  :index="subMenu.path"
                >
                  <el-icon :size="18"><component :is="getIcon(subMenu.icon)" /></el-icon>
                  <span>{{ subMenu.name }}</span>
                </el-menu-item>
              </el-sub-menu>
              <!-- 没有子菜单的情况 -->
              <el-menu-item v-else :index="menu.path">
                <el-icon :size="20"><component :is="getIcon(menu.icon)" /></el-icon>
                <span>{{ menu.name }}</span>
              </el-menu-item>
            </template>
          </el-menu>
        </el-aside>
        <el-container>
          <el-header class="header">
            <div class="header-left">
              <el-button type="primary" @click="collapseSidebar">
                <el-icon><ArrowLeft /></el-icon>
              </el-button>
            </div>
            <div class="header-right">
              <el-dropdown>
                <span class="user-info">
                  <el-icon><UserFilled /></el-icon>
                  <span>{{ userInfo?.username || '用户' }}</span>
                  <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </el-header>
          <el-main class="main">
            <router-view />
          </el-main>
        </el-container>
      </el-container>
    </template>
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './store/modules/user'
import { HomeFilled, UserFilled, Lock, Menu, House, Avatar, ArrowLeft, ArrowDown, User, Setting, DataAnalysis, PieChart } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const isCollapse = ref(false)

// 计算当前激活的菜单
const activeMenu = computed(() => {
  const path = router.currentRoute.value.path
  // 查找当前路径对应的菜单
  const findActiveMenu = (menus) => {
    for (const menu of menus) {
      if (menu.path === path) {
        return menu.id.toString()
      }
      if (menu.children && menu.children.length > 0) {
        const result = findActiveMenu(menu.children)
        if (result) {
          return menu.id.toString()
        }
      }
    }
    return ''
  }
  return findActiveMenu(userStore.menus)
})

// 获取用户信息
const userInfo = computed(() => userStore.userInfo)

// 获取用户菜单
const userMenus = computed(() => userStore.menus)

// 处理菜单选择
const handleMenuSelect = (key) => {
  router.push(key)
}

// 折叠侧边栏
const collapseSidebar = () => {
  isCollapse.value = !isCollapse.value
}

// 处理退出登录
const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

// 根据图标名称获取图标组件
const getIcon = (iconName) => {
  const iconMap = {
    home: HomeFilled,
    user: UserFilled,
    role: Avatar,
    permission: Lock,
    menu: Menu,
    dashboard: House,
    'data-analysis': DataAnalysis,
    'pie-chart': PieChart
  }
  return iconMap[iconName] || Menu
}

// 组件挂载时获取用户信息和菜单
onMounted(async () => {
  if (userStore.isLoggedIn) {
    await userStore.getUserInfo()
    await userStore.getUserMenus()
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  background-color: #f5f7fa;
}

#app {
  height: 100vh;
  overflow: hidden;
}

.container {
  height: 100vh;
  display: flex;
}

.sidebar {
  background-color: #2c3e50;
  height: 100%;
  overflow-y: auto;
  transition: all 0.3s ease;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  border-bottom: 1px solid #34495e;
  transition: all 0.3s ease;
  background-color: #1a252f;
}

.logo h1 {
  font-size: 16px;
  margin: 0;
  padding: 0;
}

.logo-icon {
  font-size: 24px;
  color: #3498db;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.3s ease;
  font-size: 14px;
}

.user-info:hover {
  background-color: #f5f7fa;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.main {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: #f5f7fa;
}

.el-menu-vertical-demo {
  border-right: none;
  background-color: #2c3e50;
}

.el-menu {
  border-right: none;
}

.el-menu-item {
  height: 48px;
  line-height: 48px;
  margin: 0 8px;
  border-radius: 4px;
  margin-bottom: 4px;
  transition: all 0.3s ease;
}

.el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.el-menu-item.is-active {
  background-color: rgba(52, 152, 219, 0.2) !important;
  color: #3498db !important;
}

.el-sub-menu__title {
  height: 48px;
  line-height: 48px;
  margin: 0 8px;
  border-radius: 4px;
  margin-bottom: 4px;
  transition: all 0.3s ease;
}

.el-sub-menu__title:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.el-sub-menu.is-opened > .el-sub-menu__title {
  background-color: rgba(52, 152, 219, 0.2) !important;
  color: #3498db !important;
}

.el-button {
  transition: all 0.3s ease;
}

.el-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.el-table {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.el-table th {
  background-color: #fafafa !important;
  font-weight: 600;
  color: #333;
}

.el-table tr:hover {
  background-color: #f5f7fa !important;
}

.el-card {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.el-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.el-form-item__label {
  font-weight: 500;
  color: #333;
}

.el-input {
  border-radius: 4px;
  transition: all 0.3s ease;
}

.el-input:hover .el-input__inner {
  border-color: #3498db;
}

.el-input.is-focus .el-input__inner {
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.el-dialog {
  border-radius: 8px;
  overflow: hidden;
}

.el-dialog__header {
  background-color: #fafafa;
  border-bottom: 1px solid #e0e0e0;
}

.el-dialog__title {
  font-weight: 600;
  color: #333;
}

/* 动画效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}
</style>
