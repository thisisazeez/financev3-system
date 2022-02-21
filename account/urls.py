from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name= 'index'),
    path('', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),

    # ============================================== #

        # path('logout_user/', views.logout_user, name="logout_user"),
    path('report/', views.SimpleListReport.as_view(), name="report_gen"),
    
    path('add_student/', views.add_student, name="add_student"),
    path('add_student_save/', views.add_student_save, name="add_student_save"),
    path('manage_student/', views.manage_student, name="manage_student"),
    path('edit_student/<stu_id>/', views.edit_student, name="edit_student"),
    path('edit_student_save/', views.edit_student_save, name="edit_student_save"),
    path('delete_student/<stu_id>/', views.delete_student, name="delete_student"),

    path('add_ptype/', views.add_ptype, name="add_ptype"),
    path('add_ptype_save/', views.add_ptype_save, name="add_ptype_save"),
    path('manage_ptype/', views.manage_ptype, name="manage_ptype"),
    path('edit_ptype/<ptype_id>/', views.edit_ptype, name="edit_ptype"),
    path('edit_ptype_save/', views.edit_ptype_save, name="edit_ptype_save"),
    path('delete_ptype/<ptype_id>/', views.delete_ptype, name="delete_ptype"),


    path('add_department/', views.add_department, name="add_department"),
    path('add_department_save/', views.add_department_save, name="add_department_save"),
    path('manage_department/', views.manage_department, name="manage_department"),
    path('edit_department/<department_id>/', views.edit_department, name="edit_department"),
    path('edit_department_save/', views.edit_department_save, name="edit_department_save"),
    path('delete_department/<department_id>/', views.delete_department, name="delete_department"),

    path('add_programme/', views.add_programme, name="add_programme"),
    path('add_programme_save/', views.add_programme_save, name="add_programme_save"),
    path('manage_programme/', views.manage_programme, name="manage_programme"),
    path('edit_programme/<programme_id>/', views.edit_programme, name="edit_programme"),
    path('edit_programme_save/', views.edit_programme_save, name="edit_programme_save"),
    path('delete_programme/<programme_id>/', views.delete_programme, name="delete_programme"),


    path('manage_sop_admin/', views.manage_sop_admin, name="manage_sop_admin"),
    path('edit_sop_admin/<sop_id>/', views.edit_sop_admin, name="edit_sop_admin"),
    path('edit_sop_admin_save/', views.edit_sop_admin_save, name="edit_sop_admin_save"),
    path('delete_sop_admin/<sop_id>/', views.delete_sop_admin, name="delete_sop_admin"),

    path('add_status/', views.add_status, name="add_status"),
    path('add_status_save/', views.add_status_save, name="add_status_save"),
    path('manage_status/', views.manage_status, name="manage_status"),
    path('edit_status/<status_id>/', views.edit_status, name="edit_status"),
    path('edit_status_save/', views.edit_status_save, name="edit_status_save"),
    path('delete_status/<status_id>/', views.delete_status, name="delete_status"),

    path('add_intake/', views.add_intake, name="add_intake"),
    path('add_intake_save/', views.add_intake_save, name="add_intake_save"),
    path('manage_intake/', views.manage_intake, name="manage_intake"),
    path('edit_intake/<intake_id>/', views.edit_intake, name="edit_intake"),
    path('edit_intake_save/', views.edit_intake_save, name="edit_intake_save"),
    path('delete_intake/<intake_id>/', views.delete_intake, name="delete_intake"),

    # URLS for Staff
    # path('staff_home/', views.staff_home, name="staff_home"),
    # path('staff_profile/', views.staff_profile, name="staff_profile"),
    # path('staff_create_product/', views.create_product, name='staff_create_product'),
    # path('staff_view_product/', views.view_product, name='staff_view_product'),
    # path('staff_edit_product/<int:pk>', views.edit_product, name='staff_edit_product'),
    # path('staff_delete_product/<int:pk>/', views.delete_product, name='staff_delete_product'),
    # path('staff_create_invoice/', views.create_invoice, name='staff_create_invoice'),
    # path('staff_view_invoice/', views.view_invoice, name='staff_view_invoice'),
    # path('staff_delete_invoice/<int:pk>/', views.delete_invoice, name='staff_delete_invoice'),
    # path('staff_view_invoice_detail/<int:pk>/', views.view_invoice_detail, name='staff_view_invoice_detail'),
    path('add_sop/', views.add_sop, name="add_sop"),
    path('add_sop_save/', views.add_sop_save, name="add_sop_save"),
    path('manage_sop/', views.manage_sop, name="manage_sop"),
    path('edit_sop/<sop_id>/', views.edit_sop, name="edit_sop"),
    path('edit_sop_save/', views.edit_sop_save, name="edit_sop_save"),
    path('delete_sop/<sop_id>/', views.delete_sop, name="delete_sop"),
    
    
    # URSL for Finance
    path('search_/', views.SearchResultsView.as_view(), name="finance_search_result"),
    path('search_stu/', views.search, name="finance_search"),
    # path('finance_home/', views.finance_home, name="finance_home"),
    # path('finance_profile/', views.finance_profile, name="finance_profile"),
    path('payslip/<int:pk>/', views.payslip, name='dashboard_payslip'),
    # path('invoices/create',views.createInvoice, name='create-invoice'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('view_invoice/', views.view_invoice, name='view_invoice'),
    path('delete_invoice/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('finance_dashboard/venue_pdf/', views.venue_pdf, name='venue_pdf'),
    path('view_invoice_detail/<int:pk>/', views.view_invoice_detail, name='view_invoice_detail'),
    path('add_reciept/<student_id>/', views.add_reciept, name="add_reciept"),
    path('add_reciept_save/', views.add_reciept_save, name="add_reciept_save"),
    path('manage_reciept/', views.manage_reciept, name="manage_reciept"),
    path('edit_reciept/<reciept_id>/', views.edit_reciept, name="edit_reciept"),
    path('create_pdf/<reciept_id>/', views.pdf_report_create, name="pdf_report_create"),
    path('_pdf/<reciept_id>/', views.pdf__create, name="pdf__create"),
    path('edit_reciept_save/', views.edit_reciept_save, name="edit_reciept_save"),
    path('delete_reciept/<reciept_id>/', views.delete_reciept, name="delete_reciept"),
]