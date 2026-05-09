import { Context } from 'grammy'
import { getEvents } from '../../../api/events.api'
import { eventNavigationKeyboard } from '../../../keyboards/events.keyboard'
import { formatEvent } from '../../../utils/formatters'

export async function filter(ctx: Context, data: string[]) {
  const game = data[2]

  const events = await getEvents(game === 'all' ? undefined : game)

  if (!events.length) {
    return ctx.answerCallbackQuery({
      text: 'События не найдены',
    })
  }

  const page = 0
  const event = events[page]

  await ctx.deleteMessage()

  await ctx.reply(formatEvent(event), {
    reply_markup: eventNavigationKeyboard(event.id, page, events.length, false, game),
  })

  await ctx.answerCallbackQuery()
}
