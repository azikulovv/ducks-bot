export const getGameLabel = (type: string) => {
  return (
    {
      poker: '🃏 Покер',
      billiards: '🎱 Бильярд',
      darts: '🎯 Дартс',
    }[type] ?? type
  )
}
