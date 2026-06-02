export const getGameLabel = (type: string) => {
  return (
    {
      poker: '🃏 Покер',
      pool: '🎱 Бильярд',
      darts: '🎯 Дартс',
    }[type] ?? type
  )
}
