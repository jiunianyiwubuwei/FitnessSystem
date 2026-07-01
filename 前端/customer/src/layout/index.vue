<template>
  <div class="app-wrapper">
    <el-container>
      <el-aside width="200px" class="sidebar-container">
        <Menu></Menu>
      </el-aside>
      <el-container>
        <el-header>
          <Header></Header>
        </el-header>
        <el-main>
          <tabs></tabs>
          <router-view></router-view>
        </el-main>
        <el-footer class="index-footer">
          <Footer></Footer>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from "@/layout/header/index.vue";
import Footer from "@/layout/footer/index.vue";
import Menu from "@/layout/menu/index.vue";
import Tabs from "@/layout/tabs/index.vue";

export default {
  components: {
    Header,
    Footer,
    Menu,
    Tabs,
  },
};
</script>

<style scoped>
.app-wrapper {
  position: relative;
  width: 100%;
  height: 100vh;
}
.sidebar-container {
  background-color: #2d3a4b;
  height: 100%;
}
.el-container {
  height: 100%;
}
.index-footer {
  margin: 0 auto;
  text-align: center;
}
.el-header {
  padding-left: 0px;
  padding-right: 0px;
}
</style>
