import request from "./http"

/**
 * 获取招聘需求汇总列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getRecruitmentRequirements(params) {
  return request({
    url: "/user/recruitment-requirements/",
    method: "get",
    params
  })
}

/**
 * 获取招聘需求详情
 * @param {string} id - 需求ID
 * @returns {Promise}
 */
export function getRecruitmentRequirementDetail(id) {
  return request({
    url: `/user/recruitment-requirements/${id}/`,
    method: "get"
  })
}

/**
 * 创建招聘需求
 * @param {Object} data - 招聘需求数据
 * @returns {Promise}
 */
export function createRecruitmentRequirement(data) {
  return request({
    url: "/user/recruitment-requirements/",
    method: "post",
    data
  })
}

/**
 * 更新招聘需求
 * @param {string} id - 需求ID
 * @param {Object} data - 招聘需求数据
 * @returns {Promise}
 */
export function updateRecruitmentRequirement(id, data) {
  return request({
    url: `/user/recruitment-requirements/${id}/`,
    method: "put",
    data
  })
}

/**
 * 删除招聘需求
 * @param {string} id - 需求ID
 * @returns {Promise}
 */
export function deleteRecruitmentRequirement(id) {
  return request({
    url: `/user/recruitment-requirements/${id}/`,
    method: "delete"
  })
}

/**
 * 批量删除招聘需求
 * @param {Array} ids - 需求ID列表
 * @returns {Promise}
 */
export function batchDeleteRecruitmentRequirements(ids) {
  return request({
    url: "/user/recruitment-requirements/batch-delete/",
    method: "post",
    data: { ids }
  })
}

/**
 * 导出招聘需求数据
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function exportRecruitmentRequirements(params) {
  return request({
    url: "/user/recruitment-requirements/export/",
    method: "get",
    params,
    responseType: "blob"
  })
}

/**
 * 导入招聘需求数据
 * @param {FormData} formData - 包含文件的表单数据
 * @returns {Promise}
 */
export function importRecruitmentRequirements(formData) {
  return request({
    url: "/user/recruitment-requirements/import/",
    method: "post",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}

// ==================== 招聘进度 API ====================

/**
 * 获取招聘进度列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getRecruitmentProgress(params) {
  return request({
    url: "/user/recruitment-progress/",
    method: "get",
    params
  })
}

/**
 * 获取招聘进度详情
 * @param {string} id - 候选人ID
 * @returns {Promise}
 */
export function getRecruitmentProgressDetail(id) {
  return request({
    url: `/user/recruitment-progress/${id}/`,
    method: "get"
  })
}

/**
 * 创建招聘进度记录
 * @param {Object} data - 招聘进度数据
 * @returns {Promise}
 */
export function createRecruitmentProgress(data) {
  return request({
    url: "/user/recruitment-progress/",
    method: "post",
    data
  })
}

/**
 * 更新招聘进度记录
 * @param {string} id - 候选人ID
 * @param {Object} data - 招聘进度数据
 * @returns {Promise}
 */
export function updateRecruitmentProgress(id, data) {
  return request({
    url: `/user/recruitment-progress/${id}/`,
    method: "put",
    data
  })
}

/**
 * 删除招聘进度记录
 * @param {string} id - 候选人ID
 * @returns {Promise}
 */
export function deleteRecruitmentProgress(id) {
  return request({
    url: `/user/recruitment-progress/${id}/`,
    method: "delete"
  })
}

/**
 * 批量删除招聘进度记录
 * @param {Array} ids - 候选人ID列表
 * @returns {Promise}
 */
export function batchDeleteRecruitmentProgress(ids) {
  return request({
    url: "/user/recruitment-progress/batch-delete/",
    method: "post",
    data: { ids }
  })
}

/**
 * 导出招聘进度数据
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function exportRecruitmentProgress(params) {
  return request({
    url: "/user/recruitment-progress/export/",
    method: "get",
    params,
    responseType: "blob"
  })
}

/**
 * 导入招聘进度数据
 * @param {FormData} formData - 包含文件的表单数据
 * @returns {Promise}
 */
export function importRecruitmentProgress(formData) {
  return request({
    url: "/user/recruitment-progress/import/",
    method: "post",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}

/**
 * 上传候选人简历
 * @param {FormData} formData - 包含文件的表单数据
 * @returns {Promise}
 */
export function uploadCandidateResume(formData) {
  return request({
    url: "/user/recruitment-progress/upload-resume/",
    method: "post",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}

/**
 * 下载候选人简历
 * @param {string} id - 候选人ID
 * @returns {Promise}
 */
export function downloadCandidateResume(id) {
  return request({
    url: `/user/recruitment-progress/${id}/download-resume/`,
    method: "get",
    responseType: "blob"
  })
}

/**
 * 获取人事部用户列表
 * @returns {Promise}
 */
export function getHRUsers() {
  return request({
    url: "/user/hr-users/",
    method: "get"
  })
}
