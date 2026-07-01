//引入axios
import axios from "axios";

let baseUrl="" // 使用代理，相对路径
//创建axios实例
const httpService=axios.create({
    baseURL:baseUrl,
    timeout:3000
})

//请求拦截器
httpService.interceptors.request.use(config=>{
    //在发送请求之前做些什么
    const token = window.sessionStorage.getItem("token")
    // 未登录或 token 为空时不携带 Authorization，避免无意义预检与鉴权异常
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    } else if (config.headers && config.headers.Authorization) {
        delete config.headers.Authorization
    }
    return config
},error=>{
    //对请求错误做些什么
    return Promise.reject(error)
})

//响应拦截器
httpService.interceptors.response.use(response=>{
    //对响应数据做些什么
    return response
},error=>{
    //对响应错误做些什么
    return Promise.reject(error)
})

export function get(url,params={}){
    return new Promise((resolve,reject)=>{
       httpService({
        url:url,
        method:"get",
        params:params
       }).then(res=>{
        resolve(res)   
       }).catch(err=>{
        reject(err)
       })
    })
}


export function post(url,params={}){
    return new Promise((resolve,reject)=>{
       httpService({
        url:url,
        method:"post",
        // POST 请求使用请求体传参，避免参数丢失/跨域预检干扰
        data:params,
       }).then(res=>{
        resolve(res)   
       }).catch(err=>{
        reject(err)
       })
    })
}

export function del(url,params={}){
    return new Promise((resolve,reject)=>{
       httpService({
        url:url,
        method:"delete",
        params:params
       }).then(res=>{
        resolve(res)   
       }).catch(err=>{
        reject(err)
       })
    })
}

export function fileUpload(url,params={}){
    return new Promise((resolve,reject)=>{
       httpService({
        url:url,
        method:"post",
        params:params,
        headers:{
            "Content-Type":"multipart/form-data"
        }
       }).then(res=>{
        resolve(res)   
       }).catch(err=>{
        reject(err)
       })
    })
}


export function getServerUrl(){
    return baseUrl
}

export default {
    get,
    post,
    del,
    fileUpload,
    getServerUrl
}