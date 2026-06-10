from datetime import date

from django.test import TestCase

from GesAcad.models import (
    Perfiles,
    Usuarios,
    Carreras,
    Materias,
    Carrera_Materia,
    Examenes,
    Inscripcion_Carrera,
    Inscripcion_Examen,
)


class TestModels(TestCase):

    def setUp(self):
        self.perfil = Perfiles.objects.create(
            descripcion="Alumno"
        )

        self.usuario = Usuarios.objects.create(
            nombre="Juan",
            apellido="Perez",
            dni="12345678",
            email="juan@test.com",
            password_hash="hash",
            id_perfil=self.perfil,
        )

        self.carrera = Carreras.objects.create(
            nombre="Ingeniería en Sistemas"
        )

        self.materia = Materias.objects.create(
            nombre="Programación I",
            anio=1,
            cuatrimestre=1,
        )

    # =====================================
    # __str__
    # =====================================

    def test_perfil_str(self):
        self.assertEqual(
            str(self.perfil),
            "Alumno"
        )

    def test_usuario_str(self):
        self.assertEqual(
            str(self.usuario),
            "Juan Perez"
        )

    def test_carrera_str(self):
        self.assertEqual(
            str(self.carrera),
            "Ingeniería en Sistemas"
        )

    def test_materia_str(self):
        self.assertEqual(
            str(self.materia),
            "Programación I"
        )

    # =====================================
    # Usuarios.get
    # =====================================

    def test_usuario_get_existente(self):
        usuario = Usuarios.get(
            self.usuario.id_usuario
        )

        self.assertEqual(
            usuario.id_usuario,
            self.usuario.id_usuario
        )

    def test_usuario_get_inexistente(self):
        usuario = Usuarios.get(9999)

        self.assertIsNone(usuario)

    # =====================================
    # Carreras.get
    # =====================================

    def test_carrera_get_existente(self):
        carrera = Carreras.get(
            self.carrera.id_carrera
        )

        self.assertEqual(
            carrera.nombre,
            self.carrera.nombre
        )

    def test_carrera_get_inexistente(self):
        carrera = Carreras.get(9999)

        self.assertIsNone(carrera)

    # =====================================
    # Carreras.carreras_alumno
    # =====================================

    def test_carreras_alumno(self):

        Inscripcion_Carrera.objects.create(
            id_usuario=self.usuario,
            id_carrera=self.carrera,
            estado="Alta"
        )

        carreras = Carreras.carreras_alumno(
            self.usuario
        )

        self.assertEqual(
            carreras.count(),
            1
        )

        self.assertEqual(
            carreras.first(),
            self.carrera
        )

    # =====================================
    # Examenes
    # =====================================

    def test_examen_str(self):

        examen = Examenes.objects.create(
            fecha=date(2026, 6, 1),
            id_materia=self.materia,
        )

        self.assertEqual(
            str(examen),
            "Programación I - 2026-06-01"
        )

    # =====================================
    # Inscripcion_Examen
    # =====================================

    def test_inscripcion_examen_str(self):

        examen = Examenes.objects.create(
            fecha=date(2026, 6, 1),
            id_materia=self.materia,
        )

        inscripcion = (
            Inscripcion_Examen.objects.create(
                id_examen=examen,
                id_usuario=self.usuario,
                nota=8,
                estado="Aprobado",
            )
        )

        self.assertEqual(
            str(inscripcion),
            f"8 - {examen}"
        )

    # =====================================
    # obtener_examenes_agrupados
    # =====================================

    def test_obtener_examenes_agrupados(self):

        Carrera_Materia.objects.create(
            id_carrera=self.carrera,
            id_materia=self.materia,
        )

        examen1 = Examenes.objects.create(
            fecha=date(2026, 6, 1),
            id_materia=self.materia,
        )

        examen2 = Examenes.objects.create(
            fecha=date(2026, 7, 1),
            id_materia=self.materia,
        )

        Inscripcion_Examen.objects.create(
            id_examen=examen1,
            id_usuario=self.usuario,
            nota=8,
            estado="Aprobado",
        )

        Inscripcion_Examen.objects.create(
            id_examen=examen2,
            id_usuario=self.usuario,
            nota=10,
            estado="Aprobado",
        )

        resultado = (
            Inscripcion_Examen
            .obtener_examenes_agrupados(
                self.usuario,
                self.carrera,
            )
        )

        self.assertEqual(
            len(resultado),
            1
        )

        self.assertIn(
            self.materia,
            resultado
        )

        self.assertEqual(
            len(resultado[self.materia]),
            2
        )
