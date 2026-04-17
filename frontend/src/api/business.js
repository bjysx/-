import http from "./http"

export function getPageSummary(pageCode) {
  return http.get(`/business/pages/${pageCode}/summary/`)
}

export function getPageRecords(pageCode, params) {
  return http.get(`/business/pages/${pageCode}/records/`, { params })
}

export function createRecord(pageCode, payload) {
  return http.post(`/business/pages/${pageCode}/records/`, payload)
}

export function updateRecord(pageCode, recordId, payload) {
  return http.put(`/business/pages/${pageCode}/records/${recordId}/`, payload)
}

export function deleteRecord(pageCode, recordId) {
  return http.delete(`/business/pages/${pageCode}/records/${recordId}/`)
}

export function exportRecords(pageCode, params) {
  return http.get(`/business/pages/${pageCode}/export/`, {
    params,
    responseType: "blob"
  })
}

export function getProductFields() {
  return http.get("/business/products/fields/")
}

export function getProducts(params) {
  return http.get("/business/products/", { params })
}

export function createProduct(payload) {
  return http.post("/business/products/", payload)
}

export function updateProduct(productId, payload) {
  return http.put(`/business/products/${productId}/`, payload)
}

export function deleteProduct(productId) {
  return http.delete(`/business/products/${productId}/`)
}

export function batchDeleteProducts(ids) {
  return http.post("/business/products/batch-delete/", { ids })
}

export function getWorkflows(params) {
  return http.get("/business/workflows/", { params })
}

export function getWorkflowDetail(workflowId) {
  return http.get(`/business/workflows/${workflowId}/`)
}

export function createWorkflow(payload) {
  return http.post("/business/workflows/", payload)
}

export function updateWorkflowStatus(workflowId, payload) {
  return http.post(`/business/workflows/${workflowId}/status/`, payload)
}

export function deleteWorkflow(workflowId) {
  return http.delete(`/business/workflows/${workflowId}/`)
}

export function uploadWorkflowImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  return http.post('/business/workflows/upload-image/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function getSupplierMerchandisers() {
  return http.get("/business/supplier-merchandisers/")
}
