import { Router } from 'express'
import { validate } from '../../middlewares/validate'
import { notificationDataSchema } from './notification.schemas'
import { NotificationController } from './notification.controller'
import { asyncHandler } from '../../utils/async-handler'

export const notificationRoutes = Router()
const controller = new NotificationController()

notificationRoutes.post(
  '/',
  validate({ body: notificationDataSchema }),
  asyncHandler(controller.sendNotification),
)
