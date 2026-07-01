<template>
  <div class="header-wrapper">
    <header class="header">
      <div class="header-container">
        <div class="brand">
          <div class="brand-icon">
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 22L16 10L22 22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 18H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h1>智能健身识别系统</h1>
        </div>
      </div>
    </header>
  </div>
</template>

<script>
export default {
  name: 'Header',
};
</script>

<style scoped>
.header-wrapper {
  background: var(--primary);
}

.header {
  max-width: 100%;
  margin: 0 auto;
}

.header-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
  height: 64px;
  display: flex;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.brand-icon {
  width: 32px;
  height: 32px;
  color: var(--accent);
}

.brand-icon svg {
  width: 100%;
  height: 100%;
}

.brand h1 {
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin: 0;
  letter-spacing: 1px;
}
</style>
