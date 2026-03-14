import request from '../utils/request'

const roleApi = {
  // 获取角色列表
  getRoles: (params) => {
    return request.get('/roles', { params })
  },

  // 创建角色
  createRole: (roleData) => {
    return request.post('/roles', roleData)
  },

  // 获取角色详情
  getRole: (roleId) => {
    return request.get(`/roles/${roleId}`)
  },

  // 修改角色信息
  updateRole: (roleId, roleData) => {
    return request.put(`/roles/${roleId}`, roleData)
  },

  // 删除角色
  deleteRole: (roleId) => {
    return request.delete(`/roles/${roleId}`)
  },

  // 获取角色权限
  getRolePermissions: (roleId) => {
    return request.get(`/roles/${roleId}/permissions`)
  },

  // 分配角色权限
  assignRolePermissions: (roleId, permissionIds) => {
    return request.post(`/roles/${roleId}/permissions`, permissionIds)
  },

  // 获取角色菜单
  getRoleMenus: (roleId) => {
    return request.get(`/roles/${roleId}/menus`)
  },

  // 分配角色菜单
  assignRoleMenus: (roleId, menuIds) => {
    return request.post(`/roles/${roleId}/menus`, menuIds)
  }
}

export default roleApi
