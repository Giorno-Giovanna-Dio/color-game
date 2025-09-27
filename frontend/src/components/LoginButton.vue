<template>
  <GoogleLogin @success="onSuccess" @error="onError" />
</template>

<script setup lang="ts">
import { GoogleLogin } from 'vue3-google-login'
import { useAuthStore } from '../stores/auth'
import api from '../api/axios'

const auth = useAuthStore()

async function onSuccess(resp: any) {
  const googleToken = resp.credential
  const { data } = await api.post('/api/google-login/', { token: googleToken })
  localStorage.setItem('access_token', data.access)
  localStorage.setItem('refresh_token', data.refresh)
  window.location.reload()
  await auth.googleLogin(resp.credential)
}

function onError() {
  console.error('Google login failed')
}
</script>