import { Bot } from 'grammy'
import { NotificationData } from './notification.types'

export class NotificationService {
  constructor(private readonly bot: Bot) {}

  async sendNotification(data: NotificationData) {
    await this.bot.api.sendMessage(data.telegramUserId, data.message)
  }
}
