import { Bot } from 'grammy'
import { BotContext } from '../types/context'

export function registerRulesHandler(bot: Bot<BotContext>) {
  bot.command('rules', async (ctx) => {
    await ctx.reply(`
📜 Правила клуба DUCK’S

• Уважайте других игроков
• Запрещено токсичное поведение
• Соблюдайте расписание турниров
• Администрация оставляет право модерации
`)
  })
}
