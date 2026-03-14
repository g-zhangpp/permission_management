# 后端项目说明

## 项目概述

后端项目是权限管理系统的服务端部分，基于FastAPI框架开发，提供用户认证、权限管理、角色管理、菜单管理等功能的API接口。

## 技术栈

- **语言**：Python 3.12
- **框架**：FastAPI
- **数据库**：MySQL
- **缓存**：Redis
- **认证**：JWT
- **密码加密**：bcrypt
- **ORM**：SQLAlchemy

## 项目结构

```
backend/
├── app/                 # 应用目录
│   ├── __init__.py      # 包初始化文件
│   ├── api/             # API路由
│   │   ├── __init__.py  # 包初始化文件
│   │   ├── v1/          # API版本
│   │   │   ├── __init__.py  # 包初始化文件
│   │   │   ├── auth.py  # 认证相关
│   │   │   ├── user.py  # 用户相关
│   │   │   ├── role.py  # 角色相关
│   │   │   ├── permission.py # 权限相关
│   │   │   └── menu.py  # 菜单相关
│   │   └── router.py    # 路由配置
│   ├── core/            # 核心模块
│   │   ├── __init__.py  # 包初始化文件
│   │   ├── config.yaml  # 配置文件
│   │   ├── config.py    # 配置管理
│   │   ├── security.py  # 安全相关
│   │   └── database.py  # 数据库连接
│   ├── models/          # 数据模型
│   │   ├── __init__.py  # 包初始化文件
│   │   ├── user.py      # 用户模型
│   │   ├── role.py      # 角色模型
│   │   ├── permission.py # 权限模型
│   │   ├── menu.py      # 菜单模型
│   │   └── base.py      # 基础模型
│   ├── schemas/         # 数据验证
│   │   ├── __init__.py  # 包初始化文件
│   │   ├── user.py      # 用户相关
│   │   ├── role.py      # 角色相关
│   │   ├── permission.py # 权限相关
│   │   └── menu.py      # 菜单相关
│   ├── services/        # 业务逻辑
│   │   ├── __init__.py  # 包初始化文件
│   │   ├── auth_service.py # 认证服务
│   │   ├── user_service.py # 用户服务
│   │   ├── role_service.py # 角色服务
│   │   ├── permission_service.py # 权限服务
│   │   ├── menu_service.py # 菜单服务
│   │   └── permission_scanner.py # 权限自动扫描服务
│   ├── middlewares/     # 中间件
│   │   ├── __init__.py  # 包初始化文件
│   │   ├── auth.py      # 认证中间件
│   │   └── cors.py      # CORS中间件
│   ├── utils/           # 工具函数
│   │   ├── __init__.py  # 包初始化文件
│   │   ├── password.py  # 密码工具
│   │   ├── jwt.py       # JWT工具
│   └── main.py          # 应用入口
├── migrations/          # 数据库迁移
│   └── __init__.py      # 包初始化文件
├── requirements.txt     # 依赖包
└── README.md            # 项目说明
```

## 安装步骤

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **配置文件**：
   修改 `app/core/config.yaml` 文件，配置数据库连接、JWT密钥等信息：
   ```yaml
   app:
     name: "Permission Management System"
     version: "1.0.0"
     debug: true

   database:
     url: "mysql+pymysql://username:password@localhost:3306/permission_system"

   redis:
     url: "redis://localhost:6379/0"

   security:
     secret_key: "your-secret-key"
     algorithm: "HS256"
     access_token_expire_minutes: 30
   ```

3. **数据库准备**：
   创建数据库：
   ```sql
   CREATE DATABASE permission_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

## 运行方式

1. **直接运行**：
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **使用 PM2 管理进程**：
   ```bash
   pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name permission-api
   ```

## API文档

启动服务后，可以通过以下地址访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 核心功能

### 认证功能
- 用户登录
- 用户登出
- 刷新token
- 获取当前用户信息

### 用户管理
- 获取用户列表
- 创建用户
- 获取用户详情
- 修改用户信息
- 删除用户
- 分配用户角色

### 角色管理
- 获取角色列表
- 创建角色
- 获取角色详情
- 修改角色信息
- 删除角色
- 分配角色权限
- 分配角色菜单

### 权限管理
- 获取权限列表
- 创建权限
- 获取权限详情
- 修改权限信息
- 删除权限
- 自动扫描路由生成权限

### 菜单管理
- 获取菜单列表
- 创建菜单
- 获取菜单详情
- 修改菜单信息
- 删除菜单
- 获取菜单树

## 初始化数据

系统启动时会自动初始化以下数据：

### 初始化用户
| 用户名 | 密码 | 角色 | 描述 |
| :--- | :--- | :--- | :--- |
| `admin` | `root123` | `admin` | 系统管理员，拥有所有权限 |

### 初始化角色
| 角色名称 | 描述 |
| :--- | :--- |
| `admin` | 系统管理员角色，拥有所有权限 |
| `common` | 普通用户角色，拥有基础权限 |

### 初始化菜单
系统会自动创建基础的菜单结构，包括首页和用户管理相关菜单。

## 如何增加新模块

在 `get_menu_tree` 方法中增加新模块的步骤如下：

### 1. 了解 `get_menu_tree` 方法的结构

`get_menu_tree` 方法位于 `/workSpaces/pythonProjects/permission_management/backend/app/services/menu_service.py` 文件中，主要功能是根据用户权限获取菜单树结构，并为每个菜单添加对应的权限信息。

### 2. 增加新模块的步骤

1. **在菜单表中添加新菜单**：
   - 首先需要在数据库的 `menus` 表中添加新的菜单项
   - 确保设置正确的 `path`、`component`、`icon` 等字段

2. **在 `get_menu_tree` 方法中添加权限映射**：
   - 在方法的权限映射部分（第94-108行）添加新的条件判断
   - 为新模块指定对应的权限前缀

### 3. 代码示例

假设我们要增加一个名为 "设备管理" 的模块，路径为 `/device`，具体步骤如下：

#### 步骤1：在数据库中添加菜单项

首先在 `menus` 表中添加以下记录：

| id | name | path | component | icon | parent_id | order |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 5 | 设备管理 | /device | Device | device | NULL | 3 |
| 6 | 设备列表 | /device/list | DeviceList | list | 5 | 1 |
| 7 | 设备类型 | /device/type | DeviceType | type | 5 | 2 |

#### 步骤2：修改 `get_menu_tree` 方法

在 `menu_service.py` 文件的 `get_menu_tree` 方法中添加新的权限映射：

```python
# 为每个菜单添加权限信息
for menu in all_menus:
    menu_obj = menu_dict[menu.id]
    # 根据菜单路径判断所属模块，添加对应的权限
    if '/user/list' in menu.path:
        # 用户管理模块权限
        menu_obj.permissions = [p for p in user_permissions if p.startswith('users:')]
    elif '/user/role' in menu.path:
        # 角色管理模块权限
        menu_obj.permissions = [p for p in user_permissions if p.startswith('roles:')]
    elif '/user/permission' in menu.path:
        # 权限管理模块权限
        menu_obj.permissions = [p for p in user_permissions if p.startswith('permissions:')]
    elif '/user/menu' in menu.path:
        # 菜单管理模块权限
        menu_obj.permissions = [p for p in user_permissions if p.startswith('menus:')]
    elif '/device' in menu.path:
        # 设备管理模块权限
        menu_obj.permissions = [p for p in user_permissions if p.startswith('devices:')]
    else:
        # 其他模块权限
        menu_obj.permissions = []
```

### 4. 权限配置

为新模块创建对应的权限：

1. **在权限表中添加权限**：
   - 为设备管理模块创建相关权限，如 `devices:list`、`devices:create`、`devices:update`、`devices:delete` 等

2. **为角色分配权限**：
   - 在角色管理界面为需要访问设备管理模块的角色分配对应的权限

### 5. 前端配置

在前端项目中添加对应的路由和组件：

1. **添加路由**：在 `router/index.js` 文件中添加设备管理相关路由
2. **创建组件**：在 `views/device` 目录下创建对应的组件文件
3. **配置菜单**：确保前端菜单配置与后端保持一致

## 如何在 config.yaml 中配置菜单

### 1. 配置结构

在 `app/core/config.yaml` 文件中，菜单配置位于 `init_data.menus` 部分。每个菜单项包含以下字段：

- `name`：菜单名称
- `path`：菜单路径
- `component`：菜单对应的组件
- `icon`：菜单图标
- `parent_id`：父菜单ID，一级菜单为 `null`，二级菜单为对应一级菜单的ID
- `order`：菜单排序顺序

### 2. 配置示例

#### 配置一级菜单

一级菜单的 `parent_id` 为 `null`，例如：

```yaml
menus:
  - name: "首页"
    path: "/dashboard"
    component: "Dashboard"
    icon: "home"
    parent_id: null
    order: 1
  - name: "用户管理"
    path: "/user"
    component: "User"
    icon: "user"
    parent_id: null
    order: 2
```

#### 配置二级菜单

二级菜单的 `parent_id` 为对应一级菜单的ID，例如：

```yaml
menus:
  # 一级菜单
  - name: "用户管理"
    path: "/user"
    component: "User"
    icon: "user"
    parent_id: null
    order: 2
  # 二级菜单
  - name: "用户管理"
    path: "/user/list"
    component: "UserList"
    icon: "user"
    parent_id: 2
    order: 1
  - name: "角色管理"
    path: "/user/role"
    component: "RoleList"
    icon: "role"
    parent_id: 2
    order: 2
```

### 3. 完整案例

以下是一个完整的菜单配置案例，包含一级菜单和二级菜单：

```yaml
init_data:
  # 初始化用户
  users:
    - username: "admin"
      password: "root123"
      email: "admin@example.com"
      roles: ["admin"]
  # 初始化角色
  roles:
    - name: "admin"
      description: "系统管理员角色，拥有所有权限"
    - name: "common"
      description: "普通用户角色，拥有基础权限"
  # 初始化菜单
  menus:
    # 一级菜单
    - name: "首页"
      path: "/dashboard"
      component: "Dashboard"
      icon: "home"
      parent_id: null
      order: 1
    - name: "用户管理"
      path: "/user"
      component: "User"
      icon: "user"
      parent_id: null
      order: 2
    - name: "设备管理"
      path: "/device"
      component: "Device"
      icon: "device"
      parent_id: null
      order: 3
    # 二级菜单
    - name: "用户管理"
      path: "/user/list"
      component: "UserList"
      icon: "user"
      parent_id: 2
      order: 1
    - name: "角色管理"
      path: "/user/role"
      component: "RoleList"
      icon: "role"
      parent_id: 2
      order: 2
    - name: "权限管理"
      path: "/user/permission"
      component: "PermissionList"
      icon: "permission"
      parent_id: 2
      order: 3
    - name: "菜单管理"
      path: "/user/menu"
      component: "MenuList"
      icon: "menu"
      parent_id: 2
      order: 4
    - name: "设备列表"
      path: "/device/list"
      component: "DeviceList"
      icon: "list"
      parent_id: 3
      order: 1
    - name: "设备类型"
      path: "/device/type"
      component: "DeviceType"
      icon: "type"
      parent_id: 3
      order: 2
```

### 4. 注意事项

1. **菜单ID**：系统会自动为菜单分配ID，二级菜单的 `parent_id` 应设置为对应一级菜单的ID
2. **路径设置**：菜单路径应与前端路由配置保持一致
3. **组件名称**：组件名称应与前端组件文件名称保持一致
4. **排序顺序**：通过 `order` 字段控制菜单的显示顺序，值越小显示越靠前
5. **图标设置**：图标名称应与前端使用的图标库保持一致

配置完成后，系统启动时会自动将配置的菜单数据初始化到数据库中。

## 安全措施

- **密码加密**：使用bcrypt对用户密码进行加密存储
- **JWT认证**：使用JWT进行身份验证
- **权限验证**：基于角色的权限控制（RBAC）
- **CORS设置**：配置了CORS中间件，支持跨域请求
- **参数验证**：使用Pydantic进行请求参数验证

## 监控和维护

### 日志管理
- 使用结构化日志，记录请求和错误
- 日志文件存储在 `logs` 目录

### 性能监控
- 可以使用Prometheus和Grafana进行性能监控

### 安全监控
- 定期进行安全扫描
- 使用WAF和IDS进行入侵检测

