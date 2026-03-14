<template>
  <div class="role-list-container">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item :to="{ path: '/user' }">用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>角色管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-button v-if="userStore.hasPermission('roles:create_role')" type="primary" @click="handleAddRole">添加角色</el-button>
    <el-table v-loading="loading" :data="roles" style="width: 100%" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="角色名称" />
      <el-table-column prop="description" label="角色描述" />
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
                  <el-dropdown-item v-if="userStore.hasPermission('roles:update_role')" @click="handleEditRole(scope.row)">
                    <el-icon><edit /></el-icon>
                    编辑
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.hasPermission('roles:delete_role')" @click="handleDeleteRole(scope.row.id)">
                    <el-icon><delete /></el-icon>
                    删除
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.hasPermission('roles:assign_role_permissions')" @click="handleAssignPermissions(scope.row.id)">
                    <el-icon><lock /></el-icon>
                    分配权限
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.hasPermission('roles:assign_role_menus')" @click="handleAssignMenus(scope.row.id)">
                    <el-icon><menu /></el-icon>
                    分配菜单
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button v-if="userStore.hasPermission('roles:update_role')" type="primary" size="small" @click="handleEditRole(scope.row)">编辑</el-button>
            <el-button v-if="userStore.hasPermission('roles:delete_role')" type="danger" size="small" @click="handleDeleteRole(scope.row.id)">删除</el-button>
            <el-button v-if="userStore.hasPermission('roles:assign_role_permissions')" size="small" @click="handleAssignPermissions(scope.row.id)">分配权限</el-button>
            <el-button v-if="userStore.hasPermission('roles:assign_role_menus')" size="small" @click="handleAssignMenus(scope.row.id)">分配菜单</el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑角色对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form
        :model="roleForm"
        :rules="rules"
        ref="roleFormRef"
        label-width="80px"
      >
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色描述" prop="description">
          <el-input v-model="roleForm.description" placeholder="请输入角色描述" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 分配权限对话框 -->
    <el-dialog
      v-model="permissionDialogVisible"
      title="分配权限"
      width="500px"
    >
      <el-form>
        <el-form-item label="权限列表">
          <div class="permission-list-scroll">
            <el-checkbox-group v-model="selectedPermissions">
              <el-checkbox v-for="permission in permissions" :key="permission.id" :label="permission.id" class="permission-item">
                {{ permission.name }}
              </el-checkbox>
            </el-checkbox-group>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="permissionDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAssignPermissionsSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 分配菜单对话框 -->
    <el-dialog
      v-model="menuDialogVisible"
      title="分配菜单"
      width="500px"
    >
      <el-form>
        <el-form-item label="菜单列表">
          <div class="permission-list-scroll">
            <el-checkbox-group v-model="selectedMenus">
              <template v-for="menu in menuTree" :key="menu.id">
                <el-checkbox :label="menu.id" class="permission-item menu-item">
                  {{ menu.name }}
                </el-checkbox>
                <div v-if="menu.children && menu.children.length > 0" class="sub-menu">
                  <el-checkbox 
                    v-for="subMenu in menu.children" 
                    :key="subMenu.id" 
                    :label="subMenu.id" 
                    class="permission-item sub-menu-item"
                  >
                    {{ subMenu.name }}
                  </el-checkbox>
                </div>
              </template>
            </el-checkbox-group>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="menuDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAssignMenusSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowDown, Edit, Delete, Lock, Menu } from '@element-plus/icons-vue'
import { useUserStore } from '../../store/modules/user'
import roleApi from '../../api/role'
import permissionApi from '../../api/permission'
import menuApi from '../../api/menu'

const userStore = useUserStore()

const roles = ref([])
const loading = ref(true)
const permissions = ref([])
const menus = ref([])
const dialogVisible = ref(false)
const permissionDialogVisible = ref(false)
const menuDialogVisible = ref(false)
const dialogTitle = ref('添加角色')
const roleForm = ref({ id: '', name: '', description: '' })
const selectedPermissions = ref([])
const selectedMenus = ref([])
const roleFormRef = ref(null)
const currentRoleId = ref(null)

const rules = {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' }
  ]
}

const getRoles = async () => {
  loading.value = true
  try {
    const response = await roleApi.getRoles()
    roles.value = response
  } catch (error) {
    ElMessage.error('获取角色列表失败')
  } finally {
    loading.value = false
  }
}

const getPermissions = async () => {
  try {
    const response = await permissionApi.getPermissions()
    permissions.value = response
  } catch (error) {
    ElMessage.error('获取权限列表失败')
  }
}

// 计算有层次结构的菜单
const menuTree = computed(() => {
  const menuMap = new Map()
  const roots = []
  
  console.log('Menus data:', menus.value)
  
  // 首先将所有菜单按ID映射
  menus.value.forEach(menu => {
    menuMap.set(menu.id, { ...menu, children: [] })
  })
  
  // 然后构建树结构
  menus.value.forEach(menu => {
    if (menu.parent_id === 0 || menu.parent_id === null || menu.parent_id === undefined) {
      roots.push(menuMap.get(menu.id))
    } else {
      const parent = menuMap.get(menu.parent_id)
      if (parent) {
        parent.children.push(menuMap.get(menu.id))
      } else {
        // 如果找不到父菜单，也作为根菜单处理
        roots.push(menuMap.get(menu.id))
      }
    }
  })
  
  console.log('Menu tree:', roots)
  return roots
})

const getMenus = async () => {
  try {
    const response = await menuApi.getMenus()
    menus.value = response
  } catch (error) {
    ElMessage.error('获取菜单列表失败')
  }
}

const handleAddRole = () => {
  dialogTitle.value = '添加角色'
  roleForm.value = { id: '', name: '', description: '' }
  dialogVisible.value = true
}

const handleEditRole = (row) => {
  dialogTitle.value = '编辑角色'
  roleForm.value = { ...row }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (roleForm.value.id) {
      // 编辑角色
      await roleApi.updateRole(roleForm.value.id, roleForm.value)
      ElMessage.success('编辑角色成功')
    } else {
      // 添加角色
      await roleApi.createRole(roleForm.value)
      ElMessage.success('添加角色成功')
    }
    dialogVisible.value = false
    getRoles()
  } catch (error) {
    ElMessage.error('操作失败，请稍后重试')
  }
}

const handleDeleteRole = async (roleId) => {
  try {
    await roleApi.deleteRole(roleId)
    ElMessage.success('删除角色成功')
    getRoles()
  } catch (error) {
    ElMessage.error('删除角色失败')
  }
}

const handleAssignPermissions = async (roleId) => {
  currentRoleId.value = roleId
  await getPermissions()
  // 获取角色当前权限
  try {
    const response = await roleApi.getRolePermissions(roleId)
    selectedPermissions.value = response.permissions?.map(permission => permission.id) || []
  } catch (error) {
    ElMessage.error('获取角色权限失败')
  }
  permissionDialogVisible.value = true
}

const handleAssignPermissionsSubmit = async () => {
  try {
    await roleApi.assignRolePermissions(currentRoleId.value, selectedPermissions.value)
    ElMessage.success('分配权限成功')
    permissionDialogVisible.value = false
  } catch (error) {
    ElMessage.error('分配权限失败')
  }
}

const handleAssignMenus = async (roleId) => {
  currentRoleId.value = roleId
  await getMenus()
  // 获取角色当前菜单
  try {
    const response = await roleApi.getRoleMenus(roleId)
    selectedMenus.value = response.menus?.map(menu => menu.id) || []
  } catch (error) {
    ElMessage.error('获取角色菜单失败')
  }
  menuDialogVisible.value = true
}

const handleAssignMenusSubmit = async () => {
  try {
    await roleApi.assignRoleMenus(currentRoleId.value, selectedMenus.value)
    ElMessage.success('分配菜单成功')
    menuDialogVisible.value = false
  } catch (error) {
    ElMessage.error('分配菜单失败')
  }
}

onMounted(() => {
  getRoles()
})

// 计算是否有操作按钮
const hasActionButtons = computed(() => {
  return userStore.hasPermission('roles:update_role') || 
         userStore.hasPermission('roles:delete_role') || 
         userStore.hasPermission('roles:assign_role_permissions') || 
         userStore.hasPermission('roles:assign_role_menus')
})

// 计算操作按钮数量
const getActionButtonCount = () => {
  let count = 0
  if (userStore.hasPermission('roles:update_role')) count++
  if (userStore.hasPermission('roles:delete_role')) count++
  if (userStore.hasPermission('roles:assign_role_permissions')) count++
  if (userStore.hasPermission('roles:assign_role_menus')) count++
  return count
}
</script>

<style scoped>
.role-list-container {
  padding: 20px;
}

.el-breadcrumb {
  margin-bottom: 20px;
}

.dialog-footer {
  text-align: right;
}

.permission-list-scroll {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  padding: 16px;
  background-color: #f5f7fa;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  width: 100%;
  min-width: 420px;
}

.permission-list-scroll::-webkit-scrollbar {
  width: 8px;
}

.permission-list-scroll::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.permission-list-scroll::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.permission-list-scroll::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.permission-item {
  display: block;
  margin-right: 0;
  margin-bottom: 8px;
}

.permission-item:last-child {
  margin-bottom: 0;
}

.menu-item {
  font-weight: 500;
}

.sub-menu {
  margin-left: 20px;
  margin-top: 4px;
  margin-bottom: 12px;
}

.sub-menu-item {
  font-size: 13px;
  color: #606266;
}
</style>
