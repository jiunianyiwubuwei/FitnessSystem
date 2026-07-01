<template>
  <div class="fitness-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6.5 6.5h11"/>
            <path d="M6.5 17.5h11"/>
            <path d="M3 12h3"/>
            <path d="M18 12h3"/>
            <path d="M6 8v8"/>
            <path d="M18 8v8"/>
            <circle cx="12" cy="12" r="2"/>
          </svg>
          智慧健身
        </h1>
        <p class="hero-subtitle">AI 动作识别 · 精准计数 · 卡路里追踪</p>
      </div>
    </div>

    <!-- Mode Toggle -->
    <div class="mode-toggle">
      <button
        class="mode-btn"
        :class="{ active: activeMode === 'exercise' }"
        @click="activeMode = 'exercise'"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6.5 6.5h11"/>
          <path d="M6.5 17.5h11"/>
          <path d="M3 12h3"/>
          <path d="M18 12h3"/>
          <path d="M6 8v8"/>
          <path d="M18 8v8"/>
        </svg>
        健身动作
      </button>
      <button
        class="mode-btn"
        :class="{ active: activeMode === 'dance' }"
        @click="activeMode = 'dance'"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 6v6l4 2"/>
        </svg>
        舞蹈评分
      </button>
    </div>

    <!-- Exercise Mode -->
    <div v-if="activeMode === 'exercise'" class="exercise-mode">
      <!-- Input Card -->
      <div class="card input-card">
        <div class="card-header">
          <h3 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
            设置参数
          </h3>
        </div>

        <div class="card-body">
          <!-- Weight Input -->
          <div class="input-group">
            <label class="input-label">体重 (kg)</label>
            <input
              type="number"
              class="input-field"
              v-model="weight"
              placeholder="输入您的体重"
            />
          </div>

          <!-- Exercise Type -->
          <div class="input-group">
            <label class="input-label">运动类型</label>
            <div class="select-wrapper">
              <select v-model="exerciseType" class="select-field">
                <option value="push-up">俯卧撑</option>
                <option value="pull-up">引体向上</option>
                <option value="sit-up">仰卧起坐</option>
                <option value="squat">深蹲</option>
                <option value="jumping-jack">开合跳</option>
                <option value="squat-jump">深蹲跳</option>
                <option value="jump-rope">跳绳</option>
                <option value="plank">平板支撑</option>
                <option value="side-lunge">侧弓步</option>
                <option value="arm-curl">哑铃弯举</option>
                <option value="shoulder-press">肩部推举</option>
                <option value="burpee">波比跳</option>
                <option value="high-knee">高抬腿</option>
              </select>
              <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>

          <!-- Video Upload -->
          <div class="input-group">
            <label class="input-label">上传视频</label>
            <div class="file-upload" @click="$refs.videoInput.click()">
              <input
                type="file"
                ref="videoInput"
                class="file-input"
                @change="handleFileUpload"
                accept="video/*"
                style="display: none"
              />
              <div class="file-upload-content">
                <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                <span v-if="videoFile">{{ videoFile.name }}</span>
                <span v-else>点击选择视频文件</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="card-actions">
          <button
            class="action-btn primary"
            @click="uploadVideo"
            :disabled="loading"
          >
            <svg v-if="!loading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <span v-if="loading" class="btn-spinner"></span>
            <span>{{ loading ? '处理中...' : '上传分析' }}</span>
          </button>
          <button
            class="action-btn secondary"
            @click="openCV2Camera"
            :disabled="loading"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M23 7l-7 5 7 5V7z"/>
              <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
            </svg>
            <span>{{ isCameraOpen ? '关闭摄像头' : '实时检测' }}</span>
          </button>
          <button
            class="action-btn secondary"
            @click="toggleChart"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="20" x2="18" y2="10"/>
              <line x1="12" y1="20" x2="12" y2="4"/>
              <line x1="6" y1="20" x2="6" y2="14"/>
            </svg>
            <span>{{ showChart ? '隐藏图表' : '显示图表' }}</span>
          </button>
        </div>
      </div>

      <!-- Results Card -->
      <div v-if="counter !== null" class="card results-card animate-fade-in">
        <div class="card-header">
          <h3 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
            运动结果
          </h3>
        </div>

        <div class="card-body">
          <div class="results-grid">
            <div class="result-item">
              <div class="result-icon primary">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
              </div>
              <div class="result-info">
                <span class="result-value">{{ counter }}</span>
                <span class="result-label">动作次数</span>
              </div>
            </div>
            <div class="result-item">
              <div class="result-icon energy">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
              </div>
              <div class="result-info">
                <span class="result-value">{{ calories }}</span>
                <span class="result-label">消耗卡路里 (kcal)</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chart Card -->
      <div v-if="showChart" class="card chart-card animate-fade-in">
        <div class="card-header">
          <h3 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="20" x2="18" y2="10"/>
              <line x1="12" y1="20" x2="12" y2="4"/>
              <line x1="6" y1="20" x2="6" y2="14"/>
            </svg>
            {{ currentMonth }}月卡路里消耗
          </h3>
        </div>
        <div class="card-body">
          <canvas id="calorieChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Dance Mode -->
    <div v-if="activeMode === 'dance'" class="dance-mode">
      <DanceScoreWithAnnotation></DanceScoreWithAnnotation>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from 'chart.js/auto';
import DanceScoreWithAnnotation from './DanceScoreWithAnnotation.vue';

export default {
  name: "Fitness",
  components: {
    DanceScoreWithAnnotation
  },
  data() {
    const userMessage = JSON.parse(window.sessionStorage.getItem('userMessage'));
    const userId = userMessage ? userMessage.id : null;
    const currentDate = new Date();
    return {
      activeMode: 'exercise',
      videoFile: null,
      exerciseType: "push-up",
      counter: null,
      isCameraOpen: false,
      loading: false,
      weight: null,
      calories: null,
      showChart: false,
      monthlyData: {},
      chart: null,
      userId,
      currentYear: currentDate.getFullYear(),
      currentMonth: currentDate.getMonth() + 1,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.videoFile = event.target.files[0];
      if (this.videoFile) {
        console.log("已选择视频:", this.videoFile.name);
      }
    },

    async uploadVideo() {
      if (!this.videoFile) {
        this.$message.warning("请先选择视频文件");
        return;
      }
      if (!this.weight || isNaN(parseFloat(this.weight))) {
        this.$message.warning("请输入有效的体重");
        return;
      }
      if (!this.userId) {
        this.$message.error("用户 ID 不存在，请重新登录");
        return;
      }

      this.loading = true;
      const formData = new FormData();
      formData.append("video_file", this.videoFile);
      formData.append("exercise_type", this.exerciseType);
      formData.append("weight", parseFloat(this.weight));
      formData.append("user_id", parseInt(this.userId));

      const token = sessionStorage.getItem("token");
      if (!token) {
        this.$message.error("Token 不存在，请重新登录");
        this.loading = false;
        return;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/upload/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.counter = response.data.counter;
        this.calories = response.data.calories;
        this.$message.success(`分析完成！动作计数: ${this.counter} 次，消耗卡路里: ${this.calories} kcal`);
      } catch (error) {
        console.error("上传视频失败:", error);
        this.$message.error("上传失败，请重试");
      } finally {
        this.loading = false;
      }
    },

    async openCV2Camera() {
      if (!this.weight || isNaN(parseFloat(this.weight))) {
        this.$message.warning("请输入有效的体重");
        return;
      }
      if (!this.userId) {
        this.$message.error("用户 ID 不存在，请重新登录");
        return;
      }

      if (this.isCameraOpen) {
        this.isCameraOpen = false;
        try {
          const formData = new FormData();
          formData.append("action", "stop");
          formData.append("user_id", parseInt(this.userId));

          await axios.post(
            "http://127.0.0.1:8000/api/real_time/",
            formData,
            { headers: { "Content-Type": "multipart/form-data" } }
          );

          this.$message.success("摄像头已关闭");
        } catch (error) {
          this.$message.error("关闭失败");
        }
        return;
      }

      this.isCameraOpen = true;
      try {
        const formData = new FormData();
        formData.append("exercise_type", this.exerciseType);
        formData.append("weight", parseFloat(this.weight));
        formData.append("user_id", parseInt(this.userId));

        const response = await axios.post(
          "http://127.0.0.1:8000/api/real_time/",
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );

        this.counter = response.data.counter;
        this.calories = response.data.calories;
        this.$message.success("实时检测已开启");
      } catch (error) {
        this.$message.error("启动失败，请检查后端");
        this.isCameraOpen = false;
      }
    },

    async toggleChart() {
      this.showChart = !this.showChart;
      if (this.showChart) {
        await this.fetchMonthlyCalories();
        this.renderChart();
      } else if (this.chart) {
        this.chart.destroy();
        this.chart = null;
      }
    },

    async fetchMonthlyCalories() {
      if (!this.userId) return;
      const apiUrl = `http://127.0.0.1:8000/api/calorie-record/?user_id=${this.userId}`;
      try {
        const response = await axios.get(apiUrl);
        this.monthlyData = response.data;
      } catch (error) {
        console.error('获取卡路里数据时出错:', error);
      }
    },

    renderChart() {
      const ctx = document.getElementById('calorieChart').getContext('2d');
      const labels = [];
      const data = [];

      const daysInMonth = new Date(this.currentYear, this.currentMonth, 0).getDate();
      for (let day = 1; day <= daysInMonth; day++) {
        const dayStr = day.toString().padStart(2, '0');
        const dateKey = `${this.currentYear}-${this.currentMonth.toString().padStart(2, '0')}-${dayStr}`;
        labels.push(day);
        data.push(this.monthlyData[dateKey] || 0);
      }

      if (this.chart) {
        this.chart.destroy();
      }

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: '今日消耗卡路里',
            data,
            backgroundColor: 'rgba(6, 182, 212, 0.2)',
            borderColor: 'rgba(6, 182, 212, 1)',
            borderWidth: 2,
            borderRadius: 6,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          }
        }
      });
    },
  },
};
</script>

<style scoped>
.fitness-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

/* Hero Section */
.hero-section {
  text-align: center;
  padding: var(--space-2xl) 0;
  margin-bottom: var(--space-lg);
}

.hero-content {
  display: inline-block;
}

.hero-icon {
  width: 36px;
  height: 36px;
  color: var(--accent);
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

/* Mode Toggle */
.mode-toggle {
  display: flex;
  justify-content: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-xl);
  padding: 4px;
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
}

.mode-btn {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-xl);
  font-size: 14px;
  font-weight: 500;
  font-family: var(--font-sans);
  color: var(--text-secondary);
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-fast);
}

.mode-btn svg {
  width: 18px;
  height: 18px;
}

.mode-btn:hover {
  color: var(--text-primary);
}

.mode-btn.active {
  background: var(--gradient-tech);
  color: white;
  box-shadow: 0 2px 8px rgba(6, 182, 212, 0.25);
}

/* Cards */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--space-lg);
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

.card-actions {
  padding: var(--space-md) var(--space-lg);
  border-top: 1px solid var(--border-light);
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
}

/* Input Card */
.input-group {
  margin-bottom: var(--space-lg);
}

.input-group:last-child {
  margin-bottom: 0;
}

.input-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-sm);
}

.input-field {
  width: 100%;
  padding: 12px var(--space-md);
  font-size: 14px;
  font-family: var(--font-sans);
  background: var(--bg-base);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  transition: var(--transition-fast);
}

.input-field:focus {
  border-color: var(--primary-accent);
  background: var(--bg-card);
  box-shadow: 0 0 0 3px var(--primary-glow);
  outline: none;
}

.select-wrapper {
  position: relative;
}

.select-field {
  width: 100%;
  padding: 12px var(--space-md);
  font-size: 14px;
  font-family: var(--font-sans);
  background: var(--bg-base);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  transition: var(--transition-fast);
  appearance: none;
  cursor: pointer;
}

.select-field:focus {
  border-color: var(--primary-accent);
  box-shadow: 0 0 0 3px var(--primary-glow);
  outline: none;
}

.select-arrow {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--text-muted);
  pointer-events: none;
}

/* File Upload */
.file-upload {
  border: 2px dashed var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-xl);
  text-align: center;
  cursor: pointer;
  transition: var(--transition-fast);
  background: var(--bg-base);
}

.file-upload:hover {
  border-color: var(--primary-accent);
  background: rgba(59, 130, 246, 0.02);
}

.file-upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
  font-size: 14px;
  color: var(--text-secondary);
}

.upload-icon {
  width: 32px;
  height: 32px;
  color: var(--text-muted);
}

/* Action Buttons */
.action-btn {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 10px var(--space-lg);
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

.action-btn.primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.35);
}

.action-btn.secondary {
  background: var(--bg-base);
  color: var(--text-primary);
  border: 1px solid var(--border);
}

.action-btn.secondary:hover:not(:disabled) {
  border-color: var(--primary-accent);
  color: var(--primary-accent);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Results Card */
.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-lg);
}

.result-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-lg);
  background: var(--bg-base);
  border-radius: var(--radius-md);
}

.result-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
}

.result-icon svg {
  width: 24px;
  height: 24px;
}

.result-icon.primary {
  background: var(--primary-glow);
  color: var(--primary-accent);
}

.result-icon.energy {
  background: rgba(249, 115, 22, 0.1);
  color: var(--secondary);
}

.result-info {
  display: flex;
  flex-direction: column;
}

.result-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.result-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: var(--space-xs);
}

/* Chart Card */
.chart-card .card-body {
  height: 300px;
}

/* Dance Mode */
.dance-mode {
  margin-top: 0;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
