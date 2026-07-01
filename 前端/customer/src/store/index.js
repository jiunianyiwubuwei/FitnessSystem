// store/index.js (修正后)
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    editableTabsValue: '/index',
    editableTabs: [
      {
        title: '首页',
        name: '/index'
      }
    ]
  },
  mutations: {
    ADD_TABS: (state, tab) => {
      if (state.editableTabs.findIndex(e => e.name === tab.path) === -1) {
        state.editableTabs.push({
          title: tab.name,
          name: tab.path
        })
      }
      state.editableTabsValue = tab.path
    },
    RESET_TABS: (state) => {
      state.editableTabsValue = '/index'
      state.editableTabs = [
        {
          title: '首页',
          name: '/index'
        }
      ]
    }
  }
})