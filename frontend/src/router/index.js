import { createRouter, createWebHistory } from 'vue-router'
import authGuard from '../guards/auth'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/dashboard/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user',
    name: 'User',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'list',
        name: 'UserList',
        component: () => import('../views/user/UserList.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'role',
        name: 'RoleList',
        component: () => import('../views/user/RoleList.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'permission',
        name: 'PermissionList',
        component: () => import('../views/user/PermissionList.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'menu',
        name: 'MenuList',
        component: () => import('../views/user/MenuList.vue'),
        meta: { requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 应用路由守卫
router.beforeEach(authGuard)

export default router
