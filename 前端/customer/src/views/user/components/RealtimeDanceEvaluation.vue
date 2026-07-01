<template>
  <div class="realtime-dance-container">
    <h2 class="title">💃 舞蹈评分系统</h2>

    <!-- 舞蹈选择 -->
    <div class="dance-select">
      <label>选择标准舞蹈：</label>
      <select v-model="selectedDanceId" @change="onDanceSelect">
        <option value="">请选择舞蹈</option>
        <option v-for="dance in danceList" :key="dance.id" :value="dance.id">
          {{ dance.name }} ({{ dance.dance_type }})
        </option>
      </select>
    </div>

    <!-- 视频播放区：视频原生播放，骨架叠加在 canvas -->
    <div class="video-container" v-if="selectedDanceId">
      <!-- 标准舞蹈视频 -->
      <div class="video-panel">
        <h3>📺 标准动作</h3>
        <div class="video-wrapper">
          <video
            ref="standardVideo"
            class="video-layer"
            :src="standardVideoUrl"
            controls
            @timeupdate="onVideoTimeUpdate"
            @loadedmetadata="onVideoLoaded"
            @play="onVideoPlay"
            @pause="onVideoPause"
            @ended="onVideoEnded"
          ></video>
          <!-- 骨架叠加层 -->
          <canvas ref="skeletonCanvas" class="skeleton-canvas"></canvas>
        </div>
        <div class="video-info" v-if="videoInfo">
          <span>{{ videoInfo.currentFrame }} / {{ videoInfo.totalFrames }} 帧</span>
          <span>{{ videoInfo.fps }} fps</span>
        </div>
      </div>
    </div>

    <!-- 加载提示 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>{{ loadingText }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DanceEvaluation',

  // MediaPipe POSE_CONNECTIONS（33个关键点的33条连接）
  // 定义在组件外部，避免被 Vue 响应式系统处理
  POSE_CONNECTIONS: [
    [0,1],[1,2],[2,3],[3,7],[0,4],[4,5],[5,6],[6,8],[9,10],
    [11,12],[11,13],[13,15],[15,17],[15,19],[15,21],[17,19],
    [12,14],[14,16],[16,18],[16,20],[16,22],[18,20],
    [11,23],[12,24],[23,24],[23,25],[24,26],[25,27],[26,28],
    [27,29],[28,30],[29,31],[30,32],[27,31],[28,32]
  ],

  data() {
    return {
      danceList: [],
      selectedDanceId: '',
      standardVideoUrl: '',
      standardVideoMeta: null,

      // 预计算骨架数据（从后端获取）
      keyframes: [],      // 所有帧的关键点 [[x,y,z,v], ...]
      totalFrames: 0,
      fps: 30,
      duration: 0,

      // 当前播放状态
      currentFrameIndex: 0,
      isPlaying: false,

      loading: false,
      loadingText: '',

      // 视频播放信息（帧信息）
      videoInfo: null,
    };
  },
  async mounted() {
    await this.fetchDanceList();
    // 预加载 MediaPipe 绘图库（纯绘制，无推理，文件很小）
    await this.loadDrawingUtils();
  },
  beforeDestroy() {
    this.cleanup();
  },
  methods: {
    // 加载 MediaPipe 绘图工具库（仅 drawing_utils.js，约 10KB，无推理）
    _loadScript(src) {
      return new Promise((resolve, reject) => {
        const existing = document.querySelector(`script[src="${src}"]`);
        if (existing) { resolve(); return; }
        const timer = setTimeout(() => reject(new Error('加载超时')), 5000);
        const script = document.createElement('script');
        script.src = src;
        script.async = true;
        script.onload = () => { clearTimeout(timer); resolve(); };
        script.onerror = () => { clearTimeout(timer); reject(new Error('加载失败')); };
        document.head.appendChild(script);
      });
    },

    async loadDrawingUtils() {
      try {
        await this._loadScript('/mediapipe/drawing_utils.js');
        console.log('MediaPipe drawing_utils loaded');
      } catch (e) {
        console.warn('绘图库加载失败，将使用简化绘制:', e.message);
      }
    },
    // 获取舞蹈列表
    async fetchDanceList() {
      try {
        const response = await axios.get('/api/dance/standards/');
        if (response.data.code === 200) {
          this.danceList = response.data.data;
        }
      } catch (error) {
        console.error('获取舞蹈列表失败:', error);
      }
    },

    // 选择舞蹈
    async onDanceSelect() {
      if (!this.selectedDanceId) return;

      this.cleanup();

      const dance = this.danceList.find(d => d.id == this.selectedDanceId);
      if (!dance) return;

      this.standardVideoUrl = `/media/${dance.video_path}`;
      this.loading = true;
      this.loadingText = '正在加载骨架数据...';

      try {
        const response = await axios.get(
          `/api/dance/keypoints/?dance_id=${this.selectedDanceId}`,
          { timeout: 60000 }
        );

        if (response.data.code === 200) {
          this.keyframes = response.data.keyframes || [];
          this.totalFrames = response.data.total_frames || 0;
          this.fps = response.data.fps || 30;
          this.duration = response.data.duration || 0;
        }
      } catch (error) {
        console.error('获取骨架数据失败:', error);
        this.$message.error('骨架数据加载失败');
      } finally {
        this.loading = false;
      }
    },

    // 视频元数据加载完成
    onVideoLoaded() {
      const video = this.$refs.standardVideo;
      const canvas = this.$refs.skeletonCanvas;
      if (!video || !canvas) return;

      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;

      this.videoInfo = {
        totalFrames: this.totalFrames,
        fps: this.fps,
        currentFrame: 0,
      };

      // 初始绘制第一帧骨架
      this.drawSkeleton(0);
    },

    // 视频时间更新：根据时间计算当前帧并绘制骨架
    onVideoTimeUpdate() {
      const video = this.$refs.standardVideo;
      if (!video || !this.isPlaying) return;

      // 根据当前播放时间计算帧索引
      const frameIndex = Math.floor(video.currentTime * this.fps);

      if (frameIndex !== this.currentFrameIndex && frameIndex >= 0 && frameIndex < this.totalFrames) {
        this.currentFrameIndex = frameIndex;
        this.drawSkeleton(frameIndex);

        if (this.videoInfo) {
          this.videoInfo.currentFrame = frameIndex;
        }
      }
    },

    // 绘制指定帧的骨架
    drawSkeleton(frameIndex) {
      const canvas = this.$refs.skeletonCanvas;
      const video = this.$refs.standardVideo;
      if (!canvas || !video) return;

      const ctx = canvas.getContext('2d');

      // 清空画布
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const landmarks = this.keyframes[frameIndex];
      if (!landmarks) return;

      // 使用 drawing_utils（如果有的话）
      if (window.drawConnectors) {
        window.drawConnectors(ctx, landmarks, this.POSE_CONNECTIONS, {
          color: '#00FF00',
          lineWidth: 3
        });
        window.drawLandmarks(ctx, landmarks, {
          color: '#FF4444',
          lineWidth: 2,
          radius: 5,
          fillColor: '#FF4444'
        });
      } else {
        // 兜底：手动绘制骨骼（使用原生 Canvas API）
        this.drawSkeletonManual(ctx, landmarks, canvas.width, canvas.height);
      }
    },

    // 手动绘制骨架（当 MediaPipe drawing_utils 不可用时）
    drawSkeletonManual(ctx, landmarks, w, h) {
      ctx.strokeStyle = '#00FF00';
      ctx.lineWidth = 3;

      // 绘制连接
      for (const [start, end] of this.POSE_CONNECTIONS) {
        const a = landmarks[start];
        const b = landmarks[end];
        if (!a || !b) continue;
        if ((a[3] || 1) < 0.3 || (b[3] || 1) < 0.3) continue;
        ctx.beginPath();
        ctx.moveTo(a[0] * w, a[1] * h);
        ctx.lineTo(b[0] * w, b[1] * h);
        ctx.stroke();
      }

      // 绘制关节点
      ctx.fillStyle = '#FF4444';
      for (const lm of landmarks) {
        if (!lm) continue;
        if ((lm[3] || 1) < 0.3) continue;
        ctx.beginPath();
        ctx.arc(lm[0] * w, lm[1] * h, 5, 0, Math.PI * 2);
        ctx.fill();
      }
    },

    onVideoPlay() {
      this.isPlaying = true;
    },

    onVideoPause() {
      this.isPlaying = false;
    },

    onVideoEnded() {
      this.isPlaying = false;
    },

    cleanup() {
      this.isPlaying = false;
      this.currentFrameIndex = 0;
      this.keyframes = [];
      this.totalFrames = 0;
      this.videoInfo = null;
    }
  }
};
</script>

<style scoped>
.realtime-dance-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  font-size: 28px;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.dance-select {
  text-align: center;
  margin-bottom: 20px;
}

.dance-select select {
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 8px;
  border: 2px solid #ddd;
  min-width: 300px;
}

.video-container {
  display: flex;
  justify-content: center;
}

.video-panel {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.video-panel h3 {
  text-align: center;
  padding: 10px;
  margin: 0;
  background: #f5f5f5;
}

.video-wrapper {
  position: relative;
  display: inline-block;
}

/* 视频原生播放 */
.video-layer {
  width: 640px;
  height: 480px;
  object-fit: cover;
  display: block;
  background: #000;
}

/* 骨架叠加层 */
.skeleton-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 640px;
  height: 480px;
  pointer-events: none;
}

.video-info {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background: #f5f5f5;
  font-size: 13px;
  color: #666;
}

/* 加载动画 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-overlay p {
  margin-top: 20px;
  font-size: 16px;
  color: #666;
}
</style>
