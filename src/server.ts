import express from 'express'
import { notificationRoutes } from './routes/notification/notification.routes'
import { errorHandler } from './middlewares/error-handler'

export function createApp() {
  const app = express()

  app.use(express.json({ limit: '1mb' }))

  app.get('/health', (_req, res) => {
    res.status(200).json({
      ok: true,
      service: 'ducks-bot',
      message: 'Сервис работает',
      uptime: process.uptime(),
    })
  })

  app.use('/notification', notificationRoutes)

  app.use((_req, res) => {
    res.status(404).json({
      message: 'Маршрут не найден',
    })
  })

  app.use(errorHandler)

  return app
}
