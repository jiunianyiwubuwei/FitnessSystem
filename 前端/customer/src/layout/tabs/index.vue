<template>
  <el-tabs
    v-model="editableTabsValue"
    type="card"
    class="demo-tabs"
    closable
    @tab-remove="removeTab"
    @tab-click="clicktab"
  >
    <el-tab-pane
      v-for="item in editableTabs"
      :key="item.name"
      :label="item.title"
      :name="item.name"
    >
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import store from "@/store";
import router from "@/router";

export default {
  data() {
    return {
      editableTabsValue: store.state.editableTabsValue,
      editableTabs: store.state.editableTabs,
    };
  },
  methods: {
    removeTab(targetName) {
      const tabs = this.editableTabs;
      let activeName = this.editableTabsValue;

      if (activeName === targetName) {
        tabs.forEach((tab, index) => {
          if (tab.name === targetName) {
            const nextTab = tabs[index + 1] || tabs[index - 1];
            if (nextTab) {
              activeName = nextTab.name;
            }
          }
        });
      }

      this.editableTabsValue = activeName;
      this.editableTabs = tabs.filter((tab) => tab.name !== targetName);
      // 路由到最新激活状态的 tab
      if (this.$router.currentRoute.path !== activeName) {
        router.push({ path: activeName });
      }

      // 同步状态到 Vuex
      store.state.editableTabsValue = this.editableTabsValue;
      store.state.editableTabs = this.editableTabs;
    },
    clicktab(tab) {
      console.log(tab.name);
      if (this.$router.currentRoute.path !== tab.name) {
        router.push({ path: tab.name });
      }
    },
    refreshTabs() {
      this.editableTabs = store.state.editableTabs;
      this.editableTabsValue = store.state.editableTabsValue;
    },
  },
  watch: {
    "$store.state": {
      handler() {
        this.refreshTabs();
      },
      deep: true,
      immediate: true,
    },
  },
};
</script>

<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.el-tabs--card > .el-tabs__header .el-tabs__item.is-active {
  background-color: lightgray;
}

.el-main {
  padding: 0px;
}

.el-tabs__content {
  padding: 0px !important;
}
</style>
