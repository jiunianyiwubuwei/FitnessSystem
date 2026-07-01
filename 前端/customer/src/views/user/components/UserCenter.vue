<template>
  <div class="profile-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
          个人中心
        </h1>
        <p class="hero-subtitle">管理您的账户信息和偏好设置</p>
      </div>
    </div>

    <!-- Profile Content -->
    <div class="profile-content">
      <!-- Avatar Card -->
      <div class="card avatar-card">
        <div class="avatar-section">
          <div class="avatar-wrapper" @click="$refs.avatarInput.click()">
            <img :src="userInfo.avatar || defaultAvatar" class="avatar-img" />
            <div class="avatar-overlay">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                <circle cx="12" cy="13" r="4"/>
              </svg>
              <span>更换头像</span>
            </div>
            <input
              type="file"
              ref="avatarInput"
              style="display: none"
              @change="handleAvatarUpload"
              accept="image/*"
            />
          </div>
          <div class="avatar-info">
            <h3 class="username">{{ userInfo.username }}</h3>
            <span class="user-role">运动爱好者</span>
          </div>
        </div>
      </div>

      <!-- Profile Edit Card -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            修改个人信息
          </h3>
        </div>
        <div class="card-body">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">用户名</label>
              <input
                type="text"
                class="form-input"
                v-model="userInfo.username"
                placeholder="用户名"
              />
            </div>
            <div class="form-group">
              <label class="form-label">邮箱</label>
              <input
                type="email"
                class="form-input"
                v-model="userInfo.email"
                placeholder="电子邮箱"
              />
            </div>
            <div class="form-group">
              <label class="form-label">手机号</label>
              <input
                type="text"
                class="form-input"
                v-model="userInfo.phonenumber"
                placeholder="手机号码"
              />
            </div>
          </div>
          <div class="form-actions">
            <button class="action-btn primary" @click="saveUserInfo">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                <polyline points="17 21 17 13 7 13 7 21"/>
                <polyline points="7 3 7 8 15 8"/>
              </svg>
              保存信息
            </button>
          </div>
        </div>
      </div>

      <!-- Password Change Card -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            修改密码
          </h3>
        </div>
        <div class="card-body">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">旧密码</label>
              <input
                type="password"
                class="form-input"
                v-model="passwordData.oldPassword"
                placeholder="请输入旧密码"
              />
            </div>
            <div class="form-group">
              <label class="form-label">新密码</label>
              <input
                type="password"
                class="form-input"
                v-model="passwordData.newPassword"
                placeholder="请输入新密码"
              />
            </div>
          </div>
          <div class="form-actions">
            <button class="action-btn danger" @click="changePassword">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              修改密码
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import defaultAvatar from "@/assets/默认头像.jpg";

export default {
  name: "UserCenter",
  data() {
    return {
      userInfo: {
        id: null,
        username: "",
        email: "",
        phonenumber: "",
        avatar: "",
        avatarFile: null,
      },
      passwordData: {
        id: null,
        oldPassword: "",
        newPassword: "",
      },
      token: "",
      defaultAvatar,
    };
  },
  created() {
    this.loadUserInfo();
  },
  methods: {
    loadUserInfo() {
      const user = JSON.parse(sessionStorage.getItem("userMessage"));
      const token = sessionStorage.getItem("token");
      if (user) {
        this.userInfo = { ...user };
        this.passwordData.id = user.id;
        this.token = token;
      }
    },

    handleAvatarUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.userInfo.avatarFile = file;
        this.userInfo.avatar = URL.createObjectURL(file);
      }
    },

    async saveUserInfo() {
      try {
        const token = sessionStorage.getItem("token");
        const response = await axios.post(
          "http://127.0.0.1:8000/user/save/",
          this.userInfo,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (response.data.code === 200) {
          this.$message.success("信息修改成功");
          sessionStorage.setItem("userMessage", JSON.stringify(this.userInfo));
        } else {
          this.$message.error("修改失败：" + response.data.message);
        }
      } catch (error) {
        console.error("信息修改失败：", error);
        this.$message.error("修改失败，请重试");
      }
    },

    async changePassword() {
      if (!this.passwordData.oldPassword || !this.passwordData.newPassword) {
        this.$message.warning("请填写完整信息");
        return;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/user/updateUserPwd/",
          {
            id: this.passwordData.id,
            oldPassword: this.passwordData.oldPassword,
            newPassword: this.passwordData.newPassword,
          },
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
              "Content-Type": "application/json",
            },
          }
        );
        if (response.data.code === 200) {
          this.$message.success("密码修改成功");
          this.passwordData.oldPassword = "";
          this.passwordData.newPassword = "";
        } else {
          this.$message.error("密码修改失败：" + (response.data.errorInfo || "未知错误"));
        }
      } catch (error) {
        console.error("密码修改失败：", error);
        this.$message.error("密码修改失败，请重试");
      }
    },
  },
};
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

/* Hero Section */
.hero-section {
  text-align: center;
  padding: var(--space-2xl) 0;
}

.hero-content {
  display: inline-block;
}

.hero-icon {
  width: 36px;
  height: 36px;
  color: var(--primary-accent);
  vertical-align: middle;
  margin-right: var(--space-sm);
}

.hero-title {
  font-size: 28px;
  font-weight: 800;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-sm);
}

.hero-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

/* Profile Content */
.profile-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
  padding-bottom: var(--space-2xl);
}

/* Avatar Card */
.avatar-card {
  padding: var(--space-xl);
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: var(--space-xl);
}

.avatar-wrapper {
  position: relative;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  cursor: pointer;
  overflow: hidden;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid var(--border);
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: var(--transition-fast);
  color: white;
  border-radius: 50%;
}

.avatar-overlay svg {
  width: 24px;
  height: 24px;
  margin-bottom: 4px;
}

.avatar-overlay span {
  font-size: 11px;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.avatar-info {
  flex: 1;
}

.username {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 var(--space-xs);
}

.user-role {
  display: inline-block;
  padding: 4px 12px;
  background: var(--primary-glow);
  color: var(--primary-accent);
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-full);
}

/* Card */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.card-header {
  padding: var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--border-light);
  background: var(--bg-base);
}

.card-title {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card-title svg {
  width: 18px;
  height: 18px;
  color: var(--primary-accent);
}

.card-body {
  padding: var(--space-lg);
}

/* Form */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-md);
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-sm);
}

.form-input {
  padding: 12px var(--space-md);
  font-size: 14px;
  font-family: var(--font-sans);
  background: var(--bg-base);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  transition: var(--transition-fast);
}

.form-input:focus {
  border-color: var(--primary-accent);
  background: var(--bg-card);
  box-shadow: 0 0 0 3px var(--primary-glow);
  outline: none;
}

.form-actions {
  margin-top: var(--space-lg);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--border-light);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 12px var(--space-xl);
  font-size: 14px;
  font-weight: 500;
  font-family: var(--font-sans);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-fast);
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn.primary {
  background: var(--gradient-tech);
  color: white;
  box-shadow: 0 2px 8px rgba(6, 182, 212, 0.25);
}

.action-btn.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.35);
}

.action-btn.danger {
  background: var(--bg-base);
  color: var(--danger);
  border: 1px solid var(--danger);
}

.action-btn.danger:hover {
  background: var(--danger-light);
}

@media (max-width: 640px) {
  .avatar-section {
    flex-direction: column;
    text-align: center;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
