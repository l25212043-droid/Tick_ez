import reflex as rx
from typing import TypedDict
import logging
import datetime


class SesionActiva(TypedDict):
    fecha_inicio: str
    hora_inicio: str
    ip_usuario: str
    rol: str


class IntentoFallido(TypedDict):
    correo: str
    fecha: str
    motivo: str


class UsuarioRegistrado(TypedDict):
    id_usuario: str
    correo: str
    nombre: str
    rol: str
    estado_cuenta: str
    ultimo_acceso: str


class AuthState(rx.State):
    is_logged_in: bool = False
    rol_actual: str = "Invitado"
    correo: str = ""
    nombre_usuario: str = "María González"
    id_usuario: str = "USR-2026-00184"
    estado_cuenta: str = "Activa"
    metodo_pago_default: str = "Tarjeta crédito Visa **4587"
    rfc: str = "GOMA920304ABC"
    telefono: str = "+52 664 555 0192"

    show_login: bool = False
    login_modo: str = "cliente"
    auth_modo: str = "login"
    intentos_fallidos_count: int = 0
    error_login: str = ""
    error_registro: str = ""

    sesion_activa: SesionActiva = {
        "fecha_inicio": "—",
        "hora_inicio": "—",
        "ip_usuario": "—",
        "rol": "Invitado",
    }

    intentos_fallidos: list[IntentoFallido] = [
        {
            "correo": "carlos.mendez@mail.com",
            "fecha": "12 Ene 2026 14:23",
            "motivo": "Contraseña incorrecta",
        },
        {
            "correo": "ana.lopez@mail.com",
            "fecha": "12 Ene 2026 09:15",
            "motivo": "Usuario bloqueado",
        },
        {
            "correo": "pedro.ruiz@mail.com",
            "fecha": "11 Ene 2026 22:48",
            "motivo": "Correo no registrado",
        },
    ]

    usuarios_registrados: list[UsuarioRegistrado] = [
        {
            "id_usuario": "USR-2026-00184",
            "correo": "maria.gonzalez@mail.com",
            "nombre": "María González",
            "rol": "Cliente",
            "estado_cuenta": "Activa",
            "ultimo_acceso": "Hoy 09:42",
        },
        {
            "id_usuario": "USR-2026-00102",
            "correo": "soporte@ticketera.mx",
            "nombre": "Luis Hernández",
            "rol": "EmpleadoSoporte",
            "estado_cuenta": "Activa",
            "ultimo_acceso": "Hoy 08:15",
        },
        {
            "id_usuario": "USR-2026-00001",
            "correo": "admin@ticketera.mx",
            "nombre": "Patricia Romero",
            "rol": "Administrador",
            "estado_cuenta": "Activa",
            "ultimo_acceso": "Ayer 18:30",
        },
        {
            "id_usuario": "USR-2025-09781",
            "correo": "j.castillo@mail.com",
            "nombre": "Jorge Castillo",
            "rol": "Cliente",
            "estado_cuenta": "Inactiva",
            "ultimo_acceso": "23 Dic 2025",
        },
        {
            "id_usuario": "USR-2025-09102",
            "correo": "elena.vargas@mail.com",
            "nombre": "Elena Vargas",
            "rol": "Cliente",
            "estado_cuenta": "Bloqueada",
            "ultimo_acceso": "05 Dic 2025",
        },
    ]

    @rx.var
    def total_usuarios_activos(self) -> int:
        return len(
            [
                u
                for u in self.usuarios_registrados
                if u["estado_cuenta"] == "Activa"
            ]
        )

    @rx.var
    def total_usuarios_inactivos(self) -> int:
        return len(
            [
                u
                for u in self.usuarios_registrados
                if u["estado_cuenta"] == "Inactiva"
            ]
        )

    @rx.var
    def total_usuarios_bloqueados(self) -> int:
        return len(
            [
                u
                for u in self.usuarios_registrados
                if u["estado_cuenta"] == "Bloqueada"
            ]
        )

    @rx.event
    def abrir_login(self, modo: str):
        self.login_modo = modo
        self.auth_modo = "login"
        self.show_login = True
        self.error_login = ""
        self.error_registro = ""

    @rx.event
    def cerrar_login(self):
        self.show_login = False
        self.error_login = ""
        self.error_registro = ""

    @rx.event
    def set_auth_modo(self, modo: str):
        self.auth_modo = modo
        self.error_login = ""
        self.error_registro = ""

    @rx.event
    def registrar_usuario(self, form_data: dict):
        try:
            import re

            nombre = form_data.get("nombre", "").strip()
            correo = form_data.get("correo", "").strip()
            password = form_data.get("password", "").strip()
            confirmar = form_data.get("confirmar", "").strip()
            telefono = form_data.get("telefono", "").strip()
            tipo = form_data.get("tipo", "Cliente")
            if not nombre or len(nombre) < 3:
                self.error_registro = (
                    "El nombre debe tener al menos 3 caracteres"
                )
                return rx.toast("Nombre inválido", duration=3000)
            if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo):
                self.error_registro = "Correo electrónico no válido"
                return rx.toast("Correo inválido", duration=3000)
            if any(u["correo"] == correo for u in self.usuarios_registrados):
                self.error_registro = "Este correo ya está registrado"
                return rx.toast("Correo duplicado", duration=3000)
            if len(password) < 6:
                self.error_registro = (
                    "La contraseña debe tener al menos 6 caracteres"
                )
                return rx.toast("Contraseña muy corta", duration=3000)
            if password != confirmar:
                self.error_registro = "Las contraseñas no coinciden"
                return rx.toast("Las contraseñas no coinciden", duration=3000)
            if not re.match(r"^[\+\d\s\-\(\)]{8,}$", telefono):
                self.error_registro = "Teléfono no válido"
                return rx.toast("Teléfono inválido", duration=3000)
            now = datetime.datetime.now()
            nuevo_id = f"USR-2026-{abs(hash(correo)) % 100000:05d}"
            self.usuarios_registrados.insert(
                0,
                {
                    "id_usuario": nuevo_id,
                    "correo": correo,
                    "nombre": nombre,
                    "rol": tipo,
                    "estado_cuenta": "Activa",
                    "ultimo_acceso": now.strftime("%d %b %Y %H:%M"),
                },
            )
            self.is_logged_in = True
            self.correo = correo
            self.nombre_usuario = nombre
            self.id_usuario = nuevo_id
            self.telefono = telefono
            self.estado_cuenta = "Activa"
            self.rol_actual = (
                "LoginManager"
                if tipo in ("Administrador", "EmpleadoSoporte")
                else "LoginUser"
            )
            self.sesion_activa = {
                "fecha_inicio": now.strftime("%d %b %Y"),
                "hora_inicio": now.strftime("%H:%M:%S"),
                "ip_usuario": "192.168.1.105",
                "rol": self.rol_actual,
            }
            self.show_login = False
            self.error_registro = ""
            return rx.toast(
                f"Cuenta creada · Bienvenido {nombre}", duration=3500
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            return rx.toast("Error al registrar", duration=3000)

    @rx.event
    def iniciar_sesion(self, form_data: dict):
        try:
            correo = form_data.get("correo", "").strip()
            password = form_data.get("password", "").strip()
            if not correo or not password:
                self.error_login = "Correo y contraseña requeridos"
                return rx.toast("Datos incompletos", duration=3000)
            if len(password) < 4:
                self.intentos_fallidos_count += 1
                self.intentos_fallidos.insert(
                    0,
                    {
                        "correo": correo,
                        "fecha": datetime.datetime.now().strftime(
                            "%d %b %Y %H:%M"
                        ),
                        "motivo": "Contraseña inválida",
                    },
                )
                self.error_login = "Credenciales incorrectas. Intenta de nuevo."
                return rx.toast("Error de autenticación", duration=3000)
            self.is_logged_in = True
            self.correo = correo
            now = datetime.datetime.now()
            if self.login_modo == "manager":
                self.rol_actual = "LoginManager"
                self.nombre_usuario = "Patricia Romero"
                self.id_usuario = "USR-2026-00001"
            else:
                self.rol_actual = "LoginUser"
                self.nombre_usuario = (
                    correo.split("@")[0].title() if "@" in correo else "Cliente"
                )
                self.id_usuario = f"USR-2026-{abs(hash(correo)) % 100000:05d}"
            self.sesion_activa = {
                "fecha_inicio": now.strftime("%d %b %Y"),
                "hora_inicio": now.strftime("%H:%M:%S"),
                "ip_usuario": "192.168.1.105",
                "rol": self.rol_actual,
            }
            self.show_login = False
            self.error_login = ""
            return rx.toast(f"Bienvenido, {self.nombre_usuario}", duration=3000)
        except Exception as e:
            logging.exception(f"Error: {e}")
            return rx.toast("Error al iniciar sesión", duration=3000)

    @rx.event
    def cerrar_sesion(self):
        self.is_logged_in = False
        self.rol_actual = "Invitado"
        self.correo = ""
        self.sesion_activa = {
            "fecha_inicio": "—",
            "hora_inicio": "—",
            "ip_usuario": "—",
            "rol": "Invitado",
        }
        return rx.toast("Sesión cerrada", duration=2500)

    @rx.event
    def actualizar_perfil(self, form_data: dict):
        try:
            self.nombre_usuario = form_data.get("nombre", self.nombre_usuario)
            self.correo = form_data.get("correo", self.correo)
            self.telefono = form_data.get("telefono", self.telefono)
            self.rfc = form_data.get("rfc", self.rfc)
            self.metodo_pago_default = form_data.get(
                "metodo_pago", self.metodo_pago_default
            )
            return rx.toast("Perfil actualizado correctamente", duration=3000)
        except Exception as e:
            logging.exception(f"Error: {e}")
            return rx.toast("Error al actualizar", duration=3000)

    @rx.event
    def bloquear_usuario(self, id_usuario: str):
        for u in self.usuarios_registrados:
            if u["id_usuario"] == id_usuario:
                u["estado_cuenta"] = "Bloqueada"
        return rx.toast("Usuario bloqueado", duration=2500)

    @rx.event
    def activar_usuario(self, id_usuario: str):
        for u in self.usuarios_registrados:
            if u["id_usuario"] == id_usuario:
                u["estado_cuenta"] = "Activa"
        return rx.toast("Usuario activado", duration=2500)