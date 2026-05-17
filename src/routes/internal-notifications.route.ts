import { Router } from 'express'
import { bot } from '../bot'
import { checkInternalToken } from '../middlewares/internal-token.middleware'
import {
  buildEventRegistrationMessage,
  EVENT_REGISTRATION_NOTIFICATION_TYPES,
  EventRegistrationNotificationPayload,
} from '../services/event-registration-message.service'

export const internalNotificationsRouter = Router()

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function validateEventRegistrationPayload(
  body: unknown,
): { ok: true; data: EventRegistrationNotificationPayload } | { ok: false; error: string } {
  if (!isPlainObject(body)) {
    return { ok: false, error: 'Request body must be a JSON object' }
  }

  const { type, telegramUserId, eventTitle, eventDate, eventAddress, waitingPosition } = body

  if (
    typeof type !== 'string' ||
    !EVENT_REGISTRATION_NOTIFICATION_TYPES.includes(
      type as EventRegistrationNotificationPayload['type'],
    )
  ) {
    return { ok: false, error: 'Invalid type' }
  }

  if (
    typeof telegramUserId !== 'number' ||
    !Number.isInteger(telegramUserId) ||
    telegramUserId <= 0
  ) {
    return { ok: false, error: 'Invalid telegramUserId' }
  }

  if (typeof eventTitle !== 'string' || eventTitle.trim().length === 0) {
    return { ok: false, error: 'Invalid eventTitle' }
  }

  if (typeof eventDate !== 'string' || Number.isNaN(new Date(eventDate).getTime())) {
    return { ok: false, error: 'Invalid eventDate' }
  }

  if (eventAddress !== undefined && typeof eventAddress !== 'string') {
    return { ok: false, error: 'Invalid eventAddress' }
  }

  if (
    waitingPosition !== undefined &&
    (typeof waitingPosition !== 'number' ||
      !Number.isInteger(waitingPosition) ||
      waitingPosition <= 0)
  ) {
    return { ok: false, error: 'Invalid waitingPosition' }
  }

  return {
    ok: true,
    data: {
      type: type as EventRegistrationNotificationPayload['type'],
      telegramUserId,
      eventTitle: eventTitle.trim(),
      eventDate,
      ...(eventAddress?.trim() ? { eventAddress: eventAddress.trim() } : {}),
      ...(waitingPosition ? { waitingPosition } : {}),
    },
  }
}

internalNotificationsRouter.post(
  '/event-registration',
  checkInternalToken,
  async (req, res) => {
    const validation = validateEventRegistrationPayload(req.body)

    if (!validation.ok) {
      return res.status(400).json({ success: false, error: validation.error })
    }

    const { telegramUserId } = validation.data
    const message = buildEventRegistrationMessage(validation.data)

    try {
      await bot.api.sendMessage(telegramUserId, message)

      return res.json({ success: true })
    } catch (error) {
      console.error('EVENT_REGISTRATION_NOTIFICATION_ERROR:', error)

      return res.status(500).json({
        success: false,
        error: 'Failed to send notification',
      })
    }
  },
)
