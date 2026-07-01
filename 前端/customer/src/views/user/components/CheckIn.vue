<template>
  <div class="checkin-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
          每日健康打卡
        </h1>
        <p class="hero-subtitle">记录今日健康数据，追踪您的运动旅程</p>
      </div>
    </div>

    <!-- Input Card -->
    <div class="card input-card">
      <div class="card-header">
        <h3 class="card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          录入数据
        </h3>
      </div>

      <div class="card-body">
        <div class="input-grid">
          <!-- Weight -->
          <div class="input-group">
            <label class="input-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
              </svg>
              体重 (kg)
            </label>
            <input
              type="number"
              class="input-field"
              v-model="weight"
              placeholder="今日体重"
            />
          </div>

          <!-- Sleep -->
          <div class="input-group">
            <label class="input-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
              睡眠时长 (小时)
            </label>
            <input
              type="number"
              class="input-field"
              v-model="sleepHours"
              placeholder="睡眠时长"
            />
          </div>

          <!-- Exercise Time -->
          <div class="input-group">
            <label class="input-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
              </svg>
              运动时长 (分钟)
            </label>
            <input
              type="number"
              class="input-field"
              v-model="exerciseTime"
              placeholder="运动时长"
            />
          </div>

          <!-- Exercise Type -->
          <div class="input-group">
            <label class="input-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6.5 6.5h11"/>
                <path d="M6.5 17.5h11"/>
                <path d="M3 12h3"/>
                <path d="M18 12h3"/>
              </svg>
              运动类型
            </label>
            <div class="select-wrapper">
              <select v-model="exerciseType" class="select-field">
                <option value="" disabled selected>选择运动类型</option>
                <option v-for="type in exerciseTypes" :key="type" :value="type">
                  {{ type }}
                </option>
              </select>
              <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>

          <!-- Custom Exercise Type -->
          <div v-if="exerciseType === '其他'" class="input-group full-width">
            <label class="input-label">自定义运动</label>
            <input
              type="text"
              class="input-field"
              v-model="customExerciseType"
              placeholder="请输入具体运动类型"
            />
          </div>
        </div>

        <!-- Actions -->
        <div class="card-actions">
          <button class="action-btn primary" @click="submitHealthData">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            打卡
          </button>
          <button class="action-btn secondary" @click="clearInputs">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
            清空
          </button>
        </div>
      </div>
    </div>

    <!-- Feedback -->
    <transition name="slide">
      <div v-if="feedback" class="feedback-banner">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
        </svg>
        {{ feedback }}
      </div>
    </transition>

    <!-- Chart Card -->
    <div class="card chart-card">
      <div class="card-header">
        <h3 class="card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="20" x2="18" y2="10"/>
            <line x1="12" y1="20" x2="12" y2="4"/>
            <line x1="6" y1="20" x2="6" y2="14"/>
          </svg>
          健康数据趋势
        </h3>
      </div>
      <div class="card-body">
        <div ref="chart" class="chart-container"></div>
      </div>
    </div>

    <!-- History Card -->
    <div class="card history-card">
      <div class="card-header">
        <h3 class="card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          打卡记录
        </h3>
        <span class="record-count">{{ healthRecords.length }} 条记录</span>
      </div>
      <div class="card-body">
        <div v-if="healthRecords.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/>
            <line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
          <p>暂无打卡记录</p>
          <span>开始您的第一次打卡吧</span>
        </div>
        <div v-else class="history-list">
          <div
            v-for="record in healthRecords"
            :key="record.id"
            class="history-item"
          >
            <div class="history-date">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              {{ record.date }}
            </div>
            <div class="history-details">
              <span class="detail-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                </svg>
                {{ record.weight }}kg
              </span>
              <span class="detail-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                </svg>
                {{ record.sleep_hours }}h
              </span>
              <span class="detail-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
                {{ record.exercise_time }}min
              </span>
              <span class="detail-item exercise-type">
                {{ record.exercise_type }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import * as echarts from "echarts/core";
import { LineChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  CanvasRenderer,
]);

export default {
  data() {
    return {
      weight: "",
      sleepHours: "",
      exerciseTime: "",
      exerciseType: "",
      customExerciseType: "",
      feedback: "",
      healthRecords: [],
      exerciseTypes: [
        "跑步",
        "游泳",
        "骑自行车",
        "打篮球",
        "踢足球",
        "跳绳",
        "羽毛球",
        "其他",
      ],
    };
  },

  created() {
    this.fetchHealthData();
  },

  methods: {
    async submitHealthData() {
      const userMessage = JSON.parse(sessionStorage.getItem("userMessage"));
      const userId = userMessage ? userMessage.id : null;

      const finalExerciseType =
        this.exerciseType === "其他"
          ? this.customExerciseType
          : this.exerciseType;

      try {
        const response = await axios.post(
          `http://localhost:8000/health/checkin/`,
          {
            user_id: userId,
            weight: this.weight,
            sleep_hours: this.sleepHours,
            exercise_time: this.exerciseTime,
            exercise_type: finalExerciseType,
          }
        );

        this.feedback = response.data.feedback;
        this.fetchHealthData();

        setTimeout(() => {
          this.feedback = "";
        }, 3000);
      } catch (error) {
        this.$message.error("打卡失败，请重试");
      }
    },

    async fetchHealthData() {
      const userMessage = JSON.parse(sessionStorage.getItem("userMessage"));
      const userId = userMessage ? userMessage.id : null;

      try {
        const response = await axios.get(
          `http://localhost:8000/health/data/${userId}/`
        );
        this.healthRecords = response.data;
        this.renderChart();
      } catch (error) {
        console.error("获取数据失败:", error);
      }
    },

    renderChart() {
      const chart = echarts.init(this.$refs.chart);
      const option = {
        title: {
          text: "健康数据趋势",
          left: "center",
          top: 10,
          textStyle: {
            fontSize: 14,
            fontWeight: 600,
            color: "#0f172a"
          }
        },
        legend: {
          data: ["体重", "睡眠时长", "运动时长"],
          top: 45,
          left: "center",
          itemWidth: 12,
          itemHeight: 12,
        },
        grid: {
          top: 80,
          left: 50,
          right: 20,
          bottom: 30,
        },
        xAxis: {
          type: "category",
          data: this.healthRecords.map((item) => item.date || ""),
          axisLine: { lineStyle: { color: "#e2e8f0" } },
          axisLabel: { color: "#64748b", fontSize: 11 }
        },
        yAxis: [
          {
            type: "value",
            name: "体重/运动时长",
            axisLine: { show: false },
            axisTick: { show: false },
            axisLabel: { color: "#64748b", fontSize: 11 },
            splitLine: { lineStyle: { color: "#f1f5f9" } }
          },
          {
            type: "value",
            name: "睡眠时长",
            position: "right",
            axisLine: { show: false },
            axisTick: { show: false },
            axisLabel: { color: "#64748b", fontSize: 11 },
            splitLine: { show: false }
          },
        ],
        series: [
          {
            name: "体重",
            data: this.healthRecords.map((item) => parseFloat(item.weight) || 0),
            type: "line",
            smooth: true,
            yAxisIndex: 0,
            lineStyle: { color: "#3b82f6", width: 2 },
            itemStyle: { color: "#3b82f6" },
            areaStyle: { color: "rgba(59, 130, 246, 0.1)" },
          },
          {
            name: "睡眠时长",
            data: this.healthRecords.map((item) => parseFloat(item.sleep_hours) || 0),
            type: "line",
            smooth: true,
            yAxisIndex: 1,
            lineStyle: { color: "#10b981", width: 2 },
            itemStyle: { color: "#10b981" },
            areaStyle: { color: "rgba(16, 185, 129, 0.1)" },
          },
          {
            name: "运动时长",
            data: this.healthRecords.map((item) => parseFloat(item.exercise_time) || 0),
            type: "line",
            smooth: true,
            yAxisIndex: 0,
            lineStyle: { color: "#f97316", width: 2 },
            itemStyle: { color: "#f97316" },
            areaStyle: { color: "rgba(249, 115, 22, 0.1)" },
          },
        ],
      };
      chart.setOption(option);
    },

    clearInputs() {
      this.weight = "";
      this.sleepHours = "";
      this.exerciseTime = "";
      this.exerciseType = "";
      this.customExerciseType = "";
    },
  },
};
</script>

<style scoped>
.checkin-page {
  max-width: 1000px;
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
  color: var(--success);
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
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.record-count {
  font-size: 13px;
  color: var(--text-muted);
}

.card-body {
  padding: var(--space-lg);
}

/* Input Grid */
.input-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-md);
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group.full-width {
  grid-column: 1 / -1;
}

.input-label {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-sm);
}

.input-label svg {
  width: 14px;
  height: 14px;
  color: var(--text-muted);
}

.input-field {
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
  appearance: none;
  cursor: pointer;
  transition: var(--transition-fast);
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

/* Actions */
.card-actions {
  display: flex;
  gap: var(--space-sm);
  margin-top: var(--space-lg);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--border-light);
}

.action-btn {
  display: flex;
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

.action-btn.secondary {
  background: var(--bg-base);
  color: var(--text-primary);
  border: 1px solid var(--border);
}

.action-btn.secondary:hover {
  border-color: var(--danger);
  color: var(--danger);
}

/* Feedback Banner */
.feedback-banner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  padding: var(--space-md);
  background: var(--success-light);
  border-radius: var(--radius-md);
  color: var(--success);
  font-size: 14px;
  font-weight: 500;
  margin-bottom: var(--space-lg);
}

.feedback-banner svg {
  width: 18px;
  height: 18px;
}

/* Slide Transition */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Chart */
.chart-container {
  height: 300px;
}

/* History */
.empty-state {
  text-align: center;
  padding: var(--space-2xl);
  color: var(--text-muted);
}

.empty-state svg {
  width: 48px;
  height: 48px;
  margin-bottom: var(--space-md);
  opacity: 0.5;
}

.empty-state p {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: var(--space-xs);
}

.empty-state span {
  font-size: 13px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md);
  background: var(--bg-base);
  border-radius: var(--radius-md);
  transition: var(--transition-fast);
}

.history-item:hover {
  background: var(--bg-card);
  box-shadow: var(--shadow-sm);
}

.history-date {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.history-date svg {
  width: 16px;
  height: 16px;
  color: var(--primary-accent);
}

.history-details {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.detail-item {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 13px;
  color: var(--text-secondary);
}

.detail-item svg {
  width: 14px;
  height: 14px;
  color: var(--text-muted);
}

.detail-item.exercise-type {
  padding: 4px 10px;
  background: var(--primary-glow);
  color: var(--primary-accent);
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
}

@media (max-width: 640px) {
  .input-grid {
    grid-template-columns: 1fr;
  }

  .history-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-sm);
  }

  .history-details {
    flex-wrap: wrap;
  }
}
</style>
