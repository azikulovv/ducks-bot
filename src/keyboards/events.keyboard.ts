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

  /**
   * Dynamic buttons
   */
  const isFirstPage = page === 0

  const isLastPage = page === total - 1

  /**
   * PREV
   */
  keyboard.text(
    isFirstPage ? '⏺' : '◀️',
    isFirstPage ? 'noop' : createCallback('events', 'page', String(page - 1), game),
  )

  /**
   * PAGE INFO
   */
  keyboard.text(`${page + 1}/${total}`, 'noop')

  /**
   * NEXT
   */
  keyboard.text(
    isLastPage ? '⏺' : '▶️',
    isLastPage ? 'noop' : createCallback('events', 'page', String(page + 1), game),
  )

  keyboard.row()

  /**
   * REGISTER BUTTON
   */
  if (registered) {
    keyboard.text('❌ Отписаться', createCallback('events', 'unregister', String(eventId)))
  } else {
    keyboard.text('✅ Записаться', createCallback('events', 'register', String(eventId)))
  }

  return keyboard
}
