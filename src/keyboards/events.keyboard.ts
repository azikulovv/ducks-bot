import { env } from '../config/env'
import { InlineKeyboard } from 'grammy'
import { formatDate } from '../utils/formatters'
import type { Event } from '../types/api/event'

export function eventsListKeyboard(events: Event[]) {
  const keyboard = new InlineKeyboard()

  events.forEach((event) => {
    const date = formatDate(event.startsAt, {
      dateStyle: 'short',
      timeStyle: 'short',
    })

    keyboard.webApp(`🃏 ${date} — ${event.title}`, `${env.MINI_APP_URL}/events/${event.id}`).row()
  })

  keyboard
    .url('📢 Канал DUCK’S', 'https://t.me/ducks_poker')
    .webApp('🚀 Смотреть событии', env.MINI_APP_URL)

  return keyboard
}
