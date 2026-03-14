import request from '../utils/request'

const authApi = {
  // 登录
  login: (username, password) => {
    // 使用application/x-www-form-urlencoded格式发送登录请求
    return request.post('/auth/login', `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },

  // 登出
  logout: () => {
    return request.post('/auth/logout')
  },

  // 刷新token
  refresh: () => {
    return request.post('/auth/refresh')
  },

  // 获取当前用户信息
  getMe: () => {
    return request.get('/auth/me')
  }
}

export default authApi
