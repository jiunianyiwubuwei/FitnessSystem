<template>
  <div class="news-detail-page">
    <div class="container">
      <!-- Back Button -->
      <button class="back-btn" @click="$router.back()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="19" y1="12" x2="5" y2="12"/>
          <polyline points="12 19 5 12 12 5"/>
        </svg>
        返回
      </button>

      <!-- Article Header -->
      <div class="article-header">
        <h1 class="article-title">{{ newsDetail.name }}</h1>
      </div>

      <!-- Cover Image -->
      <div class="cover-wrapper">
        <img :src="newsDetail.cover" :alt="newsDetail.name" class="cover-image" />
      </div>

      <!-- Article Content -->
      <div class="article-content" v-html="newsDetail.content"></div>

      <!-- Comments Section -->
      <div class="comments-section">
        <h2 class="section-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
          </svg>
          评论
        </h2>

        <!-- Comment Input -->
        <div class="comment-input-wrapper">
          <textarea
            v-model="newComment"
            class="comment-input"
            placeholder="发表你的评论..."
            rows="3"
          ></textarea>
          <button class="submit-comment-btn" @click="submitComment(null)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
            发表评论
          </button>
        </div>

        <!-- Comments List -->
        <div class="comments-list">
          <div v-if="comments.length === 0" class="no-comments">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
            </svg>
            <p>暂无评论，快来抢沙发吧</p>
          </div>

          <div
            v-for="comment in comments"
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-main">
              <div class="comment-avatar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div class="comment-body">
                <div class="comment-header">
                  <span class="commenter-name">{{ comment.commenter_name }}</span>
                  <span class="comment-time">{{ comment.create_time }}</span>
                </div>
                <p class="comment-text">{{ comment.content }}</p>
                <button class="reply-btn" @click="toggleReplyBox(comment.id)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="9 17 4 12 9 7"/>
                    <path d="M20 18v-2a4 4 0 0 0-4-4H4"/>
                  </svg>
                  回复
                </button>
              </div>
            </div>

            <!-- Reply Input -->
            <div v-if="replyVisible[comment.id]" class="reply-input-wrapper">
              <textarea
                v-model="replyContent"
                class="comment-input"
                placeholder="写下你的回复..."
                rows="2"
              ></textarea>
              <div class="reply-actions">
                <button class="cancel-btn" @click="replyVisible[comment.id] = false">取消</button>
                <button class="submit-comment-btn small" @click="submitComment(comment.id)">发送</button>
              </div>
            </div>

            <!-- Replies -->
            <div v-if="comment.replies && comment.replies.length > 0" class="replies-list">
              <div
                v-for="reply in comment.replies"
                :key="reply.id"
                class="reply-item"
              >
                <div class="comment-avatar small">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                </div>
                <div class="comment-body">
                  <div class="comment-header">
                    <span class="commenter-name">{{ reply.commenter_name }}</span>
                    <span class="comment-time">{{ reply.create_time }}</span>
                  </div>
                  <p class="comment-text">{{ reply.content }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      newsDetail: {},
      newComment: "",
      replyContent: "",
      comments: [],
      replyVisible: {},
    };
  },
  created() {
    this.fetchNewsDetail();
    this.fetchComments();
  },
  methods: {
    async fetchNewsDetail() {
      const newsId = this.$route.params.id;
      try {
        const response = await axios.get(
          `http://localhost:8000/health/news/${newsId}/`
        );
        this.newsDetail = response.data;
      } catch (error) {
        this.$message.error("获取文章详情失败");
      }
    },
    async fetchComments() {
      const newsId = this.$route.params.id;
      try {
        const response = await axios.get(
          `http://localhost:8000/health/news/${newsId}/comments/`
        );
        this.comments = response.data;
      } catch (error) {
        console.error("获取评论失败:", error);
      }
    },
    async submitComment(parentId = null) {
      const content = parentId ? this.replyContent : this.newComment;
      if (!content.trim()) {
        this.$message.warning("请输入评论内容");
        return;
      }

      const newsId = this.$route.params.id;
      const userMessage = JSON.parse(sessionStorage.getItem("userMessage"));
      const userId = userMessage ? userMessage.id : null;

      const commentData = {
        commenter: userId,
        content: content,
        content_type: "news",
        content_id: newsId,
        parent_id: parentId,
      };

      try {
        await axios.post(
          `http://localhost:8000/health/news/${newsId}/comments/`,
          commentData
        );

        if (parentId) {
          this.replyContent = "";
          this.replyVisible[parentId] = false;
        } else {
          this.newComment = "";
        }

        this.fetchComments();
        this.$message.success("评论发表成功");
      } catch (error) {
        this.$message.error("评论发表失败");
      }
    },
    toggleReplyBox(commentId) {
      this.replyVisible = {
        ...this.replyVisible,
        [commentId]: !this.replyVisible[commentId],
      };
    },
  },
};
</script>

<style scoped>
.news-detail-page {
  background: var(--bg-base);
  min-height: 100vh;
  padding: var(--space-lg) 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

/* Back Button */
.back-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-sm) var(--space-md);
  font-size: 14px;
  font-family: var(--font-sans);
  color: var(--text-secondary);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-fast);
  margin-bottom: var(--space-lg);
}

.back-btn svg {
  width: 16px;
  height: 16px;
}

.back-btn:hover {
  border-color: var(--primary-accent);
  color: var(--primary-accent);
}

/* Article Header */
.article-header {
  margin-bottom: var(--space-xl);
}

.article-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
}

/* Cover Image */
.cover-wrapper {
  margin-bottom: var(--space-xl);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.cover-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  display: block;
}

/* Article Content */
.article-content {
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-primary);
  margin-bottom: var(--space-2xl);
  background: var(--bg-card);
  padding: var(--space-xl);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
}

.article-content :deep(p) {
  margin-bottom: var(--space-md);
}

.article-content :deep(img) {
  max-width: 100%;
  border-radius: var(--radius-md);
  margin: var(--space-md) 0;
}

/* Comments Section */
.comments-section {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  padding: var(--space-xl);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-lg);
}

.section-title svg {
  width: 20px;
  height: 20px;
  color: var(--primary-accent);
}

/* Comment Input */
.comment-input-wrapper {
  margin-bottom: var(--space-xl);
}

.comment-input {
  width: 100%;
  padding: var(--space-md);
  font-size: 14px;
  font-family: var(--font-sans);
  background: var(--bg-base);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  resize: vertical;
  transition: var(--transition-fast);
  margin-bottom: var(--space-sm);
}

.comment-input:focus {
  border-color: var(--primary-accent);
  box-shadow: 0 0 0 3px var(--primary-glow);
  outline: none;
}

.submit-comment-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding: 10px var(--space-lg);
  font-size: 14px;
  font-weight: 500;
  font-family: var(--font-sans);
  color: white;
  background: var(--gradient-tech);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-fast);
}

.submit-comment-btn svg {
  width: 14px;
  height: 14px;
}

.submit-comment-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.35);
}

.submit-comment-btn.small {
  padding: 8px var(--space-md);
  font-size: 13px;
}

/* No Comments */
.no-comments {
  text-align: center;
  padding: var(--space-2xl);
  color: var(--text-muted);
}

.no-comments svg {
  width: 48px;
  height: 48px;
  margin-bottom: var(--space-md);
  opacity: 0.5;
}

.no-comments p {
  font-size: 14px;
}

/* Comments List */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.comment-item {
  padding-bottom: var(--space-lg);
  border-bottom: 1px solid var(--border-light);
}

.comment-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.comment-main {
  display: flex;
  gap: var(--space-md);
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--primary-glow);
  color: var(--primary-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.comment-avatar.small {
  width: 32px;
  height: 32px;
}

.comment-avatar svg {
  width: 20px;
  height: 20px;
}

.comment-avatar.small svg {
  width: 16px;
  height: 16px;
}

.comment-body {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-xs);
}

.commenter-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.comment-time {
  font-size: 12px;
  color: var(--text-muted);
}

.comment-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 var(--space-sm);
}

.reply-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  font-size: 12px;
  font-family: var(--font-sans);
  color: var(--text-muted);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: var(--transition-fast);
  border-radius: var(--radius-sm);
}

.reply-btn svg {
  width: 12px;
  height: 12px;
}

.reply-btn:hover {
  color: var(--primary-accent);
  background: var(--primary-glow);
}

/* Reply Input */
.reply-input-wrapper {
  margin-left: calc(40px + var(--space-md));
  margin-top: var(--space-md);
}

/* Reply Actions */
.reply-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-sm);
}

.cancel-btn {
  padding: 8px var(--space-md);
  font-size: 13px;
  font-family: var(--font-sans);
  color: var(--text-secondary);
  background: var(--bg-base);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-fast);
}

.cancel-btn:hover {
  background: var(--border);
}

/* Replies List */
.replies-list {
  margin-left: calc(40px + var(--space-md));
  margin-top: var(--space-md);
  padding-left: var(--space-md);
  border-left: 2px solid var(--border-light);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.reply-item {
  display: flex;
  gap: var(--space-sm);
}

@media (max-width: 640px) {
  .article-title {
    font-size: 22px;
  }

  .reply-input-wrapper,
  .replies-list {
    margin-left: 0;
  }

  .comment-avatar {
    width: 32px;
    height: 32px;
  }

  .comment-avatar svg {
    width: 16px;
    height: 16px;
  }
}
</style>
