import { defineStore } from 'pinia'
import roleApi from '../../api/role'

export const useRoleStore = defineStore('role', {
  state: () => ({
    roles: [],
    currentRole: null
  }),

  getters: {
    roleList: (state) => state.roles
  },

  actions: {
    async getRoles() {
      try {
        const response = await roleApi.getRoles()
        this.roles = response
      } catch (error) {
        console.error('获取角色列表失败:', error)
      }
    },

    async createRole(roleData) {
      try {
        const response = await roleApi.createRole(roleData)
        this.roles.push(response)
        return response
      } catch (error) {
        console.error('创建角色失败:', error)
        throw error
      }
    },

    async updateRole(id, roleData) {
      try {
        const response = await roleApi.updateRole(id, roleData)
        const index = this.roles.findIndex(role => role.id === id)
        if (index !== -1) {
          this.roles[index] = response
        }
        return response
      } catch (error) {
        console.error('更新角色失败:', error)
        throw error
      }
    },

    async deleteRole(id) {
      try {
        await roleApi.deleteRole(id)
        this.roles = this.roles.filter(role => role.id !== id)
      } catch (error) {
        console.error('删除角色失败:', error)
        throw error
      }
    },

    async getRolePermissions(id) {
      try {
        return await roleApi.getRolePermissions(id)
      } catch (error) {
        console.error('获取角色权限失败:', error)
        throw error
      }
    },

    async assignRolePermissions(id, permissions) {
      try {
        return await roleApi.assignRolePermissions(id, permissions)
      } catch (error) {
        console.error('分配角色权限失败:', error)
        throw error
      }
    },

    async getRoleMenus(id) {
      try {
        return await roleApi.getRoleMenus(id)
      } catch (error) {
        console.error('获取角色菜单失败:', error)
        throw error
      }
    },

    async assignRoleMenus(id, menus) {
      try {
        return await roleApi.assignRoleMenus(id, menus)
      } catch (error) {
        console.error('分配角色菜单失败:', error)
        throw error
      }
    }
  }
})