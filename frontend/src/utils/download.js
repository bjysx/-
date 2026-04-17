export function downloadBlob(blob, fileName) {
  const fileBlob = blob instanceof Blob ? blob : new Blob([blob])
  const url = window.URL.createObjectURL(fileBlob)
  const link = document.createElement("a")
  link.href = url
  link.download = fileName
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}
