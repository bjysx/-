import request from "./http"

/**
 * 获取员工关系列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getEmployeeRelations(params) {
  return request({
    url: "/user/employee-relations/",
    method: "get",
    params
  })
}

/**
 * 获取员工关系详情
 * @param {string} id - 员工关系ID
 * @returns {Promise}
 */
export function getEmployeeRelationDetail(id) {
  return request({
    url: `/user/employee-relations/${id}/`,
    method: "get"
  })
}

/**
 * 创建员工关系
 * @param {Object} data - 员工关系数据
 * @returns {Promise}
 */
export function createEmployeeRelation(data) {
  return request({
    url: "/user/employee-relations/",
    method: "post",
    data
  })
}

/**
 * 更新员工关系
 * @param {string} id - 员工关系ID
 * @param {Object} data - 员工关系数据
 * @returns {Promise}
 */
export function updateEmployeeRelation(id, data) {
  return request({
    url: `/user/employee-relations/${id}/`,
    method: "put",
    data
  })
}

/**
 * 删除员工关系
 * @param {string} id - 员工关系ID
 * @returns {Promise}
 */
export function deleteEmployeeRelation(id) {
  return request({
    url: `/user/employee-relations/${id}/`,
    method: "delete"
  })
}

/**
 * 批量删除员工关系
 * @param {Array} ids - 员工关系ID列表
 * @returns {Promise}
 */
export function batchDeleteEmployeeRelations(ids) {
  return request({
    url: "/user/employee-relations/batch-delete/",
    method: "post",
    data: { ids }
  })
}

/**
 * 导出员工关系数据
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function exportEmployeeRelations(params) {
  return request({
    url: "/user/employee-relations/export/",
    method: "get",
    params,
    responseType: "blob"
  })
}

/**
 * 导入员工关系数据
 * @param {FormData} formData - 包含文件的表单数据
 * @returns {Promise}
 */
export function importEmployeeRelations(formData) {
  return request({
    url: "/user/employee-relations/import/",
    method: "post",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}
