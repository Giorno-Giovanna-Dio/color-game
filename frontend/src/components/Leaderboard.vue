<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getLeaderboard } from "../services/GameService"

// 玩家資料型別
interface LeaderboardRow {
  nickname: string
  best_total_ms: number
  updated_at: string
  avatar: string
}

const rows = ref<LeaderboardRow[]>([])

function formatMs(ms: number): string {
  const sec = Math.floor(ms / 1000)
  const min = Math.floor(sec / 60)
  const s = sec % 60
  const m = String(min).padStart(2, "0")
  const ss = String(s).padStart(2, "0")
  const ms100 = String(Math.floor((ms % 1000) / 100)).padStart(1, "0")
  return `${m}:${ss}.${ms100}`
}

onMounted(async () => {
  rows.value = await getLeaderboard(10) // 只抓前 10 名
})
</script>

<template>
  <div class="leaderboard">
    <h2>🏆 Leaderboard (Top 10)</h2>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Player</th>
          <th>Best Time</th>
          <th>Updated</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, i) in rows" :key="row.nickname">
          <td>{{ i + 1 }}</td>
          <td>{{ row.nickname }}</td>
          <td>{{ formatMs(row.best_total_ms) }}</td>
          <td>{{ new Date(row.updated_at).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.leaderboard {
  margin-top: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th, td {
  padding: 8px 12px;
  border-bottom: 1px solid #ddd;
}

th {
  background: #f8f8f8;
}

tr:hover {
  background: #f1f1f1;
}
</style>