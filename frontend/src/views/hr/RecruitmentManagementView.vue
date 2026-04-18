<template>
  <div class="page-shell">
    <section class="page-card">
      <!-- 顶部标签切换 -->
      <div class="mb-5">
        <el-radio-group v-model="activeTab" size="large">
          <el-radio-button value="requirements">需求汇总</el-radio-button>
          <el-radio-button value="progress">招聘进度</el-radio-button>
        </el-radio-group>
      </div>

      <!-- 招聘进度界面 -->
      <div v-if="activeTab === 'progress'">
        <!-- 筛选条件 -->
        <div class="bg-gray-50 p-4 rounded-lg mb-5">
          <div class="grid grid-cols-5 gap-4">
            <el-select v-model="progressFilters.department" placeholder="应聘部门" clearable>
              <el-option label="技术部" value="技术部" />
              <el-option label="产品部" value="产品部" />
              <el-option label="运营部" value="运营部" />
              <el-option label="销售部" value="销售部" />
              <el-option label="人力资源部" value="人力资源部" />
            </el-select>
            <el-select v-model="progressFilters.position" placeholder="岗位" clearable>
              <el-option label="前端工程师" value="前端工程师" />
              <el-option label="后端工程师" value="后端工程师" />
              <el-option label="产品经理" value="产品经理" />
              <el-option label="运营专员" value="运营专员" />
              <el-option label="销售经理" value="销售经理" />
            </el-select>
            <el-select v-model="progressFilters.interview_result" placeholder="面试结果" clearable>
              <el-option label="待面试" value="待面试" />
              <el-option label="一面通过" value="一面通过" />
              <el-option label="一面未通过" value="一面未通过" />
              <el-option label="二面通过" value="二面通过" />
              <el-option label="二面未通过" value="二面未通过" />
              <el-option label="待发OFFER" value="待发OFFER" />
              <el-option label="已发OFFER待入职" value="已发OFFER待入职" />
              <el-option label="已入职" value="已入职" />
              <el-option label="储备" value="储备" />
              <el-option label="待定" value="待定" />
              <el-option label="拒绝OFFER" value="拒绝OFFER" />
            </el-select>
            <el-input v-model="progressFilters.candidate_name" placeholder="请输入姓名" clearable />
            <div></div>
          </div>
          <div class="grid grid-cols-5 gap-4 mt-4">
            <el-select v-model="progressFilters.invite_hr" placeholder="邀约HR" clearable>
              <el-option label="张HR" value="张HR" />
              <el-option label="李HR" value="李HR" />
              <el-option label="王HR" value="王HR" />
            </el-select>
            <el-select v-model="progressFilters.expected_arrival" placeholder="预计到岗时间" clearable>
              <el-option label="一周内" value="一周内" />
              <el-option label="两周内" value="两周内" />
              <el-option label="一个月内" value="一个月内" />
              <el-option label="一个月后" value="一个月后" />
            </el-select>
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-600 whitespace-nowrap">推荐日期：</span>
              <el-date-picker
                v-model="progressFilters.recommend_date_range"
                type="daterange"
                range-separator="至"
                start-placeholder="开始"
                end-placeholder="结束"
                value-format="YYYY-MM-DD"
                class="w-full"
              />
            </div>
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-600 whitespace-nowrap">到岗日期：</span>
              <el-date-picker
                v-model="progressFilters.arrival_date_range"
                type="daterange"
                range-separator="至"
                start-placeholder="开始"
                end-placeholder="结束"
                value-format="YYYY-MM-DD"
                class="w-full"
              />
            </div>
            <div class="flex gap-2 justify-end">
              <el-button type="primary" @click="handleProgressSearch">
                <el-icon><Search /></el-icon>搜索
              </el-button>
              <el-button @click="handleProgressReset">
                <el-icon><Refresh /></el-icon>重置
              </el-button>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex justify-start items-center mb-4">
          <div class="flex gap-2">
            <el-button type="primary" @click="handleProgressAdd">
              <el-icon><Plus /></el-icon>新增
            </el-button>
            <el-button type="success" @click="handleOnboard">
              <el-icon><Check /></el-icon>办理入职
            </el-button>
            <el-button @click="handleProgressDelete">
              <el-icon><Delete /></el-icon>删除
            </el-button>
            <el-button @click="handleProgressExport">
              <el-icon><Upload /></el-icon>导出
            </el-button>
            <el-button @click="handleProgressImport">
              <el-icon><Download /></el-icon>导入
            </el-button>
          </div>
        </div>

        <!-- 数据表格 -->
        <el-table
          :data="progressTableData"
          border
          stripe
          style="width: 100%"
          @selection-change="handleProgressSelectionChange"
        >
          <el-table-column type="selection" width="50" align="center" />
          <el-table-column label="候选人" prop="candidate_name" width="100" />
          <el-table-column label="推荐日期" prop="recommend_date" width="100" />
          <el-table-column label="应聘部门" prop="department" width="100" />
          <el-table-column label="应聘岗位" prop="position" width="100" />
          <el-table-column label="来源渠道" prop="source_channel" width="100" />
          <el-table-column label="候选人简历" width="120">
            <template #default="{ row }">
              <div class="flex gap-2">
                <el-button type="primary" link size="small" @click="uploadResume(row)">上传</el-button>
                <el-button v-if="row.resume_url" type="success" link size="small" @click="downloadResume(row)">下载</el-button>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="性别" prop="gender" width="60" />
          <el-table-column label="学历" prop="education" width="80" />
          <el-table-column label="邀约HR" prop="invite_hr" width="100" />
          <el-table-column label="一面面试时间" prop="first_interview_time" width="130" />
          <el-table-column label="一面面试官" prop="first_interviewer" width="100" />
          <el-table-column label="二面面试时间" prop="second_interview_time" width="130" />
          <el-table-column label="二面面试官" prop="second_interviewer" width="100" />
          <el-table-column label="面试结果" prop="interview_result" width="100">
            <template #default="{ row }">
              <el-tag :type="getInterviewResultType(row.interview_result)" size="small">
                {{ row.interview_result }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="预计到岗时间" prop="expected_arrival" width="110" />
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <div class="flex gap-2">
                <el-button type="primary" link size="small" @click="handleProgressDetail(row)">详情</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="flex justify-end mt-4">
          <el-pagination
            v-model:current-page="progressPagination.page"
            v-model:page-size="progressPagination.pageSize"
            :total="progressPagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next"
            @size-change="handleProgressSizeChange"
            @current-change="handleProgressPageChange"
          />
        </div>

        <!-- 详情对话框 -->
        <el-dialog v-model="detailDialogVisible" title="招聘进度详情" width="900px" top="5vh">
          <el-form v-if="detailForm" :model="detailForm" label-width="120px" class="detail-form">
            <!-- 基本信息 -->
            <h4 class="section-title">基本信息</h4>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="候选人">
                  <el-input v-model="detailForm.candidate_name" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="推荐日期">
                  <el-date-picker v-model="detailForm.recommend_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="应聘部门">
                  <el-input v-model="detailForm.department" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="应聘岗位">
                  <el-input v-model="detailForm.position" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="来源渠道">
                  <el-input v-model="detailForm.source_channel" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="性别">
                  <el-select v-model="detailForm.gender" style="width: 100%">
                    <el-option label="男" value="男" />
                    <el-option label="女" value="女" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="学历">
                  <el-select v-model="detailForm.education" style="width: 100%">
                    <el-option label="博士" value="博士" />
                    <el-option label="硕士" value="硕士" />
                    <el-option label="本科" value="本科" />
                    <el-option label="大专" value="大专" />
                    <el-option label="高中" value="高中" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="邀约HR">
                  <el-input v-model="detailForm.invite_hr" />
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 储备阶段 -->
            <h4 class="section-title">储备阶段</h4>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="储备状态">
                  <el-select v-model="detailForm.reserve_status" style="width: 100%">
                    <el-option label="储备中" value="储备中" />
                    <el-option label="已激活" value="已激活" />
                    <el-option label="已放弃" value="已放弃" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="新增时间">
                  <el-input v-model="detailForm.created_at" disabled />
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 待面试阶段 -->
            <h4 class="section-title">待面试阶段</h4>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="预计面试时间">
                  <el-date-picker v-model="detailForm.expected_interview_time" type="datetime" value-format="YYYY-MM-DD HH:mm" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="实际面试时间">
                  <el-date-picker v-model="detailForm.actual_interview_time" type="datetime" value-format="YYYY-MM-DD HH:mm" style="width: 100%" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="是否到面">
                  <el-select v-model="detailForm.is_attended" style="width: 100%">
                    <el-option label="是" value="是" />
                    <el-option label="否" value="否" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="是否视频面试">
                  <el-select v-model="detailForm.is_video_interview" style="width: 100%">
                    <el-option label="是" value="是" />
                    <el-option label="否" value="否" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 初试阶段 -->
            <h4 class="section-title">初试阶段</h4>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="初试时间">
                  <el-date-picker v-model="detailForm.first_interview_actual_time" type="datetime" value-format="YYYY-MM-DD HH:mm" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="初试面试官">
                  <el-input v-model="detailForm.first_interview_actual_interviewer" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="初试结果">
                  <el-select v-model="detailForm.first_interview_result" style="width: 100%">
                    <el-option label="通过" value="通过" />
                    <el-option label="未通过" value="未通过" />
                    <el-option label="待定" value="待定" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="未通过原因">
                  <el-input v-model="detailForm.first_interview_fail_reason" type="textarea" :rows="2" />
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 复试阶段 -->
            <h4 class="section-title">复试阶段</h4>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="复试时间">
                  <el-date-picker v-model="detailForm.second_interview_actual_time" type="datetime" value-format="YYYY-MM-DD HH:mm" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="复试面试官">
                  <el-input v-model="detailForm.second_interview_actual_interviewer" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="复试结果">
                  <el-select v-model="detailForm.second_interview_result" style="width: 100%">
                    <el-option label="通过" value="通过" />
                    <el-option label="未通过" value="未通过" />
                    <el-option label="待定" value="待定" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="未通过原因">
                  <el-input v-model="detailForm.second_interview_fail_reason" type="textarea" :rows="2" />
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 确认Offer阶段 -->
            <h4 class="section-title">确认Offer阶段</h4>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="期待薪资">
                  <el-input-number v-model="detailForm.expected_salary" :min="0" :precision="2" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="谈薪确认标准">
                  <el-input v-model="detailForm.salary_confirm_standard" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="转正期限">
                  <el-input v-model="detailForm.probation_period" placeholder="如：3个月" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="社保备注">
                  <el-input v-model="detailForm.social_security_remarks" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="入职部门">
                  <el-input v-model="detailForm.onboard_department" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="入职岗位">
                  <el-input v-model="detailForm.onboard_position" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="职级">
                  <el-select v-model="detailForm.job_level" style="width: 100%">
                    <el-option label="P1" value="P1" />
                    <el-option label="P2" value="P2" />
                    <el-option label="P3" value="P3" />
                    <el-option label="P4" value="P4" />
                    <el-option label="P5" value="P5" />
                    <el-option label="M1" value="M1" />
                    <el-option label="M2" value="M2" />
                    <el-option label="M3" value="M3" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="预计入职日期">
                  <el-date-picker v-model="detailForm.expected_onboard_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 发Offer阶段 -->
            <h4 class="section-title">发Offer阶段</h4>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Offer状态">
                  <el-select v-model="detailForm.offer_status" style="width: 100%">
                    <el-option label="待发" value="待发" />
                    <el-option label="已发" value="已发" />
                    <el-option label="已接受" value="已接受" />
                    <el-option label="已拒绝" value="已拒绝" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Offer回复">
                  <el-input v-model="detailForm.offer_reply" type="textarea" :rows="2" />
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 其他信息 -->
            <h4 class="section-title">其他信息</h4>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="预计到岗时间">
                  <el-date-picker v-model="detailForm.expected_arrival" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="面试结果">
                  <el-select v-model="detailForm.interview_result" style="width: 100%">
                    <el-option label="待面试" value="待面试" />
                    <el-option label="一面通过" value="一面通过" />
                    <el-option label="一面未通过" value="一面未通过" />
                    <el-option label="二面通过" value="二面通过" />
                    <el-option label="二面未通过" value="二面未通过" />
                    <el-option label="待发OFFER" value="待发OFFER" />
                    <el-option label="已发OFFER待入职" value="已发OFFER待入职" />
                    <el-option label="已入职" value="已入职" />
                    <el-option label="储备" value="储备" />
                    <el-option label="待定" value="待定" />
                    <el-option label="拒绝OFFER" value="拒绝OFFER" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <template #footer>
            <el-button @click="detailDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleDetailSubmit" :loading="detailSubmitting">确认</el-button>
          </template>
        </el-dialog>
      </div>

      <!-- 需求汇总界面 -->
      <div v-if="activeTab === 'requirements'">
        <!-- 筛选条件 -->
        <div class="bg-gray-50 p-4 rounded-lg mb-5">
          <div class="grid grid-cols-5 gap-4">
            <el-select v-model="filters.department" placeholder="需求部门" clearable>
              <el-option label="技术部" value="技术部" />
              <el-option label="产品部" value="产品部" />
              <el-option label="运营部" value="运营部" />
              <el-option label="销售部" value="销售部" />
              <el-option label="人力资源部" value="人力资源部" />
            </el-select>
            <el-select v-model="filters.position" placeholder="岗位" clearable>
              <el-option label="前端工程师" value="前端工程师" />
              <el-option label="后端工程师" value="后端工程师" />
              <el-option label="产品经理" value="产品经理" />
              <el-option label="运营专员" value="运营专员" />
              <el-option label="销售经理" value="销售经理" />
            </el-select>
            <el-select v-model="filters.status" placeholder="当前状态" clearable>
              <el-option label="招聘中" value="招聘中" />
              <el-option label="已暂停" value="已暂停" />
              <el-option label="已完成" value="已完成" />
            </el-select>
            <el-select v-model="filters.hr" placeholder="负责HR" clearable>
              <el-option label="张HR" value="张HR" />
              <el-option label="李HR" value="李HR" />
              <el-option label="王HR" value="王HR" />
            </el-select>
            <el-select v-model="filters.urgency" placeholder="紧急程度" clearable>
              <el-option label="紧急" value="紧急" />
              <el-option label="一般" value="一般" />
              <el-option label="低" value="低" />
            </el-select>
          </div>
          <div class="flex justify-between items-center mt-4">
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-600">申请日期：</span>
              <el-date-picker
                v-model="filters.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始"
                end-placeholder="结束"
                value-format="YYYY-MM-DD"
                class="w-64"
              />
            </div>
            <div class="flex gap-2">
              <el-button type="primary" @click="handleSearch">
                <el-icon><Search /></el-icon>搜索
              </el-button>
              <el-button @click="handleReset">
                <el-icon><Refresh /></el-icon>重置
              </el-button>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex justify-between items-center mb-4">
          <div class="flex items-center gap-2">
            <el-icon class="text-blue-500"><Collection /></el-icon>
            <span class="font-semibold text-gray-700">招聘需求汇总</span>
          </div>
          <div class="flex gap-2">
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>新增
            </el-button>
            <el-button @click="handleDelete">
              <el-icon><Delete /></el-icon>删除
            </el-button>
            <el-button @click="handleExport">
              <el-icon><Upload /></el-icon>导出
            </el-button>
            <el-button @click="handleImport">
              <el-icon><Download /></el-icon>导入
            </el-button>
          </div>
        </div>

        <!-- 数据表格 -->
        <el-table
          :data="tableData"
          border
          stripe
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="50" align="center" />
          <el-table-column label="需求部门" prop="department" width="100" />
          <el-table-column label="需求提出人" prop="requester" width="100" />
          <el-table-column label="需求岗位" prop="position" width="120" />
          <el-table-column label="申请日期" prop="application_date" width="100" />
          <el-table-column label="紧急程度" width="90">
            <template #default="{ row }">
              <el-tag :type="getUrgencyType(row.urgency_level)" size="small">
                {{ row.urgency_level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="需求人数" prop="required_count" width="90" align="center" />
          <el-table-column label="已入职人数" prop="hired_count" width="100" align="center" />
          <el-table-column label="剩余人数" prop="remaining_count" width="90" align="center" />
          <el-table-column label="人员类别" prop="personnel_type" width="100" />
          <el-table-column label="招聘状态" width="90">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.recruitment_status)" size="small">
                {{ row.recruitment_status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="负责HR" prop="responsible_hr" width="100" />
          <el-table-column label="工作地" prop="work_location" width="100" />
          <el-table-column label="建议薪资范围" prop="salary_range" width="120" />
          <el-table-column label="岗位要求" prop="job_requirements" min-width="150" show-overflow-tooltip />
          <el-table-column label="备注" prop="remarks" min-width="120" show-overflow-tooltip />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <div class="flex gap-2 flex-wrap">
                <el-button type="primary" link size="small" @click="handleDetail(row)">详情</el-button>
                <el-button type="primary" link size="small" @click="handleEdit(row)">修改</el-button>
                <el-button type="danger" link size="small" @click="handleRowDelete(row)">删除</el-button>
                <el-button type="success" link size="small" @click="handleAssignHR(row)">指派HR</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="flex justify-end mt-4">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :total="pagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </section>

    <!-- 需求汇总对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增招聘需求' : '编辑招聘需求'"
      width="700px"
    >
      <el-form :model="form" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="需求部门">
              <el-select v-model="form.department" placeholder="请选择" class="w-full">
                <el-option label="技术部" value="技术部" />
                <el-option label="产品部" value="产品部" />
                <el-option label="运营部" value="运营部" />
                <el-option label="销售部" value="销售部" />
                <el-option label="人力资源部" value="人力资源部" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="需求提出人">
              <el-input v-model="form.requester" placeholder="请输入" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="需求岗位">
              <el-input v-model="form.position" placeholder="请输入" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="申请日期">
              <el-date-picker v-model="form.application_date" type="date" placeholder="选择日期" class="w-full" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="紧急程度">
              <el-select v-model="form.urgency_level" placeholder="请选择" class="w-full">
                <el-option label="紧急" value="紧急" />
                <el-option label="一般" value="一般" />
                <el-option label="低" value="低" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="需求人数">
              <el-input-number v-model="form.required_count" :min="1" class="w-full" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="人员类别">
              <el-input v-model="form.personnel_type" placeholder="请输入" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="招聘状态">
              <el-select v-model="form.recruitment_status" placeholder="请选择" class="w-full">
                <el-option label="招聘中" value="招聘中" />
                <el-option label="已暂停" value="已暂停" />
                <el-option label="已完成" value="已完成" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="工作地">
          <el-input v-model="form.work_location" placeholder="请输入工作地" />
        </el-form-item>
        <el-form-item label="建议薪资范围">
          <el-input v-model="form.salary_range" placeholder="请输入薪资范围" />
        </el-form-item>
        <el-form-item label="岗位要求">
          <el-input v-model="form.job_requirements" type="textarea" :rows="3" placeholder="请输入岗位要求" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remarks" type="textarea" :rows="2" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 指派HR弹窗 -->
    <el-dialog
      v-model="assignHRDialogVisible"
      title="指派HR"
      width="400px"
    >
      <el-form label-width="80px">
        <el-form-item label="选择HR">
          <el-select v-model="assignHRForm.hrName" placeholder="请选择HR" class="w-full">
            <el-option
              v-for="user in hrUsers"
              :key="user.id"
              :label="user.nickname || user.username"
              :value="user.nickname || user.username"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="assignHRDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAssignHRSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 招聘进度新增/编辑对话框 -->
    <el-dialog
      v-model="progressDialogVisible"
      :title="progressDialogType === 'add' ? '新增招聘进度' : '编辑招聘进度'"
      width="800px"
    >
      <el-form :model="progressForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="候选人">
              <el-input v-model="progressForm.candidate_name" placeholder="请输入候选人姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="推荐日期">
              <el-date-picker v-model="progressForm.recommend_date" type="date" placeholder="选择日期" class="w-full" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="应聘部门">
              <el-select v-model="progressForm.department" placeholder="请选择" class="w-full">
                <el-option label="技术部" value="技术部" />
                <el-option label="产品部" value="产品部" />
                <el-option label="运营部" value="运营部" />
                <el-option label="销售部" value="销售部" />
                <el-option label="人力资源部" value="人力资源部" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="应聘岗位">
              <el-input v-model="progressForm.position" placeholder="请输入岗位" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="来源渠道">
              <el-select v-model="progressForm.source_channel" placeholder="请选择" class="w-full">
                <el-option label="BOSS直聘" value="BOSS直聘" />
                <el-option label="智联招聘" value="智联招聘" />
                <el-option label="前程无忧" value="前程无忧" />
                <el-option label="猎聘" value="猎聘" />
                <el-option label="内部推荐" value="内部推荐" />
                <el-option label="官网投递" value="官网投递" />
                <el-option label="校园招聘" value="校园招聘" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别">
              <el-select v-model="progressForm.gender" placeholder="请选择" class="w-full">
                <el-option label="男" value="男" />
                <el-option label="女" value="女" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学历">
              <el-select v-model="progressForm.education" placeholder="请选择" class="w-full">
                <el-option label="博士" value="博士" />
                <el-option label="硕士" value="硕士" />
                <el-option label="本科" value="本科" />
                <el-option label="大专" value="大专" />
                <el-option label="高中及以下" value="高中及以下" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邀约HR">
              <el-select v-model="progressForm.invite_hr" placeholder="请选择" class="w-full">
                <el-option label="张HR" value="张HR" />
                <el-option label="李HR" value="李HR" />
                <el-option label="王HR" value="王HR" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="一面时间">
              <el-date-picker v-model="progressForm.first_interview_time" type="datetime" placeholder="选择时间" class="w-full" value-format="YYYY-MM-DD HH:mm:ss" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="一面面试官">
              <el-input v-model="progressForm.first_interviewer" placeholder="请输入面试官" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="二面时间">
              <el-date-picker v-model="progressForm.second_interview_time" type="datetime" placeholder="选择时间" class="w-full" value-format="YYYY-MM-DD HH:mm:ss" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="二面面试官">
              <el-input v-model="progressForm.second_interviewer" placeholder="请输入面试官" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="面试结果">
              <el-select v-model="progressForm.interview_result" placeholder="请选择" class="w-full">
                <el-option label="待面试" value="待面试" />
                <el-option label="一面通过" value="一面通过" />
                <el-option label="一面未通过" value="一面未通过" />
                <el-option label="二面通过" value="二面通过" />
                <el-option label="二面未通过" value="二面未通过" />
                <el-option label="待发OFFER" value="待发OFFER" />
                <el-option label="已发OFFER待入职" value="已发OFFER待入职" />
                <el-option label="已入职" value="已入职" />
                <el-option label="储备" value="储备" />
                <el-option label="待定" value="待定" />
                <el-option label="拒绝OFFER" value="拒绝OFFER" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预计到岗">
              <el-date-picker v-model="progressForm.expected_arrival" type="date" placeholder="选择日期" class="w-full" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="简历上传">
          <el-upload
            action="#"
            :auto-upload="false"
            :on-change="handleResumeChange"
            :file-list="resumeFileList"
            accept=".pdf,.doc,.docx"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">支持 PDF、Word 格式</div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="progressDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleProgressSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh, Plus, Delete, Upload, Download, Collection, Document, Check } from '@element-plus/icons-vue'
import {
  getRecruitmentRequirements,
  createRecruitmentRequirement,
  updateRecruitmentRequirement,
  deleteRecruitmentRequirement,
  batchDeleteRecruitmentRequirements,
  getHRUsers,
  getRecruitmentProgress,
  createRecruitmentProgress,
  updateRecruitmentProgress
} from '@/api/recruitment'

// 当前激活的标签页
const activeTab = ref('requirements')

// ========== 需求汇总相关 ==========
const filters = reactive({
  department: '',
  position: '',
  status: '',
  hr: '',
  urgency: '',
  dateRange: []
})

const tableData = ref([])
const selectedRows = ref([])

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const dialogVisible = ref(false)
const dialogType = ref('add')
const form = reactive({
  id: null,
  department: '',
  requester: '',
  position: '',
  application_date: '',
  urgency_level: '一般',
  required_count: 1,
  hired_count: 0,
  personnel_type: '',
  recruitment_status: '招聘中',
  responsible_hr: '',
  work_location: '',
  salary_range: '',
  job_requirements: '',
  remarks: ''
})

const getUrgencyType = (urgency) => {
  const map = { '紧急': 'danger', '一般': 'warning', '低': 'info' }
  return map[urgency] || 'info'
}

const getStatusType = (status) => {
  const map = { '招聘中': 'primary', '已暂停': 'warning', '已完成': 'success' }
  return map[status] || 'info'
}

const loadData = async () => {
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      department: filters.department,
      position: filters.position,
      status: filters.status,
      hr: filters.hr,
      urgency: filters.urgency
    }
    if (filters.dateRange && filters.dateRange.length === 2) {
      params.start_date = filters.dateRange[0]
      params.end_date = filters.dateRange[1]
    }
    const res = await getRecruitmentRequirements(params)
    tableData.value = res.results || []
    pagination.total = res.total || 0
  } catch (error) {
    ElMessage.error('加载数据失败')
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadData()
}

const handleReset = () => {
  filters.department = ''
  filters.position = ''
  filters.status = ''
  filters.hr = ''
  filters.urgency = ''
  filters.dateRange = []
  handleSearch()
}

const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

const handleAdd = () => {
  dialogType.value = 'add'
  Object.assign(form, {
    id: null,
    department: '',
    requester: '',
    position: '',
    application_date: '',
    urgency_level: '一般',
    required_count: 1,
    hired_count: 0,
    personnel_type: '',
    recruitment_status: '招聘中',
    responsible_hr: '',
    work_location: '',
    salary_range: '',
    job_requirements: '',
    remarks: ''
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleDetail = (row) => {
  ElMessage.info(`查看详情: ${row.position}`)
}

const handleDelete = async () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要删除的数据')
    return
  }
  try {
    await ElMessageBox.confirm('确定删除选中的数据吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const ids = selectedRows.value.map(row => row.id)
    await batchDeleteRecruitmentRequirements(ids)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleExport = () => {
  ElMessage.success('导出成功')
}

const handleImport = () => {
  ElMessage.info('导入功能')
}

const handleSubmit = async () => {
  try {
    if (dialogType.value === 'add') {
      await createRecruitmentRequirement(form)
      ElMessage.success('新增成功')
    } else {
      await updateRecruitmentRequirement(form.id, form)
      ElMessage.success('修改成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  loadData()
}

const handlePageChange = (page) => {
  pagination.page = page
  loadData()
}

// ========== 招聘进度相关 ==========
const progressFilters = reactive({
  department: '',
  position: '',
  interview_result: '',
  candidate_name: '',
  invite_hr: '',
  expected_arrival: '',
  recommend_date_range: [],
  arrival_date_range: []
})

const progressTableData = ref([])
const progressSelectedRows = ref([])

const progressPagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const getInterviewResultType = (result) => {
  const map = {
    '待面试': 'info',
    '一面通过': 'warning',
    '一面未通过': 'danger',
    '二面通过': 'warning',
    '二面未通过': 'danger',
    '待发OFFER': 'primary',
    '已发OFFER待入职': 'success',
    '已入职': 'success',
    '储备': 'info',
    '待定': 'warning',
    '拒绝OFFER': 'danger'
  }
  return map[result] || 'info'
}

const handleProgressSearch = () => {
  progressPagination.page = 1
  loadProgressData()
}

const handleProgressReset = () => {
  progressFilters.department = ''
  progressFilters.position = ''
  progressFilters.interview_result = ''
  progressFilters.candidate_name = ''
  progressFilters.invite_hr = ''
  progressFilters.expected_arrival = ''
  progressFilters.recommend_date_range = []
  progressFilters.arrival_date_range = []
  handleProgressSearch()
}

const handleProgressSelectionChange = (selection) => {
  progressSelectedRows.value = selection
}

// ========== 招聘进度对话框相关 ==========
const progressDialogVisible = ref(false)
const progressDialogType = ref('add')
const progressForm = reactive({
  id: null,
  candidate_name: '',
  recommend_date: '',
  department: '',
  position: '',
  source_channel: '',
  resume_url: '',
  gender: '',
  education: '',
  invite_hr: '',
  first_interview_time: '',
  first_interviewer: '',
  second_interview_time: '',
  second_interviewer: '',
  interview_result: '待面试',
  expected_arrival: '',
  // 储备阶段
  reserve_status: '',
  created_at: '',
  // 待面试阶段
  expected_interview_time: '',
  actual_interview_time: '',
  is_attended: '',
  is_video_interview: '',
  // 初试阶段
  first_interview_actual_time: '',
  first_interview_actual_interviewer: '',
  first_interview_result: '',
  first_interview_fail_reason: '',
  // 复试阶段
  second_interview_actual_time: '',
  second_interview_actual_interviewer: '',
  second_interview_result: '',
  second_interview_fail_reason: '',
  // 确认offer阶段
  expected_salary: '',
  salary_confirm_standard: '',
  probation_period: '',
  social_security_remarks: '',
  onboard_department: '',
  onboard_position: '',
  job_level: '',
  expected_onboard_date: '',
  // 发offer阶段
  offer_status: '',
  offer_reply: ''
})

// 详情对话框数据
const detailDialogVisible = ref(false)
const detailSubmitting = ref(false)
const detailForm = reactive({
  id: null,
  candidate_name: '',
  recommend_date: '',
  department: '',
  position: '',
  source_channel: '',
  gender: '',
  education: '',
  invite_hr: '',
  // 储备阶段
  reserve_status: '',
  created_at: '',
  // 待面试阶段
  expected_interview_time: '',
  actual_interview_time: '',
  is_attended: '',
  is_video_interview: '',
  // 初试阶段
  first_interview_actual_time: '',
  first_interview_actual_interviewer: '',
  first_interview_result: '',
  first_interview_fail_reason: '',
  // 复试阶段
  second_interview_actual_time: '',
  second_interview_actual_interviewer: '',
  second_interview_result: '',
  second_interview_fail_reason: '',
  // 确认offer阶段
  expected_salary: null,
  salary_confirm_standard: '',
  probation_period: '',
  social_security_remarks: '',
  onboard_department: '',
  onboard_position: '',
  job_level: '',
  expected_onboard_date: '',
  // 发offer阶段
  offer_status: '',
  offer_reply: '',
  // 其他字段
  first_interview_time: '',
  first_interviewer: '',
  second_interview_time: '',
  second_interviewer: '',
  interview_result: '待面试',
  expected_arrival: ''
})

const handleProgressAdd = () => {
  progressDialogType.value = 'add'
  // 重置表单
  Object.assign(progressForm, {
    id: null,
    candidate_name: '',
    recommend_date: '',
    department: '',
    position: '',
    source_channel: '',
    resume_url: '',
    gender: '',
    education: '',
    invite_hr: '',
    first_interview_time: '',
    first_interviewer: '',
    second_interview_time: '',
    second_interviewer: '',
    interview_result: '待面试',
    expected_arrival: '',
    // 新增字段
    reserve_status: '',
    created_at: '',
    expected_interview_time: '',
    actual_interview_time: '',
    is_attended: '',
    is_video_interview: '',
    first_interview_actual_time: '',
    first_interview_actual_interviewer: '',
    first_interview_result: '',
    first_interview_fail_reason: '',
    second_interview_actual_time: '',
    second_interview_actual_interviewer: '',
    second_interview_result: '',
    second_interview_fail_reason: '',
    expected_salary: null,
    salary_confirm_standard: '',
    probation_period: '',
    social_security_remarks: '',
    onboard_department: '',
    onboard_position: '',
    job_level: '',
    expected_onboard_date: '',
    offer_status: '',
    offer_reply: ''
  })
  progressDialogVisible.value = true
}

const handleProgressSubmit = async () => {
  try {
    if (progressDialogType.value === 'add') {
      await createRecruitmentProgress(progressForm)
      ElMessage.success('新增成功')
    } else {
      await updateRecruitmentProgress(progressForm.id, progressForm)
      ElMessage.success('修改成功')
    }
    progressDialogVisible.value = false
    loadProgressData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleOnboard = () => {
  if (progressSelectedRows.value.length === 0) {
    ElMessage.warning('请选择要办理入职的候选人')
    return
  }
  ElMessage.success('办理入职成功')
}

const handleProgressDelete = () => {
  if (progressSelectedRows.value.length === 0) {
    ElMessage.warning('请选择要删除的数据')
    return
  }
  ElMessageBox.confirm('确定删除选中的数据吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
  })
}

const handleProgressExport = () => {
  ElMessage.success('导出成功')
}

const handleProgressImport = () => {
  ElMessage.info('导入功能')
}

const uploadResume = (row) => {
  ElMessage.info(`上传简历: ${row.candidate_name}`)
}

const downloadResume = (row) => {
  ElMessage.success(`下载简历: ${row.candidate_name}`)
}

const viewResumeDetail = (row) => {
  ElMessage.info(`查看简历详情: ${row.candidate_name}`)
}

const handleProgressDetail = (row) => {
  if (!row) {
    ElMessage.error('行数据为空')
    return
  }
  Object.assign(detailForm, {
    id: row.id,
    candidate_name: row.candidate_name || '',
    recommend_date: row.recommend_date || '',
    department: row.department || '',
    position: row.position || '',
    source_channel: row.source_channel || '',
    gender: row.gender || '',
    education: row.education || '',
    invite_hr: row.invite_hr || '',
    // 储备阶段
    reserve_status: row.reserve_status || '',
    created_at: row.created_at || '',
    // 待面试阶段
    expected_interview_time: row.expected_interview_time || '',
    actual_interview_time: row.actual_interview_time || '',
    is_attended: row.is_attended || '',
    is_video_interview: row.is_video_interview || '',
    // 初试阶段
    first_interview_actual_time: row.first_interview_actual_time || '',
    first_interview_actual_interviewer: row.first_interview_actual_interviewer || '',
    first_interview_result: row.first_interview_result || '',
    first_interview_fail_reason: row.first_interview_fail_reason || '',
    // 复试阶段
    second_interview_actual_time: row.second_interview_actual_time || '',
    second_interview_actual_interviewer: row.second_interview_actual_interviewer || '',
    second_interview_result: row.second_interview_result || '',
    second_interview_fail_reason: row.second_interview_fail_reason || '',
    // 确认offer阶段
    expected_salary: row.expected_salary || null,
    salary_confirm_standard: row.salary_confirm_standard || '',
    probation_period: row.probation_period || '',
    social_security_remarks: row.social_security_remarks || '',
    onboard_department: row.onboard_department || '',
    onboard_position: row.onboard_position || '',
    job_level: row.job_level || '',
    expected_onboard_date: row.expected_onboard_date || '',
    // 发offer阶段
    offer_status: row.offer_status || '',
    offer_reply: row.offer_reply || '',
    // 其他字段
    first_interview_time: row.first_interview_time || '',
    first_interviewer: row.first_interviewer || '',
    second_interview_time: row.second_interview_time || '',
    second_interviewer: row.second_interviewer || '',
    interview_result: row.interview_result || '待面试',
    expected_arrival: row.expected_arrival || ''
  })
  detailDialogVisible.value = true
}

const handleDetailSubmit = async () => {
  detailSubmitting.value = true
  try {
    await updateRecruitmentProgress(detailForm.id, detailForm)
    ElMessage.success('更新成功')
    detailDialogVisible.value = false
    loadProgressData()
  } catch (error) {
    ElMessage.error('更新失败')
  } finally {
    detailSubmitting.value = false
  }
}

const handleProgressSizeChange = (size) => {
  progressPagination.pageSize = size
  loadProgressData()
}

const handleProgressPageChange = (page) => {
  progressPagination.page = page
  loadProgressData()
}

const loadProgressData = async () => {
  try {
    const params = {
      page: progressPagination.page,
      page_size: progressPagination.pageSize,
      department: progressFilters.department,
      position: progressFilters.position,
      interview_result: progressFilters.interview_result,
      keyword: progressFilters.candidate_name,
      hr: progressFilters.invite_hr
    }
    const res = await getRecruitmentProgress(params)
    progressTableData.value = res.results || []
    progressPagination.total = res.total || 0
  } catch (error) {
    console.error('加载招聘进度数据失败:', error)
    ElMessage.error('加载招聘进度数据失败: ' + (error.response?.data?.message || error.message || '未知错误'))
  }
}

// ========== 指派HR相关 ==========
const assignHRDialogVisible = ref(false)
const assignHRForm = reactive({
  requirementId: null,
  hrName: ''
})

// 人事部用户列表
const hrUsers = ref([])

// 加载人事部用户
const loadHRUsers = async () => {
  try {
    const res = await getHRUsers()
    hrUsers.value = res || []
  } catch (error) {
    ElMessage.error('加载HR列表失败')
  }
}
const hrOptions = ref([
  { label: '张HR', value: '张HR' },
  { label: '李HR', value: '李HR' },
  { label: '王HR', value: '王HR' }
])

const handleAssignHR = async (row) => {
  assignHRForm.requirementId = row.id
  assignHRForm.hrName = row.responsible_hr || ''
  await loadHRUsers()
  assignHRDialogVisible.value = true
}

const handleAssignHRSubmit = async () => {
  if (!assignHRForm.hrName) {
    ElMessage.warning('请选择HR')
    return
  }
  try {
    await updateRecruitmentRequirement(assignHRForm.requirementId, {
      responsible_hr: assignHRForm.hrName
    })
    ElMessage.success('指派HR成功')
    assignHRDialogVisible.value = false
    loadData()
  } catch (error) {
    ElMessage.error('指派HR失败')
  }
}

const handleRowDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该招聘需求吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteRecruitmentRequirement(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadData()
})

// 监听标签页切换，切换到招聘进度时加载数据
watch(activeTab, (newVal) => {
  if (newVal === 'progress') {
    loadProgressData()
  }
})
</script>

<style scoped>
.page-shell {
  @apply p-5;
}

.page-card {
  @apply bg-white rounded-lg shadow-sm p-5;
}
</style>
