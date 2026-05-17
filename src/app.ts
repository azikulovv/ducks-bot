import express from 'express'
import { bot } from './bot'
import { env } from './config/env'
import { startEventReminderJob } from './jobs/eventReminder.job'
import { internalNotificationsRouter } from './routes/internal-notifications.route'

async function bootstrap() {
  const app = express()

  app.use(express.json())
  app.use('/internal/notifications', internalNotificationsRouter)

  startEventReminderJob()

  app.listen(env.PORT, () => {
    console.log(`Internal API listening on port ${env.PORT}`)
  })

  await bot.start()
  console.log('🦆 DUCK’S bot started')
}

bootstrap()
