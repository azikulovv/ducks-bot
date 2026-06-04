import dotenv from 'dotenv'
import { z } from 'zod'

dotenv.config()

const envSchema = z.object({
  PORT: z.coerce
    .number()
    .int('PORT должен быть целым числом')
    .positive('PORT должен быть положительным числом')
    .default(3000),
  BOT_TOKEN: z.string().min(1, 'BOT_TOKEN обязателен'),
  API_URL: z.string().url('API_URL должен быть корректным URL').optional(),
  MINI_APP_URL: z.string().url('MINI_APP_URL должен быть корректным URL'),
  // BOT_API_KEY: z.string().min(1, 'BOT_API_KEY не должен быть пустым').optional(),
  // INTERNAL_API_TOKEN: z.string().min(1, 'INTERNAL_API_TOKEN не должен быть пустым').optional(),
})

const parsedEnv = envSchema.safeParse(process.env)

if (!parsedEnv.success) {
  console.error('❌ Ошибка в .env файле')
  console.error(parsedEnv.error.format())
  process.exit(1)
}

const data = parsedEnv.data

export const env = {
  PORT: data.PORT,
  BOT_TOKEN: data.BOT_TOKEN,
  API_URL: data.API_URL,
  MINI_APP_URL: data.MINI_APP_URL,
  // BOT_API_KEY: botApiKey,
  // INTERNAL_API_TOKEN: data.INTERNAL_API_TOKEN,
}
