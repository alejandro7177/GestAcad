from django.contrib.auth import hashers
from django.shortcuts import get_object_or_404, redirect, render

from .academico import Materia
from .usuario import Usuario, Alumno, Docente
from .models import (
    Carrera_Materia,
    Inscripcion_Examen,
    Inscripcion_Materia,
    Materias,
    Usuarios,
    Carreras,
)

<<<<<<< Updated upstream
=======

def obtener_materias_agrupadas(carreras, id_carrera):
    from datetime import datetime

    today = datetime.now()

    if id_carrera:
        carrera = carreras.filter(id_carrera=id_carrera).first()

        return Materias.materias_alumnos_ord(
            cuatrimestre=1 if today.month <= 6 else 2, carrera=carrera
        )
    else:
        return None


>>>>>>> Stashed changes
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
            if user.obtenerPerfil() == "Alumno":
                return redirect("alumno")
            if user.obtenerPerfil() == "Docente":
                return redirect("docente")
    return render(request, "login.html")

<<<<<<< Updated upstream
=======
#------------------------ DOCENTE --------------------------------------

>>>>>>> Stashed changes
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
    materia = Materias.get(id=materia_id)
    inscriptos_materia = Inscripcion_Materia.inscriptos_por_materia(
        materia=materia, usuario=docente
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
<<<<<<< Updated upstream
    from datetime import datetime


    today = datetime.now()
    usuario = Usuarios.get(request.session.get('user_id'))
    carreras = Carreras.carreras_alumno(alumno=usuario)
    
    id_carrera = request.GET.get('carrera')

    if id_carrera:
        carrera = carreras.filter(id_carrera=id_carrera).first()

        materias_agrupadas = Materias.materias_alumnos_ord(
            cuatrimestre= 1 if today.month <= 6 else 2,
            carrera=carrera
        )
    else:
        materias_agrupadas = None

    inscripciones_alta = Inscripcion_Materia.id_materias_alta(usuario)
    
    return render(request, 'alumno.html',{
        'materias_agrupadas':materias_agrupadas,
        'inscriptas_alta': inscripciones_alta,
        'carreras':carreras,
        'carrera_seleccionada': id_carrera
    })

=======
    _alumno : Alumno = Usuario.get(request.session.get("user_id"))
    _materia : Materia = 

    carreras = _alumno.obtener_carreras()

    materias_agrupadas = obtener_materias_agrupadas(carreras, id_carrera)
    inscripciones = Inscripcion_Materia.id_m

    return render(
        request,
        "alumno.html",
        {
            "materias_agrupadas": materias_agrupadas,
            "inscriptas_alta": inscripciones_alta,
            "carreras": carreras,
            "carrera_seleccionada": request.GET.get("carrera")
        },
    )

>>>>>>> Stashed changes
def toggle_inscripcion(request, materia_id):
    materia = get_object_or_404(Materias, id_materia=materia_id)
    usuario = Usuarios.get(id=request.session.get("user_id"))
    id_carrera = request.GET.get("carrera")

    Inscripcion_Materia.dar_alta_baja_Inscripcion_Materia(
        materia=materia, usuario=usuario
    )

    return redirect(f"/alumno?carrera={id_carrera}")
