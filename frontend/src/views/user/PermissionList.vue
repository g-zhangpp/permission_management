<template>
  <div class="permission-list-container">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item :to="{ path: '/user' }">用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>权限管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-button v-if="userStore.hasPermission('permissions:create_permission')" type="primary" @click="handleAddPermission">添加权限</el-button>
    <el-table v-loading="loading" :data="permissions" style="width: 100%" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="权限名称" />
      <el-table-column prop="code" label="权限代码" />
      <el-table-column prop="description" label="权限描述" />
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
                  <el-dropdown-item v-if="userStore.hasPermission('permissions:update_permission')" @click="handleEditPermission(scope.row)">
                    <el-icon><edit /></el-icon>
                    编辑
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.hasPermission('permissions:delete_permission')" @click="handleDeletePermission(scope.row.id)">
                    <el-icon><delete /></el-icon>
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button v-if="userStore.hasPermission('permissions:update_permission')" type="primary" size="small" @click="handleEditPermission(scope.row)">
              编辑
            </el-button>
            <el-button v-if="userStore.hasPermission('permissions:delete_permission')" type="danger" size="small" @click="handleDeletePermission(scope.row.id)">
              删除
            </el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑权限对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form
        :model="permissionForm"
        :rules="rules"
        ref="permissionFormRef"
        label-width="80px"
      >
        <el-form-item label="权限名称" prop="name">
          <el-input v-model="permissionForm.name" placeholder="请输入权限名称" />
        </el-form-item>
        <el-form-item label="权限代码" prop="code">
          <el-input v-model="permissionForm.code" placeholder="请输入权限代码" />
        </el-form-item>
        <el-form-item label="权限描述" prop="description">
          <el-input v-model="permissionForm.description" placeholder="请输入权限描述" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowDown, Edit, Delete } from '@element-plus/icons-vue'
import { useUserStore } from '../../store/modules/user'
import permissionApi from '../../api/permission'

const userStore = useUserStore()

const permissions = ref([])
const loading = ref(true)
const dialogVisible = ref(false)
const dialogTitle = ref('添加权限')
const permissionForm = ref({ id: '', name: '', code: '', description: '' })
const permissionFormRef = ref(null)

const rules = {
  name: [
    { required: true, message: '请输入权限名称', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入权限代码', trigger: 'blur' }
  ]
}

const getPermissions = async () => {
  loading.value = true
  try {
    const response = await permissionApi.getPermissions()
    permissions.value = response
  } catch (error) {
    ElMessage.error('获取权限列表失败')
  } finally {
    loading.value = false
  }
}

const handleAddPermission = () => {
  dialogTitle.value = '添加权限'
  permissionForm.value = { id: '', name: '', code: '', description: '' }
  dialogVisible.value = true
}

const handleEditPermission = (row) => {
  dialogTitle.value = '编辑权限'
  permissionForm.value = { ...row }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (permissionForm.value.id) {
      // 编辑权限
      await permissionApi.updatePermission(permissionForm.value.id, permissionForm.value)
      ElMessage.success('编辑权限成功')
    } else {
      // 添加权限
      await permissionApi.createPermission(permissionForm.value)
      ElMessage.success('添加权限成功')
    }
    dialogVisible.value = false
    getPermissions()
  } catch (error) {
    ElMessage.error('操作失败，请稍后重试')
  }
}

const handleDeletePermission = async (permissionId) => {
  try {
    await permissionApi.deletePermission(permissionId)
    ElMessage.success('删除权限成功')
    getPermissions()
  } catch (error) {
    ElMessage.error('删除权限失败')
  }
}

onMounted(() => {
  getPermissions()
})

// 计算是否有操作按钮
const hasActionButtons = computed(() => {
  return userStore.hasPermission('permissions:update_permission') || 
         userStore.hasPermission('permissions:delete_permission')
})

// 计算操作按钮数量
const getActionButtonCount = () => {
  let count = 0
  if (userStore.hasPermission('permissions:update_permission')) count++
  if (userStore.hasPermission('permissions:delete_permission')) count++
  return count
}
</script>

<style scoped>
.permission-list-container {
  padding: 20px;
}

.el-breadcrumb {
  margin-bottom: 20px;
}

.dialog-footer {
  text-align: right;
}
</style>