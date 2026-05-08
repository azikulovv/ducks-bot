import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { getRating, Rating } from '../api/ratings.api'

async function sendRating(ctx: any, game: string, title: string) {
  const rating = await getRating(game)

  const text = rating
    .map((player: Rating, index: number) => `${index + 1}. ${player.user.name} — ${player.points}`)
    .join('\n')

  await ctx.reply(`🏆 ${title}\n\n${text}`)
}

export function registerRatingsHandler(bot: Bot<BotContext>) {
  bot.command('ratingpoker', (ctx) => sendRating(ctx, 'poker', 'Рейтинг по покеру'))

  bot.command('ratingdart', (ctx) => sendRating(ctx, 'darts', 'Рейтинг по дартсу'))

  bot.command('ratingbill', (ctx) => sendRating(ctx, 'billiards', 'Рейтинг по бильярду'))
}
