import { api } from './client'
import type { GetUserByTelegramIdParams, GetUserByTelegramIdResponse } from '../types/api/user'

export async function getUserByTelegramId(params: GetUserByTelegramIdParams) {
  try {
    const response = await api.get<GetUserByTelegramIdResponse>(
      `/users/by-telegram-id/${params.telegramUserId}`,
    )
    return response.data
  } catch {
    return null
  }
}
