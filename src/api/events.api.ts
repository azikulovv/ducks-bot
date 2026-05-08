import { api } from './client'

export async function getEvents(game?: string) {
  const response = await api.get('/events', {
    params: { game },
  })

  return response.data
}
