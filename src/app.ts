import express from 'express'
import { bot } from './bot'
import { env } from './config/env'
import { startEventReminderJob } from './jobs/eventReminder.job'
import { internalNotificationsRouter } from './routes/internal-notifications.route'

async function bootstrap() {
  const app = express()

  app.use(express.json())

  app.get('/health', (req, res) => {
    res.json({
      ok: true,
      service: 'ducks-bot',
    })
  })

  app.use('/internal/notifications', internalNotificationsRouter)

  startEventReminderJob()

  app.listen(env.PORT, '0.0.0.0', () => {
    console.log(`Internal API listening on port ${env.PORT}`)
  })

  await bot.start({
    onStart: (botInfo) => {
      console.log(`🦆 DUCK’S bot started as @${botInfo.username}`)
    },
  })
}

bootstrap().catch((error) => {
  console.error('BOOTSTRAP_ERROR:', error)
  process.exit(1)
})
