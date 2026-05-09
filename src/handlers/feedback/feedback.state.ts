const feedbackUsers = new Set<string>()

export function startFeedback(userId: string) {
  feedbackUsers.add(userId)
}

export function stopFeedback(userId: string) {
  feedbackUsers.delete(userId)
}

export function isFeedbackMode(userId: string) {
  return feedbackUsers.has(userId)
}
