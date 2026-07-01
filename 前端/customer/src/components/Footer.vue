<template>
  <div class="footer-wrapper">
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-brand">
          <div class="brand-icon">
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 22L16 10L22 22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 18H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <span class="brand-name">MyAction</span>
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
export default {
  name: "Footer",
};
</script>

<style scoped>
.footer-wrapper {
  background: var(--primary);
  padding: var(--space-xl) 0;
}

.footer {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

.footer-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.brand-icon {
  width: 24px;
  height: 24px;
  color: var(--accent);
}

.brand-icon svg {
  width: 100%;
  height: 100%;
}

.brand-name {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

.footer-links {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 13px;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: var(--accent);
}

.footer-links .divider {
  color: rgba(255, 255, 255, 0.2);
}

.footer-copyright {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.3);
}
</style>
