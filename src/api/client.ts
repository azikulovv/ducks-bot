import axios from 'axios'
import { env } from '../config/env'

export const api = axios.create({
  baseURL: env.API_URL,
  headers: {
    Authorization: `Bearer ${env.BOT_API_KEY}`,
  },
})
