<template>
  <div class="user-list-container">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-button v-if="userStore.hasPermission('users:create_user')" type="primary" @click="handleAddUser">添加用户</el-button>
    <el-table v-loading="loading" :data="users" style="width: 100%" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column v-if="hasActionButtons" label="操作" width="120">
        <template #default="scope">
          <template v-if="getActionButtonCount(scope.row) > 1">
            <el-dropdown>
              <el-button type="primary" size="small">
                操作
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-if="userStore.hasPermission('users:update_user')" @click="handleEditUser(scope.row)">
                    <el-icon><edit /></el-icon>
                    编辑
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.hasPermission('users:delete_user')" @click="handleDeleteUser(scope.row.id)">
                    <el-icon><delete /></el-icon>
                    删除
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.hasPermission('users:assign_user_roles')" @click="handleAssignRoles(scope.row.id)">
                    <el-icon><user-filled /></el-icon>
                    分配角色
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button v-if="userStore.hasPermission('users:update_user')" type="primary" size="small" @click="handleEditUser(scope.row)">编辑</el-button>
            <el-button v-if="userStore.hasPermission('users:delete_user')" type="danger" size="small" @click="handleDeleteUser(scope.row.id)">删除</el-button>
            <el-button v-if="userStore.hasPermission('users:assign_user_roles')" size="small" @click="handleAssignRoles(scope.row.id)">分配角色</el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form
        :model="userForm"
        :rules="rules"
        ref="userFormRef"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!userForm.id">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 分配角色对话框 -->
    <el-dialog
      v-model="roleDialogVisible"
      title="分配角色"
      width="500px"
    >
      <el-form>
        <el-form-item label="角色列表">
          <el-checkbox-group v-model="selectedRoles">
            <el-checkbox v-for="role in roles" :key="role.id" :label="role.id">{{ role.name }}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="roleDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAssignRolesSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowDown, Edit, Delete, UserFilled } from '@element-plus/icons-vue'
import { useUserStore } from '../../store/modules/user'
import userApi from '../../api/user'
import roleApi from '../../api/role'

const userStore = useUserStore()

const users = ref([])
const loading = ref(true)
const roles = ref([])
const dialogVisible = ref(false)
const roleDialogVisible = ref(false)
const dialogTitle = ref('添加用户')
const userForm = ref({ id: '', username: '', password: '', email: '' })
const selectedRoles = ref([])
const userFormRef = ref(null)
const currentUserId = ref(null)

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

const getUsers = async () => {
  loading.value = true
  try {
    const response = await userApi.getUsers()
    users.value = response
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const getRoles = async () => {
  try {
    const response = await roleApi.getRoles()
    roles.value = response
  } catch (error) {
    ElMessage.error('获取角色列表失败')
  }
}

const handleAddUser = () => {
  dialogTitle.value = '添加用户'
  userForm.value = { id: '', username: '', password: '', email: '' }
  dialogVisible.value = true
}

const handleEditUser = (row) => {
  dialogTitle.value = '编辑用户'
  userForm.value = { ...row }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (userForm.value.id) {
      // 编辑用户
      await userApi.updateUser(userForm.value.id, userForm.value)
      ElMessage.success('编辑用户成功')
    } else {
      // 添加用户
      await userApi.createUser(userForm.value)
      ElMessage.success('添加用户成功')
    }
    dialogVisible.value = false
    getUsers()
  } catch (error) {
    ElMessage.error('操作失败，请稍后重试')
  }
}

const handleDeleteUser = async (userId) => {
  try {
    await userApi.deleteUser(userId)
    ElMessage.success('删除用户成功')
    getUsers()
  } catch (error) {
    ElMessage.error('删除用户失败')
  }
}

const handleAssignRoles = async (userId) => {
  currentUserId.value = userId
  await getRoles()
  // 获取用户当前角色
  try {
    const response = await userApi.getUserRoles(userId)
    selectedRoles.value = response.roles?.map(role => role.id) || []
  } catch (error) {
    ElMessage.error('获取用户角色失败')
  }
  roleDialogVisible.value = true
}

const handleAssignRolesSubmit = async () => {
  try {
    await userApi.assignUserRoles(currentUserId.value, selectedRoles.value)
    ElMessage.success('分配角色成功')
    roleDialogVisible.value = false
  } catch (error) {
    ElMessage.error('分配角色失败')
  }
}

onMounted(() => {
  getUsers()
})

// 计算是否有操作按钮
const hasActionButtons = computed(() => {
  return userStore.hasPermission('users:update_user') || 
         userStore.hasPermission('users:delete_user') || 
         userStore.hasPermission('users:assign_user_roles')
})

// 计算操作按钮数量
const getActionButtonCount = () => {
  let count = 0
  if (userStore.hasPermission('users:update_user')) count++
  if (userStore.hasPermission('users:delete_user')) count++
  if (userStore.hasPermission('users:assign_user_roles')) count++
  return count
}
</script>

<style scoped>
.user-list-container {
  padding: 20px;
}

.el-breadcrumb {
  margin-bottom: 20px;
}

.dialog-footer {
  text-align: right;
}
</style>
