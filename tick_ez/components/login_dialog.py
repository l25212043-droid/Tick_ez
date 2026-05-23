import reflex as rx
from tick_ez.states.auth_state import AuthState
from tick_ez.components.logo import logo


def tab_button(label: str, key: str) -> rx.Component:
    is_active = AuthState.auth_modo == key
    return rx.el.button(
        label,
        on_click=lambda: AuthState.set_auth_modo(key),
        type="button",
        class_name=rx.cond(
            is_active,
            "flex-1 px-3 py-2 rounded-lg bg-violet-600 text-white text-sm font-semibold",
            "flex-1 px-3 py-2 rounded-lg bg-gray-100 text-gray-700 text-sm font-semibold hover:bg-gray-200",
        ),
    )


def login_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.p(
                rx.cond(
                    AuthState.login_modo == "manager",
                    "Acceso para administradores y soporte",
                    "Acceso para clientes",
                ),
                class_name="text-xs text-gray-500 mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Correo electrónico",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    name="correo",
                    type="email",
                    placeholder="usuario@correo.com",
                    required=True,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-900 placeholder-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                ),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.label(
                    "Contraseña",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    name="password",
                    type="password",
                    placeholder="••••••••",
                    required=True,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-900 placeholder-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                ),
                class_name="mb-4",
            ),
            rx.cond(
                AuthState.error_login != "",
                rx.el.div(
                    rx.icon("circle-alert", class_name="h-4 w-4 text-red-600"),
                    rx.el.p(
                        AuthState.error_login,
                        class_name="text-xs text-red-700",
                    ),
                    class_name="flex items-center gap-2 p-3 bg-red-50 border border-red-100 rounded-lg mb-4",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.icon(
                    "info",
                    class_name="h-3.5 w-3.5 text-blue-600 shrink-0 mt-0.5",
                ),
                rx.el.p(
                    "Demo: usa cualquier correo y contraseña de 4+ caracteres",
                    class_name="text-xs text-blue-700",
                ),
                class_name="flex items-start gap-1.5 p-2.5 bg-blue-50 rounded-lg mb-4",
            ),
            rx.el.button(
                rx.icon("log-in", class_name="h-4 w-4"),
                "Iniciar sesión",
                type="submit",
                class_name="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700 transition-colors",
            ),
        ),
        on_submit=AuthState.iniciar_sesion,
        reset_on_submit=True,
    )


def registro_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.p(
                "Crea tu cuenta en Tick_EZ y empieza a comprar tickets",
                class_name="text-xs text-gray-500 mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Nombre completo",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    name="nombre",
                    placeholder="Ana Pérez García",
                    required=True,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                ),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.label(
                    "Correo electrónico",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    name="correo",
                    type="email",
                    placeholder="ana@correo.com",
                    required=True,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                ),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.label(
                    "Teléfono",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    name="telefono",
                    type="tel",
                    placeholder="+52 664 555 0192",
                    required=True,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                ),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.label(
                    "Tipo de usuario",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Cliente", value="Cliente"),
                        rx.el.option(
                            "EmpleadoSoporte", value="EmpleadoSoporte"
                        ),
                        rx.el.option("Administrador", value="Administrador"),
                        name="tipo",
                        default_value="Cliente",
                        class_name="w-full appearance-none pl-3 pr-9 py-2 bg-white border border-gray-300 rounded-lg text-sm cursor-pointer focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="absolute right-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Contraseña",
                        class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                    ),
                    rx.el.input(
                        name="password",
                        type="password",
                        placeholder="Mínimo 6 caracteres",
                        required=True,
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Confirmar",
                        class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                    ),
                    rx.el.input(
                        name="confirmar",
                        type="password",
                        placeholder="Repite contraseña",
                        required=True,
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                    ),
                ),
                class_name="grid grid-cols-2 gap-2 mb-4",
            ),
            rx.cond(
                AuthState.error_registro != "",
                rx.el.div(
                    rx.icon("circle-alert", class_name="h-4 w-4 text-red-600"),
                    rx.el.p(
                        AuthState.error_registro,
                        class_name="text-xs text-red-700",
                    ),
                    class_name="flex items-center gap-2 p-3 bg-red-50 border border-red-100 rounded-lg mb-4",
                ),
                rx.fragment(),
            ),
            rx.el.button(
                rx.icon("user-plus", class_name="h-4 w-4"),
                "Crear cuenta",
                type="submit",
                class_name="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700",
            ),
        ),
        on_submit=AuthState.registrar_usuario,
        reset_on_submit=True,
    )


def login_dialog() -> rx.Component:
    return rx.cond(
        AuthState.show_login,
        rx.el.div(
            rx.el.div(
                on_click=AuthState.cerrar_login,
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            logo("sm"),
                            rx.el.button(
                                rx.icon("x", class_name="h-4 w-4"),
                                on_click=AuthState.cerrar_login,
                                type="button",
                                class_name="p-1.5 rounded-lg hover:bg-gray-100 text-gray-500",
                            ),
                            class_name="flex items-center justify-between p-5 border-b border-gray-200",
                        ),
                        rx.el.div(
                            rx.el.div(
                                tab_button("Iniciar sesión", "login"),
                                tab_button("Crear cuenta", "registro"),
                                class_name="flex items-center gap-2 mb-4",
                            ),
                            rx.cond(
                                AuthState.auth_modo == "registro",
                                registro_form(),
                                login_form(),
                            ),
                            class_name="p-5",
                        ),
                        class_name="bg-white rounded-xl shadow-2xl w-full max-w-md max-h-[90vh] overflow-y-auto",
                    ),
                    class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
                ),
            ),
        ),
        rx.fragment(),
    )