import { z } from 'zod'
import { notificationDataSchema } from './notification.schemas'

export type NotificationData = z.infer<typeof notificationDataSchema>
