import { useUserStore } from '../store/modules/user'

const authGuard = (to, from, next) => {
  const userStore = useUserStore()
  const requiresAuth = to.meta.requiresAuth

  if (requiresAuth) {
    // 检查用户是否已登录
    if (userStore.isLoggedIn) {
      next()
    } else {
      // 未登录，重定向到登录页面
      next('/login')
    }
  } else {
    // 不需要认证的路由，直接放行
    next()
  }
}

export default authGuard