<template>
  <el-form ref="userRef" :model="form" :rules="rules" label-width="100px">
    <el-form-item label="手机号码：" prop="phonenumber">
      <el-input v-model="form.phonenumber" maxlength="11" />
    </el-form-item>
    <el-form-item label="用户邮箱：" prop="email">
      <el-input v-model="form.email" maxlength="50" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" :loading="submitting" @click="handleSubmit">
        {{ submitting ? "保存中..." : "保存" }}
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import requestUtil from "@/util/request";

export default {
  name: "Userinfo",
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      submitting: false, // 新增加载状态
      form: {
        id: -1,
        phonenumber: "",
        email: "",
      },
      rules: {
        email: [
          { required: true, message: "邮箱地址不能为空", trigger: "blur" },
          {
            type: "email",
            message: "请输入正确的邮箱地址",
            trigger: ["blur", "change"],
          },
        ],
        phonenumber: [
          { required: true, message: "手机号码不能为空", trigger: "blur" },
          {
            pattern: /^1[3-9]\d{9}$/, // 优化正则表达式
            message: "请输入正确的手机号码",
            trigger: "blur",
          },
        ],
      },
    };
  },
  watch: {
    user: {
      immediate: true,
      deep: true, // 添加深度监听
      handler(newVal) {
        this.form = { ...this.form, ...newVal }; // 合并保留原有字段
      },
    },
  },
  methods: {
    async handleSubmit() {
      try {
        const valid = await this.$refs.userRef.validate();
        if (!valid) return;

        this.submitting = true;
        const token = window.sessionStorage.getItem("token");
        const { data } = await requestUtil.post("user/save/", this.form, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (data.code === 200) {
          this.$message.success(data.msg || "保存成功！");
          // 使用接口返回的最新数据更新存储
          window.sessionStorage.setItem(
            "userMessage",
            JSON.stringify({
              ...this.form,
              ...data.data, // 假设接口返回更新后的数据
            })
          );
          this.$emit("saved"); // 触发保存成功事件
        } else {
          this.$message.error(data.msg || "保存失败");
        }
      } catch (error) {
        console.error("保存请求失败:", error);
        const errorMsg =
          error.response?.data?.msg || error.message || "请求失败，请检查网络";
        this.$message.error(`保存失败: ${errorMsg}`);
      } finally {
        this.submitting = false;
      }
    },
  },
};
</script>
<style lang="scss" scoped></style>
