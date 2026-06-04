import { EventGameFilter } from '../types/api/event'

export const GAMES: Record<EventGameFilter, string> = {
  [EventGameFilter.poker]: '♠️ Покер',
  [EventGameFilter.darts]: '🎯 Дартс',
  [EventGameFilter.pool]: '🎱 Бильярд',
  [EventGameFilter.mafia]: 'Мафия',
  [EventGameFilter.quiz]: 'Квиз',
  [EventGameFilter.all]: '🎮 Все',
}
