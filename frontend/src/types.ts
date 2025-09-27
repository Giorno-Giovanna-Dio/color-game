// 共用資料型別

export interface StartSessionResp {
  session_id: number
  start_nonce: string
  sig: string
}

export interface LevelResult {
  level_index: number
  grid_size: number
  elapsed_ms: number
  correct: boolean
}

export interface FinishSessionReq {
  total_ms: number
  start_nonce: string
  sig: string
}

export interface LeaderboardRow {
  username: string
  best_total_ms: number
  updated_at: string // ISO datetime
}

// 基礎色彩型別
export type HSL = { h: number; s: number; l: number }

// 使用者（依你後端而定，先給最小形）
export interface UserInfo {
  name?: string
  email?: string
  avatar?: string
  nickname?: string 
}