<template>
  <div>
    <el-dropdown>
      <span class="el-dropdown-link">
        <el-avatar shape="square" :size="40" :src="squareUrl"></el-avatar>
        &nbsp;&nbsp;{{ userMessage.username }}
        <i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>
          <router-link :to="{ name: '个人中心' }">个人中心</router-link>
        </el-dropdown-item>
        <el-dropdown-item @click.native="loginOut">安全退出</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
import { getServerUrl } from "@/util/request";
import router from "@/router";

export default {
  name: "Avatar",
  data() {
    const userMessage = JSON.parse(sessionStorage.getItem("userMessage"));
    const squareUrl =
      getServerUrl() + "/media/userAvatar/" + userMessage.avatar;
    return {
      userMessage,
      squareUrl,
    };
  },
  methods: {
    loginOut() {
      window.sessionStorage.clear();
      console.log("退出登录");
      router.replace("/login");
    },
  },
};
</script>

<style scoped lang="scss">
.el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>
