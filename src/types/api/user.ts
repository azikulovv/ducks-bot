export interface TelegramUser {
  id: number
  email: string
  telegramId: string
}

export type GetUserByTelegramIdParams = {
  telegramUserId: number
}

export type GetUserByTelegramIdResponse = TelegramUser
