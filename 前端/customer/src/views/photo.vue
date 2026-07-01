<template>
  <div>
    <h1>Upload Video</h1>
    <input type="file" @change="handleFileUpload" />
    <select v-model="exerciseType">
      <option value="push-up">Push-up</option>
      <option value="sit-up">Sit-up</option>
      <option value="squat">Squat</option>
      <option value="pull-up">Pull-up</option>
    </select>
    <button @click="uploadVideo">Upload</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      videoFile: null,
      exerciseType: "push-up",  // 默认运动类型
    };
  },
  methods: {
    handleFileUpload(event) {
      this.videoFile = event.target.files[0];  // 获取上传的文件
    },
    async uploadVideo() {
      if (!this.videoFile) {
        alert("Please select a video file.");
        return;
      }

      const formData = new FormData();
      formData.append('video_file', this.videoFile);  // 将视频文件添加到表单数据中
      formData.append('exercise_type', this.exerciseType);  // 添加运动类型

      try {
        // 发送 POST 请求上传视频
        const response = await this.$axios.post('/api/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',  // 设置正确的 Content-Type
          },
        });
        console.log(response.data);  // 打印响应结果
      } catch (error) {
        console.error("Error uploading video:", error);  // 捕获并处理错误
      }
    },
  },
};
</script>
