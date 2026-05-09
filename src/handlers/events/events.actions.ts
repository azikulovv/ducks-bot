import { open } from './handlers/open'
import { back } from './handlers/back'
import { filter } from './handlers/filter'
import { page } from './handlers/page'
import { register } from './handlers/register'
import { unregister } from './handlers/unregister'

export const eventsActions = {
  open,
  back,
  filter,
  page,
  register,
  unregister,
}

export type EventsAction = keyof typeof eventsActions
