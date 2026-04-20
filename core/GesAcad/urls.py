from django.urls import path

from .import views


urlpatterns = [
    path("login/", views.login_controler, name="login"),
    path("alumno/", views.alumno_controller, name="alumno"),
    path("alumno/incribir_materia/<int:materia_id>/", views.toggle_inscripcion, name="toggle_inscripcion")
]
