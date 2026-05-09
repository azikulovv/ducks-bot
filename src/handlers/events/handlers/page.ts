import { getEvents, registrationCheckEvent } from '../../../api/events.api'
import { eventNavigationKeyboard } from '../../../keyboards/events.keyboard'
import { formatEvent } from '../../../utils/formatters'
import { BotContext } from '../../../types/context'

export async function page(ctx: BotContext, data: string[]) {
  const requestedPage = Number(data[2])
  const game = data[3]

  const events = await getEvents(game === 'all' ? undefined : game)

  if (!events.length) {
    return ctx.answerCallbackQuery({
      text: 'События не найдены',
    })
  }

  const normalizedPage = Math.max(0, Math.min(requestedPage, events.length - 1))

  const currentPageText = ctx.callbackQuery?.message?.reply_markup?.inline_keyboard?.[0]?.[1]?.text

  const currentPage = currentPageText ? Number(currentPageText.split('/')[0]) - 1 : 0

  if (currentPage === normalizedPage) {
    return ctx.answerCallbackQuery({
      text: normalizedPage === 0 ? 'Это первая страница' : 'Это последняя страница',
    })
  }

  const event = events[normalizedPage]

  await ctx.deleteMessage()

  await ctx.reply(formatEvent(event), {
    reply_markup: eventNavigationKeyboard(event.id, normalizedPage, events.length, false, game),
  })

  await ctx.answerCallbackQuery()
}
