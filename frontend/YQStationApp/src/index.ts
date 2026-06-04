import { createRouter, createWebHistory } from 'vue-router'

import Login from './pages/Login/Login.vue'
import StudentHome from './pages/StudentHome/StudentHome.vue'
import ManagerHome from './pages/ManagerHome/ManagerHome.vue'
import LectureDetail from './pages/LectureDetail/LectureDetail.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Login
    },
    {
      path: '/studenthome',
      component: StudentHome,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/managerhome',
      component: ManagerHome,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/lecture/:id',
      component: LectureDetail,
      meta: {
        requiresAuth: true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('login_token')
  if (to.meta.requiresAuth && !token) {
      next({
        path: '/',
        query:{
          redirect: to.fullPath
        }
      })
      return
  } 
  
  next()
})

export default router