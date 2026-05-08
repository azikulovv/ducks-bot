import { Bot } from 'grammy'
import { BotContext } from '../types/context'

export function registerSupportHandler(bot: Bot<BotContext>) {
  bot.command('support', async (ctx) => {
    await ctx.reply(`
📞 Поддержка

Telegram:
@ducks_support

Телефон:
+7 777 777 77 77
`)
  })
}
