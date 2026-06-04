import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { ABOUT_MESSAGE } from '../constants/messages'

export function registerAboutHandler(bot: Bot<BotContext>) {
  bot.callbackQuery('about:open', async (ctx) => {
    await ctx.answerCallbackQuery()
    ctx.reply(ABOUT_MESSAGE)
  })
}
