import { InlineKeyboard } from 'grammy'
import { createCallback } from '../utils/callback'

export function gamesKeyboard() {
  return new InlineKeyboard()
    .text('🎱 Бильярд', createCallback('events', 'filter', 'billiard'))
    .row()
    .text('♠️ Покер', createCallback('events', 'filter', 'poker'))
    .row()
    .text('🎯 Дартс', createCallback('events', 'filter', 'darts'))
    .row()
    .text('🎮 Все', createCallback('events', 'filter', 'all'))
}

export function eventNavigationKeyboard(
  eventId: string,
  page: number,
  total: number,
  registered: boolean,
  game: string,
) {
  const keyboard = new InlineKeyboard()

  keyboard
    .text('◀️', createCallback('events', 'page', String(page - 1), game))
    .text(`${page + 1}/${total}`, 'noop')
    .text('▶️', createCallback('events', 'page', String(page + 1), game))
    .row()

  if (registered) {
    keyboard.text('❌ Отписаться', createCallback('events', 'unregister', String(eventId)))
  } else {
    keyboard.text('✅ Записаться', createCallback('events', 'register', String(eventId)))
  }

  return keyboard.text('◀️ Назад', createCallback('events', 'filter', game)).row()
}
