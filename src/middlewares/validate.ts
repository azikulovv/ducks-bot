import type { NextFunction, Request, Response } from 'express'
import type { ZodTypeAny } from 'zod'

type Schemas = {
  body?: ZodTypeAny
  query?: ZodTypeAny
  params?: ZodTypeAny
}

export const validate =
  (schemas: Schemas) =>
  (req: Request, _res: Response, next: NextFunction): void => {
    if (schemas.body) req.body = schemas.body.parse(req.body) as any
    if (schemas.query) req.query = schemas.query.parse(req.query) as any
    if (schemas.params) req.params = schemas.params.parse(req.params) as any
    next()
  }
