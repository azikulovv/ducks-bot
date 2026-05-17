import type { NextFunction, Request, Response } from 'express'
import { env } from '../config/env'

export function checkInternalToken(req: Request, res: Response, next: NextFunction) {
  const token = req.header('x-internal-token')

  if (!env.INTERNAL_API_TOKEN || token !== env.INTERNAL_API_TOKEN) {
    return res.status(401).json({ success: false, error: 'Unauthorized' })
  }

  return next()
}
