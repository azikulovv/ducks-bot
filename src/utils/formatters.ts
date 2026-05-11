import type { Event } from '../types/api/event'
import { getGameLabel } from './labels'

export function formatEvent(event: Event) {
  return `
${getGameLabel(event.gameType)}

📅 Дата и время: ${formatDate(event.startsAt, { dateStyle: 'short', timeStyle: 'short' })}
📍 Локация: ${event.address}
👥 Количество участников: ${event.participantLimit}
`
}

export type DateInput = string | number | Date

export type FormatOptions = {
  locale?: string
  dateStyle?: Intl.DateTimeFormatOptions['dateStyle']
  timeStyle?: Intl.DateTimeFormatOptions['timeStyle']
  custom?: Intl.DateTimeFormatOptions
}

/**
 * Универсальный форматтер даты/времени
 */
export function formatDate(input: DateInput, options: FormatOptions = {}): string {
  const { locale = 'ru-RU', dateStyle = 'medium', timeStyle, custom } = options

  const date = new Date(input)

  if (isNaN(date.getTime())) {
    return ''
  }

  const formatter = new Intl.DateTimeFormat(locale, {
    ...(custom || {
      dateStyle,
      ...(timeStyle && { timeStyle }),
    }),
  })

  return formatter.format(date)
}
