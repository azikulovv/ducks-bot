import { api } from './client'

export async function sendFeedback(payload: { message: string; telegramUserId: string }) {
  return api.post(`/bot/feedback`, payload)
}
