<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <div class="header">
      <h1>管理员后台</h1>
      <p>欢迎回来，{{ adminName }}！</p>
    </div>

    <!-- Stats Overview -->
    <el-row :gutter="20" class="overview">
      <el-col :span="6">
        <div class="overview-card users">
          <div class="stat-icon blue">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
          </div>
          <div class="stat-content">
            <h3>用户总数</h3>
            <p>{{ stats.users }}</p>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card new-users">
          <div class="stat-icon pink">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="8.5" cy="7" r="4"/>
              <line x1="20" y1="8" x2="20" y2="14"/>
              <line x1="23" y1="11" x2="17" y2="11"/>
            </svg>
          </div>
          <div class="stat-content">
            <h3>今日新增</h3>
            <p>{{ stats.newUsers }}</p>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card articles">
          <div class="stat-icon teal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
          </div>
          <div class="stat-content">
            <h3>健康资讯</h3>
            <p>{{ stats.articles }}</p>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card comments">
          <div class="stat-icon coral">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <div class="stat-content">
            <h3>评论总数</h3>
            <p>{{ stats.comments }}</p>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      adminName: "超级管理员",
      stats: {
        users: 0,
        newUsers: 0,
        articles: 0,
        comments: 0,
      },
    };
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const token =
          sessionStorage.getItem("token") || localStorage.getItem("token");
        if (!token) {
          console.error("Token 不存在，请先登录！");
          return;
        }

        const response = await axios.get(
          "http://127.0.0.1:8000/user/admin/status/",
          {
            headers: {
              Authorization: `Bearer ${token}`, // 携带 Token
            },
          }
        );
        const userMessage = JSON.parse(sessionStorage.getItem("userMessage"));
        this.adminName = userMessage.username;
        this.stats = response.data;
      } catch (error) {
        console.error("获取数据失败:", error);
      }
    },
    goTo(route) {
      this.$router.push({
        name: route, // 使用路由的name字段进行跳转
      });
    },
  },
};
</script>

<style scoped>
.admin-dashboard {
  padding: var(--space-xl);
  background: var(--bg-base);
  min-height: calc(100vh - 64px);
}

/* Header */
.header {
  margin-bottom: var(--space-xl);

  h1 {
    font-size: 24px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: var(--space-xs);
  }

  p {
    font-size: 14px;
    color: var(--text-secondary);
  }
}

/* Stats Overview */
.overview {
  margin-bottom: var(--space-lg);
}

.overview-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
  padding: var(--space-xl);
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  transition: var(--transition-base);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  }

  &:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
  }

  &.users::before { background: var(--gradient-hero); }
  &.new-users::before { background: var(--gradient-accent); }
  &.articles::before { background: var(--gradient-tech); }
  &.comments::before { background: var(--gradient-energy); }
}

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  svg {
    width: 26px;
    height: 26px;
  }

  &.blue { background: rgba(67, 97, 238, 0.1); color: var(--primary); }
  &.pink { background: rgba(247, 37, 133, 0.1); color: var(--accent-coral); }
  &.teal { background: rgba(6, 214, 160, 0.1); color: var(--secondary); }
  &.coral { background: rgba(255, 107, 107, 0.1); color: var(--primary-accent); }
}

.stat-content {
  h3 {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: var(--space-xs);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  p {
    font-size: 28px;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1;
  }
}

router-link {
  text-decoration: none;
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: var(--space-md);
  }

  .overview-card {
    padding: var(--space-lg);
  }

  .stat-icon {
    width: 44px;
    height: 44px;
    svg { width: 22px; height: 22px; }
  }

  .stat-content p {
    font-size: 22px;
  }
}
</style>
