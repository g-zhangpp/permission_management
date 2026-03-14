import request from '../utils/request'

const menuApi = {
  // 获取菜单列表
  getMenus: (params) => {
    return request.get('/menus', { params })
  },

  // 创建菜单
  createMenu: (menuData) => {
    return request.post('/menus', menuData)
  },

  // 获取菜单详情
  getMenu: (menuId) => {
    return request.get(`/menus/${menuId}`)
  },

  // 修改菜单信息
  updateMenu: (menuId, menuData) => {
    return request.put(`/menus/${menuId}`, menuData)
  },

  // 删除菜单
  deleteMenu: (menuId) => {
    return request.delete(`/menus/${menuId}`)
  },

  // 获取菜单树
  getMenuTree: () => {
    return request.get('/menus/tree')
  }
}

export default menuApi
