<template>
  <div class="dashboard-container">
    <el-breadcrumb separator="/" style="margin-bottom: 30px;">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="dashboard-header">
      <h1>欢迎使用权限管理系统</h1>
      <p>这是仪表盘页面，显示系统的概览信息。</p>
    </div>
    
    <div class="dashboard-stats">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon user-icon">
            <el-icon><UserFilled /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">128</div>
            <div class="stat-label">用户总数</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon role-icon">
            <el-icon><Avatar /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">10</div>
            <div class="stat-label">角色总数</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon permission-icon">
            <el-icon><Lock /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">50</div>
            <div class="stat-label">权限总数</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon menu-icon">
            <el-icon><Menu /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">20</div>
            <div class="stat-label">菜单总数</div>
          </div>
        </div>
      </el-card>
    </div>
    
    <div class="dashboard-charts">
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>用户活跃度</span>
          </div>
        </template>
        <div class="chart-content">
          <div class="placeholder-chart">
            <el-icon class="chart-icon"><DataAnalysis /></el-icon>
            <p>用户活跃度图表</p>
          </div>
        </div>
      </el-card>
      
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>角色分布</span>
          </div>
        </template>
        <div class="chart-content">
          <div class="placeholder-chart">
            <el-icon class="chart-icon"><PieChart /></el-icon>
            <p>角色分布图表</p>
          </div>
        </div>
      </el-card>
    </div>
    
    <div class="dashboard-recent">
      <el-card class="recent-card">
        <template #header>
          <div class="card-header">
            <span>最近操作</span>
          </div>
        </template>
        <el-table :data="recentActivities" style="width: 100%">
          <el-table-column prop="time" label="时间" width="180" />
          <el-table-column prop="user" label="用户" width="120" />
          <el-table-column prop="action" label="操作" />
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { UserFilled, Avatar, Lock, Menu, DataAnalysis, PieChart } from '@element-plus/icons-vue'

const recentActivities = ref([
  { time: '2026-03-13 10:30', user: 'admin', action: '登录系统' },
  { time: '2026-03-13 09:15', user: 'admin', action: '创建新用户' },
  { time: '2026-03-12 16:45', user: 'admin', action: '修改角色权限' },
  { time: '2026-03-12 14:20', user: 'admin', action: '添加新菜单' },
  { time: '2026-03-11 11:00', user: 'admin', action: '删除用户' }
])
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100%;
}

.dashboard-header {
  margin-bottom: 30px;
  text-align: left;
}

.dashboard-header h1 {
  margin: 0 0 10px;
  color: #2c3e50;
  font-size: 28px;
  font-weight: 600;
}

.dashboard-header p {
  margin: 0;
  color: #7f8c8d;
  font-size: 16px;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  font-size: 24px;
  color: #fff;
}

.user-icon {
  background: linear-gradient(135deg, #3498db, #2980b9);
}

.role-icon {
  background: linear-gradient(135deg, #27ae60, #229954);
}

.permission-icon {
  background: linear-gradient(135deg, #f39c12, #e67e22);
}

.menu-icon {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
}

.dashboard-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.chart-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 600;
  color: #2c3e50;
}

.chart-content {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fafafa;
}

.placeholder-chart {
  text-align: center;
  color: #7f8c8d;
}

.placeholder-chart el-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.dashboard-recent {
  margin-bottom: 30px;
}

.recent-card {
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.recent-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard-stats {
    grid-template-columns: 1fr;
  }
  
  .dashboard-charts {
    grid-template-columns: 1fr;
  }
  
  .chart-card {
    min-width: 100%;
  }
}
</style>
