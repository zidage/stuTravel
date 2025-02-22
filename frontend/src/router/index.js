import { createRouter, createWebHistory } from 'vue-router'
//导入组件
import LoginVue from '@/views/Login.vue'
import LayoutVue from '@/views/Layout.vue'
import UserAvatarvue from '@/views/user/UserAvatar.vue'
import UserInfoVue from '@/views/user/UserInfo.vue'
import DiaryManage from '@/views/diary/DiaryManage.vue'
import CommunityVue from '@/views/Community.vue'
import PlanManageVue from '@/views/plan/PlanManage.vue'
import PlanWorkBench from '@/views/plan/PlanWorkBench.vue'
import SelectLocation from '@/views/plan/SelectLocation.vue'
import UserResetPasswordVue from '@/views/user/UserResetPassword.vue'
import ShowDiaryVue from '@/views/diary/ShowDiary.vue'
import ShowPlanVue from '@/views/plan/ShowPlan.vue'
import PlanEditVue from '@/views/plan/PlanEdit.vue'

import { useTokenStore } from '@/stores/token.js';
//定义路由关系
const routes = [
  { path: '/login', component: LoginVue },
  { path: '/home', component: LayoutVue },

  {
    path: '/', component: LayoutVue, redirect: '/home', children: [
      { path: '/user/avatar', component: UserAvatarvue },
      { path: '/user/info', component: UserInfoVue },
      { path: '/user/resetPassword', component: UserResetPasswordVue },
      { path: '/community', component: CommunityVue },
      { path: '/user/diaryManage', component: DiaryManage },
      { path: '/plan/planManagement', component: PlanManageVue },
      { path: '/plan/PlanWorkbench', component: PlanWorkBench },
      { path: '/diary/show', component: ShowDiaryVue },
      { path: '/plan/show', component: ShowPlanVue },
      { path: '/plan/edit', component: PlanEditVue }
    ]
  }
]
//创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

//路由守卫
router.beforeEach((to, from, next) => {
  //判断是否有token
  const tokenStore = useTokenStore()
  const token = tokenStore.token
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})


//导出路由实例
export default router