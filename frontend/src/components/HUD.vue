<template>
  <div class="hud flex flex-col items-center gap-4">
    <!-- 使用者資訊卡片 -->
    <div v-if="auth.user" class="card w-96 bg-base-200 shadow-xl p-4">
      <div class="flex items-center gap-3">
        <img :src="auth.user.avatar" alt="avatar" class="w-12 h-12 rounded-full" />
        <div>
          <p class="font-bold">{{ auth.user.nickname || "尚未設定暱稱" }}</p>
        </div>
      </div>
      <div v-if="!auth.user.nickname" class="mt-3 flex gap-2">
        <input v-model="nickname" placeholder="輸入遊戲暱稱" class="input input-bordered input-sm flex-1" />
        <button @click="saveNickname" class="btn btn-accent btn-sm">確認</button>
      </div>
    </div>

    <!-- Google 登入按鈕 -->
    <div v-else class="card w-96 bg-base-200 shadow-xl p-4">
      <div id="googleBtn" class="flex justify-center"></div>
    </div>

    <!-- 遊戲控制卡片 -->
    <div class="card w-96 bg-base-200 shadow-xl p-6 text-center">
      <button 
        v-if="!game.started && !game.finished" 
        @click="start" 
        class="btn btn-soft btn-accent btn-wide btn-lg"
      >
        🚀 Start Game
      </button>

      <div v-if="game.started" class="mt-4">
        <p class="text-lg">Level {{ game.level }} / 13</p>
        <p class="text-sm opacity-80">Grid: {{ game.gridSize }}×{{ game.gridSize }}</p>
        <p class="mt-2 text-xl font-bold">⏱ {{ formatMs(game.elapsedTotalMs) }}</p>
      </div>

      <div v-if="game.finished" class="mt-4">
        <h2 class="text-2xl font-bold text-accent">🎉 遊戲完成！</h2>
        <p class="mt-2">你的總用時：{{ formatMs(game.elapsedTotalMs) }}</p>
        <button @click="restart" class="btn btn-secondary btn-wide mt-4">🔄 Restart</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" >
declare const google: any
import { ref, onMounted } from "vue"
import { useGameStore } from "../stores/game"
import { useAuthStore } from "../stores/auth"
import api from "../api/axios"

const game = useGameStore()
const auth = useAuthStore()
const nickname = ref("")

const start = () => game.startRun()
const restart = () => {
  game.finished = false
  game.results = []
  start()
}

async function saveNickname() {
  if (!auth.user) return
  const { data } = await api.post("/api/set-nickname/", {
    nickname: nickname.value,
    avatar: auth.user.avatar,
  }, {
    headers: { Authorization: `Bearer ${auth.access}` }
  })
  auth.user.nickname = data.nickname
  auth.user.avatar = data.avatar
}

function formatMs(ms: number): string {
  const sec = Math.floor(ms / 1000)
  const min = Math.floor(sec / 60)
  const s = sec % 60
  const m = String(min).padStart(2, "0")
  const ss = String(s).padStart(2, "0")
  const ms100 = String(Math.floor((ms % 1000) / 100)).padStart(1, "0")
  return `${m}:${ss}.${ms100}`
}

onMounted(() => {
  // 定義 callback
  (window as any).handleGoogleCallback = (response: any) => {
    const token = response.credential
    auth.googleLogin(token)
  }

  // 初始化 Google Identity Services
  google.accounts.id.initialize({
    client_id: "319505686194-2126ipcp4b7094l6og1np8qks7agg2d3.apps.googleusercontent.com", // 換成你的 Client ID
    callback: (window as any).handleGoogleCallback,
  })

  // 在 #googleBtn 上渲染一顆按鈕
  google.accounts.id.renderButton(
    document.getElementById("googleBtn"),
    { theme: "outline", size: "large" }
  )
})
</script>