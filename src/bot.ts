import { Bot } from 'grammy'
import { env } from './config/env'
import { BotContext } from './types/context'

import { authMiddleware } from './middlewares/auth.middleware'

import { registerStartHandler } from './handlers/start.handler'
import { registerEventsHandler } from './handlers/events.handler'
import { registerRatingsHandler } from './handlers/ratings.handler'
import { registerRulesHandler } from './handlers/rules.handler'
import { registerSupportHandler } from './handlers/support.handler'

export const bot = new Bot<BotContext>(env.BOT_TOKEN)

bot.use(authMiddleware)

registerStartHandler(bot)
registerEventsHandler(bot)
registerRatingsHandler(bot)
registerRulesHandler(bot)
registerSupportHandler(bot)

bot.catch((error) => {
  console.error('GLOBAL_BOT_ERROR:', error)
})
