export const EventGameType = {
  billiards: 'billiards',
  mafia: 'mafia',
  quiz: 'quiz',
  poker: 'poker',
  darts: 'darts',
} as const

export type EventGameType = (typeof EventGameType)[keyof typeof EventGameType]

export const EventGameFilter = {
  ...EventGameType,
  all: 'all',
} as const

export type EventGameFilter = (typeof EventGameFilter)[keyof typeof EventGameFilter]

export const EventGameStatus = {
  published: 'published',
  cancelled: 'cancelled',
  draft: 'draft',
} as const

export type EventGameStatus = (typeof EventGameStatus)[keyof typeof EventGameStatus]

export type Event = {
  id: string
  city: string
  endsAt: null
  status: EventGameStatus
  address: string
  features: string
  gameType: EventGameType
  gameRules: string
  startsAt: string
  imageUrl: string
  imageHash: string
  participantLimit: number
  _count: { registrations: number }
}

/**
 *  API types
 */
export type GetEventsParams = Partial<{
  status: EventGameStatus
  gameType: EventGameType
}>

export type GetEventsResponse = {
  data: Event[]
}

export type RegistrationCheckEventParams = {
  eventId: string
  telegramUserId: string
}

export type RegistrationCheckEventResponse = {}

export type RegisterToEventPayload = RegistrationCheckEventParams

export type RegisterToEventResponse = {}

export type UnregisterFromEventPayload = RegistrationCheckEventParams

export type UnregisterFromEventResponse = {}
