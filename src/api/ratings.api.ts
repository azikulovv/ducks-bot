import { api } from './client'

export type Rating = {
  id: string
  userId: string
  gameType: string
  points: number
  createdAt: string
  updatedAt: string
  user: { id: string; email: string; name: string }
}

export type GetRatingResponse = {
  data: Rating[]
  meta: { total: number; page: number; limit: number; pages: number }
}

export async function getRating(game: string) {
  const response = await api.get<GetRatingResponse>(`/ratings/${game}`)
  return response.data.data
}
