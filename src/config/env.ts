import dotenv from 'dotenv'

dotenv.config()

export const env = {
  BOT_TOKEN: process.env.BOT_TOKEN!,
  API_URL: process.env.API_URL!,
  BOT_API_KEY: process.env.BOT_API_KEY!,
  MINI_APP_URL: process.env.MINI_APP_URL!,
}
