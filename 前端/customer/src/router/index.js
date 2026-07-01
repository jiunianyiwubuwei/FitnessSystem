import Vue from "vue"
import VueRouter from "vue-router"
import store from "@/store"
Vue.use(VueRouter)

const routers=[

    {
        path:'/login',
        component:()=>import('../views/login/login.vue')
    },
    {
        path:'/register',
        component:()=>import('../views/register/register.vue')
    },
    {
        path: '/main',
        component: ()=>import('../views/user/main.vue'),
        meta: { role: 'user',
            requiresAuth: true
         },
         redirect: '/main/health/news',
        children: [
            {
                path: 'health/news/:id',
                component: () => import('../views/user/components/NewDetail.vue') // 健康资讯详情页
              },
            {
              path: 'health/news',
              component: () => import('../views/user/components/HealthNews.vue') // 健康资讯列表页
            },
            {
                path: 'health/checkin',
              component: () => import('../views/user/components/CheckIn.vue') //
            },
            {
                path:'/has',
                component:()=>import('../views/healthAssistans/index.vue')
            },
            {

                path:'health/fitness',
                component:()=>import('../views/user/components/Fitness.vue')
            },
            {

                path:'health/myUser',
                component:()=>import('../views/user/components/UserCenter.vue')
            },
            {
                path:'health/dance-score',
                component:()=>import('../views/user/components/DanceScoreWithAnnotation.vue')
            },
          ]
    },
    {
        path:'/admin',
        component:()=>import('../layout/index.vue'),
        name:'管理员主页',
        meta: {
            tabTitle: '用户管理' ,
            role: 'admin',
            requiresAuth: true
        },
        children:[
            {
                path:'/index',
                component:()=>import('@/views/main/index.vue'),
                name:'首页'
            },
            {
                path:'/sys/user',
                component:()=>import('../views/sys/user/index.vue'),
                name:'用户管理' ,
                meta: {
                    tabTitle: '用户管理' // 新增 meta 字段
                  }
            },
            {
                path:'/sys/role',
                component:()=>import('../views/sys/role/index.vue'),
                name:'角色管理',
                meta: {
                    tabTitle: '角色管理' // 新增 meta 字段
                  }
            },
            {
                path:'/userCenter',
                component:()=>import('../views/userCenter/index.vue'),
                name:'个人中心',
                meta: {
                    tabTitle: '个人中心' // 新增 meta 字段
                  }
            }
        ]
    },


    {
        path:'/camera',
        component:()=>import('../views/camera.vue')
    },
    // 必须放在最后：否则会先于 /main、/admin 匹配，导致登录后永远被重定向回登录页
    {
        path: "*",
        redirect: "/login"
    }


]
const router = new VueRouter({
    routes:routers,
    mode: 'history'
})


router.beforeEach((to, from, next) => {
    const token = sessionStorage.getItem("token"); // 获取 Token

    if (to.matched.some(record => record.meta.requiresAuth) && !token) {
      next("/login"); // 未登录，跳转到登录页
    } else {
      next(); // 允许访问
    }
  });
export default router

