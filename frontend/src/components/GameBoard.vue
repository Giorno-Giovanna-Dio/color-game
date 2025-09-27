<script setup lang="ts">
import { computed } from 'vue'
import { useGameStore } from '../stores/game'
const game = useGameStore()

// 可以統一控制格子大小
const tileSize = 45 // ✅ 原本 64px → 改小一點

const gridStyle = computed(() => ({
  display: 'grid',
  gap: '6px',
  gridTemplateColumns: `repeat(${game.gridSize}, ${tileSize}px)`
}))
</script>

<template>
  <div v-if="game.started" class="board" 
    :class="{ shake: game.shake }"
    :style="gridStyle">
    <div
      v-for="(c, i) in game.tiles"
      :key="i"
      class="tile"
      :style="{ 
        background: c, 
        width: tileSize + 'px', 
        height: tileSize + 'px', 
        borderRadius: '6px', 
        cursor: 'pointer' 
      }"
      @click="game.clickTile(i)"
    />
  </div>
  <div v-else>按 Start 開始一關！</div>
</template>

<style scoped>
.tile {
  border-radius: 6px;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.tile:hover {
  transform: scale(1.15);
  z-index: 1;
}

/* 🔹 shake 效果 */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-5px); }
  40% { transform: translateX(5px); }
  60% { transform: translateX(-5px); }
  80% { transform: translateX(5px); }
}

.board.shake .tile {
  animation: shake 0.4s;
}
</style>