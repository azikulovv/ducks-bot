import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { openAppKeyboard } from '../keyboards/common.keyboard'

export function registerStartHandler(bot: Bot<BotContext>) {
  bot.command('start', async (ctx) => {
    await ctx.reply(
      `
🦆 Добро пожаловать в DUCK’S Club

Доступные команды:

/events
/ratingpoker
/ratingdart
/ratingbill
/rules
/support
`,
      {
        reply_markup: openAppKeyboard(),
      },
    )
  })
}
