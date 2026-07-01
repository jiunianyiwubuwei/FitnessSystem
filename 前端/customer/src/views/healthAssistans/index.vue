<template>
  <div class="assistant-page">
    <!-- Header -->
    <div class="assistant-header">
      <div class="header-content">
        <div class="brand">
          <div class="brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
            </svg>
          </div>
          <div class="brand-text">
            <h1>AI 健康助手</h1>
            <p>智能健康咨询 · 科学养生建议</p>
          </div>
        </div>
        <button class="clear-btn" @click="clearChat">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 6h18"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
          </svg>
          清空记录
        </button>
      </div>
    </div>

    <!-- Chat Container -->
    <div class="chat-container">
      <!-- Messages -->
      <div class="messages" ref="messageContainer">
        <!-- Welcome Message -->
        <div v-if="messages.length === 0" class="welcome-state">
          <div class="welcome-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
            </svg>
          </div>
          <h2>您好，我是 AI 健康助手</h2>
          <p>可以问我关于健康、营养、运动等方面的问题</p>
          <div class="suggestion-chips">
            <button
              v-for="suggestion in suggestions"
              :key="suggestion"
              class="suggestion-chip"
              @click="inputText = suggestion"
            >
              {{ suggestion }}
            </button>
          </div>
        </div>

        <!-- Message Bubbles -->
        <transition-group name="message" tag="div" class="messages-list">
          <div
            v-for="(msg, index) in messages"
            :key="index"
            :class="['message-bubble', msg.role]"
          >
            <div class="avatar">
              <svg v-if="msg.role === 'user'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
              </svg>
            </div>
            <div class="content">
              <div class="text" v-html="formatContent(msg.content)"></div>
              <div class="timestamp">{{ formatTime(msg.timestamp) }}</div>
            </div>
          </div>
        </transition-group>

        <!-- Loading Indicator -->
        <div v-if="loading" class="loading-indicator">
          <div class="loading-dots">
            <span></span><span></span><span></span>
          </div>
          <p>正在分析您的健康问题...</p>
        </div>
      </div>

      <!-- Input Area -->
      <div class="input-area">
        <div class="input-wrapper">
          <textarea
            v-model="inputText"
            :rows="3"
            placeholder="请输入健康问题，例如：如何科学降血压？"
            resize="none"
            @keydown.enter.native.prevent="sendMessage"
            class="input-field"
          ></textarea>
          <button
            class="send-btn"
            @click="sendMessage"
            :disabled="!canSend"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </div>
        <p class="input-hint">按 Enter 发送，Shift + Enter 换行</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HealthAssistant",
  data() {
    return {
      messages: [],
      inputText: "",
      loading: false,
      suggestions: [
        "如何科学降血压？",
        "每天应该运动多久？",
        "睡眠不好怎么办？",
        "饮食应该如何搭配？",
      ],
    };
  },
  computed: {
    canSend() {
      return this.inputText.trim().length > 0 && !this.loading;
    },
  },
  methods: {
    formatContent(text) {
      if (!text) return '';
      return text
        .replace(/\n/g, "<br>")
        .replace(/(https?:\/\/\S+)/g, '<a href="$1" target="_blank">$1</a>');
    },
    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString("zh-CN", {
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    async sendMessage() {
      const question = this.inputText.trim();
      if (!question) return;

      this.messages.push({
        role: "user",
        content: question,
        timestamp: Date.now(),
      });
      this.inputText = "";
      this.scrollToBottom();

      try {
        this.loading = true;
        this.scrollToBottom();

        const response = await axios.post(
          "http://127.0.0.1:8000//api2/GetAdvice/",
          { question: question }
        );

        this.messages.push({
          role: "assistant",
          content: response.data.answer,
          timestamp: Date.now(),
        });
      } catch (error) {
        this.$message.error("获取健康建议失败，请稍后重试");
        console.error("API Error:", error);
      } finally {
        this.loading = false;
        this.scrollToBottom();
      }
    },
    clearChat() {
      this.messages = [];
      this.$message.success("对话记录已清空");
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messageContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
  },
};
</script>

<style scoped>
.assistant-page {
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  background: var(--bg-base);
}

/* Header */
.assistant-header {
  background: var(--gradient-hero);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  padding: var(--space-md) var(--space-lg);
  flex-shrink: 0;
}

.header-content {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.brand-icon {
  width: 44px;
  height: 44px;
  background: rgba(6, 182, 212, 0.15);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

.brand-icon svg {
  width: 24px;
  height: 24px;
}

.brand-text h1 {
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin: 0 0 2px;
}

.brand-text p {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

.clear-btn {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-md);
  font-size: 13px;
  font-family: var(--font-sans);
  color: rgba(255, 255, 255, 0.7);
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-fast);
}

.clear-btn svg {
  width: 14px;
  height: 14px;
}

.clear-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

/* Chat Container */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
  overflow: hidden;
}

/* Messages */
.messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-lg);
  scroll-behavior: smooth;
}

/* Welcome State */
.welcome-state {
  text-align: center;
  padding: var(--space-3xl) var(--space-lg);
  animation: fadeIn 0.4s ease-out;
}

.welcome-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto var(--space-lg);
  background: var(--primary-glow);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-accent);
}

.welcome-icon svg {
  width: 36px;
  height: 36px;
}

.welcome-state h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 var(--space-sm);
}

.welcome-state > p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 var(--space-xl);
}

.suggestion-chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  justify-content: center;
}

.suggestion-chip {
  padding: var(--space-sm) var(--space-md);
  font-size: 13px;
  font-family: var(--font-sans);
  color: var(--text-secondary);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: var(--transition-fast);
}

.suggestion-chip:hover {
  border-color: var(--primary-accent);
  color: var(--primary-accent);
  background: var(--primary-glow);
}

/* Messages List */
.messages-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.message-bubble {
  display: flex;
  gap: var(--space-md);
  max-width: 80%;
  animation: fadeIn 0.3s ease-out;
}

.message-bubble.user {
  margin-left: auto;
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-bubble.user .avatar {
  background: var(--gradient-tech);
  color: white;
}

.message-bubble.assistant .avatar {
  background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
  color: white;
}

.avatar svg {
  width: 18px;
  height: 18px;
}

.content {
  padding: var(--space-md);
  border-radius: var(--radius-lg);
  max-width: calc(100% - 60px);
}

.message-bubble.user .content {
  background: var(--gradient-tech);
  color: white;
  border-radius: var(--radius-lg) 0 var(--radius-lg) var(--radius-lg);
}

.message-bubble.assistant .content {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 0 var(--radius-lg) var(--radius-lg) var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.text {
  font-size: 14px;
  line-height: 1.7;
  word-break: break-word;
}

.text :deep(a) {
  color: var(--primary-accent);
  text-decoration: underline;
}

.timestamp {
  font-size: 11px;
  margin-top: var(--space-xs);
  opacity: 0.6;
}

/* Loading */
.loading-indicator {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  color: var(--text-muted);
  font-size: 14px;
}

.loading-dots {
  display: flex;
  gap: 4px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background: var(--primary-accent);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* Input Area */
.input-area {
  padding: var(--space-md) var(--space-lg);
  background: var(--bg-card);
  border-top: 1px solid var(--border-light);
  flex-shrink: 0;
}

.input-wrapper {
  display: flex;
  gap: var(--space-sm);
  align-items: flex-end;
}

.input-field {
  flex: 1;
  padding: var(--space-md);
  font-size: 14px;
  font-family: var(--font-sans);
  background: var(--bg-base);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  resize: none;
  transition: var(--transition-fast);
  line-height: 1.5;
}

.input-field:focus {
  border-color: var(--primary-accent);
  box-shadow: 0 0 0 3px var(--primary-glow);
  outline: none;
}

.send-btn {
  width: 44px;
  height: 44px;
  background: var(--gradient-tech);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition-fast);
  flex-shrink: 0;
}

.send-btn svg {
  width: 18px;
  height: 18px;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.35);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-hint {
  font-size: 11px;
  color: var(--text-muted);
  margin: var(--space-xs) 0 0;
  text-align: center;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-enter-active {
  transition: all 0.3s ease;
}
.message-enter {
  opacity: 0;
  transform: translateY(20px);
}

@media (max-width: 640px) {
  .message-bubble {
    max-width: 90%;
  }

  .suggestion-chips {
    flex-direction: column;
    align-items: stretch;
  }

  .suggestion-chip {
    text-align: center;
  }
}
</style>
