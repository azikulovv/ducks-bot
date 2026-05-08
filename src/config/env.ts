import dotenv from 'dotenv'

dotenv.config()

export const env = {
  BOT_TOKEN: process.env.BOT_TOKEN!,
  API_URL: process.env.API_URL!,
  MINI_APP_URL: process.env.MINI_APP_URL!,
  API_TOKEN: process.env.API_TOKEN!,
}
