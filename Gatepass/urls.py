"""
URL configuration for Gatepass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gpass import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.show),
    path('student_register',views.student_register),
    path('login', views.login, name='login'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('student_home', views.student_home, name='student_home'),
    path('logout', views.logout, name='logout'),
    path('staff_register', views.staff_register, name='staff_register'),
    path('admin_view_students', views.admin_view_students, name='admin_view_students'),
    path('admin_view_staff', views.admin_view_staff, name='admin_view_staff'),
    path('view_profile',views.view_profile,name='view_profile'),
    path('edit-profile/<int:stud_id>', views.edit_profile, name='edit_profile'),
    path('search', views.search_form, name='search_form'),
    path('search-result', views.search_result, name='search_result'),
    path('send_request', views.send_request, name='send_request'),
    path('view_requests', views.view_requests, name='view_requests'),
    path('student_view_requests', views.student_view_requests, name='student_view_requests'),
    path('approve/<int:request_id>', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>', views.reject_request, name='reject_request'),
    path('view_approved_gate_pass',views.view_approved_gate_pass,name='view_approved_gate_pass'),
    path('track_student_movement',views.track_student_movement,name='track_student_movement'),
    path('mark-out/<int:request_id>', views.mark_student_out, name='mark_student_out'),
    path('mark-in/<int:request_id>', views.mark_student_in, name='mark_student_in'),
    path('nfc_scan', views.nfc_scan, name='nfc_scan'),
    path('staff_home', views.staff_home, name='staff_home'),
    path('staff_view_requests', views.staff_view_requests, name='staff_view_requests'),
    path('admin_view_gate_pass_history', views.admin_view_gate_pass_history, name='admin_view_gate_pass_history'),
    path('view_gate_pass_history', views.view_gate_pass_history, name='gate_pass_history'),
    path('assign_nfc_tag', views.assign_nfc_tag, name='assign_nfc_tag'),
    path('view_nfc_tags', views.view_nfc_tags, name='view_nfc_tags'),
    path('remove_nfc_tag/<int:tag_id>', views.remove_nfc_tag, name='remove_nfc_tag'),
    path('out_students_status', views.out_students_status, name='out_students_status'),
    path('get_latest_movement', views.get_latest_movement, name='get_latest_movement'),
    path('api/nfc_scan', views.api_nfc_scan, name='api_nfc_scan'),
    path('gate_open/check_student.php', views.api_nfc_scan, name='api_nfc_scan_legacy'),
]
