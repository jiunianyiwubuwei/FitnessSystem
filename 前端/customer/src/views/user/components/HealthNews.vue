<template>
  <div class="news-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
          健康资讯
        </h1>
        <p class="hero-subtitle">专业的健身知识与健康资讯，助您科学运动</p>
      </div>
    </div>

    <!-- News Grid -->
    <div class="news-grid">
      <div
        v-for="news in newsList"
        :key="news.id"
        class="news-card"
        @click="goToDetail(news.id)"
      >
        <div class="news-image">
          <img :src="news.cover" :alt="news.name" />
          <div class="news-overlay">
            <span class="read-more">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="16"/>
                <line x1="8" y1="12" x2="16" y2="12"/>
              </svg>
              阅读全文
            </span>
          </div>
        </div>
        <div class="news-content">
          <h3 class="news-name">{{ news.name }}</h3>
          <div class="news-meta">
            <span class="news-category">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              健康科普
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="newsList.length === 0 && !loading" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
      </svg>
      <p>暂无健康资讯</p>
      <span>敬请期待更多内容</span>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      newsList: [],
      loading: true,
    };
  },
  created() {
    this.fetchHealthNews();
  },
  methods: {
    async fetchHealthNews() {
      this.loading = true;
      try {
        const response = await axios.get("http://localhost:8000/health/news/");
        this.newsList = response.data;
      } catch (error) {
        console.error("获取健康资讯失败:", error);
        this.$message.error("获取资讯失败，请重试");
      } finally {
        this.loading = false;
      }
    },
    goToDetail(newsId) {
      this.$router.push(`/main/health/news/${newsId}`);
    },
  },
};
</script>

<style scoped>
.news-page {
  max-width: 1200px;
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

/* News Grid */
.news-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg);
  margin-bottom: var(--space-2xl);
}

/* News Card */
.news-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  overflow: hidden;
  cursor: pointer;
  transition: var(--transition-base);
}

.news-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.news-card:hover .news-overlay {
  opacity: 1;
}

.news-card:hover .news-image img {
  transform: scale(1.05);
}

.news-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.news-overlay {
  position: absolute;
  inset: 0;
  background: rgba(10, 22, 40, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: var(--transition-base);
}

.read-more {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: white;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-full);
}

.read-more svg {
  width: 14px;
  height: 14px;
}

.news-content {
  padding: var(--space-md);
}

.news-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-sm);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-meta {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.news-category {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 12px;
  color: var(--text-muted);
}

.news-category svg {
  width: 12px;
  height: 12px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: var(--space-3xl);
  color: var(--text-muted);
}

.empty-state svg {
  width: 64px;
  height: 64px;
  margin-bottom: var(--space-md);
  opacity: 0.5;
}

.empty-state p {
  font-size: 18px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: var(--space-xs);
}

.empty-state span {
  font-size: 14px;
}

@media (max-width: 1024px) {
  .news-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .news-grid {
    grid-template-columns: 1fr;
  }

  .news-image {
    height: 180px;
  }
}
</style>
