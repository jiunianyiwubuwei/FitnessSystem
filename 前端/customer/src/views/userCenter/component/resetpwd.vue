<template>
  <el-form ref="pwdRef" :model="form" :rules="rules" label-width="80px">
    <el-form-item label="旧密码" prop="oldPassword">
      <el-input
        v-model="form.oldPassword"
        placeholder="请输入旧密码"
        type="password"
        show-password
      />
    </el-form-item>
    <el-form-item label="新密码" prop="newPassword">
      <el-input
        v-model="form.newPassword"
        placeholder="请输入新密码"
        type="password"
        show-password
      />
    </el-form-item>
    <el-form-item label="确认密码" prop="confirmPassword">
      <el-input
        v-model="form.confirmPassword"
        placeholder="请确认密码"
        type="password"
        show-password
      />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="handleSubmit">保存</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import requestUtil from "@/util/request";

export default {
  data() {
    const equalToPassword = (rule, value, callback) => {
      if (this.form.newPassword !== value) {
        callback(new Error("两次输入的密码不一致"));
      } else {
        callback();
      }
    };

    return {
      form: {
        id: null,
        oldPassword: "",
        newPassword: "",
        confirmPassword: "",
      },
      rules: {
        oldPassword: [
          { required: true, message: "旧密码不能为空", trigger: "blur" },
        ],
        newPassword: [
          { required: true, message: "新密码不能为空", trigger: "blur" },
          {
            min: 6,
            max: 20,
            message: "长度在 6 到 20 个字符",
            trigger: "blur",
          },
        ],
        confirmPassword: [
          { required: true, message: "确认密码不能为空", trigger: "blur" },
          { required: true, validator: equalToPassword, trigger: "blur" },
        ],
      },
    };
  },
  created() {
    this.loadUserInfo();
  },
  methods: {
    loadUserInfo() {
      try {
        const userData = JSON.parse(sessionStorage.getItem("userMessage"));
        if (userData && userData.id) {
          this.form.id = userData.id;
          console.log("从sessionStorage加载的用户ID:", this.form.id);
        } else {
          this.$message.warning("未检测到登录信息，请重新登录");
          this.$router.push("/login");
        }
      } catch (e) {
        console.error("解析用户信息失败:", e);
        this.$message.error("用户信息异常");
      }
    },
    handleSubmit() {
      this.$refs.pwdRef.validate((valid) => {
        if (valid) {
          requestUtil
            .post("user/updateUserPwd/", this.form, {
              headers: {
                "Content-Type": "application/json", // 明确指定JSON格式
              },
            })
            .then((result) => {
              const data = result.data;
              if (data.code === 200) {
                this.$message.success("密码修改成功，请重新登录");
                // 设置3秒延迟
                const timer = setTimeout(() => {
                  this.$router.push("/login");
                  clearTimeout(timer); // 清除定时器（可选）
                }, 3000);
                // 可选：添加组件销毁时的清理（防止组件卸载后执行）
                this.$once("hook:beforeDestroy", () => {
                  clearTimeout(timer);
                });
              } else {
                this.$message.error(data.errorInfo);
              }
            })
            .catch((error) => {
              this.$message.error("请求失败");
              console.error(error);
            });
        }
      });
    },
  },
};
</script>

<style scoped></style>
