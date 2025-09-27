// src/router/index.ts
import { createRouter, createWebHistory} from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { defineAsyncComponent } from 'vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/game-test',
    name: 'GameTest',
    component: defineAsyncComponent(() => import('../views/GameTest.vue')),
  },
  // 其他路由...
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router