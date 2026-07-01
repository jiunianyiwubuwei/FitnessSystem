<template>
  <div id="app">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-container">
        <!-- Logo & Brand -->
        <router-link to="/main" class="brand">
          <div class="brand-icon">
            <el-image style="width: 32px; height: 32px" src="/logo.png" fit="contain"></el-image>
          </div>
          <span class="brand-text">MyAction</span>
        </router-link>

        <!-- Nav Links -->
        <div class="nav-links">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="nav-link"
            :class="{ active: isActive(link.path) }"
          >
            <span class="nav-icon" v-html="link.icon"></span>
            <span class="nav-text">{{ link.name }}</span>
          </router-link>
        </div>

        <!-- User Menu -->
        <div class="user-menu" @click="toggleDropdown" ref="userMenuRef">
          <div class="user-avatar">
            <img :src="userAvatar" alt="avatar" />
            <span class="user-status"></span>
          </div>
          <div class="user-info">
            <span class="user-name">{{ userName }}</span>
          </div>

          <!-- Dropdown -->
          <transition name="dropdown">
            <div v-if="showDropdown" class="dropdown-menu">
              <div class="dropdown-header">
                <span class="dropdown-name">{{ userName }}</span>
                <span class="dropdown-role">运动爱好者</span>
              </div>
              <div class="dropdown-divider"></div>
              <button class="dropdown-item" @click="goToProfile">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                个人中心
              </button>
              <button class="dropdown-item logout" @click="logout">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                退出登录
              </button>
            </div>
          </transition>
        </div>
      </div>
    </nav>

    <!-- Sub-page Content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-brand">
          <div class="footer-logo">
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.5"/>
              <circle cx="16" cy="8.5" r="1.8" fill="currentColor"/>
              <path d="M16 10.5 L16 16.5 L16 21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M16 11.5 L12.5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M12.5 15 L10.5 18.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M16 11.5 L19.5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M19.5 15 L21.5 18.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M16 21 L13.5 26" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M16 21 L18.5 26" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="16" cy="8.5" r="1.8" fill="currentColor"/>
              <circle cx="16" cy="16.5" r="1.2" fill="currentColor"/>
              <circle cx="12.5" cy="15" r="1.2" fill="currentColor"/>
              <circle cx="19.5" cy="15" r="1.2" fill="currentColor"/>
              <circle cx="10.5" cy="18.5" r="1.2" fill="currentColor"/>
              <circle cx="21.5" cy="18.5" r="1.2" fill="currentColor"/>
              <circle cx="13.5" cy="26" r="1.2" fill="currentColor"/>
              <circle cx="18.5" cy="26" r="1.2" fill="currentColor"/>
            </svg>
          </div>
          <span>FitMotion</span>
        </div>
        <div class="footer-links">
          <a href="#">隐私政策</a>
          <span class="divider">|</span>
          <a href="#">使用条款</a>
          <span class="divider">|</span>
          <a href="#">常见问题</a>
        </div>
        <div class="footer-copyright">
          © 2025 Chongqing Ability Limited Company. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import userAvatar from "@/assets/默认头像.jpg";

export default {
  name: "MainPage",
  data() {
    return {
      userAvatar: "",
      userName: "用户",
      showDropdown: false,
      navLinks: [
        {
          name: "健康资讯",
          path: "/main/health/news",
          icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>'
        },
        {
          name: "健康助手",
          path: "/has",
          icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
        },
        {
          name: "健康打卡",
          path: "/main/health/checkin",
          icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
        },
        {
          name: "智慧健身",
          path: "/main/health/fitness",
          icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6.5 6.5h11"/><path d="M6.5 17.5h11"/><path d="M3 12h3"/><path d="M18 12h3"/><path d="M6 8v8"/><path d="M18 8v8"/><circle cx="12" cy="12" r="2"/></svg>'
        },
        {
          name: "个人中心",
          path: "/main/health/myUser",
          icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
        }
      ]
    };
  },
  created() {
    this.loadUserInfo();
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
  },
  methods: {
    loadUserInfo() {
      const user = JSON.parse(sessionStorage.getItem("userMessage"));
      if (user && user.avatar) {
        this.userAvatar = user.avatar;
      } else {
        this.userAvatar = userAvatar;
      }
      if (user && user.username) {
        this.userName = user.username;
      }
    },

    isActive(path) {
      return this.$route.path.startsWith(path);
    },

    toggleDropdown(e) {
      e.stopPropagation();
      this.showDropdown = !this.showDropdown;
    },

    handleClickOutside(e) {
      if (this.$refs.userMenuRef && !this.$refs.userMenuRef.contains(e.target)) {
        this.showDropdown = false;
      }
    },

    goToProfile() {
      this.showDropdown = false;
      this.$router.push("/main/health/myUser");
    },

    logout() {
      this.showDropdown = false;
      sessionStorage.clear();
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-base);
}

/* Navigation Bar */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 12px rgba(67, 97, 238, 0.06);
}

.navbar-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-xl);
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  text-decoration: none;
  color: white;
  transition: var(--transition-fast);
}

.brand:hover {
  opacity: 0.9;
}

.brand-icon {
  width: 32px;
  height: 32px;
  color: var(--primary);
}

.brand-text {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--text-primary);
}

/* Nav Links */
.nav-links {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-sm) var(--space-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: var(--transition-fast);
  position: relative;
}

.nav-link:hover {
  color: var(--primary);
  background: var(--bg-elevated);
}

.nav-link.active {
  color: var(--primary);
  background: rgba(67, 97, 238, 0.08);
  font-weight: 600;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2.5px;
  background: var(--primary);
  border-radius: 1.5px;
}

.nav-icon {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon :deep(svg) {
  width: 100%;
  height: 100%;
}

.nav-text {
  white-space: nowrap;
}

/* User Menu */
.user-menu {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-fast);
  position: relative;
}

.user-menu:hover {
  background: var(--bg-elevated);
}

.user-avatar {
  position: relative;
  width: 34px;
  height: 34px;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--border);
  transition: var(--transition-fast);
}

.user-avatar:hover img {
  border-color: var(--primary);
}

.user-status {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 9px;
  height: 9px;
  background: var(--success);
  border-radius: 50%;
  border: 2px solid white;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

/* Dropdown Menu */
.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 180px;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-light);
  overflow: hidden;
  z-index: 1000;
}

.dropdown-header {
  padding: var(--space-md);
  background: var(--bg-base);
}

.dropdown-name {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.dropdown-role {
  display: block;
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.dropdown-divider {
  height: 1px;
  background: var(--border-light);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  font-size: 14px;
  color: var(--text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: var(--transition-fast);
  text-align: left;
  font-family: var(--font-sans);
}

.dropdown-item svg {
  width: 16px;
  height: 16px;
}

.dropdown-item:hover {
  background: var(--bg-base);
  color: var(--text-primary);
}

.dropdown-item.logout:hover {
  background: var(--danger-light);
  color: var(--danger);
}

/* Dropdown Animation */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Main Content */
.main-content {
  flex: 1;
  padding: var(--space-lg) 0;
}

/* Footer */
.footer {
  background: white;
  padding: var(--space-xl) 0;
  margin-top: auto;
  border-top: 1px solid var(--border-light);
}

.footer-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
}

.footer-logo {
  width: 22px;
  height: 22px;
  color: var(--primary);
}

.footer-logo svg {
  width: 100%;
  height: 100%;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 13px;
}

.footer-links a {
  color: var(--text-muted);
  text-decoration: none;
  transition: var(--transition-fast);

  &:hover {
    color: var(--primary);
  }
}

.footer-links .divider {
  color: var(--border);
}

.footer-copyright {
  font-size: 12px;
  color: var(--text-muted);
}

/* Responsive */
@media (max-width: 768px) {
  .navbar-container {
    padding: 0 var(--space-md);
  }

  .nav-text {
    display: none;
  }

  .nav-link {
    padding: var(--space-sm);
  }

  .user-info {
    display: none;
  }
}
</style>
