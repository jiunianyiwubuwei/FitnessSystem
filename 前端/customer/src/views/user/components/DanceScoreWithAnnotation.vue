<template>
  <div class="dance-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
          舞蹈评分系统
        </h1>
        <p class="hero-subtitle">AI 关键点标注 · 骨架可视化 · 智能评分分析</p>
      </div>
    </div>

    <!-- Tab Toggle -->
    <div class="tab-toggle" v-if="phase === 'idle'">
      <button
        class="tab-btn"
        :class="{ active: contentMode === 'upload' }"
        @click="contentMode = 'upload'"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        上传视频
      </button>
      <button
        class="tab-btn"
        :class="{ active: contentMode === 'history' }"
        @click="switchToHistory"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12 6 12 12 16 14"/>
        </svg>
        标注历史
      </button>
    </div>

    <!-- Phase 1: Upload Area -->
    <div v-if="phase === 'idle' && contentMode === 'upload'" class="upload-section">
      <div class="card">
        <div class="card-body">
          <!-- Drop Zone -->
          <div
            class="upload-zone"
            :class="{ 'drag-over': isDragOver, 'file-selected': selectedFile }"
            @dragover.prevent="isDragOver = true"
            @dragleave="isDragOver = false"
            @drop.prevent="handleDrop"
            @click="$refs.fileInput.click()"
          >
            <input
              type="file"
              ref="fileInput"
              class="file-input-hidden"
              accept="video/*"
              @change="handleFileSelect"
            />
            <div class="upload-icon">
              <svg v-if="!selectedFile" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="23 7 16 12 23 17 23 7"/>
                <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
            </div>
            <p class="upload-text" v-if="!selectedFile">
              拖拽视频到此处，或<span class="upload-link">点击选择文件</span>
            </p>
            <p class="upload-text file-name" v-else>
              {{ selectedFile.name }}
              <span class="file-size">({{ formatFileSize(selectedFile.size) }})</span>
            </p>
            <p class="upload-hint" v-if="!selectedFile">支持 MP4, AVI, MOV 等常见视频格式</p>
            <p class="upload-hint" v-else>点击可重新选择其他文件</p>
          </div>

          <!-- Dance Select -->
          <div class="select-group">
            <label class="select-label">选择舞蹈标准（可选）</label>
            <div class="select-wrapper">
              <select v-model="selectedDance" class="select-field">
                <option :value="null">-- 不评分，仅标注 --</option>
                <option v-for="dance in danceList" :key="dance.id" :value="dance.id">
                  {{ dance.name }}
                </option>
              </select>
              <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>

          <!-- Upload Button -->
          <button
            class="action-btn primary full-width"
            @click="startUpload"
            :disabled="!selectedFile || isUploading"
          >
            <svg v-if="!isUploading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
            <span v-if="isUploading" class="btn-spinner"></span>
            <span>{{ isUploading ? '上传中...' : '开始处理（标注+评分）' }}</span>
          </button>

          <!-- Tip -->
          <div class="tip-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="16" x2="12" y2="12"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
            <span>上传后系统将自动完成：关键点标注 → 骨架可视化 → 舞蹈评分</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Phase 1: History List -->
    <div v-if="phase === 'idle' && contentMode === 'history'" class="history-section">
      <div class="history-header">
        <button class="back-btn" @click="contentMode = 'upload'">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
          返回
        </button>
        <h3 class="history-title">标注历史</h3>
      </div>

      <!-- Loading -->
      <div v-if="historyLoading" class="loading-state">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="historyRecords.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12 6 12 12 16 14"/>
        </svg>
        <p>暂无标注记录</p>
        <span>上传视频进行关键点标注吧</span>
      </div>

      <!-- Search -->
      <div v-else class="search-bar">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          v-model="historySearch"
          type="text"
          placeholder="搜索文件名..."
          class="search-input"
        />
        <button v-if="historySearch" class="search-clear" @click="historySearch = ''">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
        <span class="record-count">{{ filteredHistoryRecords.length }} 条记录</span>
        <button class="clear-btn" @click="clearHistory">清空</button>
      </div>

      <!-- Record List -->
      <div v-if="filteredHistoryRecords.length > 0" class="record-list">
        <div
          v-for="record in filteredHistoryRecords"
          :key="record.id"
          class="record-card"
          @click="playHistoryRecord(record)"
        >
          <div class="card-preview">
            <video :src="record.video_url" class="preview-video" muted preload="metadata"></video>
            <div class="play-overlay">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5 3 19 12 5 21 5 3"/>
              </svg>
            </div>
          </div>
          <div class="card-info">
            <h4 class="filename">{{ record.original_filename }}</h4>
            <div class="stats-tags">
              <span class="stat-tag">{{ record.valid_frame_count || 0 }} / {{ record.total_frame_count || 0 }} 有效帧</span>
              <span class="stat-tag">{{ record.duration ? record.duration.toFixed(1) + 's' : '—' }}</span>
              <span class="stat-tag">{{ record.fps || 0 }} fps</span>
            </div>
            <div class="card-footer">
              <span class="time">{{ formatDateTime(record.created_at) }}</span>
              <span class="view-link">查看骨架 →</span>
            </div>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else-if="historySearch" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <p>没有找到匹配的记录</p>
        <span>试试其他关键词</span>
      </div>

      <!-- Pagination -->
      <div v-if="historyTotal > 0" class="pagination">
        <button class="page-btn" :disabled="historyPage <= 1" @click="loadHistoryPage(historyPage - 1)">上一页</button>
        <span class="page-info">第 {{ historyPage }} / {{ historyTotalPages }} 页</span>
        <button class="page-btn" :disabled="historyPage >= historyTotalPages" @click="loadHistoryPage(historyPage + 1)">下一页</button>
      </div>
    </div>

    <!-- History Dialog -->
    <div v-if="phase === 'idle' && showHistoryDialog" class="dialog-overlay" @click.self="showHistoryDialog = false">
      <div class="dialog-box">
        <div class="dialog-header">
          <h3>骨架标注播放</h3>
          <button class="dialog-close" @click="showHistoryDialog = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <AnnotatedVideoPlayer
          ref="historyPlayer"
          :initial-annotation-id="historyAnnotationId"
        />
      </div>
    </div>

    <!-- Phase 2: Processing -->
    <div v-if="phase === 'processing'" class="processing-overlay">
      <div class="processing-modal">
        <div class="modal-header">
          <div class="modal-title-row">
            <svg class="modal-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12a9 9 0 11-6.219-8.56"/>
            </svg>
            <h2>正在处理...</h2>
          </div>
          <span class="phase-badge" :class="'phase-' + processingPhase">
            {{ processingPhaseLabel }}
          </span>
        </div>

        <div class="modal-progress">
          <div class="progress-bar-wrap">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progress + '%' }"></div>
            </div>
            <span class="progress-percent">{{ progress }}%</span>
          </div>
          <p class="progress-message">{{ processingMessage }}</p>
        </div>

        <div class="modal-stats">
          <div class="stat-item">
            <span class="stat-label">总帧数</span>
            <span class="stat-value">{{ totalFrames || '—' }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">FPS</span>
            <span class="stat-value">{{ fps || '—' }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">时长</span>
            <span class="stat-value">{{ fmtDuration(duration) }}</span>
          </div>
        </div>

        <div class="modal-phases">
          <div class="phase-step" :class="{ active: processingPhase === 'annotation', done: progress >= 85 }">
            <div class="step-icon">
              <svg v-if="progress >= 85" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12a9 9 0 11-6.219-8.56"/>
              </svg>
            </div>
            <span class="step-name">关键点标注</span>
            <span class="step-desc">{{ progress >= 85 ? '已完成' : '处理中' }}</span>
          </div>
          <div class="phase-arrow">→</div>
          <div class="phase-step" :class="{ active: processingPhase === 'scoring', done: progress >= 95 }">
            <div class="step-icon">
              <svg v-if="progress >= 95" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12a9 9 0 11-6.219-8.56"/>
              </svg>
            </div>
            <span class="step-name">舞蹈评分</span>
            <span class="step-desc">{{ progress >= 95 ? '已完成' : (progress >= 85 ? '处理中' : '等待中') }}</span>
          </div>
        </div>

        <p class="modal-hint">请稍候，标注完成后视频将自动播放...</p>
      </div>
    </div>

    <!-- Phase 3: Results -->
    <div v-if="phase === 'done'" class="result-section">

      <!-- Player + Angle Panel -->
      <div class="result-layout">

        <!-- Player -->
        <div class="player-wrapper" :class="{ 'full-width': fullWidthMode || sidePanelCollapsed }">
          <div class="player-header">
            <div class="header-info">
              <h3 class="header-title">{{ uploadedFilename }}</h3>
              <span class="header-meta">{{ totalFrames }} 帧 | {{ fps }} fps | {{ fmtDuration(duration) }}</span>
            </div>
            <div class="header-actions">
              <span v-if="isPlaying" class="pause-hint">暂停查看角度</span>
              <button class="reset-btn-small" @click="reset">重新上传</button>
            </div>
          </div>

          <!-- Pre-render Overlay -->
          <div v-if="isPreRendering" class="pre-render-overlay">
            <div class="spinner"></div>
            <p>正在渲染骨架... {{ preRenderProgress }}/{{ totalFrames }}</p>
            <div class="progress-bar-sm">
              <div class="progress-fill-sm" :style="{ width: preRenderPercent + '%' }"></div>
            </div>
          </div>

          <!-- Video + Skeleton -->
          <div class="video-container" :class="{ 'full-width': fullWidthMode }">
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

          <!-- Skeleton Controls -->
          <div class="skeleton-control-bar">
            <div class="ctrl-group">
              <button
                class="ctrl-btn"
                :class="{ active: showSkeleton }"
                @click="toggleSkeleton"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                  <path d="M2 17l10 5 10-5"/>
                  <path d="M2 12l10 5 10-5"/>
                </svg>
                {{ showSkeleton ? '隐藏骨架' : '显示骨架' }}
              </button>
              <button
                class="ctrl-btn"
                :class="{ active: colorByQuality }"
                @click="colorByQuality = !colorByQuality; reRenderCurrentSkeleton()"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <circle cx="12" cy="12" r="6"/>
                  <circle cx="12" cy="12" r="2"/>
                </svg>
                {{ colorByQuality ? '质量染色ON' : '质量染色OFF' }}
              </button>
              <button
                class="ctrl-btn"
                :class="{ active: fullWidthMode }"
                @click="fullWidthMode = !fullWidthMode; $nextTick(() => syncCanvasSize())"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
                </svg>
                {{ fullWidthMode ? '退出全宽' : '全宽模式' }}
              </button>
            </div>
            <div class="ctrl-group sliders">
              <label class="ctrl-label">
                <span>透明度</span>
                <input
                  type="range" min="0.1" max="1" step="0.05"
                  v-model.number="skeletonOpacity"
                  @input="drawSkeleton(currentFrameIndex)"
                />
                <span class="ctrl-val">{{ Math.round(skeletonOpacity * 100) }}%</span>
              </label>
              <label class="ctrl-label">
                <span>线粗</span>
                <input
                  type="range" min="1" max="6" step="1"
                  v-model.number="skeletonThickness"
                  @change="reRenderAllSkeletons()"
                />
                <span class="ctrl-val">{{ skeletonThickness }}px</span>
              </label>
            </div>
          </div>

          <!-- Playback Controls -->
          <div class="bottom-control-bar">
            <div class="controls-row">
              <button class="ctrl-btn play-btn" @click="togglePlay">
                <svg v-if="!isPlaying" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="5 3 19 12 5 21 5 3"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="6" y="4" width="4" height="16"/>
                  <rect x="14" y="4" width="4" height="16"/>
                </svg>
              </button>
              <button class="ctrl-btn" @click="prevFrame" title="上一帧">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="19 20 9 12 19 4 19 20"/>
                  <line x1="5" y1="19" x2="5" y2="5"/>
                </svg>
              </button>
              <button class="ctrl-btn" @click="nextFrame" title="下一帧">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="5 4 15 12 5 20 5 4"/>
                  <line x1="19" y1="5" x2="19" y2="19"/>
                </svg>
              </button>
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
            <div class="frame-info-row">
              <span>帧: <strong>{{ currentFrameIndex }}</strong> / {{ totalFrames }}</span>
              <span class="sep">|</span>
              <span>有效帧: <strong>{{ validFrameCount }}</strong></span>
              <span class="sep">|</span>
              <span>当前帧: <strong>{{ formatTime(currentTime) }}</strong></span>
              <span class="sep">|</span>
              <span class="valid-badge" :class="currentFrameValid ? 'valid' : 'invalid'">
                {{ currentFrameValid ? '有效' : '无效' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Angle Panel -->
        <div class="angle-panel" :class="{ collapsed: sidePanelCollapsed }">
          <button
            class="panel-collapse-btn"
            @click="sidePanelCollapsed = !sidePanelCollapsed"
          >
            {{ sidePanelCollapsed ? '◀' : '▶' }}
          </button>

          <div v-if="isPlaying" class="panel-playing-hint">
            <span>播放中，暂停查看角度详情</span>
          </div>

          <div v-else class="panel-content">
            <div class="panel-header">
              <h3 class="panel-title">帧角度分析</h3>
              <span class="panel-frame-info">第 {{ currentFrameIndex }} 帧 | {{ formatTime(currentTime) }}</span>
            </div>

            <div class="frame-jump-bar">
              <button class="fjump-btn" @click="prevFrame">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="19 20 9 12 19 4 19 20"/>
                </svg>
              </button>
              <div class="fjump-range">
                <input
                  type="range" min="0" :max="totalFrames - 1"
                  v-model.number="currentFrameIndex"
                  @input="jumpToFrame(currentFrameIndex)"
                  class="fjump-slider"
                />
              </div>
              <button class="fjump-btn" @click="nextFrame">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="5 4 15 12 5 20 5 4"/>
                </svg>
              </button>
            </div>

            <div class="angle-grid">
              <div
                v-for="(angleData, joint) in currentAnglesDisplay"
                :key="joint"
                class="angle-item"
                :style="{
                  borderLeftColor: getScoreColor(angleData.qualityScore),
                  backgroundColor: getScoreColorAlpha(angleData.qualityScore, 0.07)
                }"
              >
                <div class="angle-info">
                  <span class="angle-joint">{{ angleData.cnName }}</span>
                  <span class="angle-value" v-if="angleData.angle !== null">{{ angleData.angle.toFixed(1) }}°</span>
                  <span class="angle-value angle-null" v-else>—</span>
                </div>
                <div class="angle-bar-bg">
                  <div
                    class="angle-bar-fill"
                    :style="{
                      width: angleData.barWidth + '%',
                      backgroundColor: getScoreColor(angleData.qualityScore)
                    }"
                  ></div>
                </div>
                <span class="angle-level-tag" :style="{ color: getScoreColor(angleData.qualityScore), backgroundColor: getScoreColorAlpha(angleData.qualityScore, 0.15) }">
                  {{ angleData.levelText }}
                </span>
              </div>
            </div>

            <div class="panel-footer">
              <p>暂停播放，可逐帧查看各关节角度</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Score Result -->
      <div v-if="scoreResult" class="card score-card">
        <div class="score-header">
          <div class="score-circle" :class="'grade-' + scoreResult.grade">
            <span class="score-num">{{ roundScore(scoreResult.total_score) }}</span>
            <span class="score-unit">分</span>
          </div>
          <div class="grade-badge" :class="'grade-' + scoreResult.grade">
            {{ scoreResult.grade }}
          </div>
          <div class="score-comment">{{ scoreResult.comment }}</div>
        </div>

        <div class="score-header-actions">
          <button class="download-report-btn" @click="downloadReport" title="下载详细评分报告">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            下载详细报告
          </button>
        </div>

        <div class="score-bars">
          <div class="score-row">
            <span class="label">准确度</span>
            <div class="bar-wrap"><div class="bar-fill bar-accuracy" :style="{ width: scoreResult.accuracy_score + '%' }"></div></div>
            <span class="bar-num">{{ roundScore(scoreResult.accuracy_score) }}%</span>
          </div>
          <div class="score-row">
            <span class="label">节奏感</span>
            <div class="bar-wrap"><div class="bar-fill bar-rhythm" :style="{ width: clampScore(scoreResult.rhythm_score) + '%' }"></div></div>
            <span class="bar-num">{{ roundScore(clampScore(scoreResult.rhythm_score)) }}%</span>
          </div>
          <div class="score-row">
            <span class="label">流畅度</span>
            <div class="bar-wrap"><div class="bar-fill bar-fluency" :style="{ width: clampScore(scoreResult.fluency_score) + '%' }"></div></div>
            <span class="bar-num">{{ roundScore(clampScore(scoreResult.fluency_score)) }}%</span>
          </div>
        </div>

        <div v-if="hasJointScores(scoreResult)" class="joint-section">
          <h4 class="section-subtitle">关节评分详情</h4>
          <div class="joint-grid">
            <div
              v-for="(value, joint) in scoreResult.joint_scores"
              :key="joint"
              class="joint-item"
              :style="getJointColorStyle(value)"
            >
              <span class="joint-name">{{ joint }}</span>
              <span class="joint-score" :style="{ color: getScoreColor(typeof value === 'object' ? value.mean : value) }">{{ formatJointScore(value) }}</span>
            </div>
          </div>
        </div>

        <div v-if="scoreResult && (scoreResult.analysis || filteredTips.length > 0)" class="summary-section">
          <h4 class="section-subtitle">综合评语</h4>
          <p v-if="scoreResult.analysis" class="summary-text">{{ scoreResult.analysis }}</p>
          <div v-if="filteredTips.length > 0" class="summary-tips">
            <div
              v-for="(tip, i) in filteredTips"
              :key="i"
              class="summary-tip-item"
              :style="getTipColorStyle(typeof tip === 'object' ? tip.current_score : null)"
            >
              <div class="tip-header">
                <span class="tip-joint">{{ typeof tip === 'object' ? tip.joint_cn : '改进建议' }}</span>
                <span
                  v-if="typeof tip === 'object' && tip.current_score != null"
                  class="tip-score-badge"
                  :style="{
                    backgroundColor: getScoreColorAlpha(tip.current_score, 0.15),
                    color: getScoreColor(tip.current_score)
                  }"
                >
                  {{ tip.current_score.toFixed(1) }}%
                </span>
              </div>
              <div v-if="typeof tip === 'object' && tip.current_score != null" class="tip-bar-wrap">
                <div
                  class="tip-bar-fill"
                  :style="{ width: Math.min(100, tip.current_score) + '%', backgroundColor: getScoreColor(tip.current_score) }"
                ></div>
              </div>
              <p class="tip-desc">{{ typeof tip === 'object' ? tip.tip : tip }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- No Score Standard -->
      <div v-else class="card annotation-card">
        <div class="annotation-complete">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
          <h3>标注完成</h3>
          <p>视频已成功提取关键点，上方的播放器展示了骨架可视化效果。</p>
          <p class="hint-small">如需进行舞蹈评分，请在上传时选择舞蹈标准。</p>
        </div>
      </div>
    </div>

    <!-- Phase 4: Failed -->
    <div v-if="phase === 'failed'" class="error-section">
      <div class="card error-card">
        <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="15" y1="9" x2="9" y2="15"/>
          <line x1="9" y1="9" x2="15" y2="15"/>
        </svg>
        <h3>处理失败</h3>
        <p>{{ errorMessage }}</p>
        <button class="reset-btn" @click="reset">重新上传</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AnnotatedVideoPlayer from './AnnotatedVideoPlayer.vue';

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
  name: 'DanceScoreWithAnnotation',
  components: { AnnotatedVideoPlayer },

  data() {
    return {
      contentMode: 'upload',
      phase: 'idle',
      isDragOver: false,
      isUploading: false,
      selectedFile: null,
      selectedDance: null,
      danceList: [],
      taskId: null,
      annotationId: null,
      progress: 0,
      processingPhase: 'annotation',
      processingMessage: '',
      errorMessage: '',
      totalFrames: 0,
      fps: 0,
      duration: 0,
      uploadedFilename: '',
      hasDanceStandard: false,
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
      isPreRendering: false,
      preRenderProgress: 0,
      skeletonImages: {},
      skeletonLandmarks: {},
      scoreResult: null,
      currentAngles: null,
      skeletonAngles: {},
      historyRecords: [],
      historyLoading: false,
      historyPage: 1,
      historyPageSize: 10,
      historyTotal: 0,
      showHistoryDialog: false,
      historyAnnotationId: null,
      historySearch: '',
      showSkeleton: true,
      skeletonOpacity: 0.85,
      skeletonThickness: 2,
      fullWidthMode: false,
      colorByQuality: false,
      sidePanelCollapsed: false,
    };
  },

  computed: {
    historyTotalPages() {
      return Math.ceil(this.historyTotal / this.historyPageSize) || 1;
    },
    filteredHistoryRecords() {
      if (!this.historySearch.trim()) return this.historyRecords;
      const q = this.historySearch.trim().toLowerCase();
      return this.historyRecords.filter(r =>
        (r.original_filename || '').toLowerCase().includes(q) ||
        (r.dance_name || '').toLowerCase().includes(q)
      );
    },
    currentAnglesDisplay() {
      if (!this.currentAngles) return {};
      const result = {};
      for (const [joint, angle] of Object.entries(this.currentAngles)) {
        const isKick = joint.includes('leg_kick');
        const maxAngle = isKick ? 90 : 180;
        const normalizedAngle = angle !== null ? Math.min(Math.max(angle, 0), maxAngle) : 0;
        const barWidth = angle !== null ? (normalizedAngle / maxAngle) * 100 : 0;
        let level = 'medium';
        let levelText = '一般';
        let qualityScore = 55;
        if (angle !== null) {
          if (isKick) {
            if (angle >= 45) { level = 'excellent'; levelText = '优秀'; qualityScore = 85 + (angle - 45) / 45 * 15; }
            else if (angle >= 30) { level = 'good'; levelText = '良好'; qualityScore = 55 + (angle - 30) / 15 * 30; }
            else { level = 'bad'; levelText = '待改进'; qualityScore = Math.max(0, 55 - (30 - angle) / 30 * 55); }
          } else {
            if (angle >= 140) { level = 'excellent'; levelText = '优秀'; qualityScore = 85 + (angle - 140) / 40 * 15; }
            else if (angle >= 100) { level = 'good'; levelText = '良好'; qualityScore = 55 + (angle - 100) / 40 * 30; }
            else { level = 'bad'; levelText = '待改进'; qualityScore = Math.max(0, 55 - (100 - angle) / 100 * 55); }
          }
        }
        result[joint] = { angle, cnName: JOINT_NAMES_CN[joint] || joint, barWidth, level, levelText, qualityScore: Math.min(100, qualityScore) };
      }
      return result;
    },
    userId() {
      const user = JSON.parse(sessionStorage.getItem('userMessage') || '{}');
      return user.id || null;
    },
    token() {
      return sessionStorage.getItem('token') || '';
    },
    processingPhaseLabel() {
      if (this.processingPhase === 'annotation') return '正在提取关键点标注...';
      if (this.processingPhase === 'scoring') return '正在计算舞蹈评分...';
      return '处理完成';
    },
    filteredTips() {
      if (!this.scoreResult || !this.scoreResult.improvement_tips) return [];
      return this.scoreResult.improvement_tips.filter(tip => this.hasSignificantTip(tip));
    },
    preRenderPercent() {
      if (!this.totalFrames || this.totalFrames === 0) return 0;
      return (this.preRenderProgress / this.totalFrames * 100).toFixed(1);
    },
  },

  mounted() {
    this.fetchDanceList();
  },

  beforeDestroy() {
    this.stopPolling();
    if (this.resizeObserver) this.resizeObserver.disconnect();
    this.cleanupVideo();
  },

  methods: {
    handleFileSelect(e) {
      const file = e.target.files[0];
      if (file) this.selectedFile = file;
    },
    handleDrop(e) {
      this.isDragOver = false;
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('video/')) this.selectedFile = file;
    },
    async fetchDanceList() {
      try {
        const response = await fetch('/api/dance/standards/', {
          headers: { 'Authorization': `Bearer ${this.token}` }
        });
        if (response.ok) {
          const data = await response.json();
          this.danceList = data.data || [];
        }
      } catch (error) {
        console.error('获取舞蹈列表失败:', error);
      }
    },
    async startUpload() {
      if (!this.selectedFile) { alert('请先选择视频文件！'); return; }
      this.isUploading = true;
      this.uploadedFilename = this.selectedFile.name;
      const formData = new FormData();
      formData.append('video_file', this.selectedFile);
      if (this.userId) formData.append('user_id', this.userId);
      if (this.selectedDance) formData.append('dance_id', this.selectedDance);
      this.hasDanceStandard = !!this.selectedDance;
      try {
        const response = await axios.post('/api/combined/upload/', formData, {
          headers: { 'Authorization': `Bearer ${this.token}` },
        });
        if (response.data.code === 202 || response.data.code === 200) {
          this.taskId = response.data.task_id;
          this.annotationId = response.data.annotation_id;
          this.phase = 'processing';
          this.startPolling();
        } else {
          alert(response.data.error || '上传失败');
        }
      } catch (error) {
        alert('上传失败: ' + (error.message || '网络错误'));
      } finally {
        this.isUploading = false;
      }
    },
    startPolling() { this.stopPolling(); this.pollTimer = setInterval(() => this.checkStatus(), 2000); },
    stopPolling() { if (this.pollTimer) { clearInterval(this.pollTimer); this.pollTimer = null; } },
    async checkStatus() {
      if (!this.taskId) return;
      try {
        const resp = await axios.get(`/api/combined/status/?task_id=${this.taskId}`, {
          headers: { 'Authorization': `Bearer ${this.token}` },
        });
        if (resp.data.code === 200) {
          const d = resp.data.data;
          this.progress = d.progress || 0;
          this.processingMessage = d.message || '';
          this.totalFrames = d.total_frames || 0;
          this.fps = d.fps || 0;
          this.duration = d.duration || 0;
          this.processingPhase = d.phase === 'scoring' ? 'scoring' : d.phase === 'done' ? 'done' : 'annotation';
          if (d.annotation_id && !this.annotationId) { this.annotationId = d.annotation_id; }
          if (d.status === 'completed') {
            this.stopPolling();
            this.onProcessingComplete(d);
          } else if (d.status === 'failed') {
            this.stopPolling();
            this.phase = 'failed';
            this.errorMessage = d.error || '处理失败';
          } else {
            if (d.progress >= 85 && !this.videoSrc && d.video_url) {
              this.videoSrc = d.video_url.startsWith('http') ? d.video_url : 'http://127.0.0.1:8000' + d.video_url;
            }
          }
        }
      } catch (e) { console.error('轮询失败:', e); }
    },
    onProcessingComplete(data) {
      this.videoSrc = data.video_url ? (data.video_url.startsWith('http') ? data.video_url : 'http://127.0.0.1:8000' + data.video_url) : this.videoSrc;
      if (data.score) { this.scoreResult = data.score; }
      else if (data.score_status === 'no_standard') { this.scoreResult = null; }
      else if (data.score_status === 'failed') {
        this.scoreResult = null;
        this.$message.warning('标注完成，但评分失败: ' + (data.score_error || '未知错误'));
      }
      this.phase = 'done';
      this.uploadedFilename = this.uploadedFilename || (data.video_url ? data.video_url.split('/').pop() : '');
      this.$nextTick(() => { this.startPreRendering(); });
    },
    async startPreRendering() {
      const video = this.$refs.videoEl;
      if (!video || !this.annotationId) return;
      if (video.readyState < 1) { await new Promise(resolve => video.addEventListener('loadedmetadata', resolve, { once: true })); }
      this.isPreRendering = true;
      this.preRenderProgress = 0;
      this.skeletonImages = {};
      try {
        const resp = await axios.get(`/api/annotation/frames/?annotation_id=${this.annotationId}&start_frame=0&end_frame=${this.totalFrames > 0 ? this.totalFrames - 1 : 0}`, { headers: { 'Authorization': `Bearer ${this.token}` }, timeout: 60000 });
        if (resp.data.code !== 200) {
          this.$message.error(resp.data.error || '获取帧数据失败');
          this.isPreRendering = false;
          return;
        }
        const frames = resp.data.data.frames || [];
        const videoW = Math.round(video.videoWidth || 640);
        const videoH = Math.round(video.videoHeight || 480);
        this.validFrameCount = frames.filter(f => f.is_valid).length;
        this.skeletonAngles = {};
        this.skeletonLandmarks = {};
        for (const f of frames) {
          if (f.angles) this.skeletonAngles[f.frame_index] = f.angles;
          if (f.landmarks) this.skeletonLandmarks[f.frame_index] = { landmarks: f.landmarks, is_valid: f.is_valid };
        }
        await this.batchPreRender(frames, videoW, videoH);
        this.isPreRendering = false;
        this.$nextTick(() => {
          this.syncCanvasSize();
          this.currentFrameIndex = 0;
          this.drawSkeleton(0);
        });
      } catch (error) {
        this.isPreRendering = false;
        this.$message.error('加载帧数据失败: ' + (error.message || '网络错误'));
      }
    },
    batchPreRender(frames, videoW, videoH) {
      return new Promise(resolve => {
        const BATCH = 50;
        let i = 0;
        const processBatch = () => {
          const end = Math.min(i + BATCH, frames.length);
          for (; i < end; i++) {
            const f = frames[i];
            const frameAngles = f.angles || {};
            this.skeletonImages[f.frame_index] = this.renderSkeletonToImageData(f.landmarks, f.is_valid, videoW, videoH, frameAngles);
            this.preRenderProgress = i + 1;
          }
          if (i < frames.length) { requestAnimationFrame(processBatch); }
          else { resolve(); }
        };
        requestAnimationFrame(processBatch);
      });
    },
    renderSkeletonToImageData(landmarks, isValid, w, h, angles) {
      const offCanvas = document.createElement('canvas');
      offCanvas.width = w; offCanvas.height = h;
      const ctx = offCanvas.getContext('2d');
      if (!isValid || !landmarks || landmarks.length === 0) { return ctx.getImageData(0, 0, w, h); }
      const pts = [];
      for (let i = 0; i < landmarks.length; i += 4) { pts.push([landmarks[i], landmarks[i+1], landmarks[i+2], landmarks[i+3]]); }
      const thickness = this.skeletonThickness;
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      const frameAngles = angles || (this.currentFrameIndex != null ? (this.skeletonAngles[this.currentFrameIndex] || {}) : {});
      const jointColorMap = this.buildJointColorMap(frameAngles);
      for (const [a, b] of POSE_CONNECTIONS) {
        const pA = pts[a]; const pB = pts[b];
        if (!pA || !pB) continue;
        if ((pA[3] || 0) < 0.3 || (pB[3] || 0) < 0.3) continue;
        let color = '#00FF00';
        if (this.colorByQuality && jointColorMap) { color = jointColorMap[a] || jointColorMap[b] || '#00FF00'; }
        ctx.strokeStyle = color; ctx.lineWidth = thickness;
        ctx.beginPath(); ctx.moveTo(pA[0] * w, pA[1] * h); ctx.lineTo(pB[0] * w, pB[1] * h); ctx.stroke();
      }
      ctx.fillStyle = '#FF4444';
      for (const p of pts) {
        if (!p) continue;
        if ((p[3] || 0) < 0.3) continue;
        ctx.beginPath(); ctx.arc(p[0] * w, p[1] * h, 4, 0, Math.PI * 2); ctx.fill();
      }
      return ctx.getImageData(0, 0, w, h);
    },
    buildJointColorMap(angles) {
      const map = {};
      for (const [joint, angle] of Object.entries(angles)) {
        if (angle === null) continue;
        const isKick = joint.includes('leg_kick');
        let score;
        if (isKick) {
          score = Math.max(0, Math.min(100, ((angle - 30) / (45 - 30)) * 100));
        } else {
          score = Math.max(0, Math.min(100, ((angle - 100) / (140 - 100)) * 100));
        }
        const jointIdx = this.getJointPointIndex(joint);
        if (jointIdx !== null) { map[jointIdx] = this.getScoreColor(score); }
      }
      return map;
    },
    getJointPointIndex(joint) {
      const mapping = { 'left_shoulder': 11, 'right_shoulder': 12, 'left_elbow': 13, 'right_elbow': 14, 'left_hip': 23, 'right_hip': 24, 'left_knee': 25, 'right_knee': 26, 'left_leg_kick': 27, 'right_leg_kick': 28 };
      return mapping[joint] !== undefined ? mapping[joint] : null;
    },
    getJointAngleLevel(joint, angle) {
      if (angle === null) return 'bad';
      const isKick = joint.includes('leg_kick');
      if (isKick) { if (angle >= 45) return 'excellent'; if (angle >= 30) return 'good'; return 'bad'; }
      if (angle >= 140) return 'excellent';
      if (angle >= 100) return 'good';
      return 'bad';
    },
    onVideoLoaded() {
      const video = this.$refs.videoEl;
      if (!video) return;
      this.videoDuration = video.duration;
      this.syncCanvasSize();
      if (!this.resizeObserver) {
        this.resizeObserver = new ResizeObserver(() => { this.syncCanvasSize(); });
        this.resizeObserver.observe(video);
      }
    },
    syncCanvasSize() {
      const video = this.$refs.videoEl; const skCanvas = this.$refs.skeletonCanvas;
      if (!video || !skCanvas) return;
      const w = Math.round(video.videoWidth || video.clientWidth || 640);
      const h = Math.round(video.videoHeight || video.clientHeight || 480);
      skCanvas.width = w; skCanvas.height = h;
    },
    onTimeUpdate() {
      const video = this.$refs.videoEl;
      if (!video) return;
      this.currentTime = video.currentTime;
      this.seekbarPercent = this.videoDuration > 0 ? (this.currentTime / this.videoDuration) * 100 : 0;
      const frameIndex = this.fps > 0 ? Math.floor(video.currentTime * this.fps) : 0;
      if (frameIndex !== this.currentFrameIndex) { this.currentFrameIndex = frameIndex; this.updateCurrentFrame(); }
    },
    updateCurrentFrame() {
      const frameData = this.skeletonImages[this.currentFrameIndex];
      this.currentFrameValid = !!(frameData && this.hasNonEmptyPixels(frameData));
      this.currentAngles = this.skeletonAngles[this.currentFrameIndex] || null;
      this.drawSkeleton(this.currentFrameIndex);
    },
    hasNonEmptyPixels(imgData) {
      for (let i = 3; i < imgData.data.length; i += 4) { if (imgData.data[i] > 0) return true; }
      return false;
    },
    drawSkeleton(frameIndex) {
      const skCanvas = this.$refs.skeletonCanvas;
      if (!skCanvas) return;
      const ctx = skCanvas.getContext('2d');
      ctx.clearRect(0, 0, skCanvas.width, skCanvas.height);
      if (!this.showSkeleton) return;
      const imgData = this.skeletonImages[frameIndex];
      if (imgData) { ctx.globalAlpha = this.skeletonOpacity; ctx.putImageData(imgData, 0, 0); ctx.globalAlpha = 1; }
    },
    toggleSkeleton() { this.showSkeleton = !this.showSkeleton; this.drawSkeleton(this.currentFrameIndex); },
    reRenderCurrentSkeleton() { this.drawSkeleton(this.currentFrameIndex); },
    reRenderAllSkeletons() {
      if (!this.videoSrc || Object.keys(this.skeletonLandmarks).length === 0) return;
      const video = this.$refs.videoEl;
      const videoW = Math.round(video?.videoWidth || 640);
      const videoH = Math.round(video?.videoHeight || 480);
      const allFrames = Object.entries(this.skeletonLandmarks).map(([fi, data]) => ({ frame_index: parseInt(fi), landmarks: data.landmarks, is_valid: data.is_valid, angles: this.skeletonAngles[fi] || {} }));
      this.batchPreRender(allFrames, videoW, videoH).then(() => { this.drawSkeleton(this.currentFrameIndex); });
    },
    togglePlay() { const video = this.$refs.videoEl; if (!video) return; if (this.isPlaying) video.pause(); else video.play(); },
    onPlay() { this.isPlaying = true; },
    onPause() { this.isPlaying = false; },
    onEnded() { this.isPlaying = false; },
    setPlaybackRate() { const video = this.$refs.videoEl; if (video) video.playbackRate = parseFloat(this.playbackRate); },
    seekTo(e) {
      const seekbar = this.$refs.seekbarEl;
      if (!seekbar) return;
      const rect = seekbar.getBoundingClientRect();
      const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      const video = this.$refs.videoEl;
      if (video && this.videoDuration) { video.currentTime = ratio * this.videoDuration; }
    },
    prevFrame() { const video = this.$refs.videoEl; if (!video || !this.fps) return; const step = 1 / this.fps; video.currentTime = Math.max(0, video.currentTime - step); },
    nextFrame() { const video = this.$refs.videoEl; if (!video || !this.fps) return; const step = 1 / this.fps; video.currentTime = Math.min(video.duration, video.currentTime + step); },
    jumpToFrame(frameIndex) { const video = this.$refs.videoEl; if (!video || !this.fps) return; const clamped = Math.max(0, Math.min(frameIndex, this.totalFrames - 1)); video.currentTime = clamped / this.fps; },
    formatTime(seconds) { if (!seconds || isNaN(seconds)) return '0:00'; const m = Math.floor(seconds / 60); const s = Math.floor(seconds % 60); return `${m}:${s.toString().padStart(2, '0')}`; },
    formatDateTime(isoString) { if (!isoString) return '—'; const d = new Date(isoString); return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`; },
    formatFileSize(bytes) { if (!bytes) return '—'; if (bytes < 1024) return bytes + ' B'; if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'; if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB'; return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB'; },
    fmtDuration(val) { if (!val || isNaN(val)) return '—'; return val.toFixed(1) + 's'; },
    roundScore(val) { if (val == null || isNaN(val)) return '--'; return Math.round(val); },
    clampScore(val) { if (val == null || isNaN(val)) return 0; return Math.min(100, val); },
    hasJointScores(result) { return result && result.joint_scores && Object.keys(result.joint_scores).length > 0; },
    hasTips(result) { return result && result.improvement_tips && result.improvement_tips.length > 0; },
    hasSignificantTip(tip) {
      if (typeof tip !== 'object' || tip.current_score == null) return true;
      if (tip.angle_diff == null) return true;
      return tip.angle_diff >= 5;
    },
    formatJointScore(value) { if (typeof value === 'object' && value !== null && value.mean != null) return value.mean.toFixed(1) + '%'; if (typeof value === 'number') return value.toFixed(1) + '%'; return '--'; },
    getJointClass(value) { return ''; },
    getScoreColor(score) {
      if (score == null) return 'rgb(156,163,175)';
      const stops = [
        { score: 85, r: 16,  g: 185, b: 129 },
        { score: 70, r: 132, g: 204, b: 22  },
        { score: 55, r: 245, g: 158, b: 11  },
        { score: 40, r: 239, g: 68,  b: 68  },
      ];
      if (score >= 85) return `rgb(${stops[0].r},${stops[0].g},${stops[0].b})`;
      if (score <= 40) return `rgb(${stops[3].r},${stops[3].g},${stops[3].b})`;
      for (let i = 0; i < stops.length - 1; i++) {
        const a = stops[i];
        const b = stops[i + 1];
        if (score >= b.score && score < a.score) {
          const t = (score - b.score) / (a.score - b.score);
          return `rgb(${Math.round(a.r + (b.r - a.r) * t)},${Math.round(a.g + (b.g - a.g) * t)},${Math.round(a.b + (b.b - a.b) * t)})`;
        }
      }
      return `rgb(${stops[0].r},${stops[0].g},${stops[0].b})`;
    },
    getScoreColorAlpha(score, alpha) {
      if (score == null) return 'rgba(156,163,175,0.07)';
      const rgb = this.getScoreColor(score).match(/\d+/g).map(Number);
      return `rgba(${rgb[0]},${rgb[1]},${rgb[2]},${alpha})`;
    },
    getJointColorStyle(value) {
      const score = typeof value === 'object' ? value.mean : value;
      return {
        borderLeftColor: this.getScoreColor(score),
        backgroundColor: this.getScoreColorAlpha(score, 0.07),
      };
    },
    getTipClass(score) { if (score == null) return ''; if (score >= 85) return 'tip-excellent'; if (score >= 70) return 'tip-good'; if (score >= 55) return 'tip-medium'; return 'tip-bad'; },
    getTipColorStyle(score) {
      if (score == null) return {};
      return {
        borderLeftColor: this.getScoreColor(score),
        backgroundColor: this.getScoreColorAlpha(score, 0.05),
      };
    },
    generateDanceReport() {
      const r = this.scoreResult;
      if (!r) return '';

      const now = new Date();
      const dateStr = `${now.getFullYear()}年${String(now.getMonth() + 1).padStart(2, '0')}月${String(now.getDate()).padStart(2, '0')}日`;
      const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
      const filename = this.uploadedFilename || '未命名视频';
      const danceName = this.selectedDance
        ? (this.danceList.find(d => d.id === this.selectedDance)?.name || '未知舞蹈')
        : '未选择标准舞蹈';

      const gradeMap = { S: 'S级（卓越）', A: 'A级（优秀）', B: 'B级（良好）', C: 'C级（合格）', D: 'D级（较差）', E: 'E级（不合格）' };
      const gradeLabel = gradeMap[r.grade] || r.grade;

      const jointNamesCN = {
        'left_elbow': '左臂（肘关节）', 'right_elbow': '右臂（肘关节）',
        'left_shoulder': '左肩关节', 'right_shoulder': '右肩关节',
        'left_hip': '左髋关节', 'right_hip': '右髋关节',
        'left_knee': '左膝关节', 'right_knee': '右膝关节',
        'left_leg_kick': '左腿（踢腿）', 'right_leg_kick': '右腿（踢腿）',
        'trunk': '躯干稳定性',
      };

      const levelLabel = (score) => {
        if (score >= 85) return '优秀';
        if (score >= 70) return '良好';
        if (score >= 55) return '一般';
        return '待改进';
      };

      const levelColor = (score) => {
        if (score >= 85) return '◆ 优秀（深绿）';
        if (score >= 70) return '○ 良好（浅绿）';
        if (score >= 55) return '△ 一般（橙色）';
        return '× 待改进（红色）';
      };

      let report = '';
      report += '═══════════════════════════════════════════════════════════════════\n';
      report += '                     舞蹈评分详细分析报告\n';
      report += '═══════════════════════════════════════════════════════════════════\n\n';

      report += '【报告基本信息】\n';
      report += `  报告生成时间：${dateStr} ${timeStr}\n`;
      report += `  评测用户视频：${filename}\n`;
      report += `  参考舞蹈标准：${danceName}\n`;
      report += `  视频总帧数：${this.totalFrames} 帧\n`;
      report += `  视频帧率：${this.fps} fps\n`;
      report += `  视频时长：${this.fmtDuration(this.duration)}\n`;
      report += `  有效帧数：${this.validFrameCount} 帧\n`;
      report += '\n';

      report += '═══════════════════════════════════════════════════════════════════\n';
      report += '【一、总体评分结果】\n';
      report += '═══════════════════════════════════════════════════════════════════\n\n';
      report += `  ┌─────────────────────────────────────────┐\n`;
      report += `  │   综合评分：${String(r.total_score.toFixed(1)).padStart(5)} 分   等级：${gradeLabel.padStart(10)}│\n`;
      report += `  └─────────────────────────────────────────┘\n\n`;
      report += `  准确度得分：${r.accuracy_score?.toFixed(1) || '--'}%\n`;
      report += `  节奏感得分：${r.rhythm_score?.toFixed(1) || '--'}%\n`;
      report += `  流畅度得分：${r.fluency_score?.toFixed(1) || '--'}%\n`;
      report += '\n';

      report += '  各维度说明：\n';
      report += '  ① 准确度（权重 45%）：衡量您的动作角度与标准舞蹈动作的吻合程度，\n';
      report += '     由系统通过 MediaPipe 姿态识别提取33个身体关键点后逐帧比对计算得出。\n';
      report += '  ② 节奏感（权重 25%）：衡量您的动作切换节奏与标准舞蹈的匹配程度，\n';
      report += '     通过分析关节角度变化的时间间隔与标准曲线的偏差来量化评分。\n';
      report += '  ③ 流畅度（权重 30%）：衡量动作之间的衔接是否连贯平滑，\n';
      report += '     通过统计相邻帧之间的角度变化幅度是否在合理范围内来计算。\n';
      report += '\n';

      report += `  系统评语：${r.comment || '暂无'}\n`;
      report += '\n';

      if (r.phase_scores && Object.keys(r.phase_scores).length > 0) {
        report += '  分阶段得分：\n';
        for (const [phase, score] of Object.entries(r.phase_scores)) {
          report += `    · ${phase}阶段：${score.toFixed(1)}% [${levelLabel(score)}]\n`;
        }
        report += '\n';
      }

      report += '═══════════════════════════════════════════════════════════════════\n';
      report += '【二、各关节评分详情】\n';
      report += '═══════════════════════════════════════════════════════════════════\n\n';
      report += '  系统对以下10个核心关节进行了逐帧角度分析与评分：\n\n';

      if (r.joint_scores && Object.keys(r.joint_scores).length > 0) {
        const sorted = Object.entries(r.joint_scores).sort((a, b) => {
          const scoreA = typeof a[1] === 'object' ? a[1].mean : a[1];
          const scoreB = typeof b[1] === 'object' ? b[1].mean : b[1];
          return scoreA - scoreB;
        });

        const excellent = sorted.filter(([, v]) => (typeof v === 'object' ? v.mean : v) >= 85);
        const good = sorted.filter(([, v]) => {
          const s = typeof v === 'object' ? v.mean : v;
          return s >= 70 && s < 85;
        });
        const medium = sorted.filter(([, v]) => {
          const s = typeof v === 'object' ? v.mean : v;
          return s >= 55 && s < 70;
        });
        const poor = sorted.filter(([, v]) => (typeof v === 'object' ? v.mean : v) < 55);

        report += '  【优秀部位】\n';
        if (excellent.length > 0) {
          for (const [joint, data] of excellent) {
            const s = typeof data === 'object' ? data.mean : data;
            const min = typeof data === 'object' ? data.min : null;
            report += `    ${jointNamesCN[joint] || joint}：${s.toFixed(1)}%  ${levelColor(s)}\n`;
            if (min !== null) report += `      └─ 本次最低帧得分：${min.toFixed(1)}%\n`;
            report += '      └─ 评估：动作角度高度接近标准，与参考舞蹈吻合度极高，表现堪称出色。\n';
            report += '      └─ 建议：继续保持当前动作规范，可在动作幅度与力度上适度加强以进一步提升。\n';
          }
        } else {
          report += '    （无）\n';
        }
        report += '\n';

        report += '  【良好部位】\n';
        if (good.length > 0) {
          for (const [joint, data] of good) {
            const s = typeof data === 'object' ? data.mean : data;
            report += `    ${jointNamesCN[joint] || joint}：${s.toFixed(1)}%  ${levelColor(s)}\n`;
            report += '      └─ 评估：动作基本符合标准，存在小幅偏差，整体表现良好。\n';
            report += '      └─ 建议：注意动作的幅度和角度，可在细节处理上进一步精雕细琢。\n';
          }
        } else {
          report += '    （无）\n';
        }
        report += '\n';

        report += '  【一般部位】\n';
        if (medium.length > 0) {
          for (const [joint, data] of medium) {
            const s = typeof data === 'object' ? data.mean : data;
            report += `    ${jointNamesCN[joint] || joint}：${s.toFixed(1)}%  ${levelColor(s)}\n`;
            report += '      └─ 评估：动作存在明显偏差，与标准有较大差距，需要针对性练习。\n';
            report += '      └─ 建议：分解动作单独练习，感受标准动作的关节角度，逐步建立肌肉记忆。\n';
          }
        } else {
          report += '    （无）\n';
        }
        report += '\n';

        report += '  【待改进部位】\n';
        if (poor.length > 0) {
          for (const [joint, data] of poor) {
            const s = typeof data === 'object' ? data.mean : data;
            report += `    ${jointNamesCN[joint] || joint}：${s.toFixed(1)}%  ${levelColor(s)}\n`;
            report += '      └─ 评估：当前动作与标准偏差较大，是影响整体评分的核心因素。\n';
            report += '      └─ 建议：\n';
            if (joint.includes('leg_kick')) {
              report += '        → 加强腿部柔韧性与力量训练，建议每日做踢腿拉伸练习。\n';
              report += '        → 可借助把杆或墙壁辅助，逐步提高踢腿高度和控腿时间。\n';
            } else if (joint.includes('elbow') || joint.includes('knee')) {
              report += '        → 加强相应关节的伸展与弯曲训练，注意关节完全伸直或弯曲到位。\n';
              report += '        → 建议进行辅助拉伸练习，每次保持30秒，重复3-5组。\n';
            } else if (joint.includes('shoulder')) {
              report += '        → 加强肩部活动范围训练，建议做肩部绕环和抬手扩展练习。\n';
              report += '        → 注意发力时收紧肩胛骨，避免耸肩借力。\n';
            } else if (joint.includes('hip')) {
              report += '        → 加强髋部柔韧性和核心力量，注意抬腿时收紧腹部发力。\n';
              report += '        → 建议进行仰卧起坐和侧桥训练，提升髋部控制能力。\n';
            } else {
              report += '        → 建议反复观看标准舞蹈视频，理解目标姿态后再进行针对性练习。\n';
            }
          }
        } else {
          report += '    （无）\n';
        }
        report += '\n';

        const avgScore = sorted.reduce((acc, [, v]) => acc + (typeof v === 'object' ? v.mean : v), 0) / sorted.length;
        const strongest = sorted[sorted.length - 1];
        const weakest = sorted[0];

        report += '  【关节综合对比】\n';
        report += `    全部关节平均得分：${avgScore.toFixed(1)}%\n`;
        if (strongest && strongest[1]) {
          const sName = jointNamesCN[strongest[0]] || strongest[0];
          const sScore = typeof strongest[1] === 'object' ? strongest[1].mean : strongest[1];
          report += `    表现最佳关节：${sName}（${sScore.toFixed(1)}%）\n`;
        }
        if (weakest && weakest[1] && weakest[0] !== strongest[0]) {
          const wName = jointNamesCN[weakest[0]] || weakest[0];
          const wScore = typeof weakest[1] === 'object' ? weakest[1].mean : weakest[1];
          report += `    表现最弱关节：${wName}（${wScore.toFixed(1)}%）\n`;
        }
        report += '\n';
      } else {
        report += '  暂无关节评分数据。\n\n';
      }

      report += '═══════════════════════════════════════════════════════════════════\n';
      report += '【三、评分细则与标准说明】\n';
      report += '═══════════════════════════════════════════════════════════════════\n\n';
      report += '  1. 评分维度说明\n';
      report += '  ┌────────┬────────────────────────────────────────────────────────┐\n';
      report += '  │ 维度    │ 评判标准                                                │\n';
      report += '  ├────────┼────────────────────────────────────────────────────────┤\n';
      report += '  │ 准确度  │ 通过MediaPipe提取全身33个关键点，计算用户动作与标准舞    │\n';
      report += '  │ 45%权重 │ 蹈视频各关节角度的偏差，偏差越小得分越高。              │\n';
      report += '  ├────────┼────────────────────────────────────────────────────────┤\n';
      report += '  │ 节奏感  │ 分析用户动作的时间节点与标准节奏的匹配程度，节奏稳定、   │\n';
      report += '  │ 25%权重 │ 动作切换时机准确则得分高。                              │\n';
      report += '  ├────────┼────────────────────────────────────────────────────────┤\n';
      report += '  │ 流畅度  │ 衡量动作之间的衔接连贯性，相邻帧角度变化幅度在合理范围   │\n';
      report += '  │ 30%权重 │ 内越多，得分越高。出现骤变或卡顿会降低流畅度得分。       │\n';
      report += '  └────────┴────────────────────────────────────────────────────────┘\n\n';

      report += '  2. 等级划分标准\n';
      report += '  ┌────────┬──────────────────────┬────────────────────────────────┐\n';
      report += '  │ 等级    │ 综合得分              │ 表现描述                        │\n';
      report += '  ├────────┼──────────────────────┼────────────────────────────────┤\n';
      report += '  │   S    │  95 分及以上          │  完美级别，堪称标准范本         │\n';
      report += '  │   A    │  85 分 - 94 分        │  优秀，动作非常标准              │\n';
      report += '  │   B    │  75 分 - 84 分        │  良好，有小幅偏差需继续努力      │\n';
      report += '  │   C    │  65 分 - 74 分        │  合格，存在明显差距需加强练习    │\n';
      report += '  │   D    │  50 分 - 64 分        │  较差，基础薄弱需系统训练        │\n';
      report += '  │   E    │  50 分以下            │  不合格，差距较大需从基础开始    │\n';
      report += '  └────────┴──────────────────────┴────────────────────────────────┘\n\n';

      report += '  3. 关节评分体系\n';
      report += '  系统对以下10个核心关节进行独立评分，每个关节满分100分：\n\n';
      report += '  ┌──────────────────┬──────────────────────────┬────────────────────────┐\n';
      report += '  │ 关节名称          │ 测量方式                  │ 优秀标准                │\n';
      report += '  ├──────────────────┼──────────────────────────┼────────────────────────┤\n';
      report += '  │ 左臂（肘关节）    │ 肩-肘-腕三点角度          │ 伸直时 170°-180°        │\n';
      report += '  │ 右臂（肘关节）    │ 肩-肘-腕三点角度          │ 伸直时 170°-180°        │\n';
      report += '  │ 左肩关节          │ 肘-肩-髋三点角度          │ 抬臂时 100°-180°        │\n';
      report += '  │ 右肩关节          │ 肘-肩-髋三点角度          │ 抬臂时 100°-180°        │\n';
      report += '  │ 左髋关节          │ 肩-髋-膝三点角度          │ 抬腿时 90°-180°         │\n';
      report += '  │ 右髋关节          │ 肩-髋-膝三点角度          │ 抬腿时 90°-180°         │\n';
      report += '  │ 左膝关节          │ 髋-膝-踝三点角度          │ 伸直时 170°-180°        │\n';
      report += '  │ 右膝关节          │ 髋-膝-踝三点角度          │ 伸直时 170°-180°        │\n';
      report += '  │ 左腿（踢腿）      │ 髋-踝连线与垂直方向夹角   │ 踢出时角度越小越好       │\n';
      report += '  │ 右腿（踢腿）      │ 髋-踝连线与垂直方向夹角   │ 踢出时角度越小越好       │\n';
      report += '  └──────────────────┴──────────────────────────┴────────────────────────┘\n\n';

      report += '  4. 单帧评分规则（核心算法）\n\n';
      report += '  系统采用双层标准评分体系，对每一帧画面进行逐关节分析：\n\n';
      report += '  第①层 - 优秀层（Excellent Range）：\n';
      report += '    · 关节角度落在标准参考动作的 P10-P90 百分位区间内\n';
      report += '    · 得分范围：90-100分\n';
      report += '    · 越接近标准动作的均值角度，得分越高（最高100分）\n\n';
      report += '  第②层 - 可接受层（Acceptable Range）：\n';
      report += '    · 关节角度超出优秀层，但在四分位距（IQR）的1.5倍扩展范围内\n';
      report += '    · 得分范围：70-89分\n';
      report += '    · 偏离优秀层越多，得分越低\n\n';
      report += '  第③层 - 偏差层（Deviation）：\n';
      report += '    · 超出可接受范围，根据偏离程度梯度扣分\n';
      report += '    · 偏差≤10°：55分；偏差≤20°：42分\n';
      report += '    · 偏差≤35°：30分；偏差≤50°：18分\n';
      report += '    · 偏差>50°：最低可至0分\n\n';

      report += '  5. 动作阶段分析\n';
      report += '  系统将舞蹈动作分为三个阶段进行独立评分：\n';
      report += '  · 起势阶段（Preparatory Phase）：准备阶段，动作幅度较小，\n';
      report += '    评估身体的预启动姿态是否到位，手臂与腿部是否处于正确起始位置。\n';
      report += '  · 发力阶段（Power Phase）：主要动作阶段，角度变化最剧烈，\n';
      report += '    评估关节角度是否达到标准动作的峰值，力度与幅度是否充足。\n';
      report += '  · 收势阶段（Recovery Phase）：恢复阶段，动作逐渐回归初始位置，\n';
      report += '    评估动作回收是否自然流畅，是否有急促或僵硬的情况。\n\n';

      report += '═══════════════════════════════════════════════════════════════════\n';
      report += '【四、综合评语与训练建议】\n';
      report += '═══════════════════════════════════════════════════════════════════\n\n';
      report += '  ' + (r.analysis || '暂无综合评语。').replace(/\n/g, '\n  ') + '\n\n';

      if (r.improvement_tips && r.improvement_tips.length > 0) {
        report += '  【重点改进建议】\n';
        report += '  以下是针对本次评测中表现较弱部位的具体训练建议：\n\n';
        for (let i = 0; i < r.improvement_tips.length; i++) {
          const tip = r.improvement_tips[i];
          if (typeof tip === 'object') {
            const jointCn = tip.joint_cn || '未知部位';
            const currentScore = tip.current_score?.toFixed(1) || '--';
            const tipText = tip.tip || '暂无建议';
            report += `  ${i + 1}. ${jointCn}（当前得分：${currentScore}%）\n`;
            report += `     ${tipText}\n`;
            if (tip.angle_diff != null) {
              report += `     └─ 当前动作角度与标准偏差约：${tip.angle_diff.toFixed(1)}°\n`;
            }
            report += '\n';
          } else {
            report += `  ${i + 1}. ${tip}\n\n`;
          }
        }
      }

      report += '  【分阶段训练计划建议】\n\n';
      const totalScore = r.total_score || 0;
      if (totalScore >= 85) {
        report += '  阶段一（短期目标，1-2周）：\n';
        report += '    · 维持每日基本功练习，巩固现有动作规范性\n';
        report += '    · 开始接触更高难度的舞蹈动作组合，拓展动作库\n';
        report += '    · 建议每次练习时长：30-45分钟\n\n';
        report += '  阶段二（中期目标，3-4周）：\n';
        report += '    · 在保持准确度的前提下，提升动作的表现力和感染力\n';
        report += '    · 增加舞蹈表现力训练，关注表情与肢体协调\n';
        report += '    · 建议每次练习时长：45-60分钟\n\n';
        report += '  阶段三（长期目标，1个月以上）：\n';
        report += '    · 学习完整舞蹈套路，尝试自主编舞与即兴表演\n';
        report += '    · 可考虑参加舞蹈社群或团队训练，提升舞台经验\n';
        report += '    · 建议每次练习时长：60分钟以上\n\n';
      } else if (totalScore >= 65) {
        report += '  阶段一（短期目标，1-2周）：\n';
        report += '    · 每天进行15-20分钟基础拉伸，增强关节柔韧性\n';
        report += '    · 重点练习本次评测中得分较低的关节部位\n';
        report += '    · 建议每次练习时长：30分钟\n\n';
        report += '  阶段二（中期目标，3-4周）：\n';
        report += '    · 每天进行30分钟完整舞蹈动作练习，注意准确性\n';
        report += '    · 观看标准舞蹈视频，对比自身动作进行微调\n';
        report += '    · 建议每次练习时长：45分钟\n\n';
        report += '  阶段三（长期目标，1个月以上）：\n';
        report += '    · 每周至少完成3次完整舞蹈套路练习\n';
        report += '    · 逐步提高动作完成速度和流畅度\n';
        report += '    · 建议每次练习时长：60分钟\n\n';
      } else {
        report += '  阶段一（短期目标，1-2周）：\n';
        report += '    · 每天进行30分钟基础柔韧性训练，重点拉伸腿部、肩部和髋部\n';
        report += '    · 分解练习每个基础动作，感受正确姿态\n';
        report += '    · 建议每次练习时长：30分钟\n\n';
        report += '  阶段二（中期目标，3-4周）：\n';
        report += '    · 每天进行45分钟舞蹈基础训练\n';
        report += '    · 从最简单的舞蹈片段开始，逐步增加动作复杂度\n';
        report += '    · 建议每次练习时长：45分钟\n\n';
        report += '  阶段三（长期目标，1个月以上）：\n';
        report += '    · 每周至少进行4次舞蹈练习，逐步建立肌肉记忆\n';
        report += '    · 坚持记录练习视频，对比进步并持续改进\n';
        report += '    · 建议每次练习时长：60分钟\n\n';
      }

      report += '  【辅助训练建议】\n';
      report += '  · 力量训练：每周进行2-3次核心力量训练，提升身体稳定性\n';
      report += '  · 柔韧性训练：每天练习前进行10-15分钟全身拉伸\n';
      report += '  · 视频对比：建议每周录制2-3次练习视频，与标准舞蹈反复对比\n';
      report += '  · 镜子练习：利用全身镜进行练习，实时观察自身姿态\n';
      report += '  · 呼吸配合：注意动作与呼吸的协调，避免憋气导致动作僵硬\n\n';

      report += '═══════════════════════════════════════════════════════════════════\n';
      report += '【五、科学健身知识小贴士】\n';
      report += '═══════════════════════════════════════════════════════════════════\n\n';
      report += '  1. 热身的重要性\n';
      report += '    运动前进行5-10分钟热身（如快走、开合跳）可以：\n';
      report += '    · 提高肌肉温度，增加关节活动范围\n';
      report += '    · 减少运动损伤风险，提升动作表现\n';
      report += '    · 帮助身体更快进入运动状态\n\n';
      report += '  2. 正确的呼吸节奏\n';
      report += '    · 发力时呼气，收力时吸气\n';
      report += '    · 避免憋气，这会导致血压升高和动作僵硬\n';
      report += '    · 保持呼吸平稳，有助于动作的节奏感和流畅度\n\n';
      report += '  3. 运动后的拉伸放松\n';
      report += '    · 练习结束后进行10-15分钟静态拉伸\n';
      report += '    · 每个拉伸动作保持15-30秒，不要弹震\n';
      report += '    · 重点拉伸本次练习中使用较多的关节\n\n';
      report += '  4. 常见错误动作警示\n';
      report += '    · 耸肩：会导致肩部紧张，影响手臂动作表现\n';
      report += '    · 驼背：影响整体姿态，降低舞蹈美感\n';
      report += '    · 膝盖内扣：增加膝关节压力，可能造成运动损伤\n';
      report += '    · 踢腿时腿部不直：影响踢腿高度和视觉效果\n';
      report += '    · 动作过于急促：降低动作准确性，影响节奏感得分\n\n';
      report += '  5. 训练频率建议\n';
      report += '    · 初学者：每周3-4次，每次30-45分钟\n';
      report += '    · 中级水平：每周4-5次，每次45-60分钟\n';
      report += '    · 进阶水平：每周5-7次，每次60分钟以上\n';
      report += '    · 切记给身体留出休息时间，避免过度训练\n\n';

      report += '═══════════════════════════════════════════════════════════════════\n';
      report += '                              报告结束\n';
      report += '═══════════════════════════════════════════════════════════════════\n';
      report += '\n  本报告由舞蹈评分系统自动生成，基于MediaPipe姿态识别技术与动态角度\n';
      report += '标准学习算法。报告内容仅供参考，实际舞蹈水平需结合专业教练指导\n';
      report += '进行综合评估。如有疑问，请咨询专业舞蹈教练或运动康复专家。\n\n';
      report += `  报告生成时间：${dateStr} ${timeStr}\n`;
      report += `  系统版本：Dance Evaluation System v1.0\n`;

      return report;
    },
    downloadReport() {
      if (!this.scoreResult) {
        this.$message.warning('暂无评分数据，无法生成报告');
        return;
      }
      const report = this.generateDanceReport();
      const blob = new Blob([report], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      const safeName = (this.uploadedFilename || 'dance_report').replace(/\.[^/.]+$/, '');
      const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
      link.href = url;
      link.download = `舞蹈评分报告_${safeName}_${timestamp}.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      this.$message.success('报告已成功下载');
    },
    async switchToHistory() { this.contentMode = 'history'; this.historyPage = 1; await this.loadHistoryPage(1); },
    async loadHistoryPage(page) {
      this.historyLoading = true;
      this.historyPage = page;
      try {
        const params = new URLSearchParams({ page, page_size: this.historyPageSize });
        if (this.userId) params.append('user_id', this.userId);
        const response = await axios.get(`/api/annotation/list/?${params.toString()}`, { headers: { Authorization: `Bearer ${this.token}` }, timeout: 10000 });
        if (response.data.code === 200) { this.historyRecords = response.data.data.items || []; this.historyTotal = response.data.data.total || 0; }
        else { this.$message.error(response.data.error || '加载历史失败'); }
      } catch (error) { console.error('加载标注历史失败:', error); this.$message.error('加载历史失败'); }
      finally { this.historyLoading = false; }
    },
    playHistoryRecord(record) { this.historyAnnotationId = record.id; this.showHistoryDialog = true; },
    async clearHistory() {
      if (!confirm('确定要清空所有标注历史吗？此操作不可恢复。')) return;
      try {
        const params = new URLSearchParams(); if (this.userId) params.append('user_id', this.userId);
        const response = await axios.post(`/api/annotation/clear/?${params.toString()}`, {}, { headers: { Authorization: `Bearer ${this.token}` }, timeout: 10000 });
        if (response.data.code === 200) { this.$message.success(`已清空 ${response.data.data.deleted_count} 条记录`); this.historyRecords = []; this.historyTotal = 0; }
        else { this.$message.error(response.data.error || '清空失败'); }
      } catch (error) { this.$message.error('清空历史失败'); }
    },
    reset() {
      this.stopPolling();
      this.phase = 'idle'; this.contentMode = 'upload'; this.taskId = null; this.annotationId = null;
      this.progress = 0; this.processingPhase = 'annotation'; this.processingMessage = ''; this.errorMessage = '';
      this.totalFrames = 0; this.fps = 0; this.duration = 0; this.uploadedFilename = '';
      this.selectedFile = null; this.selectedDance = null; this.videoSrc = '';
      this.scoreResult = null; this.skeletonImages = {}; this.skeletonAngles = {};
      this.skeletonLandmarks = {}; this.currentAngles = null; this.isPreRendering = false;
      this.preRenderProgress = 0; this.currentFrameIndex = 0; this.validFrameCount = 0;
      this.seekbarPercent = 0; this.isPlaying = false; this.currentTime = 0; this.videoDuration = 0;
      this.showHistoryDialog = false; this.historyAnnotationId = null; this.historySearch = '';
      this.showSkeleton = true; this.skeletonOpacity = 0.85; this.skeletonThickness = 2;
      this.fullWidthMode = false; this.colorByQuality = false; this.sidePanelCollapsed = false;
      this.cleanupVideo();
    },
    cleanupVideo() { const video = this.$refs.videoEl; if (video) { video.pause(); video.removeAttribute('src'); video.load(); } },
  },
};
</script>

<style scoped>
.dance-page {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

/* Hero */
.hero-section {
  text-align: center;
  padding: var(--space-2xl) 0 var(--space-lg);
}
.hero-icon {
  width: 32px; height: 32px;
  color: var(--secondary);
  vertical-align: middle;
  margin-right: var(--space-sm);
}
.hero-title {
  font-size: 26px; font-weight: 800; color: var(--text-primary);
  display: inline-flex; align-items: center;
}
.hero-subtitle { font-size: 14px; color: var(--text-secondary); margin-top: var(--space-xs); }

/* Card */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
}
.card-body { padding: var(--space-lg); }

/* Tab Toggle */
.tab-toggle {
  display: flex; justify-content: center; gap: var(--space-sm);
  margin-bottom: var(--space-lg);
  padding: 4px;
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  width: fit-content; margin-left: auto; margin-right: auto;
}
.tab-btn {
  display: flex; align-items: center; gap: var(--space-sm);
  padding: var(--space-sm) var(--space-xl);
  font-size: 14px; font-weight: 500; font-family: var(--font-sans);
  color: var(--text-secondary); background: transparent;
  border: none; border-radius: var(--radius-md); cursor: pointer; transition: var(--transition-fast);
}
.tab-btn svg { width: 16px; height: 16px; }
.tab-btn:hover { color: var(--text-primary); }
.tab-btn.active {
  background: var(--gradient-tech); color: white;
  box-shadow: 0 2px 8px rgba(6, 182, 212, 0.25);
}

/* Upload Zone */
.upload-zone {
  border: 2px dashed var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-2xl);
  background: var(--bg-base);
  text-align: center; cursor: pointer; transition: var(--transition-fast);
  margin-bottom: var(--space-lg);
}
.upload-zone:hover, .upload-zone.drag-over {
  border-color: var(--primary-accent);
  background: rgba(59, 130, 246, 0.02);
}
.upload-zone.file-selected {
  border-color: var(--danger);
  background: rgba(239, 68, 68, 0.02);
}
.upload-icon {
  margin-bottom: var(--space-md);
}
.upload-icon svg { width: 48px; height: 48px; color: var(--text-muted); }
.upload-text { font-size: 15px; color: var(--text-primary); margin-bottom: var(--space-xs); }
.upload-text.file-name { font-weight: 600; color: var(--danger); }
.upload-link { color: var(--primary-accent); font-weight: 600; }
.upload-hint { font-size: 13px; color: var(--text-muted); }
.file-input-hidden { display: none; }

/* Select Group */
.select-group { margin-bottom: var(--space-lg); }
.select-label { display: block; font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: var(--space-sm); }
.select-wrapper { position: relative; }
.select-field {
  width: 100%; padding: 12px var(--space-md); font-size: 14px; font-family: var(--font-sans);
  background: var(--bg-base); border: 1.5px solid var(--border);
  border-radius: var(--radius-md); appearance: none; cursor: pointer; transition: var(--transition-fast);
}
.select-field:focus { border-color: var(--primary-accent); box-shadow: 0 0 0 3px var(--primary-glow); outline: none; }
.select-arrow {
  position: absolute; right: 14px; top: 50%; transform: translateY(-50%);
  width: 16px; height: 16px; color: var(--text-muted); pointer-events: none;
}

/* Action Button */
.action-btn {
  display: inline-flex; align-items: center; justify-content: center; gap: var(--space-sm);
  padding: 12px var(--space-xl); font-size: 14px; font-weight: 500; font-family: var(--font-sans);
  border: none; border-radius: var(--radius-md); cursor: pointer; transition: var(--transition-fast);
}
.action-btn svg { width: 16px; height: 16px; }
.action-btn.primary {
  background: var(--gradient-tech); color: white;
  box-shadow: 0 2px 8px rgba(6, 182, 212, 0.25);
}
.action-btn.primary:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(6, 182, 212, 0.35); }
.action-btn.primary:disabled { opacity: 0.6; cursor: not-allowed; }
.action-btn.full-width { width: 100%; }
.btn-spinner {
  width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite;
}

/* Tip Box */
.tip-box {
  display: flex; align-items: center; gap: var(--space-sm);
  margin-top: var(--space-lg); padding: var(--space-md);
  background: var(--info-light); border-radius: var(--radius-md);
  font-size: 13px; color: var(--info);
}
.tip-box svg { width: 16px; height: 16px; flex-shrink: 0; }

/* History Section */
.history-header {
  display: flex; align-items: center; gap: var(--space-md);
  margin-bottom: var(--space-lg);
}
.back-btn {
  display: flex; align-items: center; gap: var(--space-xs);
  padding: var(--space-xs) var(--space-md); font-size: 13px; font-family: var(--font-sans);
  color: var(--text-secondary); background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius-md); cursor: pointer; transition: var(--transition-fast);
}
.back-btn svg { width: 14px; height: 14px; }
.back-btn:hover { border-color: var(--primary-accent); color: var(--primary-accent); }
.history-title { font-size: 16px; font-weight: 600; color: var(--text-primary); }

/* Loading / Empty */
.loading-state, .empty-state {
  text-align: center; padding: var(--space-3xl);
}
.empty-state svg { width: 64px; height: 64px; margin-bottom: var(--space-md); opacity: 0.4; color: var(--text-muted); }
.empty-state p { font-size: 16px; font-weight: 500; color: var(--text-secondary); margin-bottom: var(--space-xs); }
.empty-state span { font-size: 13px; color: var(--text-muted); }
.spinner {
  width: 36px; height: 36px; margin: 0 auto var(--space-md);
  border: 3px solid var(--border); border-top-color: var(--primary-accent);
  border-radius: 50%; animation: spin 0.8s linear infinite;
}

/* Search Bar */
.search-bar {
  display: flex; align-items: center; gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md); background: var(--bg-card);
  border: 1px solid var(--border); border-radius: var(--radius-lg);
  margin-bottom: var(--space-lg);
}
.search-icon { width: 16px; height: 16px; color: var(--text-muted); flex-shrink: 0; }
.search-input {
  flex: 1; border: none; background: transparent; font-size: 14px; font-family: var(--font-sans);
  color: var(--text-primary); outline: none;
}
.search-clear { padding: 4px; background: none; border: none; cursor: pointer; color: var(--text-muted); }
.search-clear svg { width: 14px; height: 14px; }
.search-clear:hover { color: var(--text-primary); }
.record-count { font-size: 12px; color: var(--text-muted); white-space: nowrap; }
.clear-btn {
  padding: 4px 12px; font-size: 12px; font-family: var(--font-sans);
  background: transparent; border: 1px solid var(--danger); color: var(--danger);
  border-radius: var(--radius-md); cursor: pointer; transition: var(--transition-fast);
}
.clear-btn:hover { background: var(--danger-light); }

/* Record List */
.record-list { display: flex; flex-direction: column; gap: var(--space-md); }
.record-card {
  display: flex; background: var(--bg-card); border: 1px solid var(--border-light);
  border-radius: var(--radius-lg); overflow: hidden; cursor: pointer;
  transition: var(--transition-base);
}
.record-card:hover { border-color: var(--primary-accent); box-shadow: var(--shadow-md); transform: translateY(-2px); }
.card-preview { width: 160px; flex-shrink: 0; position: relative; background: #000; }
.preview-video { width: 100%; height: 100px; object-fit: cover; }
.play-overlay {
  position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  background: rgba(0,0,0,0.4); opacity: 0; transition: var(--transition-fast);
}
.record-card:hover .play-overlay { opacity: 1; }
.play-overlay svg { width: 32px; height: 32px; color: white; }
.card-info { flex: 1; padding: var(--space-md); display: flex; flex-direction: column; gap: var(--space-xs); min-width: 0; }
.filename { font-size: 14px; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin: 0; }
.stats-tags { display: flex; gap: var(--space-xs); flex-wrap: wrap; }
.stat-tag {
  padding: 2px 8px; font-size: 11px; background: var(--primary-glow);
  color: var(--primary-accent); border-radius: var(--radius-full); font-weight: 500;
}
.card-footer { display: flex; justify-content: space-between; align-items: center; margin-top: auto; }
.time { font-size: 12px; color: var(--text-muted); }
.view-link { font-size: 12px; font-weight: 600; color: var(--primary-accent); }

/* Pagination */
.pagination { display: flex; align-items: center; justify-content: center; gap: var(--space-md); margin-top: var(--space-xl); }
.page-btn {
  padding: var(--space-xs) var(--space-lg); font-size: 13px; font-family: var(--font-sans);
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius-md); cursor: pointer; transition: var(--transition-fast);
}
.page-btn:hover:not(:disabled) { border-color: var(--primary-accent); color: var(--primary-accent); }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.page-info { font-size: 13px; color: var(--text-secondary); }

/* Dialog */
.dialog-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15, 23, 42, 0.7); display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.dialog-box {
  background: var(--bg-card); border-radius: var(--radius-xl);
  width: 960px; max-width: 95vw; max-height: 90vh; overflow-y: auto; box-shadow: var(--shadow-xl);
}
.dialog-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: var(--space-md) var(--space-lg); border-bottom: 1px solid var(--border-light);
}
.dialog-header h3 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 0; }
.dialog-close {
  padding: 4px; background: none; border: none; cursor: pointer; color: var(--text-muted);
  border-radius: var(--radius-sm); transition: var(--transition-fast);
}
.dialog-close svg { width: 18px; height: 18px; }
.dialog-close:hover { color: var(--text-primary); background: var(--bg-base); }

/* Processing Modal */
.processing-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15, 23, 42, 0.8); display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.processing-modal {
  background: var(--bg-card); border-radius: var(--radius-xl);
  padding: var(--space-2xl); width: 480px; max-width: 95vw;
  box-shadow: var(--shadow-xl);
}
.modal-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-lg); }
.modal-title-row { display: flex; align-items: center; gap: var(--space-sm); }
.modal-icon { width: 24px; height: 24px; color: var(--primary-accent); animation: spin 1s linear infinite; }
.modal-header h2 { font-size: 20px; font-weight: 700; color: var(--text-primary); margin: 0; }
.phase-badge {
  padding: 4px 12px; border-radius: var(--radius-full); font-size: 12px; font-weight: 600;
}
.phase-annotation { background: var(--primary-glow); color: var(--primary-accent); }
.phase-scoring { background: rgba(249, 115, 22, 0.1); color: var(--secondary); }
.phase-done { background: var(--success-light); color: var(--success); }

.modal-progress { margin-bottom: var(--space-lg); }
.progress-bar-wrap { display: flex; align-items: center; gap: var(--space-md); margin-bottom: var(--space-sm); }
.progress-bar { flex: 1; height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }
.progress-fill {
  height: 100%; background: var(--gradient-tech); border-radius: 4px;
  transition: width 0.3s;
}
.progress-percent { font-size: 16px; font-weight: 700; color: var(--primary-accent); min-width: 48px; }
.progress-message { font-size: 13px; color: var(--text-secondary); text-align: center; }

.modal-stats {
  display: flex; justify-content: center; gap: var(--space-xl);
  margin-bottom: var(--space-lg); padding: var(--space-md); background: var(--bg-base);
  border-radius: var(--radius-md);
}
.stat-item { text-align: center; }
.stat-label { display: block; font-size: 12px; color: var(--text-muted); }
.stat-value { display: block; font-size: 20px; font-weight: 700; color: var(--text-primary); }

.modal-phases { display: flex; align-items: center; justify-content: center; gap: var(--space-md); margin-bottom: var(--space-lg); }
.phase-step {
  display: flex; flex-direction: column; align-items: center; gap: 4px;
  padding: var(--space-md) var(--space-lg); border-radius: var(--radius-md);
  background: var(--bg-base); min-width: 120px; transition: var(--transition-base);
}
.phase-step.active { background: var(--primary-glow); border: 1px solid rgba(59, 130, 246, 0.2); }
.phase-step.done { background: var(--success-light); border: 1px solid rgba(16, 185, 129, 0.2); }
.step-icon { width: 24px; height: 24px; color: var(--text-muted); }
.step-icon svg { width: 100%; height: 100%; }
.phase-step.active .step-icon { color: var(--primary-accent); }
.phase-step.done .step-icon { color: var(--success); }
.step-name { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.step-desc { font-size: 11px; color: var(--text-muted); }
.phase-arrow { font-size: 20px; color: var(--border); }
.modal-hint { font-size: 12px; color: var(--text-muted); text-align: center; }

/* Result Layout */
.result-layout { display: flex; gap: var(--space-lg); align-items: flex-start; }

/* Player Wrapper */
.player-wrapper { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.player-wrapper.full-width { flex: 1; }

.player-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: var(--space-sm); flex-wrap: wrap; gap: var(--space-sm);
}
.header-info {}
.header-title { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 0; }
.header-meta { font-size: 13px; color: var(--text-muted); }
.header-actions { display: flex; align-items: center; gap: var(--space-sm); }
.pause-hint {
  font-size: 12px; color: var(--primary-accent);
  background: var(--primary-glow); padding: 3px 10px; border-radius: var(--radius-full); font-weight: 500;
}

/* Pre-render Overlay */
.pre-render-overlay {
  background: rgba(255,255,255,0.95); border: 1px solid var(--border-light);
  border-bottom: none; padding: var(--space-lg);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0; text-align: center; color: var(--text-secondary);
}
.pre-render-overlay .spinner { margin: 0 auto var(--space-sm); }
.progress-bar-sm { max-width: 300px; margin: var(--space-sm) auto 0; height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; }
.progress-fill-sm { height: 100%; background: var(--gradient-tech); border-radius: 2px; transition: width 0.2s; }

/* Video Container */
.video-container { position: relative; background: #000; border: 1px solid var(--border-light); border-bottom: none; text-align: center; min-width: 0; }
.video-container.full-width { max-width: 100% !important; }
.render-canvas { display: none; }
.video-layer { display: block; width: 100%; max-width: 1200px; margin: 0 auto; background: #000; }
.skeleton-canvas {
  position: absolute; top: 0; left: 50%; transform: translateX(-50%);
  max-width: 1200px; width: 100%; height: 100%;
  pointer-events: none;
}

/* Skeleton Control Bar */
.skeleton-control-bar {
  display: flex; align-items: center; justify-content: space-between;
  gap: var(--space-sm); padding: var(--space-sm) var(--space-md);
  background: var(--bg-base); border: 1px solid var(--border-light); border-top: none; flex-wrap: wrap;
}
.ctrl-group { display: flex; align-items: center; gap: var(--space-xs); flex-wrap: wrap; }
.ctrl-group.sliders { gap: var(--space-md); }
.ctrl-btn {
  display: flex; align-items: center; gap: 4px;
  padding: 5px 10px; font-size: 12px; font-family: var(--font-sans);
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius-md); cursor: pointer; transition: var(--transition-fast); color: var(--text-secondary);
}
.ctrl-btn svg { width: 14px; height: 14px; }
.ctrl-btn:hover { border-color: var(--primary-accent); color: var(--primary-accent); }
.ctrl-btn.active { background: var(--gradient-tech); color: white; border-color: transparent; }
.ctrl-label { display: flex; align-items: center; gap: var(--space-xs); font-size: 12px; color: var(--text-secondary); white-space: nowrap; }
.ctrl-label input[type="range"] { width: 60px; accent-color: var(--primary-accent); cursor: pointer; }
.ctrl-val { font-size: 11px; font-weight: 600; color: var(--primary-accent); min-width: 30px; }
.speed-select {
  padding: 4px 8px; border: 1px solid var(--border); border-radius: var(--radius-md);
  font-size: 12px; background: var(--bg-card); cursor: pointer; font-family: var(--font-sans);
}

/* Bottom Control Bar */
.bottom-control-bar {
  display: flex; flex-direction: column;
  border: 1px solid var(--border-light); border-top: none; border-radius: 0 0 var(--radius-lg) var(--radius-lg);
  overflow: hidden;
}
.controls-row {
  display: flex; align-items: center; gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md); background: var(--bg-base); flex-wrap: wrap;
}
.ctrl-btn.play-btn { padding: 5px 14px; }
.time-display { font-size: 13px; color: var(--text-secondary); white-space: nowrap; }
.seekbar-wrap { flex: 1; min-width: 80px; cursor: pointer; padding: var(--space-xs) 0; }
.seekbar { position: relative; height: 5px; background: var(--border); border-radius: 3px; }
.seekbar-progress { position: absolute; left: 0; top: 0; height: 100%; background: var(--gradient-tech); border-radius: 3px; transition: width 0.1s; }
.seekbar-thumb {
  position: absolute; top: 50%; transform: translate(-50%, -50%);
  width: 12px; height: 12px; background: var(--primary-accent); border-radius: 50%;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
}
.frame-info-row {
  display: flex; align-items: center; justify-content: center; gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md); background: var(--bg-base);
  border-top: 1px solid var(--border-light); font-size: 12px; color: var(--text-secondary); flex-wrap: wrap;
}
.frame-info-row strong { color: var(--text-primary); }
.sep { color: var(--border); }
.valid-badge { padding: 2px 8px; border-radius: var(--radius-full); font-size: 11px; font-weight: 600; }
.valid-badge.valid { background: var(--success-light); color: var(--success); }
.valid-badge.invalid { background: var(--danger-light); color: var(--danger); }

/* Angle Panel */
.angle-panel {
  width: 360px; flex-shrink: 0; background: var(--bg-card);
  border-radius: var(--radius-lg); border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm); position: sticky; top: var(--space-lg);
  max-height: calc(100vh - 40px); overflow-y: auto; display: flex; flex-direction: column;
  transition: width 0.3s ease; z-index: 10;
}
.angle-panel.collapsed { width: 36px; overflow: visible; }
.panel-collapse-btn {
  position: absolute; top: 50%; right: -20px; transform: translateY(-50%);
  width: 20px; height: 60px; background: var(--gradient-tech); color: white;
  border: none; border-radius: 0 var(--radius-md) var(--radius-md) 0; cursor: pointer;
  font-size: 11px; display: flex; align-items: center; justify-content: center;
  transition: var(--transition-fast);
}
.panel-collapse-btn:hover { background: linear-gradient(135deg, var(--primary-accent), var(--accent)); }
.panel-playing-hint {
  padding: var(--space-xl); text-align: center; color: var(--text-muted); font-size: 14px; background: var(--bg-base);
}
.panel-playing-hint span { background: var(--primary-glow); color: var(--primary-accent); padding: 6px 14px; border-radius: var(--radius-full); font-weight: 500; }
.panel-header { padding: var(--space-md) var(--space-lg); border-bottom: 1px solid var(--border-light); background: var(--gradient-tech); }
.panel-title { font-size: 15px; font-weight: 700; color: white; margin: 0 0 4px; }
.panel-frame-info { font-size: 13px; color: rgba(255,255,255,0.8); }

.frame-jump-bar { display: flex; align-items: center; gap: var(--space-sm); padding: var(--space-sm) var(--space-md); background: var(--bg-base); border-bottom: 1px solid var(--border-light); }
.fjump-btn { padding: 5px 10px; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-sm); cursor: pointer; transition: var(--transition-fast); flex-shrink: 0; }
.fjump-btn svg { width: 14px; height: 14px; color: var(--text-secondary); }
.fjump-btn:hover { border-color: var(--primary-accent); }
.fjump-btn:hover svg { color: var(--primary-accent); }
.fjump-range { flex: 1; }
.fjump-slider { width: 100%; accent-color: var(--primary-accent); cursor: pointer; height: 20px; }

.angle-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-md); padding: var(--space-md); }
.angle-item { padding: var(--space-sm) var(--space-md); border-radius: var(--radius-md); border-left: 4px solid var(--border); transition: var(--transition-fast); }
.angle-item.angle-excellent { background: rgba(16, 185, 129, 0.07); border-left-color: var(--success); }
.angle-item.angle-good { background: rgba(16, 185, 129, 0.04); border-left-color: #69f0ae; }
.angle-item.angle-medium { background: rgba(245, 158, 11, 0.07); border-left-color: var(--warning); }
.angle-item.angle-bad { background: rgba(239, 68, 68, 0.07); border-left-color: var(--danger); }
.angle-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
.angle-joint { font-size: 13px; color: var(--text-secondary); font-weight: 600; }
.angle-value { font-size: 16px; font-weight: 800; color: var(--text-primary); }
.angle-null { color: var(--text-muted); font-size: 13px; }
.angle-bar-bg { height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; margin-bottom: 5px; }
.angle-bar-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }
.bar-excellent { background: var(--success); }
.bar-good { background: #69f0ae; }
.bar-medium { background: var(--warning); }
.bar-bad { background: var(--danger); }
.angle-level-tag { font-size: 12px; padding: 2px 8px; border-radius: var(--radius-full); font-weight: 700; }
.tag-excellent { background: rgba(16,185,129,0.2); color: var(--success); }
.tag-good { background: rgba(16,185,129,0.15); color: #059669; }
.tag-medium { background: rgba(245,158,11,0.2); color: var(--warning); }
.tag-bad { background: rgba(239,68,68,0.2); color: var(--danger); }
.panel-footer { padding: var(--space-sm) var(--space-md); border-top: 1px solid var(--border-light); }
.panel-footer p { font-size: 12px; color: var(--text-muted); text-align: center; margin: 0; }

/* Score Card */
.score-card { padding: var(--space-lg); margin-top: var(--space-lg); }
.score-header { display: flex; align-items: center; justify-content: center; gap: var(--space-lg); margin-bottom: var(--space-sm); flex-wrap: wrap; }
.score-header-actions { display: flex; justify-content: flex-end; margin-bottom: var(--space-lg); }
.score-circle { width: 90px; height: 90px; border-radius: 50%; border: 4px solid; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.score-circle.grade-S { border-color: #ffd700; background: rgba(255,215,0,0.1); }
.score-circle.grade-A { border-color: var(--success); background: var(--success-light); }
.score-circle.grade-B { border-color: var(--primary-accent); background: var(--primary-glow); }
.score-circle.grade-C { border-color: var(--warning); background: var(--warning-light); }
.score-circle.grade-D, .score-circle.grade-E { border-color: var(--danger); background: var(--danger-light); }
.score-num { font-size: 36px; font-weight: 800; color: var(--text-primary); line-height: 1; }
.score-unit { font-size: 12px; color: var(--text-muted); }
.grade-badge { padding: var(--space-sm) var(--space-xl); border-radius: var(--radius-md); font-size: 28px; font-weight: 900; color: white; }
.grade-badge.grade-S { background: linear-gradient(135deg, #ffd700, #ff8c00); }
.grade-badge.grade-A { background: var(--success); }
.grade-badge.grade-B { background: var(--primary-accent); }
.grade-badge.grade-C { background: var(--warning); }
.grade-badge.grade-D, .grade-badge.grade-E { background: var(--danger); }
.score-comment { text-align: center; color: var(--text-secondary); font-size: 15px; width: 100%; }

.download-report-btn {
  display: inline-flex; align-items: center; gap: var(--space-sm);
  padding: var(--space-sm) var(--space-lg); font-size: 13px; font-weight: 600;
  font-family: var(--font-sans); color: var(--primary-accent);
  background: var(--primary-glow); border: 1.5px solid rgba(59, 130, 246, 0.3);
  border-radius: var(--radius-md); cursor: pointer; transition: var(--transition-fast);
}
.download-report-btn svg { width: 16px; height: 16px; }
.download-report-btn:hover {
  background: rgba(59, 130, 246, 0.15); border-color: var(--primary-accent);
  transform: translateY(-1px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.score-bars { margin-bottom: var(--space-lg); }
.score-row { display: flex; align-items: center; gap: var(--space-md); margin-bottom: var(--space-sm); }
.score-row .label { width: 56px; font-size: 13px; color: var(--text-muted); font-weight: 500; }
.bar-wrap { flex: 1; height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.4s; }
.bar-accuracy { background: var(--gradient-tech); }
.bar-rhythm { background: var(--gradient-energy); }
.bar-fluency { background: linear-gradient(90deg, var(--accent), var(--primary-accent)); }
.bar-num { width: 40px; text-align: right; font-size: 13px; font-weight: 600; color: var(--text-secondary); }

/* Joint Section */
.joint-section, .summary-section { margin-top: var(--space-lg); }
.section-subtitle { font-size: 14px; font-weight: 600; color: var(--text-muted); margin-bottom: var(--space-md); }
.joint-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: var(--space-sm); }
.joint-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: var(--space-sm) var(--space-md); border-radius: var(--radius-md);
  background: var(--bg-base); border-left: 3px solid var(--border); transition: var(--transition-fast);
}
.joint-item.joint-excellent { background: rgba(16,185,129,0.07); border-left-color: var(--success); }
.joint-item.joint-good { background: rgba(16,185,129,0.04); border-left-color: #69f0ae; }
.joint-item.joint-medium { background: rgba(245,158,11,0.07); border-left-color: var(--warning); }
.joint-item.joint-bad { background: rgba(239,68,68,0.07); border-left-color: var(--danger); }
.joint-name { font-size: 12px; color: var(--text-secondary); }
.joint-score { font-size: 13px; font-weight: 700; color: var(--text-primary); }

.summary-text {
  background: var(--bg-base); border-left: 3px solid var(--primary-accent);
  border-radius: var(--radius-md); padding: var(--space-md);
  font-size: 13px; color: var(--text-secondary); line-height: 1.8; margin-bottom: var(--space-md);
  white-space: pre-wrap; word-break: break-word;
}
.summary-tips { display: flex; flex-direction: column; gap: var(--space-sm); }
.summary-tip-item {
  padding: var(--space-sm) var(--space-md); border-radius: var(--radius-md);
  border-left: 3px solid var(--border); background: var(--bg-base); transition: var(--transition-fast);
}
.summary-tip-item.tip-excellent { border-left-color: var(--success); background: rgba(16,185,129,0.05); }
.summary-tip-item.tip-good { border-left-color: #69f0ae; background: rgba(16,185,129,0.03); }
.summary-tip-item.tip-medium { border-left-color: var(--warning); background: rgba(245,158,11,0.05); }
.summary-tip-item.tip-bad { border-left-color: var(--danger); background: rgba(239,68,68,0.05); }
.tip-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.tip-joint { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.tip-score-badge { font-size: 11px; font-weight: 700; padding: 2px 6px; border-radius: var(--radius-full); }
.tip-score-badge.tip-excellent { background: rgba(16,185,129,0.15); color: var(--success); }
.tip-score-badge.tip-good { background: rgba(16,185,129,0.1); color: #059669; }
.tip-score-badge.tip-medium { background: rgba(245,158,11,0.15); color: var(--warning); }
.tip-score-badge.tip-bad { background: rgba(239,68,68,0.15); color: var(--danger); }
.tip-bar-wrap { height: 3px; background: var(--border); border-radius: 2px; overflow: hidden; margin: 4px 0; }
.tip-bar-fill { height: 100%; border-radius: 2px; transition: width 0.4s; }
.tip-bar-fill.tip-excellent { background: var(--success); }
.tip-bar-fill.tip-good { background: #69f0ae; }
.tip-bar-fill.tip-medium { background: var(--warning); }
.tip-bar-fill.tip-bad { background: var(--danger); }
.tip-desc { font-size: 12px; color: var(--text-secondary); margin: 0; line-height: 1.5; }

/* Annotation Card */
.annotation-card { padding: var(--space-xl); margin-top: var(--space-lg); }
.annotation-complete { text-align: center; }
.annotation-complete svg { width: 48px; height: 48px; color: var(--success); margin-bottom: var(--space-md); }
.annotation-complete h3 { color: var(--success); font-size: 18px; margin: 0 0 var(--space-sm); }
.annotation-complete p { color: var(--text-secondary); font-size: 14px; margin-bottom: var(--space-xs); }
.hint-small { font-size: 12px !important; color: var(--text-muted) !important; }

/* Error */
.error-section { text-align: center; padding: var(--space-xl); }
.error-card { padding: var(--space-2xl); max-width: 480px; margin: 0 auto; text-align: center; }
.error-icon { width: 48px; height: 48px; color: var(--danger); margin-bottom: var(--space-md); }
.error-card h3 { color: var(--danger); margin: 0 0 var(--space-sm); }
.error-card p { color: var(--text-secondary); font-size: 14px; margin-bottom: var(--space-lg); }
.reset-btn {
  padding: 10px var(--space-xl); font-size: 14px; font-family: var(--font-sans); font-weight: 500;
  background: var(--bg-base); border: 1px solid var(--border); color: var(--text-primary);
  border-radius: var(--radius-md); cursor: pointer; transition: var(--transition-fast);
}
.reset-btn:hover { background: var(--text-primary); color: white; }
.reset-btn-small {
  padding: 4px 12px; font-size: 12px; font-family: var(--font-sans);
  background: var(--bg-base); border: 1px solid var(--border); color: var(--text-secondary);
  border-radius: var(--radius-md); cursor: pointer; transition: var(--transition-fast);
}
.reset-btn-small:hover { border-color: var(--primary-accent); color: var(--primary-accent); }

/* Animations */
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .result-layout { flex-direction: column; }
  .angle-panel { width: 100%; position: static; max-height: none; }
  .angle-panel.collapsed { width: 100%; }
  .panel-collapse-btn { display: none; }
  .card-preview { width: 120px; }
}
</style>
