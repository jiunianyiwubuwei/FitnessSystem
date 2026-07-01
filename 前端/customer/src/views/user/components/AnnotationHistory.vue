<template>
  <div class="annotation-history-container">
    <h2 class="title">📋 标注历史</h2>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="records.length === 0" class="empty-state">
      <div class="empty-icon">📭</div>
      <p>暂无标注记录</p>
      <p class="empty-hint">上传视频进行关键点标注吧</p>
      <button class="upload-link-btn" @click="$router.push('/main/health/annotation')">
        去上传视频
      </button>
    </div>

    <!-- 标注列表 -->
    <div v-else class="record-list">
      <div
        v-for="record in records"
        :key="record.id"
        class="record-card"
        @click="playAnnotation(record)"
      >
        <div class="card-left">
          <div class="video-preview">
            <video :src="record.video_url" class="preview-video" muted preload="metadata"></video>
            <div class="play-overlay">
              <span class="play-icon">▶</span>
            </div>
          </div>
        </div>

        <div class="card-right">
          <div class="filename">{{ record.original_filename }}</div>

          <div class="stats-row">
            <span class="stat-tag">
              📊 {{ record.valid_frame_count }} / {{ record.total_frame_count }} 有效帧
            </span>
            <span class="stat-tag">
              ⏱ {{ record.duration ? record.duration.toFixed(1) + 's' : '—' }}
            </span>
            <span class="stat-tag">
              🎬 {{ record.fps }} fps
            </span>
          </div>

          <div class="progress-bar-wrap">
            <div
              class="progress-fill"
              :style="{ width: (record.valid_frame_count / record.total_frame_count * 100).toFixed(1) + '%' }"
            ></div>
          </div>
          <div class="progress-label">
            有效率 {{ (record.valid_frame_count / record.total_frame_count * 100).toFixed(1) }}%
          </div>

          <div class="card-footer">
            <span class="time">{{ formatTime(record.created_at) }}</span>
            <span class="view-btn">查看骨架 ▶</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="pagination">
      <button
        class="page-btn"
        :disabled="page <= 1"
        @click="loadPage(page - 1)"
      >上一页</button>
      <span class="page-info">第 {{ page }} / {{ totalPages }} 页</span>
      <button
        class="page-btn"
        :disabled="page >= totalPages"
        @click="loadPage(page + 1)"
      >下一页</button>
    </div>

    <!-- 播放骨架弹窗 -->
    <el-dialog
      title="骨架标注播放"
      :visible.sync="dialogVisible"
      width="900px"
      :close-on-click-modal="true"
    >
      <AnnotatedVideoPlayer
        v-if="dialogVisible"
        ref="dialogPlayer"
        :initial-annotation-id="currentAnnotationId"
      />
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import AnnotatedVideoPlayer from './AnnotatedVideoPlayer.vue';

export default {
  name: 'AnnotationHistory',
  components: { AnnotatedVideoPlayer },
  data() {
    return {
      records: [],
      loading: true,
      page: 1,
      pageSize: 10,
      total: 0,
      dialogVisible: false,
      currentAnnotationId: null,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.total / this.pageSize) || 1;
    },
    userId() {
      const user = JSON.parse(sessionStorage.getItem('userMessage') || '{}');
      return user.id || null;
    },
    token() {
      return sessionStorage.getItem('token') || '';
    },
  },
  mounted() {
    this.loadPage(1);
  },
  methods: {
    async loadPage(page) {
      this.loading = true;
      this.page = page;
      try {
        const params = new URLSearchParams({
          page: page,
          page_size: this.pageSize,
        });
        if (this.userId) params.append('user_id', this.userId);

        const response = await axios.get(
          `/api/annotation/list/?${params.toString()}`,
          { headers: { Authorization: `Bearer ${this.token}` }, timeout: 10000 }
        );

        if (response.data.code === 200) {
          this.records = response.data.data.items;
          this.total = response.data.data.total;
        } else {
          this.$message.error(response.data.error || '加载失败');
        }
      } catch (error) {
        console.error('加载标注列表失败:', error);
        this.$message.error('加载标注列表失败');
      } finally {
        this.loading = false;
      }
    },

    playAnnotation(record) {
      this.currentAnnotationId = record.id;
      this.dialogVisible = true;
    },

    formatTime(isoString) {
      if (!isoString) return '—';
      const d = new Date(isoString);
      return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
    },
  },
};
</script>

<style scoped>
.annotation-history-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif;
}

.title {
  text-align: center;
  font-size: 26px;
  margin-bottom: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 0;
  color: #888;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e0e0e0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 12px;
}

.empty-hint {
  font-size: 13px;
  color: #aaa;
  margin-bottom: 16px;
}

.upload-link-btn {
  padding: 10px 28px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  border: none;
  border-radius: 20px;
  font-size: 15px;
  cursor: pointer;
}

.record-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.record-card {
  display: flex;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.record-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 20px rgba(102,126,234,0.15);
  transform: translateY(-2px);
}

.card-left {
  width: 160px;
  flex-shrink: 0;
}

.video-preview {
  position: relative;
  width: 160px;
  height: 100px;
  background: #000;
  overflow: hidden;
}

.preview-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0.3);
  opacity: 0;
  transition: opacity 0.2s;
}

.record-card:hover .play-overlay {
  opacity: 1;
}

.play-icon {
  font-size: 28px;
  color: #fff;
}

.card-right {
  flex: 1;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.filename {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stats-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.stat-tag {
  font-size: 12px;
  color: #667eea;
  background: rgba(102,126,234,0.08);
  padding: 2px 8px;
  border-radius: 10px;
}

.progress-bar-wrap {
  height: 6px;
  background: #eee;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.5s;
  max-width: 100%;
}

.progress-label {
  font-size: 11px;
  color: #aaa;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2px;
}

.time {
  font-size: 12px;
  color: #bbb;
}

.view-btn {
  font-size: 12px;
  color: #667eea;
  font-weight: 600;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}

.page-btn {
  padding: 8px 20px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: #667eea;
  color: #fff;
  border-color: #667eea;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #888;
}
</style>
