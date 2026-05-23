import reflex as rx
from tick_ez.states.auth_state import AuthState


def estado_badge(estado: rx.Var) -> rx.Component:
    return rx.match(
        estado,
        (
            "Activa",
            rx.el.span(
                "Activa",
                class_name="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 text-xs font-semibold w-fit",
            ),
        ),
        (
            "Inactiva",
            rx.el.span(
                "Inactiva",
                class_name="px-2 py-0.5 rounded-md bg-gray-100 text-gray-700 text-xs font-semibold w-fit",
            ),
        ),
        (
            "Bloqueada",
            rx.el.span(
                "Bloqueada",
                class_name="px-2 py-0.5 rounded-md bg-red-50 text-red-700 text-xs font-semibold w-fit",
            ),
        ),
        rx.el.span("—", class_name="text-xs"),
    )


def usuario_row(u: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={u['correo']}",
                class_name="size-9 rounded-full bg-gray-100",
            ),
            rx.el.div(
                rx.el.p(
                    u["nombre"],
                    class_name="text-sm font-semibold text-gray-900 leading-tight",
                ),
                rx.el.p(
                    u["correo"],
                    class_name="text-xs text-gray-500",
                ),
            ),
            class_name="flex items-center gap-3 flex-1",
        ),
        rx.el.div(
            rx.el.span(
                u["rol"],
                class_name="text-xs font-medium text-violet-700 bg-violet-50 px-2 py-0.5 rounded-md w-fit",
            ),
            class_name="hidden md:flex w-32",
        ),
        rx.el.div(
            estado_badge(u["estado_cuenta"]),
            class_name="hidden md:flex w-28",
        ),
        rx.el.div(
            u["ultimo_acceso"],
            class_name="hidden lg:block text-xs text-gray-500 w-32",
        ),
        rx.el.div(
            rx.cond(
                u["estado_cuenta"] == "Bloqueada",
                rx.el.button(
                    rx.icon("lock_open", class_name="h-3.5 w-3.5"),
                    "Activar",
                    on_click=lambda: AuthState.activar_usuario(u["id_usuario"]),
                    class_name="flex items-center gap-1 px-2.5 py-1.5 bg-emerald-50 text-emerald-700 rounded-md text-xs font-semibold hover:bg-emerald-100",
                ),
                rx.el.button(
                    rx.icon("lock", class_name="h-3.5 w-3.5"),
                    "Bloquear",
                    on_click=lambda: AuthState.bloquear_usuario(
                        u["id_usuario"]
                    ),
                    class_name="flex items-center gap-1 px-2.5 py-1.5 bg-red-50 text-red-700 rounded-md text-xs font-semibold hover:bg-red-100",
                ),
            ),
        ),
        class_name="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors",
    )


def intento_row(i: dict) -> rx.Component:
    return rx.el.div(
        rx.icon("shield-alert", class_name="h-4 w-4 text-red-500 shrink-0"),
        rx.el.div(
            rx.el.p(
                i["correo"],
                class_name="text-sm font-semibold text-gray-900",
            ),
            rx.el.p(
                i["motivo"],
                class_name="text-xs text-gray-500",
            ),
        ),
        rx.el.span(
            i["fecha"],
            class_name="ml-auto text-xs text-gray-500 font-mono",
        ),
        class_name="flex items-center gap-3 p-3 bg-red-50/50 border border-red-100 rounded-lg",
    )


def perfil_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.img(
                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.correo}",
                    class_name="size-16 rounded-full bg-gray-100",
                ),
                rx.el.div(
                    rx.el.h3(
                        AuthState.nombre_usuario,
                        class_name="text-base font-bold text-gray-900",
                    ),
                    rx.el.p(
                        AuthState.id_usuario,
                        class_name="text-xs text-gray-500 font-mono",
                    ),
                    rx.el.div(
                        rx.el.span(
                            AuthState.rol_actual,
                            class_name="px-2 py-0.5 rounded-md bg-violet-50 text-violet-700 text-xs font-semibold",
                        ),
                        estado_badge(AuthState.estado_cuenta),
                        class_name="flex items-center gap-2 mt-1",
                    ),
                ),
                class_name="flex items-center gap-4 mb-5",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Nombre completo",
                            class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="nombre",
                            default_value=AuthState.nombre_usuario,
                            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Correo electrónico",
                            class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="correo",
                            type="email",
                            default_value=AuthState.correo,
                            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Teléfono",
                            class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="telefono",
                            default_value=AuthState.telefono,
                            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "RFC",
                            class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="rfc",
                            default_value=AuthState.rfc,
                            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3",
                ),
                rx.el.div(
                    rx.el.label(
                        "Método de pago predeterminado",
                        class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                    ),
                    rx.el.input(
                        name="metodo_pago",
                        default_value=AuthState.metodo_pago_default,
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("save", class_name="h-4 w-4"),
                        "Guardar cambios",
                        type="submit",
                        class_name="flex items-center gap-2 px-4 py-2 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700",
                    ),
                    rx.el.button(
                        rx.icon("log-out", class_name="h-4 w-4"),
                        "Cerrar sesión",
                        on_click=AuthState.cerrar_sesion,
                        type="button",
                        class_name="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg text-sm font-semibold hover:bg-gray-50",
                    ),
                    class_name="flex gap-2",
                ),
                on_submit=AuthState.actualizar_perfil,
                reset_on_submit=False,
            ),
            class_name="bg-white p-6 rounded-xl border border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "shield-check", class_name="h-5 w-5 text-emerald-600"
                    ),
                    rx.el.h3(
                        "Sesión activa",
                        class_name="text-base font-bold text-gray-900",
                    ),
                    class_name="flex items-center gap-2 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Fecha inicio",
                            class_name="text-xs text-gray-500 mb-0.5",
                        ),
                        rx.el.p(
                            AuthState.sesion_activa["fecha_inicio"],
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Hora inicio",
                            class_name="text-xs text-gray-500 mb-0.5",
                        ),
                        rx.el.p(
                            AuthState.sesion_activa["hora_inicio"],
                            class_name="text-sm font-semibold text-gray-900 font-mono",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "IP usuario",
                            class_name="text-xs text-gray-500 mb-0.5",
                        ),
                        rx.el.p(
                            AuthState.sesion_activa["ip_usuario"],
                            class_name="text-sm font-semibold text-gray-900 font-mono",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Rol", class_name="text-xs text-gray-500 mb-0.5"
                        ),
                        rx.el.p(
                            AuthState.sesion_activa["rol"],
                            class_name="text-sm font-semibold text-violet-700",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4",
                ),
                class_name="bg-white p-5 rounded-xl border border-gray-200 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("shield-alert", class_name="h-5 w-5 text-red-600"),
                    rx.el.h3(
                        "Intentos fallidos",
                        class_name="text-base font-bold text-gray-900",
                    ),
                    rx.el.span(
                        AuthState.intentos_fallidos.length().to_string(),
                        class_name="ml-auto px-2 py-0.5 rounded-md bg-red-50 text-red-700 text-xs font-bold",
                    ),
                    class_name="flex items-center gap-2 mb-4",
                ),
                rx.el.div(
                    rx.foreach(AuthState.intentos_fallidos, intento_row),
                    class_name="flex flex-col gap-2",
                ),
                class_name="bg-white p-5 rounded-xl border border-gray-200",
            ),
        ),
        class_name="grid grid-cols-1 lg:grid-cols-2 gap-5",
    )


def manager_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p("Activos", class_name="text-xs text-gray-500 mb-1"),
                rx.el.p(
                    AuthState.total_usuarios_activos.to_string(),
                    class_name="text-2xl font-bold text-emerald-600",
                ),
                class_name="bg-white p-4 rounded-xl border border-gray-200",
            ),
            rx.el.div(
                rx.el.p("Inactivos", class_name="text-xs text-gray-500 mb-1"),
                rx.el.p(
                    AuthState.total_usuarios_inactivos.to_string(),
                    class_name="text-2xl font-bold text-gray-700",
                ),
                class_name="bg-white p-4 rounded-xl border border-gray-200",
            ),
            rx.el.div(
                rx.el.p(
                    "Bloqueados",
                    class_name="text-xs text-gray-500 mb-1",
                ),
                rx.el.p(
                    AuthState.total_usuarios_bloqueados.to_string(),
                    class_name="text-2xl font-bold text-red-600",
                ),
                class_name="bg-white p-4 rounded-xl border border-gray-200",
            ),
            rx.el.div(
                rx.el.p(
                    "Intentos fallidos",
                    class_name="text-xs text-gray-500 mb-1",
                ),
                rx.el.p(
                    AuthState.intentos_fallidos.length().to_string(),
                    class_name="text-2xl font-bold text-amber-600",
                ),
                class_name="bg-white p-4 rounded-xl border border-gray-200",
            ),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-5",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("users", class_name="h-5 w-5 text-violet-600"),
                rx.el.h3(
                    "Gestión de usuarios",
                    class_name="text-base font-bold text-gray-900",
                ),
                class_name="flex items-center gap-2 mb-4",
            ),
            rx.el.div(
                rx.foreach(AuthState.usuarios_registrados, usuario_row),
                class_name="flex flex-col gap-2",
            ),
            class_name="bg-white p-5 rounded-xl border border-gray-200",
        ),
    )


def login_landing() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "shield-check", class_name="h-12 w-12 text-violet-600 mb-3"
            ),
            rx.el.h2(
                "Sistema de Sesión",
                class_name="text-2xl font-bold text-gray-900 mb-1",
            ),
            rx.el.p(
                "Inicia sesión para acceder a tu perfil, notificaciones y operaciones",
                class_name="text-sm text-gray-600 mb-6",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("user", class_name="h-4 w-4"),
                    "Acceder como Cliente",
                    on_click=lambda: AuthState.abrir_login("cliente"),
                    class_name="flex items-center justify-center gap-2 px-5 py-2.5 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700",
                ),
                rx.el.button(
                    rx.icon("shield", class_name="h-4 w-4"),
                    "Acceder como Manager",
                    on_click=lambda: AuthState.abrir_login("manager"),
                    class_name="flex items-center justify-center gap-2 px-5 py-2.5 bg-white border border-gray-300 text-gray-700 rounded-lg text-sm font-semibold hover:bg-gray-50",
                ),
                class_name="flex flex-wrap gap-3",
            ),
            class_name="bg-white p-8 rounded-xl border border-gray-200 max-w-xl",
        ),
    )


def cuenta_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Cuenta y seguridad",
                    class_name="text-2xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    "Gestiona tu sesión, perfil y permisos del sistema",
                    class_name="text-sm text-gray-600",
                ),
                class_name="mb-6",
            ),
            rx.cond(
                AuthState.is_logged_in,
                rx.cond(
                    AuthState.rol_actual == "LoginManager",
                    rx.el.div(
                        perfil_panel(),
                        manager_panel(),
                        class_name="flex flex-col gap-6",
                    ),
                    perfil_panel(),
                ),
                login_landing(),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )