import { bot } from './bot'
import { env } from './config/env'
import { createApp } from './server'
import { startEventReminderJob } from './jobs/eventReminder.job'

async function bootstrap() {
  const app = createApp()

  app.listen(env.PORT, '0.0.0.0', () => {
    console.log(`Внутренний API запущен на порту ${env.PORT}`)
  })

  await bot.start({
    onStart: (botInfo) => {
      console.log(`🦆 Бот DUCK’S запущен как @${botInfo.username}`)
    },
  })

  startEventReminderJob()
}

bootstrap().catch((error) => {
  console.error('ОШИБКА_ЗАПУСКА:', error)
  process.exit(1)
})
