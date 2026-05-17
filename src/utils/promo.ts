import { env } from '../config/env'
import { BotContext } from '../types/context'

const PROMO_CODE_PATTERN = /^[a-zA-Z0-9_-]{2,64}$/

export function extractStartPayload(ctx: BotContext): string | undefined {
  const text = ctx.message?.text?.trim()

  if (!text) return undefined

  const match = text.match(/^\/start(?:@\w+)?(?:\s+(.+))?$/)
  const payload = match?.[1]?.trim()

  return payload || undefined
}

export function isValidPromoCode(code: string): boolean {
  return PROMO_CODE_PATTERN.test(code)
}

export function buildMiniAppUrl(promoCode?: string): string {
  if (!promoCode) return env.MINI_APP_URL

  const url = new URL(env.MINI_APP_URL)
  url.searchParams.set('promo', promoCode)
  url.searchParams.set('promoSource', 'telegram_bot')

  return url.toString()
}
