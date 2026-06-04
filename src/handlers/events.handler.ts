import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { getEvents } from '../api/events.api'
import { EVENTS_MESSAGE } from '../constants/messages'
import { eventsListKeyboard } from '../keyboards/events.keyboard'

async function eventsListCallback(ctx: BotContext) {
  const events = await getEvents()

  const filteredEvents = events
    .filter((event) => new Date(event.startsAt).getTime() >= Date.now())
    .sort((a, b) => new Date(a.startsAt).getTime() - new Date(b.startsAt).getTime())
    .slice(0, 3)

  await ctx.reply(EVENTS_MESSAGE, {
    reply_markup: eventsListKeyboard(filteredEvents),
  })
}

export function registerEventsHandler(bot: Bot<BotContext>) {
  bot.command('events', eventsListCallback)
  bot.callbackQuery('events:list', async (ctx) => {
    await ctx.answerCallbackQuery()
    await eventsListCallback(ctx)
  })
}
