import { Bot, InlineKeyboard } from 'grammy'
import { BotContext } from '../types/context'
import { RULES_MESSAGE } from '../constants/messages'

export function registerRulesHandler(bot: Bot<BotContext>) {
  bot.command('rules', async (ctx) => {
    await ctx.reply(RULES_MESSAGE, {
      reply_markup: new InlineKeyboard().webApp(
        '📖 Открыть правила',
        `${process.env.MINI_APP_URL}/rules`,
      ),
    })
  })
}
