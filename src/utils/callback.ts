export function createCallback(...parts: string[]) {
  return parts.join(':')
}

export function parseCallback(data: string) {
  return data.split(':')
}
