export const menuConfig = [
  {
    key: "work",
    title: "工作中心",
    icon: "Briefcase",
    children: [
      { key: "work-work-log-management", title: "日志管理", path: "/work/work-log-management", pageCode: "work-work-log-management" },
      { key: "work-work-meeting-management", title: "会议管理", path: "/work/work-meeting-management", pageCode: "work-work-meeting-management" }
    ]
  },
  {
    key: "sales",
    title: "总览",
    icon: "TrendCharts",
    children: [
      { key: "sales-domestic-board", title: "国内电商看板", path: "/sales/domestic-board", pageCode: "sales-domestic-board" },
      { key: "sales-cross-border-board", title: "跨境电商看板", path: "/sales/cross-border-board", pageCode: "sales-cross-border-board" },
      { key: "sales-b2b-key-account-board", title: "B2B大客户看板", path: "/sales/b2b-key-account-board", pageCode: "sales-b2b-key-account-board" },
      { key: "sales-channel-board", title: "渠道看板", path: "/sales/channel-board", pageCode: "sales-channel-board" },
      { key: "sales-resource-management", title: "资源管理", path: "/sales/resource-management", pageCode: "sales-resource-management" },
      { key: "sales-forecast-model", title: "业务预估模型", path: "/sales/forecast-model", pageCode: "sales-forecast-model" }
    ]
  },
  {
    key: "operations",
    title: "运营中心",
    icon: "DataLine",
    children: [
      { key: "operations-channel-products", title: "渠道在售商品", path: "/operations/channel-products", pageCode: "operations-channel-products" },
      { key: "operations-sales-overview", title: "销售情况", path: "/operations/sales-overview", pageCode: "operations-sales-overview" },
      { key: "operations-promotion-analysis", title: "推广分析", path: "/operations/promotion-analysis", pageCode: "operations-promotion-analysis" },
      { key: "operations-b-customer-management", title: "B维大客户管理", path: "/operations/b-customer-management", pageCode: "operations-b-customer-management" },
      { key: "operations-churn-warning", title: "流失预警", path: "/operations/churn-warning", pageCode: "operations-churn-warning" },
      { key: "operations-c-user-analysis", title: "C端用户分析", path: "/operations/c-user-analysis", pageCode: "operations-c-user-analysis" }
    ]
  },
  {
    key: "product",
    title: "商品中心",
    icon: "Goods",
    children: [
      { key: "product-product-list", title: "商品列表", path: "/product/product-list", pageCode: "product-product-list" },
      {
        key: "product-product-development",
        title: "商品产品开发",
        children: [
          { key: "product-double-star", title: "跨境", path: "/product/double-star", pageCode: "product-double-star" },
          { key: "product-white-label", title: "内贸", path: "/product/white-label", pageCode: "product-white-label" }
        ]
      },
      { key: "product-new-product-monitor", title: "新品动销监控", path: "/product/new-product-monitor", pageCode: "product-new-product-monitor" },
      { key: "product-hot-slow-analysis", title: "爆款/滞销分析", path: "/product/hot-slow-analysis", pageCode: "product-hot-slow-analysis" },
      { key: "product-refund-reason-analysis", title: "退款原因分析", path: "/product/refund-reason-analysis", pageCode: "product-refund-reason-analysis" }
    ]
  },
  {
    key: "supply-chain",
    title: "供应链中心",
    icon: "Box",
    children: [
      { key: "supply-chain-purchase-order-tracking", title: "采购订单追踪", path: "/supply-chain/purchase-order-tracking", pageCode: "supply-chain-purchase-order-tracking" },
      { key: "supply-chain-supply-chain-grading", title: "供应链分级管理", path: "/supply-chain/supply-chain-grading", pageCode: "supply-chain-supply-chain-grading" },
      { key: "supply-chain-inventory-health", title: "库存健康度", path: "/supply-chain/inventory-health", pageCode: "supply-chain-inventory-health" },
      { key: "supply-chain-factory-capacity-board", title: "工厂产能汇总看板", path: "/supply-chain/factory-capacity-board", pageCode: "supply-chain-factory-capacity-board" },
      { key: "supply-chain-inventory-management", title: "库存管理", path: "/supply-chain/inventory-management", pageCode: "supply-chain-inventory-management" },
      { key: "supply-chain-inbound-shelf-time", title: "预计到库及上架时间", path: "/supply-chain/inbound-shelf-time", pageCode: "supply-chain-inbound-shelf-time" },
      { key: "supply-chain-quality-management", title: "品控及质量管理", path: "/supply-chain/quality-management", pageCode: "supply-chain-quality-management" }
    ]
  },
  {
    key: "finance",
    title: "财务中心",
    icon: "Wallet",
    children: [
      { key: "finance-receivables-collections", title: "回款与应收", path: "/finance/receivables-collections", pageCode: "finance-receivables-collections" },
      { key: "finance-cost-accounting-center", title: "核算价中心", path: "/finance/cost-accounting-center", pageCode: "finance-cost-accounting-center" },
      { key: "finance-expense-details", title: "费用明细", path: "/finance/expense-details", pageCode: "finance-expense-details" },
      { key: "finance-profit-analysis", title: "利润分析", path: "/finance/profit-analysis", pageCode: "finance-profit-analysis" },
      { key: "finance-budget-rules", title: "预算及规则", path: "/finance/budget-rules", pageCode: "finance-budget-rules" },
      { key: "finance-financial-insight", title: "主题财务状况透析", path: "/finance/financial-insight", pageCode: "finance-financial-insight" }
    ]
  },
  {
    key: "hr",
    title: "人力资源中心",
    icon: "User",
    children: [
      { key: "hr-goal-management", title: "目标管理版块", path: "/hr/goal-management", pageCode: "hr-goal-management" },
      {
        key: "hr-recruitment-management",
        title: "招聘管理",
        children: [
          { key: "hr-recruitment-requirements", title: "需求汇总", path: "/hr/requirements-summary", pageCode: "hr-recruitment-requirements" },
          { key: "hr-recruitment-progress", title: "招聘进度", path: "/hr/recruitment-progress", pageCode: "hr-recruitment-progress" }
        ]
      },
      { key: "hr-compensation-benefits", title: "薪资福利管理", path: "/hr/compensation-benefits", pageCode: "hr-compensation-benefits" },
      { key: "hr-performance-management", title: "绩效管理", path: "/hr/performance-management", pageCode: "hr-performance-management" },
      {
        key: "hr-employee-relations",
        title: "员工关系管理",
        children: [
          { key: "hr-employee-roster", title: "花名册", path: "/hr/employee-roster", pageCode: "hr-employee-roster" },
          { key: "hr-resigned-employees", title: "离职员工", path: "/hr/resigned-employees", pageCode: "hr-resigned-employees" },
          { key: "hr-employee-others", title: "其他", path: "/hr/employee-others", pageCode: "hr-employee-others" }
        ]
      },
      { key: "hr-grade-system", title: "职级体系", path: "/hr/grade-system", pageCode: "hr-grade-system" },
      { key: "hr-labor-cost-forecast", title: "人力成本预估", path: "/hr/labor-cost-forecast", pageCode: "hr-labor-cost-forecast" },
      { key: "hr-structural-labor-insight", title: "结构性人力成本透析", path: "/hr/structural-labor-insight", pageCode: "hr-structural-labor-insight" }
    ]
  },
  {
    key: "administration",
    title: "行政中心",
    icon: "OfficeBuilding",
    children: [
      { key: "administration-asset-management", title: "固定资产管理", path: "/administration/asset-management", pageCode: "administration-asset-management" },
      { key: "administration-admin-log-management", title: "日志管理", path: "/administration/admin-log-management", pageCode: "administration-admin-log-management" },
      { key: "administration-meeting-management", title: "会议管理", path: "/administration/meeting-management", pageCode: "administration-meeting-management" }
    ]
  },

  {
    key: "design",
    title: "设计中心",
    icon: "MagicStick",
    children: [
      { key: "design-design-assets", title: "设计资产库", path: "/design/design-assets", pageCode: "design-design-assets" },
      { key: "design-design-demand-management", title: "设计需求管理", path: "/design/design-demand-management", pageCode: "design-design-demand-management" },
      { key: "design-design-efficiency-analysis", title: "设计效能分析", path: "/design/design-efficiency-analysis", pageCode: "design-design-efficiency-analysis" }
    ]
  },
  {
    key: "work",
    title: "工作中心",
    icon: "Briefcase",
    children: [
      { key: "work-work-log-management", title: "日志管理", path: "/work/work-log-management", pageCode: "work-work-log-management" },
      { key: "work-work-meeting-management", title: "会议管理", path: "/work/work-meeting-management", pageCode: "work-work-meeting-management" }
    ]
  }
]

export const buttonPermissions = ["view", "create", "update", "delete", "export"]

export const flatPageMap = menuConfig.reduce((accumulator, section) => {
  const processPage = (page, sectionTitle) => {
    if (page.pageCode) {
      accumulator[page.pageCode] = {
        ...page,
        sectionTitle
      }
    }
    if (page.children) {
      page.children.forEach((childPage) => processPage(childPage, sectionTitle))
    }
  }
  section.children.forEach((page) => processPage(page, section.title))
  return accumulator
}, {})

export const routePages = menuConfig.flatMap((section) => {
  const processPage = (page) => {
    if (page.pageCode) {
      return [{
        ...page,
        sectionTitle: section.title
      }]
    } else if (page.children) {
      return page.children.flatMap((childPage) => processPage(childPage))
    }
    return []
  }
  return section.children.flatMap((page) => processPage(page))
})
