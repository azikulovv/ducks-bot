import { api } from './client'

export async function getUserByTelegramId(telegramId: number) {
  try {
    const response = await api.get(`/users/by-telegram-id/${telegramId}`)

    return response.data
  } catch {
    return null
  }
}
