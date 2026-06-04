import type { ErrorRequestHandler } from 'express'
import { ZodError } from 'zod'
import { AppError } from '../errors/app-error'

export const errorHandler: ErrorRequestHandler = (error, _req, res, _next) => {
  if (error instanceof ZodError) {
    return res.status(400).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid request payload',
        details: error.flatten(),
      },
    })
  }

  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      error: { code: error.code, message: error.message, details: error.details },
    })
  }

  console.error(error)
  return res
    .status(500)
    .json({ error: { code: 'INTERNAL_SERVER_ERROR', message: 'Unexpected server error' } })
}
