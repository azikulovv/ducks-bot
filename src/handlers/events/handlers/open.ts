import path from 'node:path'
import { Context, InputFile } from 'grammy'
import { gamesKeyboard } from '../../../keyboards/events.keyboard'

export async function open(ctx: Context) {
  await ctx.replyWithPhoto(new InputFile(path.join(process.cwd(), 'assets/logo.jpg')), {
    caption: '🎮 Выберите игру',
    reply_markup: gamesKeyboard(),
  })
}
