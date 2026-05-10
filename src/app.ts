import { bot } from './bot'
import { startEventReminderJob } from './jobs/eventReminder.job'

async function bootstrap() {
  startEventReminderJob()

  await bot.start()
  console.log('🦆 DUCK’S bot started')
}

bootstrap()
