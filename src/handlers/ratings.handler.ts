import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { getRating } from '../api/ratings.api'
import { Rating } from '../types/api/rating'
import type { EventGameType } from '../types/api/event'

async function sendRating(ctx: any, game: EventGameType, title: string) {
  const rating = await getRating({ gameType: game })

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
