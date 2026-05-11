import { getEvents, registrationCheckEvent } from '../../../api/events.api'
import { eventNavigationKeyboard } from '../../../keyboards/events.keyboard'
import { formatEvent } from '../../../utils/formatters'
import { BotContext } from '../../../types/context'
import { EventGameFilter } from '../../../types/api/event'

export async function filter(ctx: BotContext, data: string[]) {
  const game = data[2] as EventGameFilter

  const events = await getEvents({ gameType: game === EventGameFilter.all ? undefined : game })

  if (!events.length) {
    return ctx.answerCallbackQuery({
      text: 'События не найдены',
    })
  }

  const page = 0
  const event = events[page]

  const registration = await registrationCheckEvent({
    eventId: event.id,
    telegramUserId: ctx.user?.telegramId!,
  })

  await ctx.deleteMessage()

  await ctx.reply(formatEvent(event), {
    reply_markup: eventNavigationKeyboard(
      event.id,
      page,
      events.length,
      registration.data?.status !== 'cancelled',
      game,
    ),
  })

  await ctx.answerCallbackQuery()
}
