import { api } from './client'
import { EventGameStatus } from '../types/api/event'
import type {
  Event,
  GetEventsParams,
  GetEventsResponse,
  RegisterToEventPayload,
  RegisterToEventResponse,
  RegistrationCheckEventParams,
  UnregisterFromEventPayload,
  UnregisterFromEventResponse,
} from '../types/api/event'

export async function getEvents(params?: GetEventsParams): Promise<Event[]> {
  const { data } = await api.get<GetEventsResponse>('/events', {
    params: { status: EventGameStatus.published, ...params },
  })

  return data.data
}

export async function registrationCheckEvent(params: RegistrationCheckEventParams) {
  return api.get(`/bot/events/${params.eventId}/registration`, {
    params: { telegramUserId: params.telegramUserId },
  })
}

export async function registerToEvent(payload: RegisterToEventPayload) {
  return api.post<RegisterToEventResponse, RegisterToEventPayload>(
    `/bot/events/${payload.eventId}/register`,
    payload,
  )
}

export async function unregisterFromEvent(payload: UnregisterFromEventPayload) {
  return api.delete<UnregisterFromEventResponse, UnregisterFromEventPayload>(
    `/bot/events/${payload.eventId}/register`,
    {
      data: payload,
    },
  )
}
