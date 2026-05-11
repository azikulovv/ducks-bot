export type PaginatedResponse<T> = {
  data: T[]
  meta: {
    page: number
    total: number
    limit: number
    pages: number
  }
}
