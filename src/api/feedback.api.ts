import { api } from './client'
import type { SendFeedbackPayload, SendFeedbackResponse } from '../types/api/feedback'

export async function sendFeedback(payload: SendFeedbackPayload) {
  return api.post<SendFeedbackResponse, SendFeedbackPayload>(`/bot/feedback`, payload)
}
