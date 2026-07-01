<template>
  <el-form
    ref="formRef"
    :model="form"
    label-width="100px"
    style="text-align: center; padding-bottom: 10px"
  >
    <el-upload
      name="avatar"
      :headers="headers"
      class="avatar-uploader"
      :action="serverUrl + 'user/uploadImage'"
      :show-file-list="false"
      :on-success="handleAvatarSuccess"
      :before-upload="beforeAvatarUpload"
    >
      <img v-if="imageUrl" :src="imageUrl" class="avatar" />
      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
    </el-upload>
    <el-button @click="handleConfirm">确认更换</el-button>
  </el-form>
</template>

<script>
import { getServerUrl } from "@/util/request";
import requestUtil from "@/util/request";

export default {
  props: {
    user: {
      type: Object,
      default: () => ({}),
      required: true,
    },
  },
  data() {
    return {
      serverUrl: getServerUrl(),
      headers: {
        Authorization: sessionStorage.getItem("token"),
      },
      form: {
        id: -1,
        avatar: "",
      },
      imageUrl: "",
    };
  },
  created() {
    this.initForm();
  },
  watch: {
    user: {
      immediate: true,
      handler(newVal) {
        this.form = { ...newVal };
        this.imageUrl = this.serverUrl + "media/userAvatar/" + newVal.avatar;
      },
    },
  },
  methods: {
    initForm() {
      this.form = { ...this.user };
      this.imageUrl = this.serverUrl + "media/userAvatar/" + this.user.avatar;
    },
    handleAvatarSuccess(res) {
      this.imageUrl = this.serverUrl + "media/userAvatar/" + res.title;
      this.form.avatar = res.title;
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error("图片必须是jpg格式");
      }
      if (!isLt2M) {
        this.$message.error("图片大小不能超过2M!");
      }
      return isJPG && isLt2M;
    },
    async handleConfirm() {
      try {
        const result = await requestUtil.post("user/updateAvatar", this.form);
        if (result.data.code === 200) {
          this.$message.success("执行成功！");
        } else {
          this.$message.error(result.data.errorInfo);
        }
      } catch (error) {
        this.$message.error("请求失败，请检查网络连接");
      }
    },
  },
};
</script>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 120px;
  height: 120px;
  display: block;
}
</style>
