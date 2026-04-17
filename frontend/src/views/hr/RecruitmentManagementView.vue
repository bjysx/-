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
        <div class="flex justify-between items-center mb-4">
          <div class="flex items-center gap-2">
            <el-icon class="text-blue-500"><Document /></el-icon>
            <span class="font-semibold text-gray-700">招聘进度</span>
          </div>
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
          <el-table-column label="简历详情" width="120" fixed="right">
            <template #default="{ row }">
              <div class="flex gap-2">
                <el-button type="primary" link size="small" @click="viewResumeDetail(row)">查看</el-button>
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
  expected_arrival: ''
})

const handleProgressAdd = () => {
  progressDialogType.value = 'add'
  // 重置表单
  Object.assign(progressForm, {
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
    expected_arrival: ''
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
