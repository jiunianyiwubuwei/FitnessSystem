<template>
  <div class="login-page">
    <!-- Decorative background shapes -->
    <div class="bg-shape shape-ring shape-ring-1"></div>
    <div class="bg-shape shape-ring shape-ring-2"></div>
    <div class="bg-shape shape-dot-grid"></div>
    <div class="bg-shape shape-squiggly shape-squiggly-1"></div>
    <div class="bg-shape shape-squiggly shape-squiggly-2"></div>

    <div class="login-container">
      <!-- Left Brand Panel -->
      <div class="brand-panel">
        <div class="brand-bg-art" aria-hidden="true">
          <!-- Decorative sports elements -->
          <svg class="art-dumbbell art-dumbbell-1" viewBox="0 0 80 24" fill="none">
            <rect x="0" y="8" width="18" height="8" rx="4" fill="rgba(255,255,255,0.25)"/>
            <rect x="18" y="10" width="44" height="4" rx="2" fill="rgba(255,255,255,0.3)"/>
            <rect x="62" y="8" width="18" height="8" rx="4" fill="rgba(255,255,255,0.25)"/>
          </svg>
          <svg class="art-dumbbell art-dumbbell-2" viewBox="0 0 80 24" fill="none">
            <rect x="0" y="8" width="18" height="8" rx="4" fill="rgba(255,255,255,0.2)"/>
            <rect x="18" y="10" width="44" height="4" rx="2" fill="rgba(255,255,255,0.25)"/>
            <rect x="62" y="8" width="18" height="8" rx="4" fill="rgba(255,255,255,0.2)"/>
          </svg>
          <svg class="art-circle art-circle-1" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="22" stroke="rgba(255,255,255,0.15)" stroke-width="2" stroke-dasharray="6 4"/>
          </svg>
          <svg class="art-circle art-circle-2" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="18" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
          </svg>
          <svg class="art-running-track" viewBox="0 0 120 60" fill="none">
            <rect x="10" y="10" width="100" height="40" rx="20" stroke="rgba(255,255,255,0.12)" stroke-width="2"/>
            <rect x="30" y="20" width="60" height="20" rx="10" stroke="rgba(255,255,255,0.08)" stroke-width="1.5"/>
          </svg>
          <svg class="art-lightning" viewBox="0 0 24 36" fill="none">
            <path d="M14 2 L4 20 H12 L10 34 L20 14 H12 L14 2Z" fill="rgba(255,255,255,0.18)" stroke="rgba(255,255,255,0.12)" stroke-width="1" stroke-linejoin="round"/>
          </svg>
          <svg class="art-arm arm-left" viewBox="0 0 60 80" fill="none">
            <!-- Stylized arm doing bicep curl -->
            <circle cx="30" cy="10" r="8" fill="rgba(255,255,255,0.2)" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <path d="M30 18 L30 45" stroke="rgba(255,255,255,0.3)" stroke-width="4" stroke-linecap="round"/>
            <path d="M30 30 L18 38" stroke="rgba(255,255,255,0.3)" stroke-width="4" stroke-linecap="round"/>
            <path d="M30 45 L22 60" stroke="rgba(255,255,255,0.25)" stroke-width="4" stroke-linecap="round"/>
            <circle cx="30" cy="10" r="3" fill="rgba(255,255,255,0.3)"/>
            <circle cx="18" cy="38" r="3" fill="rgba(255,255,255,0.25)"/>
          </svg>
          <svg class="art-arm arm-right" viewBox="0 0 60 80" fill="none">
            <circle cx="30" cy="10" r="8" fill="rgba(255,255,255,0.18)" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
            <path d="M30 18 L30 45" stroke="rgba(255,255,255,0.25)" stroke-width="4" stroke-linecap="round"/>
            <path d="M30 30 L42 38" stroke="rgba(255,255,255,0.25)" stroke-width="4" stroke-linecap="round"/>
            <path d="M30 45 L38 60" stroke="rgba(255,255,255,0.2)" stroke-width="4" stroke-linecap="round"/>
            <circle cx="30" cy="10" r="3" fill="rgba(255,255,255,0.25)"/>
            <circle cx="42" cy="38" r="3" fill="rgba(255,255,255,0.2)"/>
          </svg>
        </div>

        <div class="brand-content">
          <div class="logo-wrap">
            <el-image class="brand-logo" src="/logo.png" fit="contain"></el-image>
          </div>
          <h1 class="brand-title">MyAction</h1>
          <p class="brand-subtitle">您的个人智能运动管家</p>

          <div class="motion-trail" aria-hidden="true">
            <div class="trail-dot trail-dot-1"></div>
            <div class="trail-dot trail-dot-2"></div>
            <div class="trail-dot trail-dot-3"></div>
          </div>

          <div class="feature-list">
            <div class="feature-item">
              <div class="feature-pill">
                <svg viewBox="0 0 20 20" fill="none">
                  <path d="M10 2C10 2 4 6 4 11C4 14.31 6.69 17 10 17C13.31 17 16 14.31 16 11C16 6 10 2 10 2Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
                  <path d="M10 17L7 21L10 20L13 21L10 17Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" fill="rgba(255,255,255,0.3)"/>
                </svg>
              </div>
              <span>精准动作识别</span>
            </div>
            <div class="feature-item">
              <div class="feature-pill">
                <svg viewBox="0 0 20 20" fill="none">
                  <path d="M2 13L6 9L9 12L13 7L18 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle cx="6" cy="9" r="1.5" fill="currentColor"/>
                  <circle cx="9" cy="12" r="1.5" fill="currentColor"/>
                  <circle cx="13" cy="7" r="1.5" fill="currentColor"/>
                </svg>
              </div>
              <span>运动数据可视化</span>
            </div>
            <div class="feature-item">
              <div class="feature-pill">
                <svg viewBox="0 0 20 20" fill="none">
                  <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
                  <path d="M10 7L10 10L12.5 12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </div>
              <span>随时随地开练</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Form Panel -->
      <div class="form-panel">
        <div class="form-card">
          <div class="form-header">
            <div class="form-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                <polyline points="10 17 15 12 10 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="15" y1="12" x2="3" y2="12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
              </svg>
            </div>
            <h2 class="form-title">欢迎回来</h2>
            <p class="form-desc">登录 MyAction，开启今日运动</p>
          </div>

          <form class="login-form" @submit.prevent="handleLogin">
            <div class="field-group" :class="{ 'has-error': usernameError }">
              <label class="field-label">用户名</label>
              <div class="field-wrap" :class="{ focused: usernameFocused }">
                <span class="field-prefix">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                </span>
                <input
                  class="field-input"
                  type="text"
                  placeholder="请输入用户名"
                  v-model="username"
                  @focus="usernameFocused = true"
                  @blur="usernameFocused = false"
                  autocomplete="username"
                />
              </div>
              <p class="field-error" v-if="usernameError">{{ usernameError }}</p>
            </div>

            <div class="field-group" :class="{ 'has-error': passwordError }">
              <label class="field-label">密码</label>
              <div class="field-wrap" :class="{ focused: passwordFocused }">
                <span class="field-prefix">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                </span>
                <input
                  class="field-input"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="请输入密码"
                  v-model="password"
                  @focus="passwordFocused = true"
                  @blur="passwordFocused = false"
                  autocomplete="current-password"
                />
                <button type="button" class="field-suffix" @click="showPassword = !showPassword">
                  <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                </button>
              </div>
              <p class="field-error" v-if="passwordError">{{ passwordError }}</p>
            </div>

            <div class="form-options">
              <label class="check-option">
                <input type="checkbox" v-model="rememberMe" />
                <span class="check-box"></span>
                <span class="check-label">记住我</span>
              </label>
              <a class="forgot-link" href="#">忘记密码？</a>
            </div>

            <button
              type="submit"
              class="submit-btn"
              :class="{ loading: isLoading }"
              :disabled="isLoading"
            >
              <span class="btn-bg-flow"></span>
              <span class="btn-inner">
                <span v-if="!isLoading">开始训练</span>
                <span v-else class="btn-loading">
                  <span class="spinner"></span>
                  登录中...
                </span>
              </span>
            </button>
          </form>

          <div class="form-footer-text">
            还没有账户？
            <span class="register-link" @click="redirectToRegister">立即加入</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { post } from "@/util/request.js";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      isLoading: false,
      rememberMe: false,
      showPassword: false,
      usernameFocused: false,
      passwordFocused: false,
      usernameError: "",
      passwordError: "",
    };
  },
  methods: {
    validate() {
      this.usernameError = "";
      this.passwordError = "";
      let valid = true;
      if (!this.username.trim()) {
        this.usernameError = "请输入用户名";
        valid = false;
      }
      if (!this.password) {
        this.passwordError = "请输入密码";
        valid = false;
      } else if (this.password.length < 6) {
        this.passwordError = "密码长度不能少于 6 位";
        valid = false;
      }
      return valid;
    },

    async handleLogin() {
      if (!this.validate()) return;

      this.isLoading = true;
      const loginData = {
        username: this.username.trim(),
        password: this.password,
      };

      try {
        const response = await post("user/login/", loginData);
        if (response.data.code === 200) {
          this.$message.success("登录成功");
          window.sessionStorage.setItem("token", response.data.token);
          const userMessage = {
            ...response.data.user,
            roles: response.data.roles,
          };
          window.sessionStorage.setItem("userMessage", JSON.stringify(userMessage));
          window.sessionStorage.setItem("menuList", JSON.stringify(response.data.menulist));

          if (response.data.user.id === 1) {
            this.$router.push("/admin");
          } else {
            this.$router.push("/main");
          }
        } else {
          this.$message.error("登录失败，请检查账号或密码");
        }
      } catch (error) {
        console.error("登录请求失败", error);
        this.$message.error("登录失败，请稍后再试");
      } finally {
        this.isLoading = false;
      }
    },

    redirectToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>

<style lang="scss" scoped>
/* Page wrapper */
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F2F5FF;
  position: relative;
  overflow: hidden;
  padding: var(--space-lg);
}

/* Background decorative shapes */
.bg-shape { position: absolute; pointer-events: none; }

.shape-ring {
  border-radius: 50%;
}
.shape-ring-1 {
  width: 700px;
  height: 700px;
  top: -250px;
  right: -200px;
  border: 2px solid rgba(67, 97, 238, 0.06);
  background: radial-gradient(circle, rgba(67, 97, 238, 0.04) 0%, transparent 70%);
}
.shape-ring-2 {
  width: 400px;
  height: 400px;
  bottom: -100px;
  left: -100px;
  border: 1.5px solid rgba(6, 214, 160, 0.06);
  background: radial-gradient(circle, rgba(6, 214, 160, 0.03) 0%, transparent 70%);
}

.shape-dot-grid {
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: radial-gradient(circle, rgba(67, 97, 238, 0.08) 1.5px, transparent 1.5px);
  background-size: 32px 32px;
}

.shape-squiggly {
  opacity: 0.5;
}
.shape-squiggly-1 {
  top: 15%;
  right: 5%;
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, rgba(247, 37, 133, 0.08), rgba(67, 97, 238, 0.05));
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  animation: morphShape 8s ease-in-out infinite;
}
.shape-squiggly-2 {
  bottom: 10%;
  left: 8%;
  width: 80px;
  height: 80px;
  background: linear-gradient(45deg, rgba(6, 214, 160, 0.08), rgba(67, 97, 238, 0.04));
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
  animation: morphShape 10s ease-in-out infinite reverse;
}

@keyframes morphShape {
  0%, 100% { border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }
  50% { border-radius: 70% 30% 30% 70% / 70% 70% 30% 30%; }
}

/* Main container */
.login-container {
  display: flex;
  width: 960px;
  max-width: 100%;
  min-height: 560px;
  background: white;
  border-radius: 28px;
  overflow: hidden;
  position: relative;
  z-index: 1;
  box-shadow:
    0 4px 6px rgba(67, 97, 238, 0.04),
    0 20px 60px rgba(67, 97, 238, 0.1),
    0 1px 3px rgba(0, 0, 0, 0.04);
  animation: containerReveal 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes containerReveal {
  from { opacity: 0; transform: translateY(20px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

/* ══ Brand Panel ══ */
.brand-panel {
  flex: 0 0 42%;
  background: linear-gradient(145deg, #6675F6 0%, #4361EE 40%, #4CC9F0 100%);
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
    background:
      radial-gradient(ellipse at 20% 80%, rgba(247, 37, 133, 0.18) 0%, transparent 55%),
      radial-gradient(ellipse at 80% 20%, rgba(6, 214, 160, 0.15) 0%, transparent 55%);
    pointer-events: none;
  }
}

.brand-bg-art {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.art-dumbbell {
  position: absolute;
  opacity: 0.7;
}
.art-dumbbell-1 {
  width: 100px;
  top: 12%;
  right: 8%;
  animation: floatDumbbell 5s ease-in-out infinite;
  transform-origin: center;
}
.art-dumbbell-2 {
  width: 70px;
  bottom: 18%;
  left: 6%;
  animation: floatDumbbell 7s ease-in-out infinite 1s;
}

.art-circle {
  position: absolute;
}
.art-circle-1 {
  width: 120px;
  top: -20px;
  right: -20px;
  animation: rotateArt 20s linear infinite;
  transform-origin: 60px 60px;
}
.art-circle-2 {
  width: 80px;
  bottom: 10%;
  right: 15%;
  animation: rotateArt 15s linear infinite reverse;
  transform-origin: 40px 40px;
}

.art-running-track {
  position: absolute;
  width: 140px;
  top: 55%;
  left: -10px;
  animation: floatTrack 6s ease-in-out infinite;
}

.art-lightning {
  position: absolute;
  width: 28px;
  top: 30%;
  left: 12%;
  animation: flashLightning 3s ease-in-out infinite;
  opacity: 0.8;
}

.art-arm {
  position: absolute;
  opacity: 0.6;
}
.arm-left {
  width: 60px;
  bottom: 25%;
  right: 5%;
  animation: armSwing 4s ease-in-out infinite;
  transform-origin: bottom center;
}
.arm-right {
  width: 50px;
  top: 20%;
  left: 8%;
  animation: armSwing 4s ease-in-out infinite 2s;
  transform-origin: bottom center;
}

@keyframes floatDumbbell {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-8px) rotate(3deg); }
}
@keyframes rotateArt {
  to { transform: rotate(360deg); }
}
@keyframes floatTrack {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(8px); }
}
@keyframes flashLightning {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  10% { opacity: 0.9; transform: scale(1.1); }
  20% { opacity: 0.3; }
  30% { opacity: 0.9; transform: scale(1.05); }
  40% { opacity: 0.3; }
}
@keyframes armSwing {
  0%, 100% { transform: rotate(-5deg); }
  50% { transform: rotate(8deg); }
}

.brand-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
  animation: contentRise 0.7s ease-out;
}

@keyframes contentRise {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: translateY(0); }
}

.logo-wrap {
  width: 76px;
  height: 76px;
  margin: 0 auto var(--space-lg);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.15);
  border: 1.5px solid rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: logoBounce 3s ease-in-out infinite;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(67, 97, 238, 0.3);
}

.brand-logo {
  width: 52px;
  height: 52px;
}

@keyframes logoBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.brand-title {
  font-size: 36px;
  font-weight: 800;
  color: white;
  letter-spacing: 2px;
  margin-bottom: 6px;
  text-shadow: 0 2px 12px rgba(67, 97, 238, 0.3);
}

.brand-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.72);
  letter-spacing: 0.5px;
  margin-bottom: var(--space-xl);
}

/* Motion trail dots */
.motion-trail {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-bottom: var(--space-xl);
}

.trail-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  animation: trailBounce 1.4s ease-in-out infinite;

  &.trail-dot-2 { animation-delay: 0.2s; width: 10px; height: 10px; background: rgba(255, 255, 255, 0.7); }
  &.trail-dot-3 { animation-delay: 0.4s; }
}

@keyframes trailBounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
  40% { transform: translateY(-8px); opacity: 1; }
}

/* Feature list */
.feature-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(8px);
  text-align: left;
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  letter-spacing: 0.3px;
  transition: background 0.2s, transform 0.2s;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateX(4px);
  }
}

.feature-pill {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  svg {
    width: 16px;
    height: 16px;
    color: white;
  }
}

/* ══ Form Panel ══ */
.form-panel {
  flex: 1;
  padding: var(--space-2xl);
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-card {
  width: 100%;
  max-width: 360px;
  animation: cardRise 0.7s ease-out 0.1s both;
}

@keyframes cardRise {
  from { opacity: 0; transform: translateY(18px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-header {
  margin-bottom: var(--space-xl);
}

.form-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(67, 97, 238, 0.1), rgba(6, 214, 160, 0.08));
  border: 1.5px solid rgba(67, 97, 238, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-md);
  color: #4361EE;

  svg { width: 22px; height: 22px; }
}

.form-title {
  font-size: 24px;
  font-weight: 700;
  color: #1B1F3B;
  margin-bottom: 4px;
  letter-spacing: -0.3px;
}

.form-desc {
  font-size: 13px;
  color: #9499B3;
}

/* Form fields */
.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 12px;
  font-weight: 600;
  color: #5A6082;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.field-wrap {
  position: relative;
  display: flex;
  align-items: center;
  background: #F4F6FB;
  border: 1.5px solid #DDE1F0;
  border-radius: 12px;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;

  &.focused {
    border-color: #4361EE;
    background: white;
    box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
  }

  .has-error & {
    border-color: rgba(247, 37, 133, 0.4);
    background: rgba(247, 37, 133, 0.02);
  }
}

.field-prefix {
  width: 18px;
  height: 18px;
  color: #9499B3;
  padding-left: 14px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s;

  svg { width: 100%; height: 100%; }

  .field-wrap.focused & {
    color: #4361EE;
  }
}

.field-input {
  flex: 1;
  padding: 13px 10px;
  font-size: 14px;
  font-family: var(--font-sans);
  background: transparent;
  border: none;
  outline: none;
  color: #1B1F3B;
  caret-color: #4361EE;

  &::placeholder {
    color: #B0B5CC;
  }
}

.field-suffix {
  width: 20px;
  height: 20px;
  margin-right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #9499B3;
  padding: 0;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s;

  &:hover { color: #5A6082; }
  svg { width: 100%; height: 100%; }
}

.field-error {
  font-size: 11px;
  color: #F72585;
  padding-left: 2px;
}

/* Options row */
.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.check-option {
  display: flex;
  align-items: center;
  gap: 7px;
  cursor: pointer;
  user-select: none;

  input[type="checkbox"] { display: none; }
}

.check-box {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1.5px solid #DDE1F0;
  background: #F4F6FB;
  transition: border-color 0.2s, background 0.2s;
  position: relative;
  flex-shrink: 0;

  .check-option input:checked + & {
    background: linear-gradient(135deg, #6675F6, #4361EE);
    border-color: transparent;
    box-shadow: 0 2px 6px rgba(67, 97, 238, 0.3);

    &::after {
      content: '';
      position: absolute;
      left: 4px;
      top: 2px;
      width: 5px;
      height: 8px;
      border: 2px solid white;
      border-top: none;
      border-left: none;
      transform: rotate(45deg);
    }
  }
}

.check-label {
  font-size: 12px;
  color: #9499B3;
}

.forgot-link {
  font-size: 12px;
  color: #4361EE;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
  cursor: pointer;

  &:hover { color: #6675F6; text-decoration: underline; }
}

/* Submit button */
.submit-btn {
  width: 100%;
  padding: 15px;
  font-size: 15px;
  font-weight: 700;
  font-family: var(--font-sans);
  letter-spacing: 1px;
  color: white;
  background: linear-gradient(135deg, #6675F6, #4361EE, #4CC9F0);
  background-size: 200% 100%;
  background-position: 0% 50%;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: background-position 0.5s ease, transform 0.2s, box-shadow 0.3s;
  margin-top: 4px;

  &:hover:not(:disabled) {
    background-position: 100% 50%;
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(67, 97, 238, 0.35);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.btn-bg-flow {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
  opacity: 0;
  transition: opacity 0.3s;

  .submit-btn:hover & { opacity: 1; }
}

.btn-inner {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.25);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Footer text */
.form-footer-text {
  text-align: center;
  margin-top: var(--space-xl);
  padding-top: var(--space-lg);
  border-top: 1.5px solid #F0F2FA;
  font-size: 13px;
  color: #9499B3;
}

.register-link {
  color: #4361EE;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s;

  &:hover {
    color: #F72585;
    text-decoration: underline;
  }
}

/* ══ Responsive ══ */
@media (max-width: 768px) {
  .login-page { padding: 0; }

  .login-container {
    flex-direction: column;
    min-height: 100vh;
    border-radius: 0;
    box-shadow: none;
  }

  .brand-panel {
    flex: 0 0 auto;
    padding: var(--space-xl);
    min-height: 200px;

    .feature-list { display: none; }
    .motion-trail { display: none; }
  }

  .form-panel {
    padding: var(--space-xl) var(--space-lg);
  }
}
</style>
