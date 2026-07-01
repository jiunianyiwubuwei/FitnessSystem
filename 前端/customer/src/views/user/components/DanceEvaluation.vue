<template>
  <div class="dance-container">
    <h2 class="title">💃 舞蹈评分系统</h2>

    <!-- 上传区域 -->
    <div class="upload-section">
      <div class="control-row">
        <input type="file" class="file-input" @change="handleFileUpload" accept="video/*" />
        <select v-model="selectedDance" class="dance-select">
          <option v-for="dance in danceList" :key="dance.id" :value="dance.id">
            {{ dance.name }}
          </option>
        </select>
      </div>
      <button class="start-btn" @click="startEvaluation" :disabled="!videoFile">
        🎯 开始评分
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-section">
      <div class="spinner"></div>
      <p>{{ loadingMessage }}</p>
      <p class="tip">提示：请允许浏览器弹窗</p>
    </div>

    <!-- 结果展示 -->
    <div v-if="!loading && result" class="result-section">
      <h3>🎉 评分完成！</h3>
      <div class="result-summary">
        <div class="score-display">
          <span class="score">{{ result.total_score }}</span>
          <span class="grade" :class="'grade-' + result.grade">{{ result.grade }}</span>
        </div>
        <p class="comment">{{ result.comment }}</p>
        <div class="detail-scores">
          <div>准确度: {{ result.accuracy_score }}分</div>
          <div>节奏感: {{ result.rhythm_score }}分</div>
          <div>流畅度: {{ result.fluency_score }}分</div>
        </div>
      </div>
      <button class="reset-btn" @click="reset">重新评分</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "DanceEvaluation",
  data() {
    return {
      videoFile: null,
      selectedDance: null,
      danceList: [],
      loading: false,
      loadingMessage: '正在处理...',
      result: null,
      videoObjectUrl: null,
      storageKey: 'dance_eval_' + Date.now()
    };
  },
  computed: {
    userId() {
      const user = JSON.parse(sessionStorage.getItem('userMessage') || '{}');
      return user.id || null;
    },
    token() {
      return sessionStorage.getItem('token') || '';
    }
  },
  mounted() {
    this.fetchDanceList();
    // 监听 storage 事件（来自子窗口）
    window.addEventListener('storage', this.handleStorageEvent);
    // 监听 message 事件
    window.addEventListener('message', this.handleMessage);
  },
  beforeDestroy() {
    window.removeEventListener('storage', this.handleStorageEvent);
    window.removeEventListener('message', this.handleMessage);
    this.cleanup();
  },
  methods: {
    // 获取舞蹈列表
    async fetchDanceList() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/dance/standards/', {
          headers: { 'Authorization': `Bearer ${this.token}` }
        });
        if (response.ok) {
          const data = await response.json();
          this.danceList = data.data || [];
          if (this.danceList.length > 0) {
            this.selectedDance = this.danceList[0].id;
          }
        }
      } catch (error) {
        console.error('获取舞蹈列表失败:', error);
      }
    },

    // 处理文件选择
    handleFileUpload(event) {
      this.videoFile = event.target.files[0];
      this.result = null;
      if (this.videoFile) {
        console.log('已选择:', this.videoFile.name);
      }
    },

    // 开始评分
    async startEvaluation() {
      if (!this.videoFile) {
        alert('请先选择视频文件！');
        return;
      }
      if (!this.selectedDance) {
        alert('请选择舞蹈类型！');
        return;
      }
      if (!this.userId) {
        alert('用户未登录！');
        return;
      }

      this.loading = true;
      this.loadingMessage = '正在准备分析窗口...';
      this.storageKey = 'dance_eval_' + Date.now();

      try {
        // 创建视频 URL
        this.videoObjectUrl = URL.createObjectURL(this.videoFile);
        this.loadingMessage = '正在打开分析窗口...';

        // 先打开评分窗口
        this.openScoreWindow();

        // 延迟打开视频窗口，确保评分窗口先加载
        await new Promise(r => setTimeout(r, 800));
        this.openPoseWindow();

        this.loading = false;

      } catch (error) {
        console.error('启动失败:', error);
        alert('启动失败: ' + error.message);
        this.loading = false;
        this.cleanup();
      }
    },

    // 打开体态识别窗口
    openPoseWindow() {
      const videoUrl = this.videoObjectUrl;
      const storageKey = this.storageKey;

      const html = `<!DOCTYPE html>
<html>
<head>
  <title>体态识别 - 舞蹈评分</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #000; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: Arial, sans-serif; overflow: hidden; }
    .container { position: relative; width: 100%; max-width: 900px; }
    video { width: 100%; display: block; background: #000; }
    canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
    .info { position: fixed; top: 15px; left: 15px; background: rgba(0,0,0,0.85); color: #0f0; padding: 15px 20px; border-radius: 12px; font-size: 15px; font-family: 'Courier New', monospace; z-index: 100; border: 1px solid #0f0; }
    .controls { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 15px; z-index: 100; }
    button { padding: 12px 30px; border: none; border-radius: 25px; cursor: pointer; font-size: 15px; font-weight: bold; transition: all 0.2s; }
    button:hover { transform: scale(1.05); }
    .play { background: #4CAF50; color: #fff; }
    .pause { background: #FF9800; color: #fff; }
    .close { background: #f44336; color: #fff; }
    .speed-control { position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; z-index: 100; }
    .speed-btn { padding: 8px 18px; border: 2px solid #fff; background: transparent; color: #fff; border-radius: 18px; font-size: 13px; cursor: pointer; transition: all 0.2s; }
    .speed-btn.active { background: #667eea; border-color: #667eea; }
    .loading-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); display: flex; flex-direction: column; justify-content: center; align-items: center; color: #fff; z-index: 200; }
    .loading-overlay.hidden { display: none; }
    .spinner { width: 50px; height: 50px; border: 4px solid #333; border-top: 4px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20px; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .error { color: #f44336; padding: 20px; text-align: center; }
  </style>
</head>
<body>
  <div class="loading-overlay" id="loadingOverlay">
    <div class="spinner"></div>
    <p id="loadingMsg">正在加载 MediaPipe...</p>
    <p style="font-size:12px;color:#888;margin-top:10px;">请确保网络连接</p>
  </div>

  <div class="container">
    <video id="video" playsinline crossorigin="anonymous"></video>
    <canvas id="canvas"></canvas>
  </div>

  <div class="info">
    <div>帧: <span id="frameCount">0</span> | FPS: <span id="fps">0</span></div>
    <div style="margin-top:5px;">状态: <span id="status">初始化中</span></div>
  </div>

  <div class="speed-control">
    <button class="speed-btn" data-speed="0.25">0.25x</button>
    <button class="speed-btn active" data-speed="0.5">0.5x</button>
    <button class="speed-btn" data-speed="1">1x</button>
  </div>

  <div class="controls">
    <button class="play" id="playBtn">▶ 播放</button>
    <button class="pause" id="pauseBtn">⏸ 暂停</button>
    <button class="close" id="closeBtn">✕ 关闭</button>
  </div>

  <script>
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const frameEl = document.getElementById('frameCount');
    const fpsEl = document.getElementById('fps');
    const statusEl = document.getElementById('status');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingMsg = document.getElementById('loadingMsg');

    const STORAGE_KEY = '${storageKey}';

    let pose = null;
    let frameCount = 0;
    let lastTime = Date.now();
    let isPlaying = false;
    let playSpeed = 0.5;
    let initDone = false;

    // ===== 动态加载脚本（带超时重试） =====
    function loadScript(src, timeout) {
      return new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
          cleanup();
          reject(new Error('加载超时: ' + src));
        }, timeout);

        const script = document.createElement('script');
        script.src = src;
        script.onload = () => { clearTimeout(timer); resolve(); };
        script.onerror = () => { clearTimeout(timer); reject(new Error('加载失败: ' + src)); };
        document.head.appendChild(script);
      });
    }

    // ===== CDN 列表已内联到 tryLoadFromCDNs 中 =====

    async function tryLoadFromCDNs() {
      const errors = [];
      const scripts = [
        // 方案1: jsdelivr npm latest
        'https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils@0.3.1675466862/camera_utils.js',
        'https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils@0.3.1675466124/drawing_utils.js',
        'https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5.1675469404/pose.js',
        // 方案2: unpkg npm latest
        'https://unpkg.com/@mediapipe/camera_utils@0.3.1675466862/camera_utils.js',
        'https://unpkg.com/@mediapipe/drawing_utils@0.3.1675466124/drawing_utils.js',
        'https://unpkg.com/@mediapipe/pose@0.5.1675469404/pose.js',
        // 方案3: cloudflare
        'https://cdnjs.cloudflare.com/ajax/libs/mediapipe/0.3.1675466862/camera_utils.js',
        'https://cdnjs.cloudflare.com/ajax/libs/mediapipe/0.3.1675466124/drawing_utils.js',
        'https://cdnjs.cloudflare.com/ajax/libs/mediapipe/0.5.1675469404/pose.js',
        // 方案4: unpkg 旧版
        'https://unpkg.com/@mediapipe/camera_utils@0.3.90001.0/camera_utils.js',
        'https://unpkg.com/@mediapipe/drawing_utils@0.3.90001.0/drawing_utils.js',
        'https://unpkg.com/@mediapipe/pose@0.3.90001.0/pose.js',
        // 方案5: 本地文件
        '/mediapipe/camera_utils.js',
        '/mediapipe/drawing_utils.js',
        '/mediapipe/pose.js',
      ];

      const required = ['camera_utils.js', 'drawing_utils.js', 'pose.js'];
      const loaded = new Set();

      for (const src of scripts) {
        const fileName = src.split('/').pop();
        if (loaded.has(fileName)) continue;
        try {
          await loadScript(src, 8000);
          loaded.add(fileName);
          if (loaded.size === 3) return; // all loaded
        } catch (e) {
          errors.push('加载失败: ' + src);
        }
      }

      if (!window.Pose) {
        throw new Error('所有CDN均加载失败: ' + errors.join('; '));
      }
    }

    function showError(msg) {
      loadingOverlay.innerHTML = '<div class="error">' + msg + '<br><br><button onclick="location.reload()" style="padding:10px 20px;background:#667eea;color:#fff;border:none;border-radius:5px;cursor:pointer;">重试</button></div>';
    }

    video.src = '${videoUrl}';
    video.muted = true;
    video.playbackRate = playSpeed;

    // 发送当前视频时间到评分窗口
    function sendDuration() {
      if (video.videoWidth > 0) {
        localStorage.setItem(STORAGE_KEY + '_duration', video.duration.toString());
        localStorage.setItem(STORAGE_KEY + '_trigger', Date.now().toString());
      }
    }

    function sendCurrentTime() {
      localStorage.setItem(STORAGE_KEY + '_currentTime', video.currentTime.toString());
    }

    video.onloadedmetadata = () => {
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
      statusEl.textContent = '已加载';
      sendDuration();
    };

    // ===== 初始化 MediaPipe =====
    async function initPose() {
      try {
        statusEl.textContent = '加载模型...';
        loadingMsg.textContent = '正在加载 MediaPipe...';

        // 尝试从 CDN 加载
        await tryLoadFromCDNs();

        pose = new window.Pose({
          locateFile: (f) => 'https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5.1675469404/' + f
        });

        pose.setOptions({
          modelComplexity: 2,
          smoothLandmarks: true,
          enableSegmentation: false,
          smoothSegmentation: false,
          minDetectionConfidence: 0.4,
          minTrackingConfidence: 0.3
        });

        pose.onResults(onResults);

        loadingOverlay.classList.add('hidden');
        statusEl.textContent = '就绪';
        initDone = true;
        startRAFProcessing();

      } catch (err) {
        console.error('MediaPipe 初始化失败:', err);
        showError('MediaPipe 加载失败<br><br>' + err.message + '<br><br>请检查网络连接后重试');
      }
    }

    // ===== 帧处理 =====
    let lastVideoTime = -1;
    let processingPromise = null;
    let missedFrames = 0;

    function startRAFProcessing() {
      function processNextFrame(timestamp) {
        if (!isPlaying || video.readyState < 2) {
          requestAnimationFrame(processNextFrame);
          return;
        }

        const currentVideoTime = video.currentTime;
        if (currentVideoTime === lastVideoTime) {
          requestAnimationFrame(processNextFrame);
          return;
        }
        lastVideoTime = currentVideoTime;
        sendCurrentTime();

        if (processingPromise) {
          missedFrames++;
        }

        if (!processingPromise) {
          processingPromise = pose.send({ image: video })
            .catch(err => { console.error('处理帧失败:', err); })
            .finally(() => {
              processingPromise = null;
              if (missedFrames > 0) {
                missedFrames = 0;
                processingPromise = pose.send({ image: video })
                  .catch(err => {})
                  .finally(() => { processingPromise = null; });
              }
            });
        }

        frameCount++;
        const now = Date.now();
        if (now - lastTime >= 1000) {
          fpsEl.textContent = frameCount;
          frameCount = 0;
          lastTime = now;
        }

        requestAnimationFrame(processNextFrame);
      }
      requestAnimationFrame(processNextFrame);
    }

    function onResults(results) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (!results.poseLandmarks) {
        sendData(null);
        return;
      }

      sendData(results.poseLandmarks);

      window.drawConnectors(ctx, results.poseLandmarks, window.POSE_CONNECTIONS, {
        color: '#00FF00',
        lineWidth: 3
      });

      window.drawLandmarks(ctx, results.poseLandmarks, {
        color: '#FF4444',
        lineWidth: 2,
        radius: 6,
        fillColor: '#FF4444',
        lineColors: '#FFFFFF'
      });
    }

    function sendData(landmarks) {
      const data = {
        type: 'pose_data',
        landmarks: landmarks ? landmarks.map(l => ({ x: l.x, y: l.y, z: l.z || 0, visibility: l.visibility || 1 })) : null,
        timestamp: Date.now()
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      localStorage.setItem(STORAGE_KEY + '_trigger', Date.now().toString());
      sendCurrentTime();
    }

    document.getElementById('playBtn').onclick = () => {
      video.play();
      isPlaying = true;
      statusEl.textContent = '播放中';
    };

    document.getElementById('pauseBtn').onclick = () => {
      video.pause();
      isPlaying = false;
      statusEl.textContent = '已暂停';
    };

    document.getElementById('closeBtn').onclick = () => {
      isPlaying = false;
      sendData(null);
      localStorage.setItem(STORAGE_KEY + '_close', 'true');
      localStorage.setItem(STORAGE_KEY + '_trigger', Date.now().toString());
      window.close();
    };

    document.querySelectorAll('.speed-btn').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        playSpeed = parseFloat(btn.dataset.speed);
        video.playbackRate = playSpeed;
      };
    });

    video.onended = () => {
      isPlaying = false;
      statusEl.textContent = '播放结束';
      localStorage.setItem(STORAGE_KEY + '_ended', 'true');
      localStorage.setItem(STORAGE_KEY + '_trigger', Date.now().toString());
    };

    video.onplay = () => { isPlaying = true; };
    video.onpause = () => { isPlaying = false; };

    initPose();
  <\/script>
</body>
</html>`;

      const poseWindow = window.open('', '_blank', 'width=950,height=650,menubar=no,toolbar=no,location=no');
      if (!poseWindow) {
        alert('请允许弹出窗口！');
        throw new Error('无法打开窗口');
      }
      poseWindow.document.write(html);
      poseWindow.document.close();
      return poseWindow;
    },

    // 打开评分统计窗口
    openScoreWindow() {
      const storageKey = this.storageKey;

      const html = `<!DOCTYPE html>
<html>
<head>
  <title>评分统计 - 舞蹈评分</title>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
      color: #fff;
      min-height: 100vh;
      padding: 20px;
      font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif;
    }

    .title {
      text-align: center;
      font-size: 22px;
      margin-bottom: 18px;
      color: #e0e0e0;
      letter-spacing: 2px;
    }

    /* 顶部总分区域 */
    .score-header {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 24px;
      margin-bottom: 16px;
    }
    .score-big {
      width: 110px;
      height: 110px;
      border-radius: 50%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      border: 4px solid;
      box-shadow: 0 0 20px rgba(255,255,255,0.1);
      transition: all 0.5s;
    }
    .score-big .num { font-size: 42px; font-weight: 800; }
    .score-big .unit { font-size: 13px; opacity: 0.7; }
    .grade-big {
      font-size: 40px;
      font-weight: 900;
      padding: 8px 24px;
      border-radius: 16px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* 总体评价 */
    .eval-text {
      text-align: center;
      font-size: 14px;
      color: #aaa;
      margin-bottom: 16px;
      min-height: 20px;
    }

    /* 三项评分 */
    .score-bars { margin-bottom: 16px; }
    .score-row {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }
    .score-row .label {
      width: 56px;
      font-size: 13px;
      color: #ccc;
    }
    .score-row .bar-wrap {
      flex: 1;
      height: 10px;
      background: rgba(255,255,255,0.1);
      border-radius: 5px;
      overflow: hidden;
    }
    .score-row .bar-fill {
      height: 100%;
      border-radius: 5px;
      transition: width 0.4s ease;
    }
    .score-row .bar-num {
      width: 42px;
      text-align: right;
      font-size: 13px;
      font-weight: 600;
    }
    .bar-accuracy { background: linear-gradient(90deg, #667eea, #764ba2); }
    .bar-rhythm { background: linear-gradient(90deg, #f093fb, #f5576c); }
    .bar-fluency { background: linear-gradient(90deg, #4facfe, #00f2fe); }

    /* 问题区域 */
    .problems-section {
      background: rgba(244, 67, 54, 0.1);
      border: 1px solid rgba(244, 67, 54, 0.3);
      border-radius: 12px;
      padding: 12px 14px;
      margin-bottom: 16px;
    }
    .problems-section.no-problem {
      background: rgba(76, 175, 80, 0.1);
      border-color: rgba(76, 175, 80, 0.3);
    }
    .problems-title {
      font-size: 13px;
      color: #f44336;
      margin-bottom: 8px;
      font-weight: 600;
    }
    .problems-section.no-problem .problems-title { color: #4caf50; }
    .problem-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 5px 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      font-size: 12px;
    }
    .problem-item:last-child { border-bottom: none; }
    .problem-part { color: #ddd; }
    .problem-detail { color: #ff8a80; font-size: 11px; }
    .problem-suggestion { color: #80deea; font-size: 11px; }

    /* 关节角度 - 实时对比卡片 */
    .angles-title {
      font-size: 13px;
      color: #aaa;
      margin-bottom: 10px;
      padding-bottom: 6px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .angle-card {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 12px;
      border-radius: 10px;
      margin-bottom: 8px;
      background: rgba(255,255,255,0.05);
      border-left: 4px solid #555;
      transition: all 0.3s;
    }
    .angle-card.excellent { border-left-color: #00e676; background: rgba(0,230,118,0.08); }
    .angle-card.good { border-left-color: #69f0ae; background: rgba(105,240,174,0.08); }
    .angle-card.medium { border-left-color: #ffca28; background: rgba(255,202,40,0.08); }
    .angle-card.bad { border-left-color: #ff5252; background: rgba(255,82,82,0.1); }
    .angle-card.offline { border-left-color: #555; opacity: 0.4; }

    .angle-icon { font-size: 18px; }
    .angle-info { flex: 1; }
    .angle-name { font-size: 12px; color: #bbb; }
    .angle-target { font-size: 11px; color: #777; margin-top: 1px; }
    .angle-center { text-align: center; min-width: 70px; }
    .angle-current { font-size: 22px; font-weight: 700; }
    .angle-card.excellent .angle-current { color: #00e676; }
    .angle-card.good .angle-current { color: #69f0ae; }
    .angle-card.medium .angle-current { color: #ffca28; }
    .angle-card.bad .angle-current { color: #ff5252; }
    .angle-card.offline .angle-current { color: #888; }
    .angle-diff { font-size: 11px; }
    .angle-diff.positive { color: #81c784; }
    .angle-diff.negative { color: #ff8a80; }
    .angle-diff.neutral { color: #90a4ae; }
    .angle-meter { width: 50px; }
    .meter-circle {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      border: 3px solid;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      font-weight: 600;
      transition: all 0.3s;
    }

    /* 底部状态 */
    .status-bar {
      margin-top: 16px;
      padding: 10px 14px;
      border-radius: 10px;
      font-size: 13px;
      text-align: center;
      background: rgba(255,255,255,0.05);
    }
    .status-bar.processing { background: rgba(255, 152, 0, 0.15); color: #ffb74d; }
    .status-bar.complete { background: rgba(76,175,80,0.15); color: #81c784; }

    /* 进度指示 */
    .progress-bar-wrap {
      display: flex;
      gap: 3px;
      margin-top: 6px;
      justify-content: center;
    }
    .progress-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: rgba(255,255,255,0.2);
      transition: background 0.2s;
    }
    .progress-dot.active { background: #667eea; }
    .progress-dot.good { background: #4caf50; }
    .progress-dot.warn { background: #ff9800; }

    /* 阶段评分卡片 */
    .stage-cards-wrap {
      background: rgba(255,255,255,0.05);
      border-radius: 12px;
      padding: 10px 14px;
      border: 1px solid rgba(255,255,255,0.08);
    }
    .stage-cards-title {
      font-size: 12px;
      color: #aaa;
      margin-bottom: 8px;
      font-weight: 600;
    }
    .stage-card {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 6px 8px;
      margin-bottom: 4px;
      border-radius: 8px;
      background: rgba(255,255,255,0.04);
      font-size: 13px;
    }
    .stage-card:last-child { margin-bottom: 0; }
    .stage-name { color: #ccc; }
    .stage-score { font-weight: 700; font-size: 15px; }
  </style>
</head>
<body>
  <h2 class="title">💃 舞蹈评分</h2>

  <div class="score-header">
    <div class="score-big" id="scoreCircle">
      <span class="num" id="scoreValue">--</span>
      <span class="unit">分</span>
    </div>
    <div class="grade-big" id="gradeBadge">--</div>
  </div>

  <div class="eval-text" id="evalText">等待分析...</div>

  <!-- 阶段完成卡片（分阶段展示分数） -->
  <div class="stage-cards-wrap" id="stageCardsWrap" style="display:none; margin-bottom:14px;">
    <div class="stage-cards-title">📊 分阶段评分</div>
    <div id="stageCardsContainer"></div>
  </div>

  <div class="score-bars">
    <div class="score-row">
      <span class="label">📐 准确度</span>
      <div class="bar-wrap"><div class="bar-fill bar-accuracy" id="accuracyBar" style="width:0%"></div></div>
      <span class="bar-num" id="accuracyVal">0%</span>
    </div>
    <div class="score-row">
      <span class="label">🎵 节奏感</span>
      <div class="bar-wrap"><div class="bar-fill bar-rhythm" id="rhythmBar" style="width:0%"></div></div>
      <span class="bar-num" id="rhythmVal">0%</span>
    </div>
    <div class="score-row">
      <span class="label">💫 流畅度</span>
      <div class="bar-wrap"><div class="bar-fill bar-fluency" id="fluencyBar" style="width:0%"></div></div>
      <span class="bar-num" id="fluencyVal">0%</span>
    </div>
  </div>

  <div class="problems-section" id="problemsSection">
    <div class="problems-title" id="problemsTitle">🔍 问题分析</div>
    <div id="problemsList"></div>
  </div>

  <div class="angles-title">🦵 关节角度实时监测</div>

  <!-- 腿部角度卡片 -->
  <div class="angle-card offline" id="leftKneeCard">
    <div class="angle-icon">🦶</div>
    <div class="angle-info">
      <div class="angle-name">左腿踢腿角度</div>
      <div class="angle-target">目标: 接近 0°（水平踢出）</div>
    </div>
    <div class="angle-center">
      <div class="angle-current" id="leftKneeAngle">--°</div>
      <div class="angle-diff neutral" id="leftKneeDiff">--</div>
    </div>
    <div class="angle-meter">
      <div class="meter-circle" id="leftKneeMeter" style="border-color:#555;color:#555;">--</div>
    </div>
  </div>

  <div class="angle-card offline" id="rightKneeCard">
    <div class="angle-icon">🦶</div>
    <div class="angle-info">
      <div class="angle-name">右腿踢腿角度</div>
      <div class="angle-target">目标: 接近 0°（水平踢出）</div>
    </div>
    <div class="angle-center">
      <div class="angle-current" id="rightKneeAngle">--°</div>
      <div class="angle-diff neutral" id="rightKneeDiff">--</div>
    </div>
    <div class="angle-meter">
      <div class="meter-circle" id="rightKneeMeter" style="border-color:#555;color:#555;">--</div>
    </div>
  </div>

  <!-- 手臂角度卡片 -->
  <div class="angle-card offline" id="leftElbowCard">
    <div class="angle-icon">💪</div>
    <div class="angle-info">
      <div class="angle-name">左臂伸展</div>
      <div class="angle-target">目标: 160°~180°（伸直）</div>
    </div>
    <div class="angle-center">
      <div class="angle-current" id="leftElbowAngle">--°</div>
      <div class="angle-diff neutral" id="leftElbowDiff">--</div>
    </div>
    <div class="angle-meter">
      <div class="meter-circle" id="leftElbowMeter" style="border-color:#555;color:#555;">--</div>
    </div>
  </div>

  <div class="angle-card offline" id="rightElbowCard">
    <div class="angle-icon">💪</div>
    <div class="angle-info">
      <div class="angle-name">右臂伸展</div>
      <div class="angle-target">目标: 160°~180°（伸直）</div>
    </div>
    <div class="angle-center">
      <div class="angle-current" id="rightElbowAngle">--°</div>
      <div class="angle-diff neutral" id="rightElbowDiff">--</div>
    </div>
    <div class="angle-meter">
      <div class="meter-circle" id="rightElbowMeter" style="border-color:#555;color:#555;">--</div>
    </div>
  </div>

  <!-- 肩膀角度卡片 -->
  <div class="angle-card offline" id="leftShoulderCard">
    <div class="angle-icon">👆</div>
    <div class="angle-info">
      <div class="angle-name">左肩抬举</div>
      <div class="angle-target">目标: 90°~120°（抬臂）</div>
    </div>
    <div class="angle-center">
      <div class="angle-current" id="leftShoulderAngle">--°</div>
      <div class="angle-diff neutral" id="leftShoulderDiff">--</div>
    </div>
    <div class="angle-meter">
      <div class="meter-circle" id="leftShoulderMeter" style="border-color:#555;color:#555;">--</div>
    </div>
  </div>

  <div class="angle-card offline" id="rightShoulderCard">
    <div class="angle-icon">👆</div>
    <div class="angle-info">
      <div class="angle-name">右肩抬举</div>
      <div class="angle-target">目标: 90°~120°（抬臂）</div>
    </div>
    <div class="angle-center">
      <div class="angle-current" id="rightShoulderAngle">--°</div>
      <div class="angle-diff neutral" id="rightShoulderDiff">--</div>
    </div>
    <div class="angle-meter">
      <div class="meter-circle" id="rightShoulderMeter" style="border-color:#555;color:#555;">--</div>
    </div>
  </div>

  <!-- 髋部角度卡片 -->
  <div class="angle-card offline" id="leftHipCard">
    <div class="angle-icon">🦵</div>
    <div class="angle-info">
      <div class="angle-name">左髋抬腿</div>
      <div class="angle-target">目标: 接近 90°（高抬腿）</div>
    </div>
    <div class="angle-center">
      <div class="angle-current" id="leftHipAngle">--°</div>
      <div class="angle-diff neutral" id="leftHipDiff">--</div>
    </div>
    <div class="angle-meter">
      <div class="meter-circle" id="leftHipMeter" style="border-color:#555;color:#555;">--</div>
    </div>
  </div>

  <div class="angle-card offline" id="rightHipCard">
    <div class="angle-icon">🦵</div>
    <div class="angle-info">
      <div class="angle-name">右髋抬腿</div>
      <div class="angle-target">目标: 接近 90°（高抬腿）</div>
    </div>
    <div class="angle-center">
      <div class="angle-current" id="rightHipAngle">--°</div>
      <div class="angle-diff neutral" id="rightHipDiff">--</div>
    </div>
    <div class="angle-meter">
      <div class="meter-circle" id="rightHipMeter" style="border-color:#555;color:#555;">--</div>
    </div>
  </div>

  <div class="status-bar processing" id="status">
    <span id="statusText">⏳ 等待检测...</span>
    <div class="progress-bar-wrap" id="progressDots"></div>
  </div>

  <script>
    const STORAGE_KEY = '${storageKey}';
    const FRAME_WINDOW = 15; // 用于平滑的帧窗口
    const PHASE_SCORE_WINDOW = 60; // 至少60帧才出一个阶段分（≈1秒@0.5x播放）
    const PHASE_COMPLETE_FRAMES = 30; // 连续30帧满足条件才判定阶段完成

    // MediaPipe Pose 关键点索引
    const LM = {
      // 肩膀
      L_SHOULDER: 11, R_SHOULDER: 12,
      // 肘部
      L_ELBOW: 13, R_ELBOW: 14,
      // 手腕
      L_WRIST: 15, R_WRIST: 16,
      // 髋部
      L_HIP: 23, R_HIP: 24,
      // 膝盖
      L_KNEE: 25, R_KNEE: 26,
      // 脚踝
      L_ANKLE: 27, R_ANKLE: 28,
      // 鼻子（用于头部参考）
      NOSE: 0
    };

    // ===== 阶段配置 =====
    // 视频总帧数未知，先用时间比例估算阶段
    // 阶段1: 0~33%, 阶段2: 33~66%, 阶段3: 66~100%
    const STAGE_PERCENT = [0.33, 0.66, 1.0];
    const STAGE_NAMES = ['起势阶段', '发力阶段', '收势阶段'];
    let stageIndex = 0;
    let stageScores = [];         // 当前阶段所有帧的原始分
    let completedStages = [];      // 已完成的阶段分数 {name, score, frames}
    let stageCompleteFrames = 0;  // 连续满足阶段完成条件的帧数
    let totalScoreLocked = false;
    let finalScore = 0;

    // 跟踪状态
    let frameCount = 0;
    let fpsCount = 0;
    let fpsStart = Date.now();
    let scores = [];
    let angleHistory = {};
    let isComplete = false;
    let lastTimestamp = 0;
    let problemFrames = { leftKnee: 0, rightKnee: 0, leftElbow: 0, rightElbow: 0, leftShoulder: 0, rightShoulder: 0, leftHip: 0, rightHip: 0 };
    let lastValidLandmarks = null; // 保留上一帧有效关键点，用于检测丢失时插值
    let lastLandmarkTime = 0;       // 上一帧有效关键点的时间戳

    // 初始化进度点
    (function initDots() {
      const container = document.getElementById('progressDots');
      for (let i = 0; i < 20; i++) {
        const dot = document.createElement('div');
        dot.className = 'progress-dot';
        dot.id = 'dot' + i;
        container.appendChild(dot);
      }
    })();

    // ===== 角度计算 =====
    function getVisibility(landmarks, idx) {
      return landmarks[idx] ? (landmarks[idx].visibility || 0) : 0;
    }

    function getPoint(landmarks, idx) {
      const lm = landmarks[idx];
      return lm ? { x: lm.x, y: lm.y, z: lm.z || 0, v: lm.visibility || 0 } : null;
    }

    // 计算两点之间的向量角度（相对于垂直向下方向）
    // 返回 0° = 水平踢出, 90° = 自然下垂
    function calcKickAngle(landmarks, hipIdx, ankleIdx) {
      const hip = getPoint(landmarks, hipIdx);
      const ankle = getPoint(landmarks, ankleIdx);
      if (!hip || !ankle || hip.v < 0.4 || ankle.v < 0.4) return null;

      // 计算腿向量（从髋到踝）
      const dx = ankle.x - hip.x;
      const dy = ankle.y - hip.y;

      // 计算与垂直方向的夹角
      // MediaPipe Y轴向下，所以垂直向下方向是 (0, 1)
      // 腿自然下垂时 dy > 0, dx ≈ 0
      // 腿水平踢出时 dy ≈ 0, |dx| 较大
      const legLen = Math.sqrt(dx * dx + dy * dy);
      if (legLen < 0.01) return null;

      // 与垂直向下的夹角 (0 = 水平踢出, 90 = 自然下垂)
      // cos(theta) = dot((0,1), (dx,dy)/len) = dy/len
      const cosAngle = Math.max(-1, Math.min(1, dy / legLen));
      const angle = Math.acos(cosAngle) * 180 / Math.PI;

      return angle;
    }

    // 标准关节角度计算 (三点夹角)
    function calcAngle(landmarks, idx1, idx2, idx3) {
      const p1 = getPoint(landmarks, idx1);
      const p2 = getPoint(landmarks, idx2);
      const p3 = getPoint(landmarks, idx3);
      if (!p1 || !p2 || !p3) return null;
      if (p1.v < 0.4 || p2.v < 0.4 || p3.v < 0.4) return null;

      const v1 = { x: p1.x - p2.x, y: p1.y - p2.y };
      const v2 = { x: p3.x - p2.x, y: p3.y - p2.y };
      const dot = v1.x * v2.x + v1.y * v2.y;
      const mag = Math.sqrt(v1.x * v1.x + v1.y * v1.y) * Math.sqrt(v2.x * v2.x + v2.y * v2.y);
      if (mag < 0.001) return null;

      const cosA = Math.max(-1, Math.min(1, dot / mag));
      return Math.acos(cosA) * 180 / Math.PI;
    }

    // ===== 评分计算 =====
    function calcKneeScore(actualAngle) {
      // 踢腿角度：0° = 完美水平踢出，>30° = 踢得不够高
      if (actualAngle === null) return null;
      if (actualAngle <= 10) return 100;
      if (actualAngle <= 20) return 95;
      if (actualAngle <= 35) return 85;
      if (actualAngle <= 50) return 75;
      if (actualAngle <= 65) return 60;
      if (actualAngle <= 80) return 45;
      return Math.max(0, 40 - (actualAngle - 80) * 1.5);
    }

    function calcArmScore(actualAngle) {
      // 手臂伸直：170-180° 最好，< 150° 说明弯曲不够
      if (actualAngle === null) return null;
      if (actualAngle >= 170) return 100;
      if (actualAngle >= 160) return 95;
      if (actualAngle >= 145) return 85;
      if (actualAngle >= 130) return 70;
      if (actualAngle >= 110) return 55;
      return Math.max(0, 40 - (actualAngle - 110) * 0.8);
    }

    function calcShoulderScore(actualAngle) {
      // 肩膀抬举：90°~120° 是好的抬臂范围
      if (actualAngle === null) return null;
      const ideal = 105;
      const diff = Math.abs(actualAngle - ideal);
      if (diff <= 10) return 100;
      if (diff <= 20) return 92;
      if (diff <= 35) return 82;
      if (diff <= 50) return 70;
      if (diff <= 65) return 55;
      return Math.max(0, 45 - (diff - 65) * 0.6);
    }

    function calcHipScore(actualAngle) {
      // 髋部抬腿：接近 90° 是好的高抬腿
      if (actualAngle === null) return null;
      const ideal = 90;
      const diff = Math.abs(actualAngle - ideal);
      if (diff <= 10) return 100;
      if (diff <= 20) return 92;
      if (diff <= 35) return 80;
      if (diff <= 50) return 65;
      if (diff <= 65) return 50;
      return Math.max(0, 40 - (diff - 65) * 0.5);
    }

    // ===== UI 更新 =====
    function updateAngleCard(id, angle, score, targetLabel) {
      const card = document.getElementById(id + 'Card');
      const angleEl = document.getElementById(id + 'Angle');
      const diffEl = document.getElementById(id + 'Diff');
      const meterEl = document.getElementById(id + 'Meter');

      if (angle === null || score === null) {
        card.className = 'angle-card offline';
        angleEl.textContent = '--°';
        diffEl.textContent = '--';
        diffEl.className = 'angle-diff neutral';
        meterEl.textContent = '--';
        meterEl.style.borderColor = '#555';
        meterEl.style.color = '#555';
        return;
      }

      // 确定颜色等级
      let cls;
      if (score >= 90) cls = 'excellent';
      else if (score >= 75) cls = 'good';
      else if (score >= 55) cls = 'medium';
      else cls = 'bad';

      card.className = 'angle-card ' + cls;
      angleEl.textContent = Math.round(angle) + '°';

      const diff = Math.round(angle - (score !== null ? getIdealAngle(id) : 0));
      const absDiff = Math.abs(diff);
      if (absDiff <= 10) {
        diffEl.textContent = '✓ 完美';
        diffEl.className = 'angle-diff positive';
      } else if (diff > 0) {
        diffEl.textContent = '↑ +' + Math.round(diff) + '°（稍高）';
        diffEl.className = 'angle-diff negative';
      } else {
        diffEl.textContent = '↓ ' + Math.round(diff) + '°（稍低）';
        diffEl.className = 'angle-diff negative';
      }

      const meterPct = Math.min(100, score);
      meterEl.textContent = Math.round(score);
      const meterColor = score >= 90 ? '#00e676' : score >= 75 ? '#69f0ae' : score >= 55 ? '#ffca28' : '#ff5252';
      meterEl.style.borderColor = meterColor;
      meterEl.style.color = meterColor;
    }

    function getIdealAngle(id) {
      const ideals = { leftKnee: 0, rightKnee: 0, leftElbow: 175, rightElbow: 175, leftShoulder: 105, rightShoulder: 105, leftHip: 90, rightHip: 90 };
      return ideals[id] || 0;
    }

    // ===== 问题分析 =====
    function updateProblems() {
      const section = document.getElementById('problemsSection');
      const titleEl = document.getElementById('problemsTitle');
      const listEl = document.getElementById('problemsList');

      const problems = [];

      // 膝盖（踢腿）
      [['leftKnee', '左腿踢腿'], ['rightKnee', '右腿踢腿']].forEach(([id, name]) => {
        const avg = getAngleAvg(id);
        if (avg !== null && avg > 35) {
          const level = avg > 65 ? '严重' : avg > 50 ? '较大' : '轻微';
          problems.push({ id, name, level, angle: avg,
            suggest: avg > 65 ? '腿部力量不足，踢腿高度严重不够' : avg > 50 ? '踢腿高度不够，注意抬腿用力' : '踢腿稍低，尽量踢得更高' });
          problemFrames[id]++;
        }
      });

      // 手臂伸直
      [['leftElbow', '左臂'], ['rightElbow', '右臂']].forEach(([id, name]) => {
        const avg = getAngleAvg(id);
        if (avg !== null && avg < 145) {
          problems.push({ id, name, level: avg < 110 ? '严重' : avg < 130 ? '较大' : '轻微', angle: avg,
            suggest: avg < 110 ? '手臂弯曲过多，请充分伸直' : avg < 130 ? '手臂伸直不够，注意伸肘' : '手臂稍微弯曲，保持伸直' });
          problemFrames[id]++;
        }
      });

      // 肩膀抬举
      [['leftShoulder', '左肩'], ['rightShoulder', '右肩']].forEach(([id, name]) => {
        const avg = getAngleAvg(id);
        if (avg !== null && (avg < 60 || avg > 140)) {
          problems.push({ id, name, level: avg < 45 || avg > 150 ? '严重' : '较大', angle: avg,
            suggest: avg < 60 ? '抬臂高度不够，尽量抬到水平' : '抬臂过高，手臂过于伸直' });
          problemFrames[id]++;
        }
      });

      // 髋部抬腿
      [['leftHip', '左髋抬腿'], ['rightHip', '右髋抬腿']].forEach(([id, name]) => {
        const avg = getAngleAvg(id);
        if (avg !== null && (avg < 55 || avg > 125)) {
          problems.push({ id, name, level: avg < 35 || avg > 140 ? '严重' : '较大', angle: avg,
            suggest: avg < 55 ? '抬腿不够高，需要更多抬髋' : '抬腿过高，注意控制幅度' });
          problemFrames[id]++;
        }
      });

      // 按严重程度排序
      problems.sort((a, b) => {
        const order = { '严重': 0, '较大': 1, '轻微': 2 };
        return order[a.level] - order[b.level];
      });

      if (problems.length === 0) {
        section.className = 'problems-section no-problem';
        titleEl.textContent = '✅ 表现优秀';
        listEl.innerHTML = '<div class="problem-item"><span class="problem-part">所有动作均达标，继续保持！</span></div>';
      } else {
        section.className = 'problems-section';
        titleEl.textContent = '🔍 发现 ' + problems.length + ' 个问题';
        listEl.innerHTML = problems.slice(0, 5).map(p =>
          '<div class="problem-item">' +
            '<span class="problem-part">⚠ ' + p.name + '</span>' +
            '<span class="problem-detail">' + p.angle.toFixed(0) + '°</span>' +
          '</div>' +
          '<div class="problem-item" style="padding-top:2px;">' +
            '<span class="problem-suggestion">💡 ' + p.suggest + '</span>' +
          '</div>'
        ).join('');
      }
    }

    function getAngleAvg(id) {
      const hist = angleHistory[id];
      if (!hist || hist.length === 0) return null;
      const recent = hist.slice(-FRAME_WINDOW);
      const valid = recent.filter(v => v !== null);
      if (valid.length === 0) return null;
      return valid.reduce((a, b) => a + b, 0) / valid.length;
    }

    // ===== 主分析函数 =====
    function analyzeFrame(landmarks) {
      // 计算各关节角度
      const kneeL = calcKickAngle(landmarks, LM.L_HIP, LM.L_ANKLE);
      const kneeR = calcKickAngle(landmarks, LM.R_HIP, LM.R_ANKLE);
      const elbowL = calcAngle(landmarks, LM.L_SHOULDER, LM.L_ELBOW, LM.L_WRIST);
      const elbowR = calcAngle(landmarks, LM.R_SHOULDER, LM.R_ELBOW, LM.R_WRIST);
      const shoulderL = calcAngle(landmarks, LM.L_ELBOW, LM.L_SHOULDER, LM.L_HIP);
      const shoulderR = calcAngle(landmarks, LM.R_ELBOW, LM.R_SHOULDER, LM.R_HIP);
      const hipL = calcAngle(landmarks, LM.L_KNEE, LM.L_HIP, LM.L_SHOULDER);
      const hipR = calcAngle(landmarks, LM.R_KNEE, LM.R_HIP, LM.R_SHOULDER);

      // 记录历史
      if (!angleHistory.leftKnee) angleHistory.leftKnee = [];
      if (!angleHistory.rightKnee) angleHistory.rightKnee = [];
      if (!angleHistory.leftElbow) angleHistory.leftElbow = [];
      if (!angleHistory.rightElbow) angleHistory.rightElbow = [];
      if (!angleHistory.leftShoulder) angleHistory.leftShoulder = [];
      if (!angleHistory.rightShoulder) angleHistory.rightShoulder = [];
      if (!angleHistory.leftHip) angleHistory.leftHip = [];
      if (!angleHistory.rightHip) angleHistory.rightHip = [];

      angleHistory.leftKnee.push(kneeL);
      angleHistory.rightKnee.push(kneeR);
      angleHistory.leftElbow.push(elbowL);
      angleHistory.rightElbow.push(elbowR);
      angleHistory.leftShoulder.push(shoulderL);
      angleHistory.rightShoulder.push(shoulderR);
      angleHistory.leftHip.push(hipL);
      angleHistory.rightHip.push(hipR);

      // 限制历史长度
      Object.keys(angleHistory).forEach(k => {
        if (angleHistory[k].length > FRAME_WINDOW * 3) angleHistory[k].shift();
      });

      // 计算单帧得分
      const sKneeL = calcKneeScore(kneeL);
      const sKneeR = calcKneeScore(kneeR);
      const sElbowL = calcArmScore(elbowL);
      const sElbowR = calcArmScore(elbowR);
      const sShoulderL = calcShoulderScore(shoulderL);
      const sShoulderR = calcShoulderScore(shoulderR);
      const sHipL = calcHipScore(hipL);
      const sHipR = calcHipScore(hipR);

      const validScores = [sKneeL, sKneeR, sElbowL, sElbowR, sShoulderL, sShoulderR, sHipL, sHipR].filter(s => s !== null);
      const instantScore = validScores.length > 0 ? validScores.reduce((a, b) => a + b, 0) / validScores.length : 0;

      // 使用指数移动平均平滑分数
      const prevScore = scores.length > 0 ? scores[scores.length - 1] : instantScore;
      const smoothedScore = prevScore * 0.75 + instantScore * 0.25;
      scores.push(smoothedScore);

      // 视频时长从 pose 窗口同步（见 localStorage _duration）
      const videoProgress = videoDuration > 0 ? lastVideoTime / videoDuration : 0;

      // 判定当前应属哪个阶段（0=起势, 1=发力, 2=收势）
      let currentStage = 0;
      if (videoProgress >= STAGE_PERCENT[1]) currentStage = 1;
      if (videoProgress >= STAGE_PERCENT[2]) currentStage = 2;

      // 记录原始分（用于阶段平均）
      stageScores.push(instantScore);

      // 阶段切换：上一个阶段结束
      if (currentStage > stageIndex && stageScores.length > 0) {
        const stageAvg = stageScores.reduce((a, b) => a + b, 0) / stageScores.length;
        const smoothedStageScore = completedStages.length > 0
          ? completedStages[completedStages.length - 1].score * 0.7 + stageAvg * 0.3
          : stageAvg;
        completedStages.push({
          name: STAGE_NAMES[stageIndex],
          score: Math.round(smoothedStageScore),
          frames: stageScores.length
        });
        // 刷新阶段卡片UI
        updateStageCards();
        // 阶段总分暂存（不更新主显示）
        finalScore = computeRunningTotal();
        stageScores = [];
        stageIndex = currentStage;
      }

      // 视频结束时处理最后阶段
      if (videoProgress >= 0.99 && !totalScoreLocked && stageScores.length > 0) {
        const lastStageAvg = stageScores.reduce((a, b) => a + b, 0) / stageScores.length;
        const smoothedLastScore = completedStages.length > 0
          ? completedStages[completedStages.length - 1].score * 0.7 + lastStageAvg * 0.3
          : lastStageAvg;
        completedStages.push({
          name: STAGE_NAMES[stageIndex],
          score: Math.round(smoothedLastScore),
          frames: stageScores.length
        });
        updateStageCards();
        totalScoreLocked = true;
        finalScore = computeRunningTotal();
        // 立即更新主显示区
        updateTotalScore(finalScore, true);
        updateProgressBars(finalScore);
        document.getElementById('evalText').textContent = '✅ 视频结束，最终得分已锁定';
        // 隐藏阶段卡片的提示文字
        const wrap = document.getElementById('stageCardsWrap');
        if (wrap) wrap.querySelector('.stage-cards-title').textContent = '📊 最终评分';
      } else if (!totalScoreLocked) {
        // 视频进行中：显示"当前阶段"分（取最近30帧平均，不显示大数字跳动）
        const recentScores = stageScores.slice(-PHASE_SCORE_WINDOW);
        const runningScore = recentScores.reduce((a, b) => a + b, 0) / (recentScores.length || 1);
        updateTotalScore(runningScore, false); // 第二个参数false=不锁定
        // 第一次有数据时显示阶段卡片
        const wrap = document.getElementById('stageCardsWrap');
        if (wrap) wrap.style.display = 'block';
      }

      // 更新 UI
      updateAngleCard('leftKnee', kneeL, sKneeL);
      updateAngleCard('rightKnee', kneeR, sKneeR);
      updateAngleCard('leftElbow', elbowL, sElbowL);
      updateAngleCard('rightElbow', elbowR, sElbowR);
      updateAngleCard('leftShoulder', shoulderL, sShoulderL);
      updateAngleCard('rightShoulder', shoulderR, sShoulderR);
      updateAngleCard('leftHip', hipL, sHipL);
      updateAngleCard('rightHip', hipR, sHipR);

      // 不再每帧更新总分进度条（已在上面根据阶段处理）
      updateProblems();

      // 更新状态
      const status = document.getElementById('status');
      const statusText = document.getElementById('statusText');
      status.className = 'status-bar processing';
      statusText.textContent = '⏳ 分析中... 第 ' + frameCount + ' 帧';

      // 更新进度点
      const dotIdx = Math.min(19, Math.floor((frameCount % 200) / 10));
      for (let i = 0; i < 20; i++) {
        const dot = document.getElementById('dot' + i);
        dot.className = 'progress-dot';
        if (i === dotIdx) {
          dot.className = 'progress-dot ' + (smoothedScore >= 75 ? 'good' : smoothedScore >= 55 ? 'active' : 'warn');
        }
      }

      // 更新评价文字
      const evalEl = document.getElementById('evalText');
      if (smoothedScore >= 90) evalEl.textContent = '🎯 动作非常标准！';
      else if (smoothedScore >= 75) evalEl.textContent = '👍 表现良好，继续保持';
      else if (smoothedScore >= 60) evalEl.textContent = '💪 有进步空间，加油';
      else if (smoothedScore >= 45) evalEl.textContent = '⚠ 需要加强练习';
      else evalEl.textContent = '❌ 差距较大，建议学习基础';
    }

    function updateTotalScore(score, locked) {
      const scoreValue = document.getElementById('scoreValue');
      const scoreCircle = document.getElementById('scoreCircle');
      const gradeBadge = document.getElementById('gradeBadge');
      const gradeColors = { S: '#ffd700', A: '#4caf50', B: '#2196f3', C: '#ff9800', D: '#ff5252', E: '#9e9e9e' };

      scoreValue.textContent = locked ? Math.round(score) : '--';

      if (locked) {
        const grade = score >= 95 ? 'S' : score >= 85 ? 'A' : score >= 75 ? 'B' : score >= 65 ? 'C' : score >= 50 ? 'D' : 'E';
        gradeBadge.textContent = grade;
        gradeBadge.style.background = 'linear-gradient(135deg, ' + gradeColors[grade] + ', ' + gradeColors[grade] + 'aa)';
        gradeBadge.style.color = '#fff';
        const color = '#667eea';
        scoreCircle.style.borderColor = color;
        scoreCircle.style.background = 'rgba(102, 126, 234, 0.1)';
      } else {
        gradeBadge.textContent = '?';
        gradeBadge.style.background = 'rgba(255,255,255,0.1)';
        gradeBadge.style.color = '#888';
        const color = score >= 75 ? '#4caf50' : score >= 55 ? '#ff9800' : '#ff5252';
        scoreCircle.style.borderColor = color;
        scoreCircle.style.background = 'rgba(' + hexToRgb(color) + ', 0.1)';
      }
    }

    function computeRunningTotal() {
      if (completedStages.length === 0 && stageScores.length === 0) return 0;
      let totalFrames = 0, totalScore = 0;
      for (const s of completedStages) {
        totalScore += s.score * s.frames;
        totalFrames += s.frames;
      }
      if (stageScores.length > 0) {
        const currentAvg = stageScores.reduce((a, b) => a + b, 0) / stageScores.length;
        totalScore += currentAvg * stageScores.length;
        totalFrames += stageScores.length;
      }
      return totalFrames > 0 ? totalScore / totalFrames : 0;
    }

    // 渲染阶段卡片（显示已完成阶段的分数）
    function updateStageCards() {
      const container = document.getElementById('stageCardsContainer');
      if (!container) return;
      container.innerHTML = completedStages.map((s, i) => {
        const color = s.score >= 85 ? '#4caf50' : s.score >= 70 ? '#ff9800' : '#ff5252';
        return '<div class="stage-card">' +
          '<span class="stage-name">' + (i + 1) + '. ' + s.name + '</span>' +
          '<span class="stage-score" style="color:' + color + '">' + s.score + '分</span>' +
          '</div>';
      }).join('');
    }

    function hexToRgb(hex) {
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      return r + ',' + g + ',' + b;
    }

    function updateProgressBars(score) {
      const accuracy = score;
      const rhythm = Math.min(100, score * 1.05);
      const fluency = Math.min(100, score * 0.98);

      document.getElementById('accuracyBar').style.width = accuracy + '%';
      document.getElementById('accuracyVal').textContent = Math.round(accuracy) + '%';
      document.getElementById('rhythmBar').style.width = rhythm + '%';
      document.getElementById('rhythmVal').textContent = Math.round(rhythm) + '%';
      document.getElementById('fluencyBar').style.width = fluency + '%';
      document.getElementById('fluencyVal').textContent = Math.round(fluency) + '%';
    }

    // ===== 数据接收 =====
    function handleData(data) {
      if (data.type !== 'pose_data') return;

      const now = Date.now();
      if (now - fpsStart >= 1000) {
        fpsCount = 0;
        fpsStart = now;
      }

      // 当检测短暂丢失时（视频遮挡、快速移动），用上一帧关键点插值继续评分
      // 超过500ms没检测到才判定为真正丢失，不再插值
      if (!data.landmarks) {
        if (lastValidLandmarks && (now - lastLandmarkTime) < 500) {
          // 短暂丢失：用上一帧关键点 + 小幅惩罚继续评分
          const elapsed = (now - lastLandmarkTime) / 1000; // 秒
          const penaltyFactor = Math.max(0.7, 1 - elapsed * 0.1); // 每秒最多扣30%分
          const fakeScore = scores.length > 0 ? scores[scores.length - 1] * penaltyFactor : 50;
          // 用插值的关键点（轻微位置偏移模拟动作）
          const interpolated = lastValidLandmarks.map(lm => ({
            x: lm.x + Math.sin(elapsed * 5) * 0.005,
            y: lm.y + Math.cos(elapsed * 3) * 0.005,
            z: lm.z || 0,
            visibility: Math.max(0.3, (lm.visibility || 1) * penaltyFactor)
          }));
          frameCount++;
          fpsCount++;
          analyzeFrameWithPenalty(interpolated, penaltyFactor);
        }
        // else: 超过500ms没检测到，直接忽略这帧
        return;
      }

      // 正常检测到：保存为最新有效关键点
      lastValidLandmarks = data.landmarks;
      lastLandmarkTime = now;

      frameCount++;
      fpsCount++;
      analyzeFrame(data.landmarks);
    }

    // 检测丢失时用惩罚因子继续分析
    function analyzeFrameWithPenalty(landmarks, penaltyFactor) {
      // 计算角度（和正常analyzeFrame一样，只是分数乘以penaltyFactor）
      const kneeL = calcKickAngle(landmarks, LM.L_HIP, LM.L_ANKLE);
      const kneeR = calcKickAngle(landmarks, LM.R_HIP, LM.R_ANKLE);
      const elbowL = calcAngle(landmarks, LM.L_SHOULDER, LM.L_ELBOW, LM.L_WRIST);
      const elbowR = calcAngle(landmarks, LM.R_SHOULDER, LM.R_ELBOW, LM.R_WRIST);
      const shoulderL = calcAngle(landmarks, LM.L_ELBOW, LM.L_SHOULDER, LM.L_HIP);
      const shoulderR = calcAngle(landmarks, LM.R_ELBOW, LM.R_SHOULDER, LM.R_HIP);
      const hipL = calcAngle(landmarks, LM.L_KNEE, LM.L_HIP, LM.L_SHOULDER);
      const hipR = calcAngle(landmarks, LM.R_KNEE, LM.R_HIP, LM.R_SHOULDER);

      // ===== 辅助函数：记录角度历史 =====
      function recordAngleHistory2(kneeL, kneeR, elbowL, elbowR, shoulderL, shoulderR, hipL, hipR) {
        if (!angleHistory.leftKnee) angleHistory.leftKnee = [];
        if (!angleHistory.rightKnee) angleHistory.rightKnee = [];
        if (!angleHistory.leftElbow) angleHistory.leftElbow = [];
        if (!angleHistory.rightElbow) angleHistory.rightElbow = [];
        if (!angleHistory.leftShoulder) angleHistory.leftShoulder = [];
        if (!angleHistory.rightShoulder) angleHistory.rightShoulder = [];
        if (!angleHistory.leftHip) angleHistory.leftHip = [];
        if (!angleHistory.rightHip) angleHistory.rightHip = [];
        angleHistory.leftKnee.push(kneeL);
        angleHistory.rightKnee.push(kneeR);
        angleHistory.leftElbow.push(elbowL);
        angleHistory.rightElbow.push(elbowR);
        angleHistory.leftShoulder.push(shoulderL);
        angleHistory.rightShoulder.push(shoulderR);
        angleHistory.leftHip.push(hipL);
        angleHistory.rightHip.push(hipR);
        Object.keys(angleHistory).forEach(k => {
          if (angleHistory[k].length > FRAME_WINDOW * 3) angleHistory[k].shift();
        });
      }

      recordAngleHistory2(kneeL, kneeR, elbowL, elbowR, shoulderL, shoulderR, hipL, hipR);

      const sKneeL = calcKneeScore(kneeL);
      const sKneeR = calcKneeScore(kneeR);
      const sElbowL = calcArmScore(elbowL);
      const sElbowR = calcArmScore(elbowR);
      const sShoulderL = calcShoulderScore(shoulderL);
      const sShoulderR = calcShoulderScore(shoulderR);
      const sHipL = calcHipScore(hipL);
      const sHipR = calcHipScore(hipR);

      const validScores = [sKneeL, sKneeR, sElbowL, sElbowR, sShoulderL, sShoulderR, sHipL, sHipR].filter(s => s !== null);
      if (validScores.length === 0) return;

      const instantScore = validScores.reduce((a, b) => a + b, 0) / validScores.length * penaltyFactor;
      const prevScore = scores.length > 0 ? scores[scores.length - 1] : instantScore;
      const smoothedScore = prevScore * 0.8 + instantScore * 0.2;
      scores.push(smoothedScore);

      updateAngleCard('leftKnee', kneeL, sKneeL !== null ? sKneeL * penaltyFactor : null);
      updateAngleCard('rightKnee', kneeR, sKneeR !== null ? sKneeR * penaltyFactor : null);
      updateAngleCard('leftElbow', elbowL, sElbowL !== null ? sElbowL * penaltyFactor : null);
      updateAngleCard('rightElbow', elbowR, sElbowR !== null ? sElbowR * penaltyFactor : null);
      updateAngleCard('leftShoulder', shoulderL, sShoulderL !== null ? sShoulderL * penaltyFactor : null);
      updateAngleCard('rightShoulder', shoulderR, sShoulderR !== null ? sShoulderR * penaltyFactor : null);
      updateAngleCard('leftHip', hipL, sHipL !== null ? sHipL * penaltyFactor : null);
      updateAngleCard('rightHip', hipR, sHipR !== null ? sHipR * penaltyFactor : null);

      // 阶段评分（用同步过来的视频时间）
      const videoProgress = videoDuration > 0 ? lastVideoTime / videoDuration : 0;
      let currentStage = 0;
      if (videoProgress >= STAGE_PERCENT[1]) currentStage = 1;
      if (videoProgress >= STAGE_PERCENT[2]) currentStage = 2;

      stageScores.push(instantScore);
      if (currentStage > stageIndex && stageScores.length > 0) {
        const stageAvg = stageScores.reduce((a, b) => a + b, 0) / stageScores.length;
        const smoothedStageScore = completedStages.length > 0
          ? completedStages[completedStages.length - 1].score * 0.7 + stageAvg * 0.3 : stageAvg;
        completedStages.push({ name: STAGE_NAMES[stageIndex], score: Math.round(smoothedStageScore), frames: stageScores.length });
        updateStageCards();
        finalScore = computeRunningTotal();
        stageScores = [];
        stageIndex = currentStage;
      }
      if (videoProgress >= 0.99 && !totalScoreLocked && stageScores.length > 0) {
        const lastAvg = stageScores.reduce((a, b) => a + b, 0) / stageScores.length;
        completedStages.push({ name: STAGE_NAMES[stageIndex], score: Math.round(lastAvg), frames: stageScores.length });
        updateStageCards();
        totalScoreLocked = true;
        finalScore = computeRunningTotal();
        updateTotalScore(finalScore, true);
        updateProgressBars(finalScore);
        document.getElementById('evalText').textContent = '✅ 视频结束，最终得分已锁定';
      } else if (!totalScoreLocked) {
        const recentScores = stageScores.slice(-PHASE_SCORE_WINDOW);
        const runningScore = recentScores.reduce((a, b) => a + b, 0) / (recentScores.length || 1);
        updateTotalScore(runningScore, false);
        const wrap = document.getElementById('stageCardsWrap');
        if (wrap) wrap.style.display = 'block';
      }
      updateProblems();
    }

    // 视频进度通过 storage 同步（pose 窗口会定期写当前播放时间）
    let videoDuration = 0; // 总时长（秒）
    let lastVideoTime = -1; // pose 窗口当前的 currentTime

    // 监听 storage 事件
    window.addEventListener('storage', (e) => {
      if (e.key === STORAGE_KEY + '_trigger') {
        // 同步视频时长和当前播放时间
        const dur = localStorage.getItem(STORAGE_KEY + '_duration');
        if (dur) videoDuration = parseFloat(dur);
        const curTime = localStorage.getItem(STORAGE_KEY + '_currentTime');
        if (curTime) lastVideoTime = parseFloat(curTime);

        const dataStr = localStorage.getItem(STORAGE_KEY);
        if (dataStr) {
          try {
            const data = JSON.parse(dataStr);
            handleData(data);
          } catch(err) { console.error('解析数据失败:', err); }
        }
      }
      if (e.key === STORAGE_KEY + '_ended' || e.key === STORAGE_KEY + '_close') {
        if (!isComplete) finishAnalysis();
      }
    });

    // 轮询（保险措施）
    setInterval(() => {
      const dur = localStorage.getItem(STORAGE_KEY + '_duration');
      if (dur) videoDuration = parseFloat(dur);
      const dataStr = localStorage.getItem(STORAGE_KEY);
      if (dataStr) {
        try {
          const data = JSON.parse(dataStr);
          if (data.timestamp !== lastTimestamp) {
            lastTimestamp = data.timestamp;
            handleData(data);
          }
        } catch(err) {}
      }
    }, 80);

    // ===== 完成分析 =====
    function finishAnalysis() {
      if (isComplete) return;
      isComplete = true;
      totalScoreLocked = true;

      // 确保所有阶段都结算
      if (stageScores.length > 0 && completedStages.length < 3) {
        const lastStageName = STAGE_NAMES[completedStages.length] || STAGE_NAMES[STAGE_NAMES.length - 1];
        const lastAvg = stageScores.reduce((a, b) => a + b, 0) / stageScores.length;
        completedStages.push({ name: lastStageName, score: Math.round(lastAvg), frames: stageScores.length });
        updateStageCards();
      }

      finalScore = completedStages.length > 0
        ? completedStages.reduce((acc, s) => acc + s.score, 0) / completedStages.length
        : (scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0);

      const grade = finalScore >= 95 ? 'S' : finalScore >= 85 ? 'A' : finalScore >= 75 ? 'B' : finalScore >= 65 ? 'C' : finalScore >= 50 ? 'D' : 'E';

      updateTotalScore(finalScore, true);
      updateProgressBars(finalScore);

      const gradeBadge = document.getElementById('gradeBadge');
      gradeBadge.textContent = grade;
      const gradeColors = { S: '#ffd700', A: '#4caf50', B: '#2196f3', C: '#ff9800', D: '#ff5252', E: '#9e9e9e' };
      gradeBadge.style.background = 'linear-gradient(135deg, ' + gradeColors[grade] + ', ' + gradeColors[grade] + 'aa)';
      gradeBadge.style.color = '#fff';

      const status = document.getElementById('status');
      const statusText = document.getElementById('statusText');
      status.className = 'status-bar complete';
      statusText.textContent = '✅ 分析完成！';

      // 找出最需改进的部位
      const problemCounts = Object.entries(problemFrames).sort((a, b) => b[1] - a[1]);
      const topProblem = problemCounts[0];
      const evalEl = document.getElementById('evalText');
      if (topProblem && topProblem[1] > 5) {
        const names = { leftKnee: '左腿踢腿', rightKnee: '右腿踢腿', leftElbow: '左臂伸直', rightElbow: '右臂伸直', leftShoulder: '左肩抬臂', rightShoulder: '右肩抬臂', leftHip: '左髋抬腿', rightHip: '右髋抬腿' };
        evalEl.textContent = '💡 建议重点改进: ' + (names[topProblem[0]] || topProblem[0]);
      } else {
        evalEl.textContent = '🎉 表现优秀！';
      }

      try {
        window.opener.postMessage({ type: 'evaluation_complete', score: finalScore, grade: grade, frameCount: frameCount }, '*');
      } catch(e) {}
    }

    console.log('评分统计窗口已启动');
  <\/script>
</body>
</html>`;

      const scoreWindow = window.open('', '_blank', 'width=400,height=750,menubar=no,toolbar=no,location=no');
      if (!scoreWindow) {
        alert('请允许弹出窗口！');
        throw new Error('无法打开窗口');
      }
      scoreWindow.document.write(html);
      scoreWindow.document.close();
      return scoreWindow;
    },

    // 处理 message 事件
    handleMessage(event) {
      if (event.data && event.data.type === 'evaluation_complete') {
        this.loading = false;
        this.result = {
          total_score: Math.round(event.data.score),
          grade: event.data.grade,
          comment: this.getComment(event.data.score),
          accuracy_score: Math.round(event.data.score),
          rhythm_score: Math.round(Math.min(100, event.data.score * 1.05)),
          fluency_score: Math.round(Math.min(100, event.data.score * 0.98))
        };
        this.cleanup();
      }
    },

    // 获取评语
    getComment(score) {
      if (score >= 95) return '完美！堪称范本！';
      if (score >= 85) return '优秀！动作非常标准！';
      if (score >= 75) return '良好！继续加油！';
      if (score >= 65) return '合格！还需要多加练习';
      if (score >= 50) return '不合格！建议观看标准动作';
      return '差距较大，请认真练习基础动作';
    },

    // 清理资源
    cleanup() {
      if (this.videoObjectUrl) {
        URL.revokeObjectURL(this.videoObjectUrl);
        this.videoObjectUrl = null;
      }
      // 清理 localStorage
      try {
        localStorage.removeItem(this.storageKey);
        localStorage.removeItem(this.storageKey + '_trigger');
        localStorage.removeItem(this.storageKey + '_ended');
        localStorage.removeItem(this.storageKey + '_close');
        localStorage.removeItem(this.storageKey + '_duration');
      } catch(e) {}
    },

    // 重置
    reset() {
      this.videoFile = null;
      this.result = null;
      this.cleanup();
    }
  }
};
</script>

<style scoped>
.dance-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  font-size: 28px;
  margin-bottom: 30px;
  color: #333;
}

.upload-section {
  background: #f9f9f9;
  padding: 30px;
  border-radius: 15px;
}

.control-row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.file-input {
  flex: 1;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.dance-select {
  padding: 12px 15px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  min-width: 150px;
}

.start-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  border: none;
  border-radius: 25px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s;
}

.start-btn:hover:not(:disabled) {
  transform: scale(1.02);
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

.start-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-section {
  text-align: center;
  padding: 50px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.tip {
  color: #ff9800;
  font-size: 14px;
  margin-top: 10px;
}

.result-section {
  background: #fff;
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.result-section h3 {
  font-size: 22px;
  margin-bottom: 20px;
}

.result-summary {
  margin: 20px 0;
}

.score-display {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-bottom: 15px;
}

.score {
  font-size: 60px;
  font-weight: bold;
  color: #667eea;
}

.grade {
  padding: 15px 25px;
  border-radius: 15px;
  font-size: 36px;
  font-weight: bold;
  color: #fff;
}

.grade.grade-S { background: linear-gradient(135deg, #ffd700, #ff8c00); }
.grade.grade-A { background: linear-gradient(135deg, #4caf50, #8bc34a); }
.grade.grade-B { background: linear-gradient(135deg, #2196f3, #03a9f4); }
.grade.grade-C { background: linear-gradient(135deg, #ff9800, #ffc107); }
.grade.grade-D { background: linear-gradient(135deg, #f44336, #ff5722); }
.grade.grade-E { background: linear-gradient(135deg, #9e9e9e, #bdbdbd); }

.comment {
  color: #666;
  font-size: 16px;
  margin-bottom: 15px;
}

.detail-scores {
  display: flex;
  justify-content: center;
  gap: 30px;
  color: #888;
  font-size: 14px;
}

.reset-btn {
  padding: 12px 30px;
  background: #666;
  color: #fff;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 20px;
}
</style>
