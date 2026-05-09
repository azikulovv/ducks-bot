import { InlineKeyboard } from 'grammy'

export function gamesKeyboard() {
  return new InlineKeyboard()
    .text('🃏 Покер', 'events:filter:poker')
    .text('🎯 Дартс', 'events:filter:darts')
    .row()
    .text('🎱 Бильярд', 'events:filter:billiards')
    .text('🎮 Все', 'events:filter:all')
}

export function eventNavigationKeyboard(
  eventId: string,
  page: number,
  total: number,
  registered: boolean,
  game?: string,
) {
  const keyboard = new InlineKeyboard()

  /**
   * navigation
   */
  if (game) {
    keyboard
      .text('⬅️', `events:page:${page - 1}:${game}`)
      .text(`${page + 1}/${total}`, 'noop')
      .text('➡️', `events:page:${page + 1}:${game}`)
      .row()
  }

  /**
   * register button
   */
  keyboard.text(
    registered ? '❌ Отписаться' : '✅ Записаться',
    registered ? `events:unregister:${eventId}` : `events:register:${eventId}`,
  )

  /**
   * back button
   */
  keyboard.row().text('⬅️ Назад', 'events:back')

  return keyboard
}
