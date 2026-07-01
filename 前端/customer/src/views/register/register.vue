<template>
  <div class="register-page">
    <div class="register-container">
      <div class="brand-panel">
        <div class="brand-content">
          <div class="logo">
            <el-image style="width: 64px; height: 64px" src="/logo.png" fit="contain"></el-image>
          </div>
          <h1 class="brand-title">MyAction</h1>
          <p class="brand-subtitle">开启您的智能健身之旅</p>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-value">100+</span>
              <span class="stat-label">运动类型</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">AI</span>
              <span class="stat-label">智能识别</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">24/7</span>
              <span class="stat-label">随时运动</span>
            </div>
          </div>
        </div>
      </div>

      <div class="form-panel">
        <div class="form-wrapper">
          <div class="form-header">
            <h2>创建账户</h2>
            <p>填写以下信息完成注册</p>
          </div>

          <el-form ref="RegisterRef" @submit.prevent="handleRegister" class="register-form">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">用户名</label>
                <input
                  class="form-input"
                  placeholder="设置用户名"
                  v-model="form.username"
                />
              </div>
              <div class="form-group">
                <label class="form-label">邮箱</label>
                <input
                  class="form-input"
                  type="email"
                  placeholder="电子邮箱"
                  v-model="form.email"
                />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">手机号码</label>
              <input
                class="form-input"
                placeholder="手机号码"
                v-model="form.phone"
              />
            </div>

            <div class="form-group">
              <label class="form-label">密码</label>
              <input
                class="form-input"
                type="password"
                placeholder="设置密码"
                v-model="form.password"
              />
            </div>

            <div class="form-group">
              <label class="form-label">确认密码</label>
              <input
                class="form-input"
                type="password"
                placeholder="再次输入密码"
                v-model="form.confirmPassword"
              />
            </div>

            <div class="form-actions">
              <button type="submit" class="submit-btn" :class="{ loading: isLoading }" :disabled="isLoading">
                <span v-if="!isLoading">注 册</span>
                <span v-else class="btn-loader"></span>
              </button>
            </div>
          </el-form>

          <div class="form-footer">
            <p>已有账户？<span class="link" @click="redirectToLogin">立即登录</span></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { post } from "@/util/request.js";

export default {
  name: "RegisterPage",
  data() {
    return {
      form: {
        username: "",
        password: "",
        confirmPassword: "",
        email: "",
        phone: "",
        status: 1,
      },
      isLoading: false,
    };
  },
  methods: {
    async handleRegister() {
      if (!this.form.username) {
        this.$message.error("请输入用户名");
        return;
      }
      if (!this.form.password) {
        this.$message.error("请输入密码");
        return;
      }
      if (this.form.password !== this.form.confirmPassword) {
        this.$message.error("两次输入的密码不一致");
        return;
      }

      this.isLoading = true;

      try {
        const response = await post("user/register/", this.form);
        if (response.data.code === 200) {
          this.$message.success("注册成功");
          this.redirectToLogin();
        } else {
          this.$message.error(response.data.msg || "注册失败");
        }
      } catch (error) {
        console.error("注册请求失败", error);
        this.$message.error("注册失败，请稍后再试");
      } finally {
        this.isLoading = false;
      }
    },

    redirectToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>

<style lang="scss" scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-base);
  position: relative;
  overflow: hidden;
  padding: var(--space-lg);

  &::before {
    content: '';
    position: absolute;
    top: -30%;
    left: -15%;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(247, 37, 133, 0.07) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: -20%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(67, 97, 238, 0.06) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
  }
}

.register-container {
  display: flex;
  width: 960px;
  min-height: 580px;
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  position: relative;
  z-index: 1;
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ── Left Brand Panel ── */
.brand-panel {
  flex: 1;
  background: var(--gradient-accent);
  padding: var(--space-2xl);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }

  &::after {
    content: '';
    position: absolute;
    top: -60px;
    right: -60px;
    width: 280px;
    height: 280px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 50%;
  }
}

.brand-content {
  text-align: center;
  color: white;
  position: relative;
  z-index: 1;
}

.logo {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--space-lg);
  animation: pulse 3s ease-in-out infinite;
  border-radius: var(--radius-md);
  overflow: hidden;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.brand-title {
  font-size: 30px;
  font-weight: 800;
  letter-spacing: 2px;
  margin-bottom: var(--space-xs);
  color: white;
}

.brand-subtitle {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.65);
  margin-bottom: var(--space-2xl);
  letter-spacing: 0.5px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-sm);
  margin-top: var(--space-xl);
}

.stat-item {
  padding: var(--space-md);
  background: rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: var(--transition-base);

  &:hover {
    background: rgba(255, 255, 255, 0.14);
    transform: translateY(-3px);
  }
}

.stat-value {
  display: block;
  font-size: 22px;
  font-weight: 700;
  color: white;
  margin-bottom: var(--space-xs);
}

.stat-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.65);
  letter-spacing: 0.3px;
}

/* ── Right Form Panel ── */
.form-panel {
  flex: 1.2;
  padding: var(--space-2xl);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  overflow-y: auto;
}

.form-wrapper {
  width: 100%;
  max-width: 380px;
}

.form-header {
  text-align: center;
  margin-bottom: var(--space-xl);

  h2 {
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: var(--space-xs);
    letter-spacing: -0.3px;
  }

  p {
    font-size: 13px;
    color: var(--text-muted);
  }
}

.register-form {
  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-md);
  }

  .form-group {
    margin-bottom: var(--space-md);
  }

  .form-label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: var(--space-xs);
  }

  .form-input {
    width: 100%;
    padding: 12px 14px;
    font-size: 14px;
    font-family: var(--font-sans);
    background: var(--bg-base);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-md);
    transition: var(--transition-fast);
    color: var(--text-primary);

    &::placeholder {
      color: var(--text-muted);
    }

    &:focus {
      border-color: var(--primary);
      background: var(--bg-card);
      box-shadow: 0 0 0 3px var(--primary-glow);
      outline: none;
    }
  }
}

.form-actions {
  margin-top: var(--space-xl);
}

.submit-btn {
  width: 100%;
  padding: 13px;
  font-size: 14px;
  font-weight: 600;
  font-family: var(--font-sans);
  letter-spacing: 1px;
  color: white;
  background: var(--gradient-accent);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-base);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--gradient-hero);
    opacity: 0;
    transition: var(--transition-base);
  }

  span {
    position: relative;
    z-index: 1;
  }

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(247, 37, 133, 0.3);

    &::before {
      opacity: 1;
    }
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.btn-loader {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.form-footer {
  text-align: center;
  margin-top: var(--space-xl);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--border-light);

  p {
    font-size: 13px;
    color: var(--text-muted);
  }

  .link {
    color: var(--primary);
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition-fast);

    &:hover {
      color: var(--accent-coral);
      text-decoration: underline;
    }
  }
}

@media (max-width: 768px) {
  .register-container {
    flex-direction: column;
    width: 100%;
    min-height: auto;
    border-radius: var(--radius-lg);
  }

  .brand-panel {
    padding: var(--space-xl);
    min-height: 180px;

    .stats-grid {
      display: none;
    }
  }

  .form-panel {
    padding: var(--space-xl);
  }

  .register-form .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
