from django.test import TestCase

from GesAcad.models import (
    Perfiles,
    Usuarios,
    Materias,
    Inscripcion_Materia,
)


class TestInscripcionMateria(TestCase):

    def setUp(self):
        self.perfil_alumno = Perfiles.objects.create(
            descripcion="Alumno"
        )

        self.perfil_docente = Perfiles.objects.create(
            descripcion="Docente"
        )

        self.alumno = Usuarios.objects.create(
            nombre="Juan",
            apellido="Perez",
            dni="12345678",
            email="juan@test.com",
            password_hash="hash",
            id_perfil=self.perfil_alumno,
        )

        self.docente = Usuarios.objects.create(
            nombre="Ana",
            apellido="Gomez",
            dni="87654321",
            email="ana@test.com",
            password_hash="hash",
            id_perfil=self.perfil_docente,
        )

        self.materia_1 = Materias.objects.create(
            nombre="Programacion I",
            anio=1,
            cuatrimestre=1,
        )

        self.materia_2 = Materias.objects.create(
            nombre="Base de Datos",
            anio=2,
            cuatrimestre=1,
        )

    # --------------------------------------------------
    # materias_alta
    # --------------------------------------------------

    def test_materias_alta_devuelve_solo_estado_alta(self):
        Inscripcion_Materia.objects.create(
            id_usuario=self.alumno,
            id_materia=self.materia_1,
            estado="Alta",
        )

        Inscripcion_Materia.objects.create(
            id_usuario=self.alumno,
            id_materia=self.materia_2,
            estado="Baja",
        )

        resultado = Inscripcion_Materia.materias_alta(
            self.alumno
        )

        self.assertEqual(resultado.count(), 1)
        self.assertEqual(
            resultado.first().id_materia,
            self.materia_1,
        )

    # --------------------------------------------------
    # id_materias_alta
    # --------------------------------------------------

    def test_id_materias_alta_devuelve_ids_correctos(self):
        Inscripcion_Materia.objects.create(
            id_usuario=self.alumno,
            id_materia=self.materia_1,
            estado="Alta",
        )

        Inscripcion_Materia.objects.create(
            id_usuario=self.alumno,
            id_materia=self.materia_2,
            estado="Baja",
        )

        ids = list(
            Inscripcion_Materia.id_materias_alta(
                self.alumno
            )
        )

        self.assertEqual(
            ids,
            [self.materia_1.id_materia]
        )

    # --------------------------------------------------
    # dar_alta_baja_Inscripcion_Materia
    # --------------------------------------------------

    def test_crea_inscripcion_en_alta_si_no_existe(self):
        resultado = (
            Inscripcion_Materia
            .dar_alta_baja_Inscripcion_Materia(
                self.materia_1,
                self.alumno,
            )
        )

        self.assertTrue(resultado)

        inscripcion = (
            Inscripcion_Materia.objects.get(
                id_usuario=self.alumno,
                id_materia=self.materia_1,
            )
        )

        self.assertEqual(
            inscripcion.estado,
            "Alta",
        )

    def test_cambia_de_alta_a_baja(self):
        inscripcion = (
            Inscripcion_Materia.objects.create(
                id_usuario=self.alumno,
                id_materia=self.materia_1,
                estado="Alta",
            )
        )

        (
            Inscripcion_Materia
            .dar_alta_baja_Inscripcion_Materia(
                self.materia_1,
                self.alumno,
            )
        )

        inscripcion.refresh_from_db()

        self.assertEqual(
            inscripcion.estado,
            "Baja",
        )

    def test_cambia_de_baja_a_alta(self):
        inscripcion = (
            Inscripcion_Materia.objects.create(
                id_usuario=self.alumno,
                id_materia=self.materia_1,
                estado="Baja",
            )
        )

        (
            Inscripcion_Materia
            .dar_alta_baja_Inscripcion_Materia(
                self.materia_1,
                self.alumno,
            )
        )

        inscripcion.refresh_from_db()

        self.assertEqual(
            inscripcion.estado,
            "Alta",
        )

    def test_cambia_de_aprobado_a_alta(self):
        inscripcion = (
            Inscripcion_Materia.objects.create(
                id_usuario=self.alumno,
                id_materia=self.materia_1,
                estado="Aprobado",
            )
        )

        (
            Inscripcion_Materia
            .dar_alta_baja_Inscripcion_Materia(
                self.materia_1,
                self.alumno,
            )
        )

        inscripcion.refresh_from_db()

        self.assertEqual(
            inscripcion.estado,
            "Alta",
        )

    # --------------------------------------------------
    # inscriptos_por_materia
    # --------------------------------------------------

    def test_inscriptos_por_materia_excluye_docente(self):
        Inscripcion_Materia.objects.create(
            id_usuario=self.docente,
            id_materia=self.materia_1,
            estado="Alta",
        )

        alumno_inscripto = Usuarios.objects.create(
            nombre="Pedro",
            apellido="Lopez",
            dni="11222333",
            email="pedro@test.com",
            password_hash="hash",
            id_perfil=self.perfil_alumno,
        )

        Inscripcion_Materia.objects.create(
            id_usuario=alumno_inscripto,
            id_materia=self.materia_1,
            estado="Alta",
        )

        resultado = (
            Inscripcion_Materia
            .inscriptos_por_materia(
                self.materia_1,
                self.docente,
            )
        )

        self.assertEqual(resultado.count(), 1)

        self.assertEqual(
            resultado.first().id_usuario,
            alumno_inscripto,
        )

    def test_inscriptos_por_materia_no_muestra_bajas(self):
        alumno_1 = Usuarios.objects.create(
            nombre="Pedro",
            apellido="Lopez",
            dni="11111111",
            email="pedro1@test.com",
            password_hash="hash",
            id_perfil=self.perfil_alumno,
        )

        alumno_2 = Usuarios.objects.create(
            nombre="Carlos",
            apellido="Diaz",
            dni="22222222",
            email="carlos@test.com",
            password_hash="hash",
            id_perfil=self.perfil_alumno,
        )

        Inscripcion_Materia.objects.create(
            id_usuario=alumno_1,
            id_materia=self.materia_1,
            estado="Alta",
        )

        Inscripcion_Materia.objects.create(
            id_usuario=alumno_2,
            id_materia=self.materia_1,
            estado="Baja",
        )

        resultado = (
            Inscripcion_Materia
            .inscriptos_por_materia(
                self.materia_1,
                self.docente,
            )
        )

        self.assertEqual(resultado.count(), 1)

        self.assertEqual(
            resultado.first().id_usuario,
            alumno_1,
        )

    def test_inscriptos_por_materia_incluye_aprobados_y_desaprobados(self):
        alumno_1 = Usuarios.objects.create(
            nombre="Pedro",
            apellido="Lopez",
            dni="33333333",
            email="pedro3@test.com",
            password_hash="hash",
            id_perfil=self.perfil_alumno,
        )

        alumno_2 = Usuarios.objects.create(
            nombre="Carlos",
            apellido="Diaz",
            dni="44444444",
            email="carlos4@test.com",
            password_hash="hash",
            id_perfil=self.perfil_alumno,
        )

        Inscripcion_Materia.objects.create(
            id_usuario=alumno_1,
            id_materia=self.materia_1,
            estado="Aprobado",
        )

        Inscripcion_Materia.objects.create(
            id_usuario=alumno_2,
            id_materia=self.materia_1,
            estado="Desaprobado",
        )

        resultado = (
            Inscripcion_Materia
            .inscriptos_por_materia(
                self.materia_1,
                self.docente,
            )
        )

        self.assertEqual(resultado.count(), 2)
