import { z } from 'zod'

export const notificationDataSchema = z.object({
  telegramUserId: z.number().min(1),
  message: z.string().min(1).max(3000),
})
