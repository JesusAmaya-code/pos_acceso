from datetime import datetime, timedelta
from functools import wraps

from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, abort)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
import os

app.secret_key = os.environ.get("SECRET_KEY", "clave-solo-para-desarrollo")

# ---------- Datos simulados ----------
USUARIOS = {
    "admin":      {"nombre": "Ana Torres",  "rol": "administrador",
                   "password": generate_password_hash("admin123")},
    "supervisor": {"nombre": "Luis Pérez",  "rol": "supervisor",
                   "password": generate_password_hash("super123")},
    "cajero":     {"nombre": "María López", "rol": "cajero",
                   "password": generate_password_hash("caja123")},
}

PERMISOS = {
    "administrador": ["ventas", "reportes", "usuarios"],
    "supervisor":    ["ventas", "reportes"],
    "cajero":        ["ventas"],
}

MODULOS = {
    "ventas":   {"titulo": "Ventas",   "icono": "🛒", "desc": "Registrar ventas y cobrar"},
    "reportes": {"titulo": "Reportes", "icono": "📊", "desc": "Cortes de caja y estadísticas"},
    "usuarios": {"titulo": "Usuarios", "icono": "👥", "desc": "Usuarios y bitácora de accesos"},
}

MAX_INTENTOS = 3
MINUTOS_BLOQUEO = 1
intentos = {}   # usuario -> {"fallos": int, "bloqueado_hasta": datetime | None}
bitacora = []   # registro de eventos de acceso


def registrar(usuario, evento):
    bitacora.insert(0, {
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "usuario": usuario,
        "evento": evento,
        "ip": request.remote_addr,
    })


# ---------- Decoradores de control de acceso ----------
def login_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def permiso_requerido(modulo):
    def decorador(f):
        @wraps(f)
        @login_requerido
        def wrapper(*args, **kwargs):
            if modulo not in PERMISOS.get(session["rol"], []):
                registrar(session["usuario"], f"Acceso denegado a '{modulo}'")
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorador


# ---------- Rutas ----------
@app.route("/")
def inicio():
    return redirect(url_for("dashboard" if "usuario" in session else "login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip().lower()
        password = request.form.get("password", "")
        estado = intentos.setdefault(usuario, {"fallos": 0, "bloqueado_hasta": None})

        # ¿Usuario bloqueado?
        if estado["bloqueado_hasta"] and datetime.now() < estado["bloqueado_hasta"]:
            restante = int((estado["bloqueado_hasta"] - datetime.now()).total_seconds()) + 1
            flash(f"Usuario bloqueado. Intenta de nuevo en {restante} segundos.", "danger")
            return render_template("login.html")

        datos = USUARIOS.get(usuario)
        if datos and check_password_hash(datos["password"], password):
            intentos[usuario] = {"fallos": 0, "bloqueado_hasta": None}
            session.clear()
            session["usuario"] = usuario
            session["nombre"] = datos["nombre"]
            session["rol"] = datos["rol"]
            registrar(usuario, "Inicio de sesión exitoso")
            return redirect(url_for("dashboard"))

        # Credenciales incorrectas
        estado["fallos"] += 1
        registrar(usuario or "(vacío)", "Intento de acceso fallido")
        if estado["fallos"] >= MAX_INTENTOS:
            estado["bloqueado_hasta"] = datetime.now() + timedelta(minutes=MINUTOS_BLOQUEO)
            estado["fallos"] = 0
            registrar(usuario, "Usuario bloqueado temporalmente")
            flash(f"Demasiados intentos. Usuario bloqueado {MINUTOS_BLOQUEO} minuto(s).", "danger")
        else:
            restantes = MAX_INTENTOS - estado["fallos"]
            flash(f"Usuario o contraseña incorrectos. Intentos restantes: {restantes}.", "danger")

    return render_template("login.html")


@app.route("/dashboard")
@login_requerido
def dashboard():
    permitidos = {k: MODULOS[k] for k in PERMISOS[session["rol"]]}
    return render_template("dashboard.html", modulos=permitidos)


@app.route("/ventas")
@permiso_requerido("ventas")
def ventas():
    return render_template("modulo.html", modulo=MODULOS["ventas"])


@app.route("/reportes")
@permiso_requerido("reportes")
def reportes():
    return render_template("modulo.html", modulo=MODULOS["reportes"])


@app.route("/usuarios")
@permiso_requerido("usuarios")
def usuarios():
    return render_template("usuarios.html", usuarios=USUARIOS, bitacora=bitacora[:15])


@app.route("/logout")
@login_requerido
def logout():
    registrar(session["usuario"], "Cierre de sesión")
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("login"))


@app.errorhandler(403)
def prohibido(e):
    return render_template("403.html"), 403


if __name__ == "__main__":
    app.run(debug=True)