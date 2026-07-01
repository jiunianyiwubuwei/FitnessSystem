const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  lintOnSave: false,
  transpileDependencies: true,
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/health': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/user': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/menu': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/role': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/api2': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  chainWebpack(config) {
    // 清除默认的svg规则
    config.module
      .rule('svg')
      .exclude.add(path.resolve(__dirname, 'src/icons/svg')) // 排除icons目录
      .end()

    // 添加新的svg处理规则
    config.module
      .rule('icons')
      .test(/\.svg$/)
      .include.add(path.resolve(__dirname, 'src/icons/svg')) // 指定icons目录
      .end()
      .use('svg-sprite-loader')
      .loader('svg-sprite-loader')
      .options({
        symbolId: 'icon-[name]' // 定义symbolId格式
      })
      .end()
      .before('svg-sprite-loader') // 确保在其他loader之前处理
      .use('svgo-loader') // 可选：添加SVG优化
      .loader('svgo-loader')
      .options({
        plugins: [
          { removeTitle: true },          // 移除<title>标签
          { removeDimensions: true },     // 移除width/height属性
          { removeAttrs: { attrs: 'fill' } } // 移除fill属性（可选）
        ]
      })
  }
})