import { Bot } from 'grammy'
import { BotContext } from '../types/context'

import { gamesKeyboard, eventNavigationKeyboard } from '../keyboards/events.keyboard'

import { getEvents, registerToEvent, unregisterFromEvent } from '../api/events.api'

import { parseCallback } from '../utils/callback'
import { formatEvent } from '../utils/formatters'

export function registerEventsHandler(bot: Bot<BotContext>) {
  bot.command('events', async (ctx) => {
    await ctx.reply('🎮 Выберите игру', {
      reply_markup: gamesKeyboard(),
    })
  })

  bot.callbackQuery('noop', async (ctx) => {
    await ctx.answerCallbackQuery()
  })

  bot.callbackQuery(/^events:/, async (ctx) => {
    try {
      const callbackData = ctx.callbackQuery.data

      console.log('CALLBACK:', callbackData)

      const data = parseCallback(callbackData)

      console.log('PARSED:', data)

      const action = data[1]

      /**
       * FILTER EVENTS
       *
       * events:filter:poker
       */
      if (action === 'filter') {
        const game = data[2]

        const events = await getEvents(game === 'all' ? undefined : game)

        if (!events.length) {
          return ctx.answerCallbackQuery({
            text: 'События не найдены',
          })
        }

        const page = 0

        const event = events[page]

        await ctx.editMessageText(formatEvent(event), {
          reply_markup: eventNavigationKeyboard(event.id, page, events.length, true, game),
        })

        await ctx.answerCallbackQuery()
      }

      /**
       * PAGINATION
       *
       * events:page:1:poker
       */
      if (action === 'page') {
        const requestedPage = Number(data[2])

        const game = data[3]

        const events = await getEvents(game === 'all' ? undefined : game)

        if (!events.length) {
          return ctx.answerCallbackQuery({
            text: 'События не найдены',
          })
        }

        /**
         * Normalize page
         */
        const normalizedPage = Math.max(0, Math.min(requestedPage, events.length - 1))

        /**
         * Current page from message
         */
        const currentPageText =
          ctx.callbackQuery.message?.reply_markup?.inline_keyboard?.[0]?.[1]?.text

        const currentPage = currentPageText ? Number(currentPageText.split('/')[0]) - 1 : 0

        /**
         * Prevent identical update
         */
        if (currentPage === normalizedPage) {
          return ctx.answerCallbackQuery({
            text: normalizedPage === 0 ? 'Это первая страница' : 'Это последняя страница',
          })
        }

        const event = events[normalizedPage]

        await ctx.editMessageText(formatEvent(event), {
          reply_markup: eventNavigationKeyboard(
            event.id,
            normalizedPage,
            events.length,
            true,
            game,
          ),
        })

        await ctx.answerCallbackQuery()
      }

      /**
       * REGISTER
       *
       * events:register:15
       */
      if (action === 'register') {
        if (!ctx.user) {
          return ctx.answerCallbackQuery({
            text: 'Нужно привязать аккаунт',
          })
        }

        const eventId = Number(data[2])

        await registerToEvent(eventId, ctx.user.id)

        await ctx.answerCallbackQuery({
          text: '✅ Вы записаны',
        })
      }

      /**
       * UNREGISTER
       *
       * events:unregister:15
       */
      if (action === 'unregister') {
        if (!ctx.user) {
          return ctx.answerCallbackQuery({
            text: 'Нужно привязать аккаунт',
          })
        }

        const eventId = Number(data[2])

        await unregisterFromEvent(eventId, ctx.user.id)

        await ctx.answerCallbackQuery({
          text: '❌ Вы отписались',
        })
      }
    } catch (error) {
      console.error('EVENTS_HANDLER_ERROR:', error)

      await ctx.answerCallbackQuery({
        text: 'Произошла ошибка',
      })
    }
  })
}
