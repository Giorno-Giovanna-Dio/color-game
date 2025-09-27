import { defineStore } from 'pinia'
import api from '../api/axios'
import type { UserInfo } from '../types'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as UserInfo | null,
    access: localStorage.getItem('access_token'),
  }),
  actions: {
    async googleLogin(googleToken: string): Promise<void> {

      console.log("[auth] googleLogin called with token:", googleToken)
      // 把前端的 Google Token 丟到後端換 JWT
      const { data } = await api.post('/api/google-login/', { token: googleToken })
      console.log("[auth] response:", data)
      
      // 存 JWT
      this.access = data.access
      localStorage.setItem('access_token', data.access)
      if (data.refresh) {
        localStorage.setItem('refresh_token', data.refresh)
      }

      // 存使用者資訊
      this.user = {
        name: data.name,
        email: data.email,
        avatar: data.avatar,
        nickname: data.nickname,
      }
    },
    logout(): void {
      this.user = null
      this.access = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
  },
})