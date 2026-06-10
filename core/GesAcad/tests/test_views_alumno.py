from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse


class TestAlumnoViews(TestCase):

    # =====================================
    # alumno_controller
    # =====================================

    @patch("GesAcad.views.Alumno")
    @patch("GesAcad.views.Materia")
    def test_alumno_controller_ok(
        self,
        mock_materia,
        mock_alumno,
    ):
        alumno = Mock()

        alumno.obtener_carreras.return_value = [
            (1, "Sistemas")
        ]

        alumno.ids_inscripciones_materia.return_value = [
            1,
            2,
        ]

        mock_alumno.get.return_value = alumno
        

        materia1 = Mock(
            id_materia=1,
            nombre="Programación I"
        )

        materia2 = Mock(
            id_materia=2,
            nombre="Base de Datos"
        )

        mock_materia.obtener_materias_agrupadas.return_value = {
            1: [materia1],
            2: [materia2],
        }

        session = self.client.session
        session["user_id"] = 1
        session.save()

        response = self.client.get(
            reverse("alumno")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "alumno.html",
        )

    # =====================================
    # login_valid
    # =====================================

    def test_alumno_controller_sin_login(self):

        response = self.client.get(
            reverse("alumno")
        )

        self.assertRedirects(
            response,
            reverse("login"),
        )

    # =====================================
    # toggle_inscripcion
    # =====================================

    @patch("GesAcad.views.InscripcionMateria")
    @patch("GesAcad.views.Alumno")
    @patch("GesAcad.views.Materia")
    def test_toggle_inscripcion(
        self,
        mock_materia,
        mock_alumno,
        mock_inscripcion,
    ):

        materia = Mock()
        materia.id_materia = 10

        alumno = Mock()
        alumno.id_usuario = 20

        mock_materia.get.return_value = materia
        mock_alumno.get.return_value = alumno

        session = self.client.session
        session["user_id"] = 20
        session.save()

        response = self.client.get(
            reverse(
                "toggle_inscripcion",
                args=[10]
            ) + "?carrera=1"
        )

        mock_inscripcion.alta_baja_inscripcion.assert_called_once_with(
            20,
            10,
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    @patch("GesAcad.views.InscripcionMateria")
    @patch("GesAcad.views.Alumno")
    @patch("GesAcad.views.Materia")
    def test_toggle_inscripcion_materia_inexistente(
        self,
        mock_materia,
        mock_alumno,
        mock_inscripcion,
    ):

        mock_materia.get.return_value = None

        session = self.client.session
        session["user_id"] = 20
        session.save()

        self.client.get(
            reverse(
                "toggle_inscripcion",
                args=[10]
            )
        )

        mock_inscripcion.alta_baja_inscripcion.assert_not_called()

    @patch("GesAcad.views.InscripcionMateria")
    @patch("GesAcad.views.Alumno")
    @patch("GesAcad.views.Materia")
    def test_toggle_inscripcion_usuario_inexistente(
        self,
        mock_materia,
        mock_alumno,
        mock_inscripcion,
    ):

        mock_materia.get.return_value = Mock()
        mock_alumno.get.return_value = None

        session = self.client.session
        session["user_id"] = 20
        session.save()

        self.client.get(
            reverse(
                "toggle_inscripcion",
                args=[10]
            )
        )

        mock_inscripcion.alta_baja_inscripcion.assert_not_called()

    # =====================================
    # mostrar_historial
    # =====================================

    @patch("GesAcad.views.Carreras")
    @patch("GesAcad.views.Usuarios")
    @patch("GesAcad.views.Inscripcion_Examen")
    def test_historial(
        self,
        mock_inscripcion_examen,
        mock_usuarios,
        mock_carreras,
    ):

        usuario = Mock()
        carrera = Mock()

        mock_usuarios.get.return_value = usuario

        mock_carreras.carreras_alumno.return_value = [
            carrera
        ]

        mock_carreras.get.return_value = carrera

        mock_inscripcion_examen.obtener_examenes_agrupados.return_value = {
            "Programacion": []
        }

        session = self.client.session
        session["user_id"] = 1
        session.save()

        response = self.client.get(
            reverse("historial")
            + "?carrera=1"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "historial.html",
        )

        mock_inscripcion_examen.obtener_examenes_agrupados.assert_called_once()
