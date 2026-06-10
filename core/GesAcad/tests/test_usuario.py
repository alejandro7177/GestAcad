from django.contrib.auth.hashers import make_password
from django.test import TestCase

from GesAcad.models import (
    Perfiles,
    Usuarios,
    Materias,
    Inscripcion_Materia,
)

from GesAcad.usuario import (
    Usuario,
    Alumno,
    Docente,
)


class TestUsuario(TestCase):

    def setUp(self):
        self.perfil_alumno = Perfiles.objects.create(
            descripcion="Alumno"
        )

        self.perfil_docente = Perfiles.objects.create(
            descripcion="Docente"
        )

        self.alumno_model = Usuarios.objects.create(
            nombre="Juan",
            apellido="Perez",
            dni="12345678",
            email="juan@test.com",
            password_hash=make_password("123456"),
            id_perfil=self.perfil_alumno,
        )

        self.docente_model = Usuarios.objects.create(
            nombre="Ana",
            apellido="Gomez",
            dni="87654321",
            email="ana@test.com",
            password_hash=make_password("654321"),
            id_perfil=self.perfil_docente,
        )

    # ==========================
    # Usuario.login()
    # ==========================

    def test_login_alumno_correcto(self):

        usuario, error = Usuario.login(
            email="juan@test.com",
            password="123456"
        )

        self.assertEqual(error, {})
        self.assertIsInstance(usuario, Alumno)

    def test_login_docente_correcto(self):

        usuario, error = Usuario.login(
            email="ana@test.com",
            password="654321"
        )

        self.assertEqual(error, {})
        self.assertIsInstance(usuario, Docente)

    def test_login_password_incorrecta(self):

        usuario, error = Usuario.login(
            email="juan@test.com",
            password="incorrecta"
        )

        self.assertIsNone(usuario)

        self.assertEqual(
            error["error"],
            1
        )

    def test_login_usuario_no_existe(self):

        usuario, error = Usuario.login(
            email="noexiste@test.com",
            password="123456"
        )

        self.assertIsNone(usuario)

        self.assertEqual(
            error["error"],
            3
        )

    # ==========================
    # nombreCompleto()
    # ==========================

    def test_nombre_completo_alumno(self):

        alumno = Alumno.get(
            self.alumno_model.id_usuario
        )

        self.assertEqual(
            alumno.nombreCompleto(),
            "Juan Perez"
        )

    def test_nombre_completo_docente(self):

        docente = Docente.get(
            self.docente_model.id_usuario
        )

        self.assertEqual(
            docente.nombreCompleto(),
            "Ana Gomez"
        )

    # ==========================
    # Alumno.get()
    # ==========================

    def test_get_alumno_correcto(self):

        alumno = Alumno.get(
            self.alumno_model.id_usuario
        )

        self.assertIsNotNone(alumno)

        self.assertEqual(
            alumno.email,
            "juan@test.com"
        )

    def test_get_alumno_devuelve_none_si_es_docente(self):

        alumno = Alumno.get(
            self.docente_model.id_usuario
        )

        self.assertIsNone(alumno)

    def test_get_alumno_inexistente(self):

        alumno = Alumno.get(9999)

        self.assertIsNone(alumno)

    # ==========================
    # Docente.get()
    # ==========================

    def test_get_docente_correcto(self):

        docente = Docente.get(
            self.docente_model.id_usuario
        )

        self.assertIsNotNone(docente)

        self.assertEqual(
            docente.email,
            "ana@test.com"
        )

    def test_get_docente_devuelve_none_si_es_alumno(self):

        docente = Docente.get(
            self.alumno_model.id_usuario
        )

        self.assertIsNone(docente)

    def test_get_docente_inexistente(self):

        docente = Docente.get(9999)

        self.assertIsNone(docente)

    # ==========================
    # inscripciones_materia()
    # ==========================

    def test_inscripciones_materia_solo_alta(self):

        materia1 = Materias.objects.create(
            nombre="Programacion",
            anio=1,
            cuatrimestre=1
        )

        materia2 = Materias.objects.create(
            nombre="Base de Datos",
            anio=2,
            cuatrimestre=1
        )

        Inscripcion_Materia.objects.create(
            id_usuario=self.alumno_model,
            id_materia=materia1,
            estado="Alta"
        )

        Inscripcion_Materia.objects.create(
            id_usuario=self.alumno_model,
            id_materia=materia2,
            estado="Baja"
        )

        alumno = Alumno.get(
            self.alumno_model.id_usuario
        )

        resultado = alumno.inscripciones_materia()

        self.assertEqual(
            resultado.count(),
            1
        )

    # ==========================
    # ids_inscripciones_materia()
    # ==========================

    def test_ids_inscripciones_materia(self):

        materia = Materias.objects.create(
            nombre="Programacion",
            anio=1,
            cuatrimestre=1
        )

        Inscripcion_Materia.objects.create(
            id_usuario=self.alumno_model,
            id_materia=materia,
            estado="Alta"
        )

        alumno = Alumno.get(
            self.alumno_model.id_usuario
        )

        ids = list(
            alumno.ids_inscripciones_materia()
        )

        self.assertEqual(
            ids,
            [materia.id_materia]
        )
