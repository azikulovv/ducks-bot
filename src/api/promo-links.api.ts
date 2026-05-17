import { api } from './client'

export type TrackTelegramPromoStartPayload = {
  telegramUserId: number | string
  promoCode: string
}

export async function trackTelegramPromoStart(
  payload: TrackTelegramPromoStartPayload,
): Promise<void> {
  try {
    await api.post('/promo-links/telegram-start', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  } catch (error) {
    console.error('PROMO_LINK_TRACK_ERROR:', {
      telegramUserId: payload.telegramUserId,
      promoCode: payload.promoCode,
      error,
    })
  }
}
