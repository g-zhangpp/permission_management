<template>
  <div class="menu-list-container">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item :to="{ path: '/user' }">用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>菜单管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-button v-if="userStore.hasPermission('menus:create_menu')" type="primary" @click="handleAddMenu">添加菜单</el-button>
    <el-table v-loading="loading" :data="menus" style="width: 100%" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="菜单名称" />
      <el-table-column prop="path" label="菜单路径" />
      <el-table-column prop="component" label="组件路径" />
      <el-table-column prop="icon" label="菜单图标" />
      <el-table-column prop="parent_id" label="父菜单ID" width="100" />
      <el-table-column prop="order" label="排序" width="80" />
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
                  <el-dropdown-item v-if="userStore.hasPermission('menus:update_menu')" @click="handleEditMenu(scope.row)">
                    <el-icon><edit /></el-icon>
                    编辑
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.hasPermission('menus:delete_menu')" @click="handleDeleteMenu(scope.row.id)">
                    <el-icon><delete /></el-icon>
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button v-if="userStore.hasPermission('menus:update_menu')" type="primary" size="small" @click="handleEditMenu(scope.row)">
              编辑
            </el-button>
            <el-button v-if="userStore.hasPermission('menus:delete_menu')" type="danger" size="small" @click="handleDeleteMenu(scope.row.id)">
              删除
            </el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>

    <!-- 菜单树 -->
    <div class="menu-tree-container">
      <h3>菜单树</h3>
      <el-tree
        :data="menuTree"
        :props="defaultProps"
        node-key="id"
        default-expand-all
      />
    </div>

    <!-- 添加/编辑菜单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form
        :model="menuForm"
        :rules="rules"
        ref="menuFormRef"
        label-width="80px"
      >
        <el-form-item label="菜单名称" prop="name">
          <el-input v-model="menuForm.name" placeholder="请输入菜单名称" />
        </el-form-item>
        <el-form-item label="菜单路径" prop="path">
          <el-input v-model="menuForm.path" placeholder="请输入菜单路径" />
        </el-form-item>
        <el-form-item label="组件路径" prop="component">
          <el-input v-model="menuForm.component" placeholder="请输入组件路径" />
        </el-form-item>
        <el-form-item label="菜单图标" prop="icon">
          <el-input v-model="menuForm.icon" placeholder="请输入菜单图标" />
        </el-form-item>
        <el-form-item label="父菜单">
          <el-select v-model="menuForm.parent_id" placeholder="请选择父菜单">
            <el-option label="无" value="0" />
            <el-option
              v-for="menu in menuOptions"
              :key="menu.id"
              :label="menu.name"
              :value="menu.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="order">
          <el-input v-model.number="menuForm.order" placeholder="请输入排序" type="number" />
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
import menuApi from '../../api/menu'

const userStore = useUserStore()

const menus = ref([])
const loading = ref(true)
const menuTree = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('添加菜单')
const menuForm = ref({ id: '', name: '', path: '', component: '', icon: '', parent_id: 0, order: 0 })
const menuFormRef = ref(null)

const rules = {
  name: [
    { required: true, message: '请输入菜单名称', trigger: 'blur' }
  ],
  path: [
    { required: true, message: '请输入菜单路径', trigger: 'blur' }
  ],
  component: [
    { required: true, message: '请输入组件路径', trigger: 'blur' }
  ]
}

const defaultProps = {
  children: 'children',
  label: 'name'
}

const menuOptions = computed(() => {
  return menus.value.filter(menu => !menuForm.value.id || menu.id !== menuForm.value.id)
})

const getMenus = async () => {
  loading.value = true
  try {
    const response = await menuApi.getMenus()
    menus.value = response
  } catch (error) {
    ElMessage.error('获取菜单列表失败')
  } finally {
    loading.value = false
  }
}

const getMenuTree = async () => {
  try {
    const response = await menuApi.getMenuTree()
    menuTree.value = response
  } catch (error) {
    ElMessage.error('获取菜单树失败')
  }
}

const handleAddMenu = () => {
  dialogTitle.value = '添加菜单'
  menuForm.value = { id: '', name: '', path: '', component: '', icon: '', parent_id: 0, order: 0 }
  dialogVisible.value = true
}

const handleEditMenu = (row) => {
  dialogTitle.value = '编辑菜单'
  menuForm.value = { ...row }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (menuForm.value.id) {
      // 编辑菜单
      await menuApi.updateMenu(menuForm.value.id, menuForm.value)
      ElMessage.success('编辑菜单成功')
    } else {
      // 添加菜单
      await menuApi.createMenu(menuForm.value)
      ElMessage.success('添加菜单成功')
    }
    dialogVisible.value = false
    getMenus()
    getMenuTree()
  } catch (error) {
    ElMessage.error('操作失败，请稍后重试')
  }
}

const handleDeleteMenu = async (menuId) => {
  try {
    await menuApi.deleteMenu(menuId)
    ElMessage.success('删除菜单成功')
    getMenus()
    getMenuTree()
  } catch (error) {
    ElMessage.error('删除菜单失败')
  }
}

onMounted(() => {
  getMenus()
  getMenuTree()
})

// 计算是否有操作按钮
const hasActionButtons = computed(() => {
  return userStore.hasPermission('menus:update_menu') || 
         userStore.hasPermission('menus:delete_menu')
})

// 计算操作按钮数量
const getActionButtonCount = () => {
  let count = 0
  if (userStore.hasPermission('menus:update_menu')) count++
  if (userStore.hasPermission('menus:delete_menu')) count++
  return count
}
</script>

<style scoped>
.menu-list-container {
  padding: 20px;
}

.el-breadcrumb {
  margin-bottom: 20px;
}

h3 {
  margin: 20px 0 10px 0;
  color: #303133;
}

.menu-tree-container {
  margin-top: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.dialog-footer {
  text-align: right;
}
</style>