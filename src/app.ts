import { bot } from './bot'

async function bootstrap() {
  await bot.start()
  console.log('🦆 DUCK’S bot started')
}

bootstrap()
