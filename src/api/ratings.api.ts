import { api } from './client'

export async function getRating(game: string) {
  const response = await api.get(`/ratings/${game}`)
  return response.data
}
