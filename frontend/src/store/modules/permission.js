import { defineStore } from 'pinia'
import permissionApi from '../../api/permission'

export const usePermissionStore = defineStore('permission', {
  state: () => ({
    permissions: []
  }),

  getters: {
    permissionList: (state) => state.permissions
  },

  actions: {
    async getPermissions() {
      try {
        const response = await permissionApi.getPermissions()
        this.permissions = response
      } catch (error) {
        console.error('获取权限列表失败:', error)
      }
    },

    async createPermission(permissionData) {
      try {
        const response = await permissionApi.createPermission(permissionData)
        this.permissions.push(response)
        return response
      } catch (error) {
        console.error('创建权限失败:', error)
        throw error
      }
    },

    async updatePermission(id, permissionData) {
      try {
        const response = await permissionApi.updatePermission(id, permissionData)
        const index = this.permissions.findIndex(permission => permission.id === id)
        if (index !== -1) {
          this.permissions[index] = response
        }
        return response
      } catch (error) {
        console.error('更新权限失败:', error)
        throw error
      }
    },

    async deletePermission(id) {
      try {
        await permissionApi.deletePermission(id)
        this.permissions = this.permissions.filter(permission => permission.id !== id)
      } catch (error) {
        console.error('删除权限失败:', error)
        throw error
      }
    }
  }
})