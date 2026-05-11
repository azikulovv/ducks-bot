import { Bot } from 'grammy'
import { env } from './config/env'
import { BotContext } from './types/context'

import { authMiddleware } from './middlewares/auth.middleware'

import { registerStartHandler } from './handlers/start.handler'
import { registerEventsHandler } from './handlers/events/events.handler'
import { registerRatingsHandler } from './handlers/ratings.handler'
import { registerRulesHandler } from './handlers/rules.handler'
import { registerSupportHandler } from './handlers/support.handler'
import { registerFeedbackHandler } from './handlers/feedback/feedback.handler'
import { NotificationService } from './services/notification.service'

export const bot = new Bot<BotContext>(env.BOT_TOKEN)
export const notificationService = new NotificationService(bot)

authMiddleware(bot)

registerStartHandler(bot)
registerRulesHandler(bot)
registerSupportHandler(bot)
registerEventsHandler(bot)
registerRatingsHandler(bot)
registerFeedbackHandler(bot)

bot.catch((error) => {
  console.error('GLOBAL_BOT_ERROR:', error)
})
