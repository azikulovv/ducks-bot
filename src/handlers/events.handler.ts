import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { gamesKeyboard, eventNavigationKeyboard } from '../keyboards/events.keyboard'

import { getEvents, registerToEvent, unregisterFromEvent } from '../api/events.api'

import { parseCallback } from '../utils/callback'
import { formatEvent } from '../utils/formatters'

export function registerEventsHandler(bot: Bot<BotContext>) {
  bot.command('events', async (ctx) => {
    await ctx.reply('🎮 Выберите игру', {
      reply_markup: gamesKeyboard(),
    })
  })

  bot.callbackQuery(/^events:/, async (ctx) => {
    const data = parseCallback(ctx.callbackQuery.data)

    const action = data[1]

    if (action === 'filter') {
      const game = data[2]

      const events = await getEvents(game === 'all' ? undefined : game)

      if (!events.length) {
        return ctx.answerCallbackQuery({
          text: 'События не найдены',
        })
      }

      const event = events[0]

      await ctx.editMessageText(formatEvent(event), {
        reply_markup: eventNavigationKeyboard(event.id, 0, events.length, false, game),
      })
    }

    if (action === 'register') {
      if (!ctx.user) {
        return ctx.answerCallbackQuery({
          text: 'Нужно привязать аккаунт',
        })
      }

      const eventId = Number(data[2])

      await registerToEvent(eventId, ctx.user.id)

      await ctx.answerCallbackQuery({
        text: 'Вы записаны',
      })
    }

    if (action === 'unregister') {
      if (!ctx.user) {
        return ctx.answerCallbackQuery({
          text: 'Нужно привязать аккаунт',
        })
      }

      const eventId = Number(data[2])

      await unregisterFromEvent(eventId, ctx.user.id)

      await ctx.answerCallbackQuery({
        text: 'Вы отписались',
      })
    }
  })
}
