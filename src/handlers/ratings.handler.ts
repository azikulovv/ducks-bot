import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { getRating } from '../api/ratings.api'

async function sendRating(ctx: any, game: string, title: string) {
  const rating = await getRating(game)

  const text = rating
    .map((player: any, index: number) => `${index + 1}. ${player.name} — ${player.points}`)
    .join('\n')

  await ctx.reply(`🏆 ${title}\n\n${text}`)
}

export function registerRatingsHandler(bot: Bot<BotContext>) {
  bot.command('ratingpoker', (ctx) => sendRating(ctx, 'poker', 'Poker Rating'))

  bot.command('ratingdart', (ctx) => sendRating(ctx, 'darts', 'Darts Rating'))

  bot.command('ratingbill', (ctx) => sendRating(ctx, 'billiard', 'Billiard Rating'))
}
