import { Event } from '../api/events.api'

export function formatEvent(event: Event) {
  return `
${'event.icon'} ${event.gameType}

📅 ${event.startsAt}
📍 ${event.address}
👥 ${event.participantLimit} limit
`
}
