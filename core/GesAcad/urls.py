from django.urls import path

from .import views


urlpatterns = [
    path("login/", views.login_controler, name="login"),
    path("logout/", views.logout_controller, name="logout"),
    path("alumno/", views.alumno_controller, name="alumno"),
    path("alumno/incribir_materia/<int:materia_id>/", views.toggle_inscripcion, name="toggle_inscripcion"),
    path("alumno/historial/", views.mostrar_historial, name="historial"),
    path("docente/", views.docente_controller, name="docente"),
    path("docente/inscriptos/<int:materia_id>/", views.docente_inscriptos, name="inscriptos")
]
