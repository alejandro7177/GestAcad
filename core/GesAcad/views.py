from django.contrib.auth import hashers
from django.shortcuts import get_object_or_404, redirect, render

from .models import Carrera_Materia, Inscripcion_Examen, Inscripcion_Materia, Materias, Usuarios, Carreras

carrera = Carreras.objects.get(id_carrera=2)


def obtener_materias_agrupadas(carreras, id_carrera):
    from datetime import datetime
    today = datetime.now()

    if id_carrera:
        carrera = carreras.filter(id_carrera=id_carrera).first()

        return Materias.materias_alumnos_ord(
            cuatrimestre= 1 if today.month <= 6 else 2,
            carrera=carrera
        )
    else:
        return None


def login_valid(func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapper

def docente_valid(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get("perfil_id") != "Docente":
            return redirect("login")
        return func(request, *args, **kwargs)
    return wrapper


def login_controler(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = Usuarios.objects.get(email=username)

            if hashers.check_password(password, user.password_hash):
                id_perfil = user.id_perfil.id_perfil
                request.session['user_id'] = user.id_usuario
                request.session['perfil_id'] = user.id_perfil.__str__()
                if id_perfil == 1:
                    return redirect("alumno")
                return redirect("docente")
            else:
                return render(request, 'login.html', {'error':'Credecinales Incorrectas!'})
            
        except Usuarios.DoesNotExist:
            return render(request, 'login.html', {'error':'El usuario no existe!'})
    return render(request, 'login.html')


@login_valid
@docente_valid
def docente_controller(request):
    usuario = Usuarios.get(request.session.get("user_id"))
    materias = Inscripcion_Materia.materias_alta(usuario=usuario)
    return render(request,"docente.html", {"materias": materias})

@login_valid
@docente_valid
def docente_inscriptos(request, materia_id):
    docente = Usuarios.get(id=request.session.get("user_id"))
    materia = Materias.get(id=materia_id)
    inscriptos_materia = Inscripcion_Materia.inscriptos_por_materia(materia=materia, usuario=docente)
    if request.session.get("perfil_id") != "Docente":
        return render(request, "inscriptos.html", {"inscriptos": None})
    if request.method == "POST":
        if not inscriptos_materia:
            return redirect("inscriptos", materia_id=materia_id)
        for inscripto in inscriptos_materia:
            estado = request.POST.get(
                f"estado_{inscripto.id_inscripcion_materia}"
            )
            if estado:
                inscripto.estado = estado
                inscripto.save()
        return redirect(
            "inscriptos",
            materia_id=materia_id
        )
    return render(request, "inscriptos.html", {"inscriptos":inscriptos_materia, "materia":materia})

@login_valid
def asignar_nota_cursada(request):
    #asignar notas por alumno inscripto a la materia
    #recibir la inscripcion a la materia que le corresponde y la nota
    materia = Materias.get_materia(request.session.get("materia_id"))
    inscripciones_a_materia = Inscripcion_Materia.get_all(materia=materia)


@login_valid
def alumno_controller(request):
    usuario = Usuarios.get(request.session.get('user_id'))   
    
    carreras = Carreras.carreras_alumno(alumno=usuario)
    id_carrera = request.GET.get('carrera')

    materias_agrupadas = obtener_materias_agrupadas(carreras, id_carrera)
    inscripciones_alta = Inscripcion_Materia.id_materias_alta(usuario)

    return render(request, 'alumno.html',{
        'materias_agrupadas':materias_agrupadas,
        'inscriptas_alta': inscripciones_alta,
        'carreras':carreras,
        'carrera_seleccionada': id_carrera
    })


def toggle_inscripcion(request, materia_id):
    materia = get_object_or_404(Materias, id_materia=materia_id)
    usuario = Usuarios.get(id=request.session.get('user_id'))
    id_carrera = request.GET.get('carrera')

    Inscripcion_Materia.dar_alta_baja_Inscripcion_Materia(materia=materia, usuario=usuario)

    return redirect(f'/alumno?carrera={id_carrera}')

