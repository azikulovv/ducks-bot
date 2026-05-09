import { api } from './client'

export type Event = {
  id: string
  imageUrl: string
  imageHash: string
  address: string
  gameType: string
  startsAt: string
  endsAt: null
  participantLimit: number
  pointsForParticipation: number
  status: string
  createdAt: string
  updatedAt: string
  _count: { registrations: number }
}

type GetEventsResponse = {
  data: Event[]
}

export async function getEvents(game?: string): Promise<Event[]> {
  const response = await api.get<GetEventsResponse>('/events', {
    params: {
      gameType: game,
      status: 'published',
    },
  })

  return response.data.data
}

export async function registerToEvent(eventId: string, userId: string) {
  return api.post(`/bot/events/${eventId}/register`, {
    eventId: eventId,
    telegramUserId: userId,
  })
}

export async function unregisterFromEvent(eventId: string, userId: string) {
  return api.delete(`/bot/events/${eventId}/register`, {
    data: {
      telegramUserId: userId,
      eventId: eventId,
    },
  })
}

export async function registrationCheckEvent(eventId: string, userId: string) {
  return api.get(`/bot/events/${eventId}/registration`, { params: { telegramUserId: userId } })
}
