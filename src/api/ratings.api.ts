import { api } from './client'
import type { GetRatingParams, GetRatingResponse, Rating } from '../types/api/rating'

export async function getRating(params: GetRatingParams): Promise<Rating[]> {
  const response = await api.get<GetRatingResponse>(`/ratings/${params.gameType}`)
  return response.data.data
}
