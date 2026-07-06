# 智能健身管理系统 (FitnessSystem)

基于 MediaPipe 的智能健身管理平台，实现 AI 运动姿态检测、动作自动计数、卡路里计算与健康数据可视化。

## 项目简介

本系统面向个人运动健康管理场景，采用前后端分离架构，前端基于 Vue2 + Element UI 构建响应式界面，后端采用 Django REST Framework 提供 API 服务。核心功能包括：AI 姿态检测与动作计数、舞蹈评分、卡路里计算、健康打卡记录与趋势分析。

## 技术栈

### 前端技术
| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 2.6.14 | 前端框架 |
| Vue CLI | 5.0.0 | 项目构建工具 |
| Element UI | 2.15.14 | UI 组件库 |
| Vuex | 3.6.2 | 状态管理 |
| Vue Router | 3.6.5 | 路由管理 |
| Axios | 1.7.7 | HTTP 请求库 |
| ECharts | 5.6.0 | 数据可视化 |
| MediaPipe | - | 姿态检测前端库 |

### 后端技术
| 技术 | 版本 | 说明 |
|------|------|------|
| Django | 4.2.20 | Web 框架 |
| Django REST Framework | 3.14.0 | RESTful API |
| MySQL | 8.0.41 | 数据库 |
| MediaPipe | 0.10.21 | 姿态检测后端库 |
| OpenCV | 4.6.0.66 | 计算机视觉 |
| djangorestframework-jwt | 1.11.0 | JWT 认证 |

## 项目结构

```
FitnessSystem/
├── 前端/                          # Vue 2 前端项目
│   └── customer/
│       ├── public/                # 静态资源
│       │   └── mediapipe/         # MediaPipe JS 库
│       └── src/
│           ├── api/               # API 请求封装
│           ├── assets/            # 图片资源
│           ├── components/         # 公共组件
│           ├── layout/             # 布局组件
│           ├── router/             # 路由配置
│           ├── store/              # Vuex 状态管理
│           ├── util/               # 工具函数
│           └── views/              # 页面组件
│               ├── user/          # 用户功能页面
│               ├── userCenter/    # 用户中心
│               ├── sys/           # 系统管理
│               └── healthAssistans/
│
├── 后端/                          # Django 后端项目
│   └── admin_project/
│       ├── admin_project/         # Django 项目配置
│       ├── fitness/               # 健身模块
│       │   ├── models.py          # 健身数据模型
│       │   ├── views.py           # 健身视图
│       │   ├── urls.py            # 路由配置
│       │   ├── dance_evaluation.py # 舞蹈评分算法
│       │   └── body_part_angle.py # 关节角度计算
│       ├── healthview/            # 健康模块
│       ├── user/                   # 用户模块
│       ├── role/                   # 角色权限模块
│       └── menu/                   # 菜单管理模块
│
└── 数据库/
    └── health.sql                 # MySQL 数据库脚本
```

## 功能模块

### 1. AI 姿态检测与动作计数

基于 MediaPipe Pose 提取 33 个人体关键点，实现以下功能：

- **实时摄像头检测**：通过摄像头实时捕捉用户动作
- **视频上传识别**：上传运动视频进行动作分析
- **动作类型支持**：俯卧撑、深蹲、开合跳、引体向上、仰卧起坐、波比跳、跑步、跳绳等 14 种运动
- **自动计数**：基于关节角度阈值切换状态机，准确率 95%+

### 2. 舞蹈评分系统

通过 AI 算法对用户舞蹈动作进行评估：

- **标准舞蹈库**：预置舞蹈标准模板
- **关键点提取**：从标准视频中提取骨骼关键点
- **动态角度学习**：自动学习舞蹈动作的关节角度标准
- **多维度评分**：
  - 准确度评分 (Accuracy)
  - 节奏评分 (Rhythm)
  - 流畅度评分 (Fluency)
  - 阶段评分 (Phase-level)
- **改进建议**：根据薄弱环节生成个性化改进提示

### 3. 卡路里计算

基于 MET (代谢当量) 公式计算运动消耗：

```
卡路里 = MET值 × 体重(kg) × 运动时长(h)
```

支持根据运动类型和用户体重动态计算。

### 4. 健康打卡与数据可视化

- **打卡记录**：体重、睡眠时长、运动时长
- **趋势分析**：ECharts 可视化健康数据趋势
- **健康建议**：基于打卡数据生成个性化健康反馈

### 5. 健康资讯

- 健康新闻浏览
- 文章评论互动
- 资讯分类管理

### 6. 用户中心

- 个人资料管理
- 头像上传
- 密码修改

### 7. 系统管理 (管理员)

- 用户管理
- 角色权限管理
- 菜单管理

## 数据库表结构

### 核心业务表

| 表名 | 说明 |
|------|------|
| `sys_user` | 用户信息表 |
| `sys_role` | 角色表 |
| `sys_menu` | 菜单表 |
| `sys_user_role` | 用户角色关联表 |
| `sys_role_menu` | 角色菜单权限关联表 |
| `news` | 健康新闻表 |
| `evaluations` | 评论表 |
| `health_data` | 健康打卡记录表 |
| `fitness_calorierecord` | 卡路里记录表 |
| `fitness_dance_standard` | 舞蹈标准模板表 |
| `fitness_dance_score` | 舞蹈评分记录表 |
| `fitness_annotated_video` | 标注视频表 |
| `fitness_annotated_frame` | 标注帧表 |

## API 接口

### 健身模块 `/api/`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/upload_video/` | POST | 上传视频进行动作识别 |
| `/api/real_time_detect/` | POST | 实时摄像头检测 |
| `/api/calorie_record_data/` | GET | 获取月度卡路里数据 |
| `/api/get_dance_standards/` | GET | 获取舞蹈标准列表 |
| `/api/preprocess_dance/` | POST | 预处理舞蹈视频 |
| `/api/dance_evaluate/` | POST | 舞蹈评分 |
| `/api/get_task_status/` | GET | 获取任务状态 |

### 健康模块 `/health/`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/health/get_health_news/` | GET | 获取健康新闻 |
| `/health/get_news_detail/<id>/` | GET | 获取新闻详情 |
| `/health/comment_list/<content_id>/` | GET/POST | 评论列表/发表 |
| `/health/health_checkin/` | POST | 健康打卡 |
| `/health/get_health_data/<user_id>/` | GET | 获取健康数据 |

### 用户模块 `/user/`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/user/login/` | POST | 用户登录 |
| `/user/register/` | POST | 用户注册 |
| `/user/save/` | POST | 更新用户信息 |
| `/user/pwd/` | POST | 修改密码 |
| `/user/image/` | POST | 上传头像 |

## 快速开始

### 环境要求

- Node.js >= 14.x
- Python 3.9+
- MySQL 8.0+

### 1. 数据库配置

```sql
-- 创建数据库
CREATE DATABASE health CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 导入数据
mysql -u root -p health < 数据库/health.sql
```

### 2. 后端部署

```bash
cd 后端/admin_project

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置数据库连接 (修改 settings.py 中的 DATABASES)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'health',
#         'USER': 'root',
#         'PASSWORD': 'your_password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# 数据库迁移
python manage.py migrate

# 运行服务器
python manage.py runserver
```

### 3. 前端部署

```bash
cd 前端/customer

# 安装依赖
npm install

# 开发模式
npm run serve

# 生产构建
npm run build
```

### 4. 访问系统

- 前端地址：http://localhost:8080
- 后端地址：http://localhost:8000

## 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 用户 | user1 | user123 |

## 项目亮点

1. **AI 姿态检测**：MediaPipe Pose 提取 33 个人体关键点，基于关节角度实现高精度动作识别
2. **智能舞蹈评分**：多维度评分算法，自动学习舞蹈标准，生成改进建议
3. **卡路里精准计算**：基于 MET 代谢当量模型，结合用户体征数据
4. **健康趋势分析**：ECharts 可视化打卡数据，智能生成健康反馈
5. **RBAC 权限管理**：完整的角色权限控制体系

## License

MIT License
