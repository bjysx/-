export function formatCurrency(value) {
  const amount = Number(value || 0)
  return new Intl.NumberFormat("zh-CN", {
    style: "currency",
    currency: "CNY",
    minimumFractionDigits: 2
  }).format(amount)
}

export function formatDate(value) {
  if (!value) {
    return "-"
  }
  return new Date(value).toLocaleDateString("zh-CN")
}

export function formatDateTime(value) {
  if (!value) {
    return "-"
  }
  return new Date(value).toLocaleString("zh-CN", {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}
