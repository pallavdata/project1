from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/makeofferletter/", views.makeformoffer, name="makeformoffer"),
    path("admin/offerletter/", views.formoffer, name="formoffer"),
    path("admin/makeformcertificate/", views.makeformcertificate, name="makeformcertificate"),
    path("admin/certificate/", views.formcertificate, name="formcertificate"),
    path("admin/htmlcertificate/", views.certificate, name="certificate"),
    path("admin/assignment/<str:id>/", views.sendassignment, name="sendassignment"),
    path("admin/interviewDone/<str:id>/", views.interviewDone, name="interviewDone"),
    path("admin/assignmentDone/<str:id>/", views.assignmentDone, name="assignmentDone"),
    path("admin/send-assignment/<str:id>/", views.sendassignmentlast, name="sendassignmentlast"),
    path("admin/assignment/", views.assignmentMail, name="assignment"),
    path("admin/email/temp/", views.mail, name="mail"),
    path("admin/add-type/", views.add_type, name="add_type"),
    path("admin/delete-type/", views.delete_type, name="delete_type"),
    path("assign-save/", views.assign_save, name="assign-save"),
    path("success", views.success, name="success"),
    path("nosuccess/", views.nosuccess, name="nosuccess"),
    path("", views.home, name="home"),
    path("admin/", views.admin, name="admin"),
    path("admin/add/", views.admin_add, name="admin_add"),
    path("admin/hire/<str:id>/", views.hire, name="hire"),
    path("job_details/<str:myid>/", views.job_details, name="job_details"),
    path("apply_job/<str:myid>/", views.apply_job, name="apply_job"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("question/", views.question_edit_home, name="question_edit_home"),
    path("question/add/<str:myid>/", views.question_edit_add, name="question_edit_add"),
    path("question/delete/<str:myid>/", views.question_edit_delete, name="question_edit_delete"),
    path("question/delete/<str:myid>/<str:delid>/", views.question_edit_delete_main, name="question_edit_delete_main"),
    path("question/update/<str:myid>/", views.question_edit_update, name="question_edit_update"),
    path("question/update/<str:myid>/<str:delid>/", views.question_edit_update_main, name="question_edit_update_main"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)