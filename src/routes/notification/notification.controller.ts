import { bot } from '../../bot'
import { NotificationService } from './notification.service'
import type { Request, Response } from 'express'

export class NotificationController {
  private readonly notificationService = new NotificationService(bot)

  sendNotification = async (req: Request, res: Response) => {
    try {
      await this.notificationService.sendNotification(req.body)

      res.status(200).json({ success: true })
    } catch (error) {
      console.error('NOTIFICATION_CONTROLLER_ERROR:', error)

      return res.status(500).json({
        success: false,
        error: 'Не удалось отправить уведомление пользователю telegram',
      })
    }
  }
}
