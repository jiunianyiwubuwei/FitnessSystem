<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="box-card">
          <template v-slot:header>
            <div class="clearfix">
              <span>个人信息</span>
            </div>
          </template>
          <div>
            <div class="text-center">
              <avatar :user="userMessage" />
            </div>
            <ul class="list-group list-group-striped">
              <li class="list-group-item">
                <svg-icon icon="user" />&nbsp;&nbsp;用户名称
                <div class="pull-right">{{ userMessage.username }}</div>
              </li>
              <li class="list-group-item">
                <svg-icon icon="phone" />&nbsp;&nbsp;手机号码
                <div class="pull-right">{{ userMessage.phonenumber }}</div>
              </li>
              <li class="list-group-item">
                <svg-icon icon="email" />&nbsp;&nbsp;用户邮箱
                <div class="pull-right">{{ userMessage.email }}</div>
              </li>
              <li class="list-group-item">
                <svg-icon icon="peoples" />&nbsp;&nbsp;所属角色
                <div class="pull-right">{{ userMessage.roles }}</div>
              </li>
              <li class="list-group-item">
                <svg-icon icon="date" />&nbsp;&nbsp;创建日期
                <div class="pull-right">{{ userMessage.login_date }}</div>
              </li>
            </ul>
          </div>
        </el-card>
      </el-col>
      <el-col :span="18">
        <el-card>
          <template v-slot:header>
            <div class="clearfix">
              <span>基本资料</span>
            </div>
          </template>
          <el-tabs v-model="activeTab">
            <el-tab-pane label="基本资料" name="userinfo">
              <userinfo :user="userMessage" />
            </el-tab-pane>
            <el-tab-pane label="修改密码" name="resetPwd">
              <Resetpwd />
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Avatar from "./component/avatar.vue";
import Resetpwd from "./component/resetpwd.vue";
import Userinfo from "./component/userinfo.vue";
export default {
  name: "UserProfile",
  components: { Avatar, Resetpwd, Userinfo },
  data() {
    return {
      userMessage: JSON.parse(sessionStorage.getItem("userMessage") || "{}"),
      activeTab: "userinfo",
    };
  },
  mounted() {
    // 添加空对象保护
    if (!this.currentUser) {
      this.currentUser = {
        username: "",
        phonenumber: "",
        email: "",
        login_date: "",
      };
    }
  },
};
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.list-group-striped > .list-group-item {
  border-left: 0;
  border-right: 0;
  border-radius: 0;
  padding-left: 0;
  padding-right: 0;
}

.list-group-item {
  border-bottom: 1px solid #e7eaec;
  border-top: 1px solid #e7eaec;
  margin-bottom: -1px;
  padding: 11px 0;
  font-size: 13px;
}

.pull-right {
  float: right !important;
}

// Vue 2深度选择器写法
::v-deep .el-card__body {
  height: 60%;
}

::v-deep .box-card {
  height: 450px;
}

.text-center {
  text-align: center;
  margin-bottom: 15px;
}
</style>
