import { Bot } from 'grammy'
import { api } from '../api/client'
import { formatDate } from '../utils/formatters'
import { getGameLabel } from '../utils/labels'

export class NotificationService {
  constructor(private bot: Bot) {}

  async sendEventReminder(eventId: string) {
    const res = await api.get(`/events/${eventId}/participants`)

    const { event, participants } = res.data

    for (const participant of participants) {
      await this.bot.api.sendMessage(
        participant.user.telegram_id,
        `🃏 Турнир «${getGameLabel(event.gameType)}» начнётся через 1 час!

📅 Дата и время: ${formatDate(event.startsAt, { dateStyle: 'medium', timeStyle: 'short' })}

⏰ Пожалуйста, приезжайте вовремя — за участие вы можете получить дополнительные бонусы.

📍 Адрес:
${event.address}
Игровое пространство DUCK’S`,
      )
    }
  }

  async sendEventReminder10Min(eventId: string) {
    const res = await api.get(`/events/${eventId}/participants`)

    const { event, participants } = res.data

    for (const participant of participants) {
      const tgId = participant.user.telegram_id

      await this.bot.api.sendMessage(
        tgId,
        `🔥 Турнир «${getGameLabel(event.gameType)}» начинается через 10 минут!

📌 В приложении вы уже можете увидеть своё место за столом.

Не опаздывайте — игра стартует строго по расписанию.`,
      )

      await this.bot.api.sendMessage(
        tgId,
        `⚠️ Если ваши планы изменились — пожалуйста, отмените запись.

Это позволит другим гостям принять участие в турнире.`,
      )
    }
  }
}
