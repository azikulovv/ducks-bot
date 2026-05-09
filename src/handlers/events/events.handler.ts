import { Bot } from 'grammy'
import { BotContext } from '../../types/context'

import { parseCallback } from '../../utils/callback'
import { EventsAction, eventsActions } from './events.actions'

export function registerEventsHandler(bot: Bot<BotContext>) {
  bot.command('events', async (ctx) => {
    await eventsActions.open(ctx)
  })

  bot.callbackQuery('noop', async (ctx) => {
    await ctx.answerCallbackQuery()
  })

  bot.callbackQuery(/^events:/, async (ctx) => {
    try {
      const data = parseCallback(ctx.callbackQuery.data)

      const action = data[1] as EventsAction

      const handler = eventsActions[action]

      if (!handler) {
        return ctx.answerCallbackQuery({
          text: 'Unknown action',
        })
      }

      await handler(ctx, data)
    } catch (error) {
      console.error('EVENTS_HANDLER_ERROR:', error)

      await ctx.answerCallbackQuery({
        text: 'Произошла ошибка',
      })
    }
  })
}
