<template>
  <div class="annotation-player-container">
    <h2 class="title">📊 视频关键点标注系统</h2>

    <!-- ============ 上传区域（未上传时） ============ -->
    <div v-if="!annotationId" class="upload-section">
      <div
        class="upload-zone"
        :class="{ 'drag-over': isDragOver }"
        @dragover.prevent="isDragOver = true"
        @dragleave="isDragOver = false"
        @drop.prevent="handleDrop"
      >
        <div class="upload-icon">📹</div>
        <p class="upload-text">将视频文件拖到此处，或<span class="upload-link">点击选择文件</span></p>
        <p class="upload-hint">支持 MP4, AVI, MOV 等常见视频格式</p>
        <input
          type="file"
          class="file-input"
          accept="video/*"
          @change="handleFileSelect"
        />
      </div>
      <div class="button-row">
        <button class="upload-btn" @click="startUpload" :disabled="!selectedFile || isUploading">
          {{ isUploading ? '上传中...' : '🚀 开始处理' }}
        </button>
      </div>
      <p class="history-link">
        想查看已标注的视频？
        <router-link to="/main/health/annotation-history">点击查看标注历史</router-link>
      </p>
    </div>

    <!-- ============ 等待处理/处理中 ============ -->
    <div v-else-if="processingStatus === 'pending' || processingStatus === 'processing'" class="processing-section">
      <div class="processing-card">
        <h3>⏳ 视频处理中</h3>
        <p class="filename">📄 {{ uploadedFilename }}</p>
        <div class="progress-wrap">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progress + '%' }"></div>
          </div>
          <div class="progress-text">{{ progress }}% — {{ processingMessage }}</div>
        </div>
        <div class="stats-row">
          <div class="stat-item"><span class="stat-label">总帧数</span><span class="stat-value">{{ totalFrames || '—' }}</span></div>
          <div class="stat-item"><span class="stat-label">已处理</span><span class="stat-value">{{ frameCount || 0 }}</span></div>
          <div class="stat-item"><span class="stat-label">FPS</span><span class="stat-value">{{ fps || '—' }}</span></div>
          <div class="stat-item"><span class="stat-label">时长</span><span class="stat-value">{{ duration ? duration.toFixed(1) + 's' : '—' }}</span></div>
        </div>
        <p class="hint-text">⏰ 视频正在后台处理中，请稍候...</p>
      </div>
    </div>

    <!-- ============ 处理失败 ============ -->
    <div v-else-if="processingStatus === 'failed'" class="error-section">
      <div class="error-card">
        <h3>❌ 处理失败</h3>
        <p class="error-msg">{{ errorMessage }}</p>
        <button class="reset-btn" @click="reset">重新上传</button>
      </div>
    </div>

    <!-- ============ 处理完成：两栏布局（视频左 + 角度分析右） ============ -->
    <div v-if="processingStatus === 'completed'" class="result-layout">

      <!-- 左栏：视频播放器 -->
      <div class="player-col">

        <!-- 顶部信息栏 -->
        <div class="player-header">
          <div class="header-left">
            <span class="header-title">📄 {{ uploadedFilename }}</span>
            <span class="header-info">{{ totalFrames }} 帧 | {{ fps }} fps | {{ duration ? duration.toFixed(1) + 's' : '—' }}</span>
          </div>
          <div class="header-right">
            <span v-if="isPreRendering" class="pre-render-hint">🔄 预渲染中 ({{ preRenderProgress }}/{{ totalFrames }})...</span>
            <button class="reset-btn-small" @click="reset">重新上传</button>
          </div>
        </div>

        <!-- 预渲染进度遮罩 -->
        <div v-if="isPreRendering" class="pre-render-overlay">
          <div class="pre-render-box">
            <div class="pr-bar-wrap">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: (preRenderProgress / totalFrames * 100).toFixed(1) + '%' }"></div>
              </div>
            </div>
            <p class="pr-text">正在预渲染骨架关键点... {{ preRenderProgress }} / {{ totalFrames }}</p>
          </div>
        </div>

        <!-- 视频 + 骨架叠加 -->
        <div class="video-container">
          <canvas ref="renderCanvas" class="render-canvas"></canvas>
          <video
            ref="videoEl"
            class="video-layer"
            :src="videoSrc"
            @loadedmetadata="onVideoLoaded"
            @timeupdate="onTimeUpdate"
            @play="onPlay"
            @pause="onPause"
            @ended="onEnded"
          ></video>
          <canvas ref="skeletonCanvas" class="skeleton-canvas"></canvas>
        </div>

        <!-- 骨架控制条 -->
        <div class="skeleton-control-bar">
          <div class="ctrl-group">
            <button class="skel-ctrl-btn" :class="{ active: showSkeleton }" @click="toggleSkeleton">
              {{ showSkeleton ? '🎨 隐藏骨架' : '👁 显示骨架' }}
            </button>
            <button class="skel-ctrl-btn" :class="{ active: colorByQuality }" @click="colorByQuality = !colorByQuality; reRenderCurrentSkeleton()">
              {{ colorByQuality ? '🌈 质量染色ON' : '⬜ 质量染色OFF' }}
            </button>
          </div>
          <div class="ctrl-group sliders-group">
            <label class="ctrl-label">
              <span>透明度</span>
              <input type="range" min="0.1" max="1" step="0.05" v-model.number="skeletonOpacity" @input="drawSkeleton(currentFrameIndex)" />
              <span class="ctrl-val">{{ Math.round(skeletonOpacity * 100) }}%</span>
            </label>
            <label class="ctrl-label">
              <span>线粗</span>
              <input type="range" min="1" max="6" step="1" v-model.number="skeletonThickness" @change="reRenderAllSkeletons()" />
              <span class="ctrl-val">{{ skeletonThickness }}px</span>
            </label>
          </div>
        </div>

        <!-- 播放控制条 -->
        <div class="controls-bar">
          <button class="ctrl-btn play-btn" @click="togglePlay">{{ isPlaying ? '⏸' : '▶' }}</button>
          <button class="ctrl-btn frame-btn" @click="prevFrame" title="上一帧">⏮</button>
          <button class="ctrl-btn frame-btn" @click="nextFrame" title="下一帧">⏭</button>
          <span class="time-display">{{ formatTime(currentTime) }} / {{ formatTime(videoDuration) }}</span>
          <div class="seekbar-wrap" @click="seekTo">
            <div class="seekbar" ref="seekbarEl">
              <div class="seekbar-progress" :style="{ width: seekbarPercent + '%' }"></div>
              <div class="seekbar-thumb" :style="{ left: seekbarPercent + '%' }"></div>
            </div>
          </div>
          <select class="speed-select" v-model="playbackRate" @change="setPlaybackRate">
            <option value="0.125">0.125x</option>
            <option value="0.25">0.25x</option>
            <option value="0.5">0.5x</option>
            <option value="0.75">0.75x</option>
            <option value="1">1x</option>
            <option value="1.5">1.5x</option>
            <option value="2">2x</option>
          </select>
        </div>

        <!-- 帧信息栏 -->
        <div class="frame-info-bar">
          <span>帧: <strong>{{ currentFrameIndex }}</strong> / {{ totalFrames }}</span>
          <span class="sep">|</span>
          <span>有效帧: <strong>{{ validFrameCount }}</strong></span>
          <span class="sep">|</span>
          <span>当前: <strong>{{ formatTime(currentTime) }}</strong></span>
          <span class="sep">|</span>
          <span class="valid-badge" :class="currentFrameValid ? 'valid' : 'invalid'">
            {{ currentFrameValid ? '✅ 有效' : '❌ 无效' }}
          </span>
        </div>

      </div>

      <!-- 右栏：角度分析面板 -->
      <div class="angle-panel" :class="{ collapsed: sidePanelCollapsed }">
        <button class="panel-collapse-btn" @click="sidePanelCollapsed = !sidePanelCollapsed">
          {{ sidePanelCollapsed ? '◀' : '▶' }}
        </button>

        <div v-if="isPlaying" class="panel-playing-hint">
          <span>▶ 播放中，暂停查看角度详情</span>
        </div>

        <div v-else class="panel-content">
          <div class="panel-header">
            <div class="panel-title">📐 帧角度分析</div>
            <div class="panel-frame-info">第 {{ currentFrameIndex }} 帧 | {{ formatTime(currentTime) }}</div>
          </div>

          <!-- 快速跳帧条 -->
          <div class="frame-jump-bar">
            <button class="fjump-btn" @click="prevFrame">⏮</button>
            <div class="fjump-range">
              <input
                type="range" min="0" :max="Math.max(0, totalFrames - 1)"
                v-model.number="currentFrameIndex"
                @input="jumpToFrame(currentFrameIndex)"
                class="fjump-slider"
              />
            </div>
            <button class="fjump-btn" @click="nextFrame">⏭</button>
          </div>

          <!-- 角度列表（两列） -->
          <div v-if="currentAngles" class="angle-grid">
            <div
              v-for="(angleData, joint) in currentAnglesDisplay"
              :key="joint"
              class="angle-item"
              :class="'angle-' + angleData.level"
            >
              <div class="angle-info">
                <span class="angle-joint">{{ angleData.cnName }}</span>
                <span class="angle-value" v-if="angleData.angle !== null">{{ angleData.angle.toFixed(1) }}°</span>
                <span class="angle-value angle-null" v-else>—</span>
              </div>
              <div class="angle-bar-bg">
                <div class="angle-bar-fill" :class="'bar-' + angleData.level" :style="{ width: angleData.barWidth + '%' }"></div>
              </div>
              <span class="angle-level-tag" :class="'tag-' + angleData.level">{{ angleData.levelText }}</span>
            </div>
          </div>
          <div v-else class="panel-empty">当前帧无角度数据</div>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
import axios from 'axios';

// MediaPipe Pose 33关键点连接关系
const POSE_CONNECTIONS = [
  [0,1],[1,2],[2,3],[3,7],[0,4],[4,5],[5,6],[6,8],[9,10],
  [11,12],[11,13],[13,15],[15,17],[15,19],[15,21],[17,19],
  [12,14],[14,16],[16,18],[16,20],[16,22],[18,20],
  [11,23],[12,24],[23,24],[23,25],[24,26],[25,27],[26,28],
  [27,29],[28,30],[29,31],[30,32],[27,31],[28,32]
];

const JOINT_NAMES_CN = {
  'left_elbow': '左臂(肘)', 'right_elbow': '右臂(肘)',
  'left_shoulder': '左肩', 'right_shoulder': '右肩',
  'left_hip': '左髋', 'right_hip': '右髋',
  'left_knee': '左膝', 'right_knee': '右膝',
  'left_leg_kick': '左腿踢腿', 'right_leg_kick': '右腿踢腿',
  'trunk': '躯干',
};

export default {
  name: 'AnnotatedVideoPlayer',

  props: {
    initialAnnotationId: { type: [Number, String], default: null },
  },

  data() {
    return {
      selectedFile: null,
      isDragOver: false,
      isUploading: false,
      uploadedFilename: '',
      annotationId: null,
      processingStatus: null,
      progress: 0,
      processingMessage: '',
      errorMessage: '',
      totalFrames: 0,
      frameCount: 0,
      fps: 0,
      duration: 0,
      videoSrc: '',
      isPlaying: false,
      currentTime: 0,
      videoDuration: 0,
      playbackRate: '0.5',
      currentFrameIndex: 0,
      currentFrameValid: true,
      validFrameCount: 0,
      seekbarPercent: 0,
      pollTimer: null,
      resizeObserver: null,

      // 骨架预渲染相关
      isPreRendering: false,
      preRenderProgress: 0,
      // skeletonImages[frameIndex] = ImageData | null
      skeletonImages: {},
      // skeletonAngles[frameIndex] = { joint: angle }
      skeletonAngles: {},
      // skeletonLandmarks[frameIndex] = { landmarks, is_valid }
      skeletonLandmarks: {},
      // 当前帧角度数据
      currentAngles: null,
      // 是否已开始播放
      hasStartedPlaying: false,

      // 播放器增强控制
      showSkeleton: true,
      skeletonOpacity: 0.85,
      skeletonThickness: 2,
      colorByQuality: false,
      sidePanelCollapsed: false,
    };
  },

  computed: {
    userId() {
      const user = JSON.parse(sessionStorage.getItem('userMessage') || '{}');
      return user.id || null;
    },
    token() {
      return sessionStorage.getItem('token') || '';
    },
    currentAnglesDisplay() {
      if (!this.currentAngles) return {};
      const result = {};
      for (const [joint, angle] of Object.entries(this.currentAngles)) {
        const isKick = joint.includes('leg_kick');
        const maxAngle = isKick ? 90 : 180;
        const normalizedAngle = angle !== null ? Math.min(Math.max(angle, 0), maxAngle) : 0;
        const barWidth = angle !== null ? (normalizedAngle / maxAngle) * 100 : 0;
        let level = 'medium', levelText = '一般';
        if (angle !== null) {
          if (isKick) {
            if (angle >= 45) { level = 'excellent'; levelText = '优秀'; }
            else if (angle >= 30) { level = 'good'; levelText = '良好'; }
            else { level = 'bad'; levelText = '待改进'; }
          } else {
            if (angle >= 140) { level = 'excellent'; levelText = '优秀'; }
            else if (angle >= 100) { level = 'good'; levelText = '良好'; }
            else { level = 'bad'; levelText = '待改进'; }
          }
        }
        result[joint] = { angle, cnName: JOINT_NAMES_CN[joint] || joint, barWidth, level, levelText };
      }
      return result;
    },
  },

  created() {
    if (this.initialAnnotationId) {
      this.annotationId = Number(this.initialAnnotationId);
      this.loadAnnotationById(this.annotationId);
    }
  },

  beforeDestroy() {
    this.stopPolling();
    if (this.resizeObserver) this.resizeObserver.disconnect();
    this.cleanupVideo();
  },

  methods: {
    // ============ 上传 & 文件选择 ============

    handleFileSelect(e) {
      const file = e.target.files[0];
      if (file) this.selectedFile = file;
    },

    handleDrop(e) {
      this.isDragOver = false;
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('video/')) this.selectedFile = file;
    },

    async startUpload() {
      if (!this.selectedFile) return;
      this.isUploading = true;
      this.uploadedFilename = this.selectedFile.name;
      const formData = new FormData();
      formData.append('video_file', this.selectedFile);
      if (this.userId) formData.append('user_id', this.userId);
      try {
        const response = await axios.post('/api/annotation/upload/', formData, {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        if (response.data.code === 202 || response.data.code === 200) {
          this.annotationId = response.data.annotation_id;
          this.processingStatus = 'pending';
          this.startPolling();
        } else {
          this.$message.error(response.data.error || '上传失败');
        }
      } catch (error) {
        this.$message.error('上传失败: ' + (error.message || '网络错误'));
      } finally {
        this.isUploading = false;
      }
    },

    startPolling() {
      this.stopPolling();
      this.pollTimer = setInterval(() => this.checkStatus(), 2000);
    },

    stopPolling() {
      if (this.pollTimer) { clearInterval(this.pollTimer); this.pollTimer = null; }
    },

    async checkStatus() {
      if (!this.annotationId) return;
      try {
        const resp = await axios.get(`/api/annotation/status/?annotation_id=${this.annotationId}`, {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        const d = resp.data;
        if (d.code === 200) {
          const s = d.data;
          this.processingStatus = s.status;
          this.progress = s.progress || 0;
          this.processingMessage = s.message || '';
          this.totalFrames = s.total_frames || 0;
          this.frameCount = s.frame_count || 0;
          this.fps = s.fps || 0;
          this.duration = s.duration || 0;
          if (s.status === 'completed') {
            this.uploadedFilename = s.original_filename || this.uploadedFilename;
            this.stopPolling();
            this.onProcessingComplete();
          } else if (s.status === 'failed') {
            this.errorMessage = s.message || '处理失败';
            this.stopPolling();
          }
        }
      } catch {}
    },

    // ============ 从标注ID直接加载 ============

    async loadAnnotationById(annotationId) {
      this.annotationId = annotationId;
      try {
        const resp = await axios.get(
          `/api/annotation/status/?annotation_id=${annotationId}`,
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
        if (resp.data.code === 200) {
          const d = resp.data.data;
          this.totalFrames = d.total_frames || 0;
          this.fps = d.fps || 0;
          this.duration = d.duration || 0;
          this.uploadedFilename = d.original_filename || '';
          this.videoSrc = d.video_url;
          this.processingStatus = 'completed';
          this.$nextTick(() => this.startPreRendering());
        } else {
          this.$message.error(resp.data.error || '加载标注失败');
        }
      } catch (error) {
        this.$message.error('加载标注失败: ' + (error.message || '网络错误'));
      }
    },

    // ============ 处理完成 ============

    onProcessingComplete() {
      this.$nextTick(() => this.startPreRendering());
    },

    // ============ 骨架预渲染（核心） ============
    // 把所有帧的关键点一次性预绘制到 skeletonImages 缓存中
    // 然后播放时直接合成，不再有网络/时序问题

    async startPreRendering() {
      const video = this.$refs.videoEl;
      if (!video) return;

      // 等待视频元数据加载（知道尺寸）
      if (video.readyState < 1) {
        await new Promise(resolve => video.addEventListener('loadedmetadata', resolve, { once: true }));
      }

      this.isPreRendering = true;
      this.preRenderProgress = 0;
      this.skeletonImages = {};

      try {
        // 一次性获取所有帧数据
        const resp = await axios.get(
          `/api/annotation/frames/?annotation_id=${this.annotationId}&start_frame=0&end_frame=${this.totalFrames > 0 ? this.totalFrames - 1 : 0}`,
          { headers: { Authorization: `Bearer ${this.token}` }, timeout: 60000 }
        );

        if (resp.data.code !== 200) {
          this.$message.error(resp.data.error || '获取帧数据失败');
          this.isPreRendering = false;
          return;
        }

        const frames = resp.data.data.frames || [];
        const videoW = Math.round(video.videoWidth || 640);
        const videoH = Math.round(video.videoHeight || 480);

        this.validFrameCount = frames.filter(f => f.is_valid).length;
        // 缓存角度和关键点数据
        this.skeletonAngles = {};
        this.skeletonLandmarks = {};
        for (const f of frames) {
          if (f.angles) this.skeletonAngles[f.frame_index] = f.angles;
          if (f.landmarks) this.skeletonLandmarks[f.frame_index] = { landmarks: f.landmarks, is_valid: f.is_valid };
        }

        // 逐帧预绘制，使用 requestAnimationFrame 分批处理避免卡UI
        await this.batchPreRender(frames, videoW, videoH);

        this.isPreRendering = false;
        this.hasStartedPlaying = false;

        // 初始化 canvas 尺寸
        this.$nextTick(() => {
          this.syncCanvasSize();
          // 默认显示第0帧
          this.currentFrameIndex = 0;
          this.drawSkeleton(0);
        });

      } catch (error) {
        this.isPreRendering = false;
        this.$message.error('加载帧数据失败: ' + (error.message || '网络错误'));
      }
    },

    // 分批预渲染，每批 N 帧，用 rAF 让 UI 有机会更新
    batchPreRender(frames, videoW, videoH) {
      return new Promise(resolve => {
        const BATCH = 50; // 每批处理50帧
        let i = 0;

        const processBatch = () => {
          const end = Math.min(i + BATCH, frames.length);
          for (; i < end; i++) {
            const f = frames[i];
            const frameAngles = f.angles || {};
            this.skeletonImages[f.frame_index] = this.renderSkeletonToImageData(
              f.landmarks, f.is_valid, videoW, videoH, frameAngles
            );
            this.preRenderProgress = i + 1;
          }
          if (i < frames.length) {
            requestAnimationFrame(processBatch);
          } else {
            resolve();
          }
        };

        requestAnimationFrame(processBatch);
      });
    },

    // 在离屏 canvas 上绘制单帧骨架，返回 ImageData
    renderSkeletonToImageData(landmarks, isValid, w, h, angles) {
      const offCanvas = document.createElement('canvas');
      offCanvas.width = w;
      offCanvas.height = h;
      const ctx = offCanvas.getContext('2d');

      if (!isValid || !landmarks || landmarks.length === 0) {
        return ctx.getImageData(0, 0, w, h); // 空白
      }

      const pts = [];
      for (let i = 0; i < landmarks.length; i += 4) {
        pts.push([landmarks[i], landmarks[i+1], landmarks[i+2], landmarks[i+3]]);
      }

      const thickness = this.skeletonThickness;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      const frameAngles = angles || {};
      const jointColorMap = this.buildJointColorMap(frameAngles);

      // 画连接线
      for (const [a, b] of POSE_CONNECTIONS) {
        const pA = pts[a];
        const pB = pts[b];
        if (!pA || !pB) continue;
        if ((pA[3] || 0) < 0.3 || (pB[3] || 0) < 0.3) continue;

        let color = '#00FF00';
        if (this.colorByQuality && jointColorMap) {
          color = jointColorMap[a] || jointColorMap[b] || '#00FF00';
        }
        ctx.strokeStyle = color;
        ctx.lineWidth = thickness;
        ctx.beginPath();
        ctx.moveTo(pA[0] * w, pA[1] * h);
        ctx.lineTo(pB[0] * w, pB[1] * h);
        ctx.stroke();
      }

      // 画关键点
      ctx.fillStyle = '#FF4444';
      for (const p of pts) {
        if (!p) continue;
        if ((p[3] || 0) < 0.3) continue;
        ctx.beginPath();
        ctx.arc(p[0] * w, p[1] * h, 4, 0, Math.PI * 2);
        ctx.fill();
      }

      return ctx.getImageData(0, 0, w, h);
    },

    buildJointColorMap(angles) {
      const map = {};
      const colors = {
        excellent: '#4caf50',
        good: '#69f0ae',
        medium: '#ffca28',
        bad: '#ff5252',
      };
      const jointIdxMap = {
        left_shoulder: 11, right_shoulder: 12,
        left_elbow: 13, right_elbow: 14,
        left_hip: 23, right_hip: 24,
        left_knee: 25, right_knee: 26,
        left_leg_kick: 27, right_leg_kick: 28,
      };
      for (const [joint, angle] of Object.entries(angles)) {
        const isKick = joint.includes('leg_kick');
        let level = 'bad';
        if (angle !== null) {
          if (isKick) {
            if (angle >= 45) level = 'excellent';
            else if (angle >= 30) level = 'good';
          } else {
            if (angle >= 140) level = 'excellent';
            else if (angle >= 100) level = 'good';
          }
        }
        const idx = jointIdxMap[joint];
        if (idx !== undefined) map[idx] = colors[level];
      }
      return map;
    },

    // ============ 视频元数据加载 ============

    onVideoLoaded() {
      const video = this.$refs.videoEl;
      if (!video) return;
      this.videoDuration = video.duration;
      this.syncCanvasSize();

      if (!this.resizeObserver) {
        this.resizeObserver = new ResizeObserver(() => {
          this.syncCanvasSize();
        });
        this.resizeObserver.observe(video);
      }
    },

    syncCanvasSize() {
      const video = this.$refs.videoEl;
      const skCanvas = this.$refs.skeletonCanvas;
      if (!video || !skCanvas) return;
      const w = Math.round(video.videoWidth || video.clientWidth || 640);
      const h = Math.round(video.videoHeight || video.clientHeight || 480);
      skCanvas.width = w;
      skCanvas.height = h;
    },

    // ============ 时间更新 -> 绘制 ============

    onTimeUpdate() {
      const video = this.$refs.videoEl;
      if (!video) return;
      this.currentTime = video.currentTime;
      this.seekbarPercent = this.videoDuration > 0 ? (this.currentTime / this.videoDuration) * 100 : 0;
      const frameIndex = this.fps > 0 ? Math.floor(video.currentTime * this.fps) : 0;
      if (frameIndex !== this.currentFrameIndex) {
        this.currentFrameIndex = frameIndex;
        this.updateCurrentFrame();
      }
    },

    updateCurrentFrame() {
      const frameData = this.skeletonImages[this.currentFrameIndex];
      this.currentFrameValid = !!(frameData && this.hasNonEmptyPixels(frameData));
      this.currentAngles = this.skeletonAngles[this.currentFrameIndex] || null;
      this.drawSkeleton(this.currentFrameIndex);
    },

    hasNonEmptyPixels(imgData) {
      // 简单判断 ImageData 是否全透明
      for (let i = 3; i < imgData.data.length; i += 4) {
        if (imgData.data[i] > 0) return true;
      }
      return false;
    },

    drawSkeleton(frameIndex) {
      const skCanvas = this.$refs.skeletonCanvas;
      if (!skCanvas) return;
      const ctx = skCanvas.getContext('2d');
      ctx.clearRect(0, 0, skCanvas.width, skCanvas.height);
      if (!this.showSkeleton) return;
      const imgData = this.skeletonImages[frameIndex];
      if (imgData) {
        ctx.globalAlpha = this.skeletonOpacity;
        ctx.putImageData(imgData, 0, 0);
        ctx.globalAlpha = 1;
      }
    },

    toggleSkeleton() {
      this.showSkeleton = !this.showSkeleton;
      this.drawSkeleton(this.currentFrameIndex);
    },

    reRenderCurrentSkeleton() {
      this.drawSkeleton(this.currentFrameIndex);
    },

    reRenderAllSkeletons() {
      if (!this.videoSrc || Object.keys(this.skeletonLandmarks).length === 0) return;
      const video = this.$refs.videoEl;
      const videoW = Math.round(video?.videoWidth || 640);
      const videoH = Math.round(video?.videoHeight || 480);
      const allFrames = Object.entries(this.skeletonLandmarks).map(([fi, data]) => ({
        frame_index: parseInt(fi),
        landmarks: data.landmarks,
        is_valid: data.is_valid,
        angles: this.skeletonAngles[fi] || {},
      }));
      this.batchPreRender(allFrames, videoW, videoH).then(() => {
        this.drawSkeleton(this.currentFrameIndex);
      });
    },

    jumpToFrame(frameIndex) {
      const video = this.$refs.videoEl;
      if (!video || !this.fps) return;
      const clamped = Math.max(0, Math.min(frameIndex, this.totalFrames - 1));
      video.currentTime = clamped / this.fps;
    },

    // ============ 播放控制 ============

    togglePlay() {
      const video = this.$refs.videoEl;
      if (!video) return;
      if (this.isPlaying) video.pause();
      else video.play();
    },

    onPlay() { this.isPlaying = true; },
    onPause() { this.isPlaying = false; },
    onEnded() { this.isPlaying = false; },

    setPlaybackRate() {
      const video = this.$refs.videoEl;
      if (video) video.playbackRate = parseFloat(this.playbackRate);
    },

    seekTo(e) {
      const seekbar = this.$refs.seekbarEl;
      if (!seekbar) return;
      const rect = seekbar.getBoundingClientRect();
      const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      const video = this.$refs.videoEl;
      if (video && this.videoDuration) {
        video.currentTime = ratio * this.videoDuration;
      }
    },

    prevFrame() {
      const video = this.$refs.videoEl;
      if (!video || !this.fps) return;
      const step = 1 / this.fps;
      video.currentTime = Math.max(0, video.currentTime - step);
    },

    nextFrame() {
      const video = this.$refs.videoEl;
      if (!video || !this.fps) return;
      const step = 1 / this.fps;
      video.currentTime = Math.min(video.duration, video.currentTime + step);
    },

    stepBackward() {
      const video = this.$refs.videoEl;
      if (!video || !this.fps) return;
      video.currentTime = Math.max(0, video.currentTime - 0.05);
    },

    stepForward() {
      const video = this.$refs.videoEl;
      if (!video || !this.fps) return;
      video.currentTime = Math.min(video.duration, video.currentTime + 0.05);
    },

    formatTime(seconds) {
      if (!seconds || isNaN(seconds)) return '0:00';
      const m = Math.floor(seconds / 60);
      const s = Math.floor(seconds % 60);
      return `${m}:${s.toString().padStart(2, '0')}`;
    },

    // ============ 重置 ============

    reset() {
      this.stopPolling();
      this.annotationId = null;
      this.processingStatus = null;
      this.progress = 0;
      this.processingMessage = '';
      this.errorMessage = '';
      this.totalFrames = 0;
      this.frameCount = 0;
      this.fps = 0;
      this.duration = 0;
      this.videoSrc = '';
      this.isPlaying = false;
      this.currentTime = 0;
      this.videoDuration = 0;
      this.currentFrameIndex = 0;
      this.validFrameCount = 0;
      this.seekbarPercent = 0;
      this.selectedFile = null;
      this.skeletonImages = {};
      this.skeletonAngles = {};
      this.skeletonLandmarks = {};
      this.currentAngles = null;
      this.isPreRendering = false;
      this.preRenderProgress = 0;
      this.hasStartedPlaying = false;
      this.showSkeleton = true;
      this.skeletonOpacity = 0.85;
      this.skeletonThickness = 2;
      this.colorByQuality = false;
      this.sidePanelCollapsed = false;
      this.cleanupVideo();
    },

    cleanupVideo() {
      const video = this.$refs.videoEl;
      if (video) {
        video.pause();
        video.removeAttribute('src');
        video.load();
      }
    },
  },
};
</script>

<style scoped>
.annotation-player-container {
  max-width: 1320px;
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

/* ============ 上传区域 ============ */
.upload-section { text-align: center; }
.upload-zone {
  position: relative;
  border: 2px dashed #c0c8e8;
  border-radius: 16px;
  padding: 60px 20px;
  background: #f8f9ff;
  transition: all 0.2s;
  cursor: pointer;
}
.upload-zone:hover, .upload-zone.drag-over {
  border-color: #667eea;
  background: #eef1ff;
}
.upload-icon { font-size: 48px; margin-bottom: 12px; }
.upload-text { font-size: 16px; color: #444; margin-bottom: 8px; }
.upload-link { color: #667eea; font-weight: 600; }
.upload-hint { font-size: 13px; color: #999; }
.upload-zone .file-input {
  position: absolute; inset: 0; opacity: 0; cursor: pointer; width: 100%; height: 100%;
}
.button-row { margin-top: 16px; }
.upload-btn {
  padding: 12px 36px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff; border: none; border-radius: 24px;
  font-size: 16px; cursor: pointer;
}
.upload-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.history-link { font-size: 13px; color: #888; margin-top: 8px; }
.history-link a { color: #667eea; text-decoration: none; font-weight: 600; }
.history-link a:hover { text-decoration: underline; }

/* ============ 处理中 ============ */
.processing-section, .error-section { text-align: center; padding: 20px; }
.processing-card, .error-card {
  background: #fff; border-radius: 16px; padding: 32px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08); display: inline-block; width: 100%; max-width: 500px;
}
.progress-wrap { margin: 16px 0; }
.progress-bar { height: 8px; background: #eee; border-radius: 4px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 4px; transition: width 0.3s; }
.progress-text { font-size: 13px; color: #888; margin-top: 6px; }
.stats-row { display: flex; justify-content: center; gap: 20px; margin: 16px 0; flex-wrap: wrap; }
.stat-item { text-align: center; }
.stat-label { display: block; font-size: 12px; color: #aaa; }
.stat-value { display: block; font-size: 20px; font-weight: 700; color: #333; }
.hint-text { font-size: 13px; color: #aaa; margin-top: 12px; }
.filename { font-size: 14px; color: #666; margin-bottom: 4px; }

/* 两栏布局 */
.result-layout {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}
.player-col {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

/* 顶部信息栏 */
.player-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 6px; flex-wrap: wrap; gap: 8px;
}
.header-left { display: flex; flex-direction: column; gap: 2px; }
.header-title { font-size: 15px; font-weight: 600; color: #333; }
.header-info { font-size: 13px; color: #888; }
.header-right { display: flex; align-items: center; gap: 10px; }
.pre-render-hint { font-size: 12px; color: #f57c00; }

/* 预渲染遮罩 */
.pre-render-overlay {
  background: rgba(255,255,255,0.92);
  border-radius: 12px 12px 0 0;
  border: 1px solid #e0e0e0;
  border-bottom: none;
  padding: 16px;
}
.pre-render-box { text-align: center; }
.pr-bar-wrap { max-width: 400px; margin: 0 auto; }
.pr-text { font-size: 13px; color: #888; margin-top: 8px; }

/* 视频容器 */
.video-container {
  position: relative;
  background: #000;
  border: 1px solid #e0e0e0;
  border-radius: 12px 12px 0 0;
  overflow: hidden;
  text-align: center;
}
.render-canvas { display: none; }
.video-layer {
  display: block;
  width: 100%;
  background: #000;
  border-radius: 12px 12px 0 0;
}
.skeleton-canvas {
  position: absolute;
  top: 0; left: 50%;
  transform: translateX(-50%);
  width: 100%; height: 100%;
  pointer-events: none;
}

/* 骨架控制条 */
.skeleton-control-bar {
  display: flex; align-items: center; justify-content: space-between;
  gap: 12px; padding: 7px 12px;
  background: #f8f9ff;
  border: 1px solid #e0e0e0;
  border-top: none;
  flex-wrap: wrap;
}
.ctrl-group { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.skel-ctrl-btn {
  padding: 4px 12px; background: #fff; border: 1px solid #ddd;
  border-radius: 14px; font-size: 12px; cursor: pointer; color: #666;
  transition: all 0.2s;
}
.skel-ctrl-btn:hover { background: #667eea; color: #fff; border-color: #667eea; }
.skel-ctrl-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff; border-color: transparent;
}
.sliders-group { gap: 12px; }
.ctrl-label { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #666; white-space: nowrap; }
.ctrl-label input[type="range"] { width: 65px; accent-color: #667eea; cursor: pointer; }
.ctrl-val { font-size: 11px; font-weight: 600; color: #667eea; min-width: 28px; }

/* 播放控制条 */
.controls-bar {
  display: flex; align-items: center; gap: 8px;
  padding: 9px 12px;
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-top: none;
  flex-wrap: wrap;
}
.ctrl-btn {
  padding: 5px 10px; background: #fff; border: 1px solid #ddd;
  border-radius: 8px; cursor: pointer; font-size: 14px;
}
.ctrl-btn:hover { background: #667eea; color: #fff; border-color: #667eea; }
.play-btn { font-size: 17px; padding: 5px 14px; }
.time-display { font-size: 13px; color: #666; white-space: nowrap; }
.seekbar-wrap { flex: 1; min-width: 80px; cursor: pointer; padding: 8px 0; }
.seekbar { position: relative; height: 6px; background: #ddd; border-radius: 3px; }
.seekbar-progress {
  position: absolute; left: 0; top: 0; height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 3px;
}
.seekbar-thumb {
  position: absolute; top: 50%; transform: translate(-50%, -50%);
  width: 14px; height: 14px; background: #667eea; border-radius: 50%;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
}
.speed-select {
  padding: 5px 8px; border: 1px solid #ddd; border-radius: 8px;
  font-size: 13px; background: #fff; cursor: pointer;
}

/* 帧信息栏 */
.frame-info-bar {
  display: flex; align-items: center; justify-content: center; gap: 12px;
  padding: 7px 12px; background: #fafafa;
  border: 1px solid #e0e0e0; border-top: none;
  border-radius: 0 0 12px 12px;
  font-size: 13px; color: #666; flex-wrap: wrap;
}
.frame-info-bar strong { color: #333; }
.frame-info-bar .sep { color: #ddd; margin: 0 4px; }
.valid-badge { padding: 2px 10px; border-radius: 10px; font-size: 12px; }
.valid-badge.valid { background: rgba(76,175,80,0.1); color: #4caf50; }
.valid-badge.invalid { background: rgba(244,67,54,0.1); color: #f44336; }

.reset-btn { padding: 10px 28px; background: #fff; border: 1px solid #ddd; border-radius: 20px; font-size: 14px; cursor: pointer; margin-top: 12px; }
.reset-btn:hover { background: #f5f5f5; }
.reset-btn-small { padding: 5px 14px; background: #fff; border: 1px solid #ddd; border-radius: 16px; font-size: 13px; cursor: pointer; }
.reset-btn-small:hover { background: #667eea; color: #fff; border-color: #667eea; }

/* ============ 角度面板 ============ */
.angle-panel {
  width: 340px;
  flex-shrink: 0;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  overflow: hidden;
  position: relative;
  transition: width 0.25s ease;
  max-height: calc(100vh - 180px);
  display: flex;
  flex-direction: column;
}
.angle-panel.collapsed { width: 36px; }

.panel-collapse-btn {
  position: absolute; top: 50%; right: -18px; transform: translateY(-50%);
  width: 18px; height: 60px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff; border: none; border-radius: 0 8px 8px 0;
  cursor: pointer; font-size: 11px;
  display: flex; align-items: center; justify-content: center;
  writing-mode: vertical-rl; letter-spacing: 1px; z-index: 10;
}
.panel-collapse-btn:hover { background: linear-gradient(135deg, #5a70d9, #6a4190); }

.panel-playing-hint {
  padding: 20px 16px; text-align: center; background: #f8f9ff;
  flex: 1; display: flex; align-items: center; justify-content: center;
}
.panel-playing-hint span {
  font-size: 12px; color: #667eea;
  background: rgba(102,126,234,0.08); padding: 5px 14px;
  border-radius: 20px; font-weight: 500;
}

.panel-content { display: flex; flex-direction: column; overflow: hidden; flex: 1; }

.panel-header {
  padding: 10px 14px; border-bottom: 1px solid #eee;
  background: linear-gradient(135deg, #667eea, #764ba2);
  flex-shrink: 0;
}
.panel-title { font-size: 13px; font-weight: 600; color: #fff; margin-bottom: 2px; }
.panel-frame-info { font-size: 11px; color: rgba(255,255,255,0.7); }

/* 快速跳帧 */
.frame-jump-bar {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 12px; background: #f8f9ff; border-bottom: 1px solid #eee;
  flex-shrink: 0;
}
.fjump-btn {
  padding: 3px 8px; background: #fff; border: 1px solid #ddd;
  border-radius: 8px; cursor: pointer; font-size: 13px;
  transition: all 0.2s; flex-shrink: 0;
}
.fjump-btn:hover { background: #667eea; color: #fff; border-color: #667eea; }
.fjump-range { flex: 1; }
.fjump-slider { width: 100%; accent-color: #667eea; cursor: pointer; height: 20px; }

/* 角度网格（两列） */
.angle-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  padding: 8px 10px;
  overflow-y: auto;
  flex: 1;
}
.angle-item {
  padding: 6px 8px; border-radius: 10px;
  border-left: 3px solid #ddd; background: #fafafa;
  transition: background 0.2s;
}
.angle-item.angle-excellent { background: rgba(76,175,80,0.06); border-left-color: #4caf50; }
.angle-item.angle-good { background: rgba(105,240,174,0.06); border-left-color: #69f0ae; }
.angle-item.angle-medium { background: rgba(255,202,40,0.06); border-left-color: #ffca28; }
.angle-item.angle-bad { background: rgba(255,82,82,0.06); border-left-color: #ff5252; }

.angle-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; gap: 4px; }
.angle-joint { font-size: 11px; color: #555; font-weight: 500; }
.angle-value { font-size: 13px; font-weight: 700; color: #333; white-space: nowrap; }
.angle-null { color: #bbb; font-size: 11px; }
.angle-bar-bg { height: 4px; background: #eee; border-radius: 2px; overflow: hidden; margin-bottom: 3px; }
.angle-bar-fill { height: 100%; border-radius: 2px; transition: width 0.3s; }
.bar-excellent { background: linear-gradient(90deg, #4caf50, #69f0ae); }
.bar-good { background: linear-gradient(90deg, #69f0ae, #b2f0d0); }
.bar-medium { background: linear-gradient(90deg, #ffca28, #ffe082); }
.bar-bad { background: linear-gradient(90deg, #ff5252, #ff8a80); }
.angle-level-tag { font-size: 10px; padding: 1px 6px; border-radius: 8px; font-weight: 600; display: inline-block; }
.tag-excellent { background: rgba(76,175,80,0.15); color: #4caf50; }
.tag-good { background: rgba(105,240,174,0.15); color: #2e7d32; }
.tag-medium { background: rgba(255,202,40,0.15); color: #f57f17; }
.tag-bad { background: rgba(255,82,82,0.15); color: #d32f2f; }

.panel-empty { padding: 20px; text-align: center; color: #aaa; font-size: 13px; }
</style>
