import { defineStore } from 'pinia'
import menuApi from '../../api/menu'

export const useMenuStore = defineStore('menu', {
  state: () => ({
    menus: [],
    menuTree: []
  }),

  getters: {
    menuList: (state) => state.menus,
    menuTreeList: (state) => state.menuTree
  },

  actions: {
    async getMenus() {
      try {
        const response = await menuApi.getMenus()
        this.menus = response
      } catch (error) {
        console.error('获取菜单列表失败:', error)
      }
    },

    async getMenuTree() {
      try {
        const response = await menuApi.getMenuTree()
        this.menuTree = response
      } catch (error) {
        console.error('获取菜单树失败:', error)
      }
    },

    async createMenu(menuData) {
      try {
        const response = await menuApi.createMenu(menuData)
        this.menus.push(response)
        // 重新获取菜单树
        await this.getMenuTree()
        return response
      } catch (error) {
        console.error('创建菜单失败:', error)
        throw error
      }
    },

    async updateMenu(id, menuData) {
      try {
        const response = await menuApi.updateMenu(id, menuData)
        const index = this.menus.findIndex(menu => menu.id === id)
        if (index !== -1) {
          this.menus[index] = response
        }
        // 重新获取菜单树
        await this.getMenuTree()
        return response
      } catch (error) {
        console.error('更新菜单失败:', error)
        throw error
      }
    },

    async deleteMenu(id) {
      try {
        await menuApi.deleteMenu(id)
        this.menus = this.menus.filter(menu => menu.id !== id)
        // 重新获取菜单树
        await this.getMenuTree()
      } catch (error) {
        console.error('删除菜单失败:', error)
        throw error
      }
    }
  }
})