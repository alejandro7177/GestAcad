from django.contrib import messages
from django.contrib.auth import hashers
from django.shortcuts import get_object_or_404, redirect, render

from .academico import Materia
from .inscripciones import InscripcionMateria
from .observer import SujetoConcreto
from .usuario import Usuario, Alumno, Docente
from .models import (
    Inscripcion_Examen,
    Inscripcion_Materia,
    Materias,
    Usuarios,
    Carreras,
)

def login_valid(func):
    def wrapper(request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")
        return func(request, *args, **kwargs)

    return wrapper


def docente_valid(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get("perfil_id") != "Docente":
            return redirect("login")
        return func(request, *args, **kwargs)

    return wrapper
#--------------------- LOGIN ------------------------------------------

def login_controler(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user, error= Usuario.login(email=username, password=password)
        if error:
            return render(request, "login.html", error)
        if user:
            request.session["user_id"] = user.id_usuario
            request.session["perfil_id"] = user.obtenerPerfil()
            if user.obtenerPerfil() == "Alumno":
                return redirect("alumno")
            if user.obtenerPerfil() == "Docente":
                return redirect("docente")
    return render(request, "login.html")

def logout_controller(request):
    request.session.flush()
    return redirect("login")

#------------------------ DOCENTE --------------------------------------

@login_valid
@docente_valid
def docente_controller(request):
    usuario = Usuarios.get(request.session.get("user_id"))
    materias = Inscripcion_Materia.materias_alta(usuario=usuario)
    return render(request, "docente.html", {"materias": materias})


@login_valid
@docente_valid
def docente_inscriptos(request, materia_id):
    docente = Usuarios.get(id=request.session.get("user_id"))
    materia = Materia.get(id=materia_id)
    inscriptos_materia = Inscripcion_Materia.inscriptos_por_materia(
        materia=materia_id, usuario=docente
    )
    if request.session.get("perfil_id") != "Docente":
        return render(request, "inscriptos.html", {"inscriptos": None})
    if request.method == "POST":
        if not inscriptos_materia:
            return redirect("inscriptos", materia_id=materia_id)
        for inscripto in inscriptos_materia:
            estado = request.POST.get(f"estado_{inscripto.id_inscripcion_materia}")
            if estado:
                inscripto.estado = estado
                inscripto.save()
        return redirect("inscriptos", materia_id=materia_id)
    return render(
        request,
        "inscriptos.html",
        {"inscriptos": inscriptos_materia, "materia": materia},
    )
#-----------------------------ALUMNO-------------------------------------------
@login_valid
def alumno_controller(request):
    _alumno = Alumno.get(request.session.get("user_id"))

    if _alumno:
        carreras = _alumno.obtener_carreras()
    id_carrera = request.GET.get("carrera")

    materias_agrupadas = Materia.obtener_materias_agrupadas(id_carrera)
    inscripciones_alta = _alumno.ids_inscripciones_materia()
    print(f"{inscripciones_alta=}")

    return render(
        request,
        "alumno.html",
        {
            "materias_agrupadas": materias_agrupadas,
            "inscriptas_alta": inscripciones_alta,
            "carreras": carreras,
            "carrera_seleccionada": id_carrera
        },
    )
@login_valid
def toggle_inscripcion(request, materia_id):
    materia = Materia.get(materia_id)
    usuario = Alumno.get(request.session.get("user_id"))
    id_carrera = request.GET.get("carrera")
    print(f"{usuario=}")
    print(f"{materia=}")
    if materia and usuario:
        res = InscripcionMateria.alta_baja_inscripcion(
            usuario.id_usuario, 
            materia.id_materia
        )
        print(f"{res=}")

        sujeto = SujetoConcreto()
        sujeto.vincular(usuario)

        if res == "Alta":
            sujeto.setEstado(f"Te inscribiste a {materia.nombre}")
        else:
            sujeto.setEstado(f"Te diste de baja de {materia.nombre}")

        messages.info(request, sujeto.getEstado())
    
    return redirect(f"/alumno?carrera={id_carrera}")

@login_valid
def mostrar_historial(request):
    _alumno = Alumno.get(request.session.get('user_id'))

    if _alumno:
        id_alumno = _alumno.id_usuario
        carreras = _alumno.obtener_carreras()
    id_carrera = request.GET.get("carrera")
    
    carrera = Carreras.get(id_carrera) 

    return render(request, "historial.html", {
        "carreras": carreras,
        "historial": Inscripcion_Examen.obtener_examenes_agrupados(id_alumno, carrera),
        "carrera_seleccionada": id_carrera
    })
