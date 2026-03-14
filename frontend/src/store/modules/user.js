import { defineStore } from 'pinia'
import authApi from '../../api/auth'
import menuApi from '../../api/menu'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo')) || null,
    permissions: JSON.parse(localStorage.getItem('permissions')) || [],
    roles: JSON.parse(localStorage.getItem('roles')) || [],
    menus: JSON.parse(localStorage.getItem('menus')) || []
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    hasPermission: (state) => (permission) => {
      return state.permissions.includes(permission)
    },
    userMenus: (state) => state.menus
  },

  actions: {
    async login(username, password) {
      try {
        const response = await authApi.login(username, password)
        const { access_token } = response
        this.token = access_token
        localStorage.setItem('token', access_token)
        
        // 获取用户信息
        await this.getUserInfo()
        if (!this.userInfo) {
          throw new Error('获取用户信息失败')
        }
        
        // 获取用户菜单
        await this.getUserMenus()
        return true
      } catch (error) {
        console.error('登录失败:', error)
        // 清除token
        this.token = ''
        localStorage.removeItem('token')
        return false
      }
    },

    async getUserInfo() {
      try {
        const userInfo = await authApi.getMe()
        this.userInfo = userInfo
        localStorage.setItem('userInfo', JSON.stringify(userInfo))
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.userInfo = null
        localStorage.removeItem('userInfo')
      }
    },

    async getUserMenus() {
      try {
        const menus = await menuApi.getMenuTree()
        this.menus = menus
        localStorage.setItem('menus', JSON.stringify(menus))
        
        // 从菜单中提取权限信息
        const permissions = new Set()
        const extractPermissions = (menuList) => {
          menuList.forEach(menu => {
            if (menu.permissions && menu.permissions.length > 0) {
              menu.permissions.forEach(permission => permissions.add(permission))
            }
            if (menu.children && menu.children.length > 0) {
              extractPermissions(menu.children)
            }
          })
        }
        extractPermissions(menus)
        this.permissions = Array.from(permissions)
        localStorage.setItem('permissions', JSON.stringify(this.permissions))
      } catch (error) {
        console.error('获取用户菜单失败:', error)
        this.menus = []
        this.permissions = []
        localStorage.removeItem('menus')
        localStorage.removeItem('permissions')
      }
    },

    logout() {
      this.token = ''
      this.userInfo = null
      this.permissions = []
      this.roles = []
      this.menus = []
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('permissions')
      localStorage.removeItem('roles')
      localStorage.removeItem('menus')
    }
  }
})
