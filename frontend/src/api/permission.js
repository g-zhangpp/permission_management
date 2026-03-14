import request from '../utils/request'

const permissionApi = {
  // 获取权限列表
  getPermissions: (params) => {
    return request.get('/permissions', { params })
  },

  // 创建权限
  createPermission: (permissionData) => {
    return request.post('/permissions', permissionData)
  },

  // 获取权限详情
  getPermission: (permissionId) => {
    return request.get(`/permissions/${permissionId}`)
  },

  // 修改权限信息
  updatePermission: (permissionId, permissionData) => {
    return request.put(`/permissions/${permissionId}`, permissionData)
  },

  // 删除权限
  deletePermission: (permissionId) => {
    return request.delete(`/permissions/${permissionId}`)
  }
}

export default permissionApi
