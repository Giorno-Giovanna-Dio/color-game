import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as null | { id: number; username: string; avatar?: string }
  }),
  actions: {
    setUser(user: any) {
      this.user = user
    }
  }
})