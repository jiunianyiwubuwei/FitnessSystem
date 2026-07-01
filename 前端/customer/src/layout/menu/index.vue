<template>
  <div>
    <el-menu
      :default-active="'/index'"
      class="el-menu-vertical-demo"
      background-color="#2d3a4b"
      text-color="#fff"
      router
      active-text-color="#ffd04b"
    >
      <el-menu-item
        index="/index"
        @click="openTab({ name: '首页', path: '/index' })"
      >
        <el-icon>
          <!-- 填充图标 -->
        </el-icon>
        <span>首页</span>
      </el-menu-item>

      <el-submenu v-for="menu in menuList" :key="menu.id" :index="menu.path">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span>{{ menu.name }}</span>
        </template>
        <el-menu-item
          v-for="item in menu.children"
          :key="item.id"
          :index="item.path"
          @click="openTab(item)"
        >
          {{ item.name }}
        </el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
import store from "@/store";

export default {
  data() {
    return {
      menuList: JSON.parse(sessionStorage.getItem("menuList")) || [],
    };
  },
  methods: {
    openTab(item) {
      store.commit("ADD_TABS", item);
    },
  },
};
</script>
<style lang="scss" scoped></style>
