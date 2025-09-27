import { defineStore } from 'pinia'
import api from '../api/axios'
import type { HSL, LevelResult, StartSessionResp, FinishSessionReq } from '../types'

function randomColorHsl(): HSL {
  // 用 HSL 較容易控制「接近但不同」
  const h = Math.floor(Math.random() * 360)
  const s = 60 + Math.floor(Math.random() * 30) // 60–90
  const l = 50 + Math.floor(Math.random() * 20) - 10 // 40–60
  return { h, s, l }
}

function hslToCss({ h, s, l }: HSL): string {
  return `hsl(${h}deg ${s}% ${l}%)`
}

export const useGameStore = defineStore('game', {
  state: () => ({
    level: 1 as number, // 1..8
    gridSize: 3 as number, // 3..10
    oddIndex: 0 as number, // 異色方塊 index
    baseColor: null as HSL | null,
    oddColor: null as HSL | null,
    started: false as boolean,
    startMs: 0 as number,
    elapsedLevelMs: 0 as number,
    sessionId: null as number | null,
    startNonce: '' as string,
    sig: '' as string,
    results: [] as LevelResult[],
    elapsedTotalMs: 0 as number,
    timerHandle: null as number | null,
    finished: false as boolean,
    shake: false as boolean,
  }),
  getters: {
    tiles(state): string[] {
      // 還沒建立顏色前避免空值
      if (!state.baseColor || !state.oddColor) return []
      const n = state.gridSize * state.gridSize
      const arr = Array.from({ length: n }, () => hslToCss(state.baseColor as HSL))
      arr[state.oddIndex] = hslToCss(state.oddColor as HSL)
      return arr
    },
  },
  actions: {
    calcGridSize(level: number): number {
      return Math.min(3 + level - 1, 13) // 1:3 → 8:10
    },
    calcDelta(level: number): { dL: number; dH: number } {
      // 調低難度：差異保持比較大
      const baseL = Math.max(15 - level, 10)   // L 差：10–19
      const baseH = Math.max(40 - 2 * level, 20) // H 差：20–38
      return { dL: baseL, dH: baseH }
    },
    newLevel(): void {
      this.gridSize = this.calcGridSize(this.level)
      const n = this.gridSize * this.gridSize
      this.oddIndex = Math.floor(Math.random() * n)

      const base = randomColorHsl()
      const { dL, dH } = this.calcDelta(this.level)
      const odd: HSL = { ...base }

      // 50% 改 lightness、50% 改 hue
      if (Math.random() < 0.5) {
        const delta = Math.random() < 0.5 ? -dL : dL
        odd.l = Math.max(0, Math.min(100, base.l + delta))
      } else {
        const delta = Math.random() < 0.5 ? -dH : dH
        odd.h = (base.h + delta + 360) % 360
      }

      this.baseColor = base
      this.oddColor = odd
      this.elapsedLevelMs = 0
    },
    async startRun(): Promise<void> {
        try {
            const { data } = await api.post<StartSessionResp>('/api/session/start/')
            this.sessionId = data.session_id
            this.startNonce = data.start_nonce
            this.sig = data.sig
        } catch (err) {
            console.warn('startRun API failed, MOCK mode', err)
            this.sessionId = 0 // 0 表示離線模式
            this.startNonce = 'mock'
            this.sig = 'mock'
        }
        this.level = 1
        this.newLevel()
        this.started = true
        this.startMs = performance.now()

        // 啟動計時器 (每 100ms 更新一次)
        this.timerHandle = window.setInterval(() => {
          this.elapsedTotalMs = Math.floor(performance.now() - this.startMs)
        }, 100)

        },
    async finishRun(): Promise<void> {
        if (this.timerHandle) {
          clearInterval(this.timerHandle)
          this.timerHandle = null
        }
        this.started = false
      },

    async clickTile(index: number): Promise<void> {
        if (!this.started) return
        const correct = index === this.oddIndex
        const end = performance.now()
        const spentBefore = this.results.reduce((a, b) => a + b.elapsed_ms, 0)
        const elapsed = Math.max(0, Math.floor(end - this.startMs) - spentBefore)

        const payload: LevelResult = { level_index: this.level, grid_size: this.gridSize, elapsed_ms: elapsed, correct }
        this.results.push(payload)

        if (this.sessionId) {
            try { await api.post(`/api/session/${this.sessionId}/level`, payload) } catch (e) { console.warn('level API failed', e) }
        }

        if (correct) {
            if (this.level >= 13) {
              // 遊戲結束
              const total = this.results.reduce((a, b) => a + b.elapsed_ms, 0)
              if (this.sessionId) {
                const body: FinishSessionReq = { total_ms: total, start_nonce: this.startNonce, sig: this.sig }
                try { await api.post(`/api/session/${this.sessionId}/finish`, body) } catch (e) { console.warn('finish API failed', e) }
              }
              this.started = false
              this.finished = true
              await this.finishRun()
            } else {
              this.level++
              this.newLevel()
            }
          } else {
            // ❌ 答錯的處理方式 (目前是停在同一關)
            // 例如：顯示錯誤提示 / 框閃紅色 / 扣分
            this.shake = true
            setTimeout(() => { this.shake = false }, 300) 
            console.warn("答錯了，重試本關")
          }
        },
  },
})