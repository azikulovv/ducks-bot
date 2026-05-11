import type { PaginatedResponse } from './index'
import type { EventGameType } from './event'

export type Rating = {
  id: string
  userId: string
  points: number
  gameType: EventGameType
  createdAt: string
  updatedAt: string
  user: {
    id: string
    name: string
    email: string
  }
}

export type GetRatingParams = {
  gameType: EventGameType
}

export type GetRatingResponse = PaginatedResponse<Rating>
