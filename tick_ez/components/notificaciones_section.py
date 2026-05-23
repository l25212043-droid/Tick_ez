import reflex as rx
from tick_ez.states.notificacion_state import NotificacionState


def tipo_icon(tipo: rx.Var) -> rx.Component:
    return rx.match(
        tipo,
        (
            "CorreoNoti",
            rx.el.div(
                rx.icon("mail", class_name="h-4 w-4 text-blue-600"),
                class_name="p-2 rounded-lg bg-blue-50",
            ),
        ),
        (
            "SMSNoti",
            rx.el.div(
                rx.icon(
                    "message-square", class_name="h-4 w-4 text-emerald-600"
                ),
                class_name="p-2 rounded-lg bg-emerald-50",
            ),
        ),
        (
            "NotiManager",
            rx.el.div(
                rx.icon("megaphone", class_name="h-4 w-4 text-violet-600"),
                class_name="p-2 rounded-lg bg-violet-50",
            ),
        ),
        rx.el.div(
            rx.icon("bell", class_name="h-4 w-4 text-gray-600"),
            class_name="p-2 rounded-lg bg-gray-100",
        ),
    )


def noti_card(n: dict) -> rx.Component:
    return rx.el.div(
        tipo_icon(n["tipo"]),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    n["asunto"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.cond(
                    ~n["visto"],
                    rx.el.span(class_name="size-2 rounded-full bg-violet-500"),
                    rx.fragment(),
                ),
                class_name="flex items-center gap-2 mb-1",
            ),
            rx.el.p(
                n["mensaje"],
                class_name="text-xs text-gray-600 mb-2",
            ),
            rx.el.div(
                rx.el.span(
                    n["tipo"],
                    class_name="text-xs font-medium text-violet-700 bg-violet-50 px-2 py-0.5 rounded-md",
                ),
                rx.el.span(
                    n["destinatario"],
                    class_name="text-xs text-gray-500 font-mono",
                ),
                rx.el.span(
                    n["fecha_envio"], class_name="text-xs text-gray-400 ml-auto"
                ),
                class_name="flex items-center gap-2 flex-wrap",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.cond(
                ~n["visto"],
                rx.el.button(
                    rx.icon("eye", class_name="h-3.5 w-3.5"),
                    on_click=lambda: NotificacionState.marcar_visto(n["id"]),
                    class_name="p-1.5 rounded-md hover:bg-violet-50 text-violet-700",
                ),
                rx.fragment(),
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                on_click=lambda: NotificacionState.cancelar_notificacion(
                    n["id"]
                ),
                class_name="p-1.5 rounded-md hover:bg-red-50 text-red-600",
            ),
            class_name="flex items-center gap-1",
        ),
        class_name="flex items-start gap-3 p-4 bg-white border border-gray-200 rounded-lg hover:border-violet-200 transition-colors",
    )


def filtro_btn(label: str) -> rx.Component:
    is_active = NotificacionState.filtro_tipo == label
    return rx.el.button(
        label,
        on_click=lambda: NotificacionState.set_filtro_tipo(label),
        class_name=rx.cond(
            is_active,
            "px-3 py-1.5 rounded-lg bg-violet-600 text-white text-xs font-semibold",
            "px-3 py-1.5 rounded-lg bg-white border border-gray-300 text-gray-700 text-xs font-semibold hover:bg-gray-50",
        ),
    )


def programar_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("calendar-plus", class_name="h-5 w-5 text-violet-600"),
            rx.el.h3(
                "Programar notificación",
                class_name="text-base font-bold text-gray-900",
            ),
            class_name="flex items-center gap-2 mb-4",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Tipo",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("CorreoNoti", value="CorreoNoti"),
                        rx.el.option("SMSNoti", value="SMSNoti"),
                        rx.el.option("NotiManager", value="NotiManager"),
                        name="tipo",
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
                rx.el.input(
                    name="asunto",
                    placeholder="Asunto",
                    required=True,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm mb-3 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                ),
                rx.el.input(
                    name="destinatario",
                    placeholder="Destinatario (correo o teléfono)",
                    required=True,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm mb-3 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                ),
                rx.el.textarea(
                    name="mensaje",
                    placeholder="Mensaje a enviar...",
                    rows="3",
                    required=True,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm mb-3 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none resize-none",
                ),
            ),
            rx.el.button(
                rx.icon("send", class_name="h-4 w-4"),
                "Programar envío",
                type="submit",
                class_name="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700",
            ),
            on_submit=NotificacionState.programar_notificacion,
            reset_on_submit=True,
        ),
        class_name="bg-white p-5 rounded-xl border border-gray-200",
    )


def notificaciones_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Notificaciones",
                        class_name="text-2xl font-bold text-gray-900 mb-1",
                    ),
                    rx.el.p(
                        rx.el.span(
                            NotificacionState.total_no_vistas.to_string(),
                            class_name="font-semibold text-violet-600",
                        ),
                        " sin leer",
                        class_name="text-sm text-gray-600",
                    ),
                ),
                rx.el.button(
                    rx.icon("check-check", class_name="h-4 w-4"),
                    "Marcar todas leídas",
                    on_click=NotificacionState.marcar_todas_vistas,
                    class_name="flex items-center gap-1.5 px-3 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg text-sm font-semibold hover:bg-gray-50",
                ),
                class_name="flex items-end justify-between mb-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            filtro_btn("Todas"),
                            filtro_btn("CorreoNoti"),
                            filtro_btn("SMSNoti"),
                            filtro_btn("NotiManager"),
                            class_name="flex items-center gap-2 mb-4 flex-wrap",
                        ),
                        rx.el.div(
                            rx.cond(
                                NotificacionState.notificaciones_filtradas.length()
                                > 0,
                                rx.el.div(
                                    rx.foreach(
                                        NotificacionState.notificaciones_filtradas,
                                        noti_card,
                                    ),
                                    class_name="flex flex-col gap-2.5",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "bell-off",
                                        class_name="h-10 w-10 text-gray-300 mb-2",
                                    ),
                                    rx.el.p(
                                        "Sin notificaciones",
                                        class_name="text-sm font-semibold text-gray-700",
                                    ),
                                    rx.el.p(
                                        "No hay mensajes en este filtro",
                                        class_name="text-xs text-gray-500",
                                    ),
                                    class_name="flex flex-col items-center justify-center py-12 bg-white border border-dashed border-gray-300 rounded-xl",
                                ),
                            ),
                        ),
                    ),
                    class_name="lg:col-span-2",
                ),
                programar_form(),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-5",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )