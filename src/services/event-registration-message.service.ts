export const EVENT_REGISTRATION_NOTIFICATION_TYPES = [
  'REGISTERED_AS_PARTICIPANT',
  'ADDED_TO_WAITING_LIST',
  'WAITING_LIST_PROMOTED',
] as const

export type EventRegistrationNotificationType =
  (typeof EVENT_REGISTRATION_NOTIFICATION_TYPES)[number]

export type EventRegistrationNotificationPayload = {
  type: EventRegistrationNotificationType
  telegramUserId: number
  eventTitle: string
  eventDate: string
  eventAddress?: string
  waitingPosition?: number
}

function formatEventRegistrationDate(input: string): string {
  const date = new Date(input)

  const parts = new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'UTC',
  }).formatToParts(date)

  const getPart = (type: Intl.DateTimeFormatPartTypes) =>
    parts.find((part) => part.type === type)?.value

  return `${getPart('day')} ${getPart('month')} ${getPart('year')}, ${getPart('hour')}:${getPart('minute')}`
}

function buildDateAndAddressLines(payload: EventRegistrationNotificationPayload) {
  return [
    `📅 Дата и время: ${formatEventRegistrationDate(payload.eventDate)}`,
    payload.eventAddress ? `📍 Адрес: ${payload.eventAddress}` : undefined,
  ].filter(Boolean)
}

export function buildEventRegistrationMessage(
  payload: EventRegistrationNotificationPayload,
): string {
  const dateAndAddressLines = buildDateAndAddressLines(payload).join('\n')

  if (payload.type === 'REGISTERED_AS_PARTICIPANT') {
    return `✅ Вы записаны на турнир «${payload.eventTitle}»

${dateAndAddressLines}

За 15 минут до начала турнира вы сможете узнать своё место за столом.

Найти его можно в личном кабинете mini app в разделе «Мои турниры».`
  }

  if (payload.type === 'ADDED_TO_WAITING_LIST') {
    const waitingPositionLine = payload.waitingPosition
      ? `\n👥 Ваша очередь: №${payload.waitingPosition}`
      : ''

    return `⏳ Вы добавлены в лист ожидания на турнир «${payload.eventTitle}»

${dateAndAddressLines}${waitingPositionLine}

Сейчас все места заняты, но если место освободится, мы автоматически добавим вас в участники.

Когда ваша очередь подойдёт, вы получите уведомление в Telegram.`
  }

  return `🎉 Ваша очередь подошла!

Вы стали участником турнира «${payload.eventTitle}»

${dateAndAddressLines}

За 15 минут до начала турнира вы сможете узнать своё место за столом.

Найти его можно в личном кабинете mini app в разделе «Мои турниры».`
}
