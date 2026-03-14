import request from '../utils/request'

const userApi = {
  // 获取用户列表
  getUsers: (params) => {
    return request.get('/users', { params })
  },

  // 创建用户
  createUser: (userData) => {
    return request.post('/users', userData)
  },

  // 获取用户详情
  getUser: (userId) => {
    return request.get(`/users/${userId}`)
  },

  // 修改用户信息
  updateUser: (userId, userData) => {
    return request.put(`/users/${userId}`, userData)
  },

  // 删除用户
  deleteUser: (userId) => {
    return request.delete(`/users/${userId}`)
  },

  // 获取用户角色
  getUserRoles: (userId) => {
    return request.get(`/users/${userId}/roles`)
  },

  // 分配用户角色
  assignUserRoles: (userId, roleIds) => {
    return request.post(`/users/${userId}/roles`, roleIds)
  }
}

export default userApi
