import cron from 'node-cron'
import { notificationService } from '../bot'
import { api } from '../api/client'

let isRunning = false

export async function startEventReminderJob() {
  cron.schedule('* * * * *', async () => {
    if (isRunning) return

    try {
      const oneHourRes = await api.get(`/events/reminders?type=1h`)
      const oneHourEvents = oneHourRes.data

      for (const event of oneHourEvents) {
        await notificationService.sendEventReminder(event.id)
      }

      const tenMinRes = await api.get(`/events/reminders?type=10m`)
      const tenMinEvents = tenMinRes.data

      for (const event of tenMinEvents) {
        await notificationService.sendEventReminder10Min(event.id)
      }
    } catch (e) {
      console.error('Reminder job error:', e)
    } finally {
      isRunning = false
    }
  })
}
