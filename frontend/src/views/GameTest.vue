<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { startSession, submitLevel, finishSession, getLeaderboard } from '../services/GameService'

const leaderboard = ref<any[]>([])

onMounted(async () => {
  leaderboard.value = await getLeaderboard()
})

async function playDemo() {
  const { session_id, start_nonce, sig } = await startSession()

  // 假裝玩 3 關
  await submitLevel(session_id, { level_index: 1, grid_size: 3, elapsed_ms: 1200, correct: true })
  await submitLevel(session_id, { level_index: 2, grid_size: 4, elapsed_ms: 1500, correct: true })
  await submitLevel(session_id, { level_index: 3, grid_size: 5, elapsed_ms: 2000, correct: false })

  // 結束遊戲
  await finishSession(session_id, { total_ms: 4700, start_nonce, sig })

  leaderboard.value = await getLeaderboard()
}
</script>

<template>
  <div>
    <h1>Game API Test</h1>
    <button @click="playDemo">Run Demo Session</button>

    <h2>Leaderboard</h2>
    <ul>
      <li v-for="row in leaderboard" :key="row.username">
        {{ row.username }} — {{ row.best_total_ms }}ms
      </li>
    </ul>
  </div>
</template>