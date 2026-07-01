<template>
    <main>
      <div class="left">
        <h2>实时检测</h2>
        <el-upload
        class="upload-demo"
        drag
        action="https://jsonplaceholder.typicode.com/posts/"
        multiple>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        </el-upload>
      </div>
      <div class="right">
        <!--动态渲染结果至页面-->
        <img :src="imgResult"  class="result" v-if="imgResult">
      </div>
      <div class="footer">
        <ul>
            <li><router-link class="delete" to="/photo">图片检测</router-link></li>
            <li><router-link class="delete" to="/video">视频检测</router-link></li>
            <li><router-link class="delete" to="/camera">实时检测</router-link></li>
        </ul>
        <div class="butt1">
            <el-button class="butt1" @click="startDetection" type="info">开始检测</el-button>
        </div>
    </div>
    </main>
    </template>
    
    <script>
    import axios from 'axios';
  import { Container } from 'element-ui';
    
    export default {
      data() {
        return {
        imgResult: ''
        };
      },
      methods: {
    
      }
    }
    </script>
    
    <style>
  *{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  .left{
    width: 50%;
    height: 600px;
  
    float: left;
    overflow: hidden;
    border: 0.2px solid #d6d0d0;
  }
  .right{
    width: 50%;
    height: 600px;
  
    float: right;
    border: 0.2px solid #d6d0d0;
    overflow: hidden;
  }
  .upload-demo{
    margin-left: 25%;
   margin-top: 180px;
  }
  h2{
    text-align: center;
    margin-top: 20px;
  }
  .result{
    width:500px ;
    height: 500px;
    background-color: blue;
    margin: 0 auto;
    margin-top: 50px;
  }
  main{
    overflow: auto;
  }
  li{
    margin-left: 20px;
    text-align: center;
    list-style: none;
    float: left;
    height: 40px;
    width: 80px;
    line-height: 40px;
}
li:hover{
    background-color: pink;
}
.footer{
  width: 100%;
    overflow: hidden;
}
/* 移除所有 router-link 的下划线 */
.delete{
    text-decoration: none;
}
.butt1{
    position: relative;
    display: inline-block;
   margin-left: 210px;
   margin-top: 2px;
}
  
    </style>