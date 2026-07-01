<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item
      v-for="(item, index) in breadcrumbList"
      :key="item.path"
      :to="index < breadcrumbList.length - 1 ? item.path : undefined"
    >
      <!-- 修改这一行 -->
      {{ (item.meta && item.meta.title) || item.name }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script>
export default {
  data() {
    return {
      breadcrumbList: [],
    };
  },
  watch: {
    $route: {
      immediate: true,
      handler(route) {
        this.updateBreadcrumb(route);
      },
    },
  },
  methods: {
    updateBreadcrumb(route) {
      let matched = route.matched.filter(
        (item) => item.meta?.title || item.name
      );
      this.breadcrumbList = matched.map((item) => ({
        path: item.path,
        name: item.meta?.title || item.name,
        meta: item.meta,
      }));
    },
  },
};
</script>
<style scoped></style>
