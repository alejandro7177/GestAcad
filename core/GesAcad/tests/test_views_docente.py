from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse


class TestDocenteViews(TestCase):

    # =====================================
    # docente_controller
    # =====================================

    def test_docente_controller_sin_login(self):

        response = self.client.get(
            reverse("docente")
        )

        self.assertRedirects(
            response,
            reverse("login")
        )

    def test_docente_controller_usuario_no_docente(self):

        session = self.client.session
        session["user_id"] = 1
        session["perfil_id"] = "Alumno"
        session.save()

        response = self.client.get(
            reverse("docente")
        )

        self.assertRedirects(
            response,
            reverse("login")
        )

    @patch("GesAcad.views.Inscripcion_Materia")
    @patch("GesAcad.views.Usuarios")
    def test_docente_controller_ok(
        self,
        mock_usuarios,
        mock_inscripcion,
    ):

        docente = Mock()

        mock_usuarios.get.return_value = docente

        mock_inscripcion.materias_alta.return_value = []

        session = self.client.session
        session["user_id"] = 1
        session["perfil_id"] = "Docente"
        session.save()

        response = self.client.get(
            reverse("docente")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "docente.html"
        )

        mock_inscripcion.materias_alta.assert_called_once_with(
            usuario=docente
        )

    # =====================================
    # docente_inscriptos GET
    # =====================================

    @patch("GesAcad.views.Materias")
    @patch("GesAcad.views.Inscripcion_Materia")
    @patch("GesAcad.views.Usuarios")
    def test_docente_inscriptos_get(
        self,
        mock_usuarios,
        mock_inscripcion,
        mock_materias,
    ):

        docente = Mock()
        materia = Mock()

        mock_usuarios.get.return_value = docente
        mock_materias.get.return_value = materia

        mock_inscripcion.inscriptos_por_materia.return_value = []

        session = self.client.session
        session["user_id"] = 1
        session["perfil_id"] = "Docente"
        session.save()

        response = self.client.get(
            reverse(
                "inscriptos",
                args=[1]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "inscriptos.html"
        )

    # =====================================
    # docente_inscriptos POST
    # =====================================

    @patch("GesAcad.views.Materias")
    @patch("GesAcad.views.Inscripcion_Materia")
    @patch("GesAcad.views.Usuarios")
    def test_docente_inscriptos_post_actualiza_estado(
        self,
        mock_usuarios,
        mock_inscripcion,
        mock_materias,
    ):

        docente = Mock()
        materia = Mock()

        inscripto = Mock()
        inscripto.id_inscripcion_materia = 10

        mock_usuarios.get.return_value = docente
        mock_materias.get.return_value = materia

        mock_inscripcion.inscriptos_por_materia.return_value = [
            inscripto
        ]

        session = self.client.session
        session["user_id"] = 1
        session["perfil_id"] = "Docente"
        session.save()

        response = self.client.post(
            reverse(
                "inscriptos",
                args=[1]
            ),
            {
                "estado_10": "Aprobado"
            }
        )

        self.assertEqual(
            inscripto.estado,
            "Aprobado"
        )

        inscripto.save.assert_called_once()

        self.assertEqual(
            response.status_code,
            302
        )

    # =====================================
    # docente_inscriptos POST sin alumnos
    # =====================================

    @patch("GesAcad.views.Materias")
    @patch("GesAcad.views.Inscripcion_Materia")
    @patch("GesAcad.views.Usuarios")
    def test_docente_inscriptos_post_sin_inscriptos(
        self,
        mock_usuarios,
        mock_inscripcion,
        mock_materias,
    ):

        docente = Mock()
        materia = Mock()

        mock_usuarios.get.return_value = docente
        mock_materias.get.return_value = materia

        mock_inscripcion.inscriptos_por_materia.return_value = []

        session = self.client.session
        session["user_id"] = 1
        session["perfil_id"] = "Docente"
        session.save()

        response = self.client.post(
            reverse(
                "inscriptos",
                args=[1]
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

    # =====================================
    # acceso de alumno a inscriptos
    # =====================================

    def test_docente_inscriptos_usuario_no_docente(self):

        session = self.client.session
        session["user_id"] = 1
        session["perfil_id"] = "Alumno"
        session.save()

        response = self.client.get(
            reverse(
                "inscriptos",
                args=[1]
            )
        )

        self.assertRedirects(
            response,
            reverse("login")
        )
