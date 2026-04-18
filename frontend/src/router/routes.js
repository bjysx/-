import AppLayout from "@/layout/AppLayout.vue"
import GenericPageView from "@/views/modules/GenericPageView.vue"
import HomeView from "@/views/dashboard/HomeView.vue"
import LoginView from "@/views/login/LoginView.vue"
import ForbiddenView from "@/views/errors/ForbiddenView.vue"
import NotFoundView from "@/views/errors/NotFoundView.vue"
import ProductListView from "@/views/product/ProductListView.vue"
import WhiteLabelWorkflowView from "@/views/product/WhiteLabelWorkflowView.vue"
import DoubleStarWorkflowView from "@/views/product/DoubleStarWorkflowView.vue"
import CrossBorderWorkflowView from "@/views/product/CrossBorderWorkflowView.vue"
import EmployeeRelationView from "@/views/hr/EmployeeRelationView.vue"
import RecruitmentManagementView from "@/views/hr/RecruitmentManagementView.vue"
import { routePages } from "@/config/menu"

export const protectedRoutes = [
  {
    path: "/",
    component: AppLayout,
    redirect: "/dashboard/home",
    children: [
      {
        path: "/dashboard/home",
        name: "dashboard-home",
        component: HomeView,
        meta: {
          title: "首页",
          section: "工作台"
        }
      },
      ...routePages.map((page) => ({
        path: page.path,
        name: page.pageCode,
        component: page.pageCode === "product-product-list" ? ProductListView : 
                  page.pageCode === "product-white-label" ? CrossBorderWorkflowView : 
                  page.pageCode === "product-double-star" ? WhiteLabelWorkflowView : 
                  page.pageCode === "hr-employee-roster" ? EmployeeRelationView : 
                  page.pageCode === "hr-resigned-employees" ? GenericPageView : 
                  page.pageCode === "hr-employee-others" ? GenericPageView :
                  page.pageCode === "hr-recruitment-management" ? RecruitmentManagementView :
                  GenericPageView,
        meta: {
          title: page.title,
          section: page.sectionTitle,
          permissionKey: page.pageCode,
          pageCode: page.pageCode
        }
      }))
    ]
  }
]

export const routes = [
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: {
      public: true,
      title: "登录"
    }
  },
  {
    path: "/forbidden",
    name: "forbidden",
    component: ForbiddenView,
    meta: {
      title: "无权限"
    }
  },
  ...protectedRoutes,
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: NotFoundView,
    meta: {
      title: "页面不存在",
      public: true
    }
  }
]
