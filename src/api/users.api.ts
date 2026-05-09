import { api } from './client'

export async function getUserByTelegramId(telegramId: number) {
  try {
    const response = await api.get(`/users/by-telegram-id/${telegramId}`)

    return response.data
  } catch {
    return null
  }
}

export async function createUser(data: { telegram_id: string; name?: string | null }) {
  const res = await api.post(`/users`, data)

  return res.data
}
