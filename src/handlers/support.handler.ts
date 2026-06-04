import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { SUPPORT_MESSAGE } from '../constants/messages'

export function registerSupportHandler(bot: Bot<BotContext>) {
  bot.command('support', async (ctx) => {
    await ctx.reply(SUPPORT_MESSAGE, {
      parse_mode: 'HTML',
    })
  })
}
