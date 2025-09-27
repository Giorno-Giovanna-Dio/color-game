import api from '../api/axios'

export async function startSession() {
  const { data } = await api.post('/api/session/start/')
  return data // { session_id, start_nonce, sig }
}

export async function submitLevel(sessionId: number, payload: {
  level_index: number
  grid_size: number
  elapsed_ms: number
  correct: boolean
}) {
  const { data } = await api.post(`/api/session/${sessionId}/level`, payload)
  return data // { ok: true }
}

export async function finishSession(sessionId: number, payload: {
  total_ms: number
  start_nonce: string
  sig: string
}) {
  const { data } = await api.post(`/api/session/${sessionId}/finish`, payload)
  return data // { ok: true }
}

export async function getLeaderboard(limit = 10) {
  try {
    const { data } = await api.get(`/api/leaderboard/?limit=${limit}`)
    return data
  } catch (e) {
    console.warn("Leaderboard API failed", e)
    return []
  }
}