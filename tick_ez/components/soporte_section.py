import reflex as rx
from tick_ez.states.soporte_state import SoporteState
from tick_ez.states.whatsapp_state import WhatsAppState


def prioridad_badge(prioridad: rx.Var) -> rx.Component:
    return rx.match(
        prioridad,
        (
            "Alta",
            rx.el.span(
                "Alta",
                class_name="px-2 py-0.5 rounded-md bg-red-50 text-red-700 text-xs font-semibold w-fit",
            ),
        ),
        (
            "Media",
            rx.el.span(
                "Media",
                class_name="px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 text-xs font-semibold w-fit",
            ),
        ),
        (
            "Baja",
            rx.el.span(
                "Baja",
                class_name="px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 text-xs font-semibold w-fit",
            ),
        ),
        rx.el.span("—"),
    )


def estado_solicitud_badge(estado: rx.Var) -> rx.Component:
    return rx.match(
        estado,
        (
            "Resuelto",
            rx.el.span(
                "Resuelto",
                class_name="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 text-xs font-semibold w-fit",
            ),
        ),
        (
            "En proceso",
            rx.el.span(
                "En proceso",
                class_name="px-2 py-0.5 rounded-md bg-violet-50 text-violet-700 text-xs font-semibold w-fit",
            ),
        ),
        (
            "Pendiente",
            rx.el.span(
                "Pendiente",
                class_name="px-2 py-0.5 rounded-md bg-gray-100 text-gray-700 text-xs font-semibold w-fit",
            ),
        ),
        rx.el.span("—"),
    )


def solicitud_card(s: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    s["folio"],
                    class_name="text-xs text-gray-500 font-mono mb-0.5",
                ),
                rx.el.p(
                    s["categoria_ayuda"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
            ),
            rx.el.div(
                prioridad_badge(s["prioridad"]),
                estado_solicitud_badge(s["estado"]),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-start justify-between mb-2",
        ),
        rx.el.p(
            s["descripcion"],
            class_name="text-xs text-gray-600 mb-3",
        ),
        rx.el.div(
            rx.el.span(s["fecha"], class_name="text-xs text-gray-400"),
            rx.el.div(
                rx.cond(
                    s["mailto_link"] != "",
                    rx.el.button(
                        rx.icon("mail", class_name="h-3 w-3"),
                        "Reenviar correo",
                        on_click=lambda: SoporteState.reenviar_mailto(
                            s["mailto_link"]
                        ),
                        class_name="flex items-center gap-1 px-2 py-1 text-xs font-semibold text-teal-700 hover:bg-teal-50 rounded",
                    ),
                    rx.fragment(),
                ),
                rx.el.button(
                    rx.icon("message-circle", class_name="h-3 w-3"),
                    "WhatsApp",
                    on_click=lambda: WhatsAppState.preparar_mensaje_soporte(
                        s["folio"], s["categoria_ayuda"], s["descripcion"]
                    ),
                    class_name="flex items-center gap-1 px-2 py-1 text-xs font-semibold text-emerald-700 hover:bg-emerald-50 rounded",
                ),
                rx.el.button(
                    "En proceso",
                    on_click=lambda: SoporteState.cambiar_estado_solicitud(
                        s["folio"], "En proceso"
                    ),
                    class_name="px-2 py-1 text-xs font-semibold text-violet-700 hover:bg-violet-50 rounded",
                ),
                rx.el.button(
                    "Resuelto",
                    on_click=lambda: SoporteState.cambiar_estado_solicitud(
                        s["folio"], "Resuelto"
                    ),
                    class_name="px-2 py-1 text-xs font-semibold text-emerald-700 hover:bg-emerald-50 rounded",
                ),
                class_name="flex items-center gap-1 flex-wrap",
            ),
            class_name="flex items-center justify-between pt-2 border-t border-gray-100 gap-2 flex-wrap",
        ),
        class_name="bg-white p-4 rounded-lg border border-gray-200",
    )


def mensaje_burbuja(m: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                m["autor"],
                class_name=rx.cond(
                    m["es_usuario"],
                    "text-xs font-semibold text-violet-100 mb-0.5",
                    "text-xs font-semibold text-gray-500 mb-0.5",
                ),
            ),
            rx.el.p(
                m["texto"],
                class_name=rx.cond(
                    m["es_usuario"],
                    "text-sm text-white",
                    "text-sm text-gray-900",
                ),
            ),
            rx.el.p(
                m["hora"],
                class_name=rx.cond(
                    m["es_usuario"],
                    "text-xs text-violet-200 mt-1 text-right",
                    "text-xs text-gray-400 mt-1",
                ),
            ),
            class_name=rx.cond(
                m["es_usuario"],
                "bg-violet-600 rounded-2xl rounded-tr-sm px-4 py-2.5 max-w-[75%]",
                "bg-gray-100 rounded-2xl rounded-tl-sm px-4 py-2.5 max-w-[75%]",
            ),
        ),
        class_name=rx.cond(
            m["es_usuario"],
            "flex justify-end mb-2",
            "flex justify-start mb-2",
        ),
    )


def sugerencia_chip(label: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: SoporteState.enviar_mensaje({"mensaje": label}),
        type="button",
        class_name="px-2.5 py-1 rounded-full bg-violet-50 text-violet-700 text-xs font-semibold hover:bg-violet-100 border border-violet-100",
    )


def chat_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "headphones",
                        class_name="h-4 w-4 text-emerald-600",
                    ),
                    class_name="p-2 rounded-full bg-emerald-50",
                ),
                rx.el.div(
                    rx.el.p(
                        "Asistente Tick_EZ",
                        class_name="text-sm font-bold text-gray-900",
                    ),
                    rx.el.div(
                        rx.el.span(
                            class_name="size-1.5 rounded-full bg-emerald-500"
                        ),
                        rx.el.span(
                            "Respuestas inteligentes en línea",
                            class_name="text-xs text-emerald-600 font-medium",
                        ),
                        class_name="flex items-center gap-1.5",
                    ),
                ),
                rx.el.button(
                    rx.icon("message_circle_x", class_name="h-4 w-4"),
                    "Finalizar",
                    on_click=SoporteState.finalizar_chat,
                    class_name="ml-auto flex items-center gap-1 px-2.5 py-1.5 bg-red-50 text-red-700 rounded-md text-xs font-semibold hover:bg-red-100",
                ),
                class_name="flex items-center gap-3 p-4 border-b border-gray-200",
            ),
            rx.el.div(
                rx.foreach(SoporteState.chat_mensajes, mensaje_burbuja),
                class_name="p-4 h-80 overflow-y-auto bg-gray-50",
            ),
            rx.el.div(
                rx.el.p(
                    "Sugerencias rápidas",
                    class_name="text-xs font-semibold text-gray-500 mb-2",
                ),
                rx.el.div(
                    sugerencia_chip("Reembolso"),
                    sugerencia_chip("Mi QR no escanea"),
                    sugerencia_chip("Descargar PDF"),
                    sugerencia_chip("Cambio de titular"),
                    sugerencia_chip("TicketStar accesible"),
                    sugerencia_chip("Pago duplicado"),
                    sugerencia_chip("No me llegó el correo"),
                    class_name="flex flex-wrap gap-1.5",
                ),
                class_name="px-3 pt-3 border-t border-gray-100 bg-white",
            ),
            rx.el.form(
                rx.el.input(
                    name="mensaje",
                    placeholder="Escribe tu mensaje y presiona Enter...",
                    default_value=SoporteState.nuevo_mensaje,
                    key=SoporteState.chat_input_key.to_string(),
                    auto_complete="off",
                    class_name="flex-1 px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                ),
                rx.el.button(
                    rx.icon("send", class_name="h-4 w-4"),
                    type="submit",
                    class_name="p-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700",
                ),
                on_submit=SoporteState.enviar_mensaje,
                reset_on_submit=True,
                class_name="flex items-center gap-2 p-3 border-t border-gray-200",
            ),
            class_name="bg-white rounded-xl border border-gray-200 overflow-hidden",
        ),
    )


def solicitud_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("file-plus", class_name="h-5 w-5 text-violet-600"),
            rx.el.h3(
                "Nueva solicitud",
                class_name="text-base font-bold text-gray-900",
            ),
            class_name="flex items-center gap-2 mb-3",
        ),
        rx.el.div(
            rx.icon(
                "info",
                class_name="h-3.5 w-3.5 text-blue-600 shrink-0 mt-0.5",
            ),
            rx.el.p(
                "Tu solicitud se registra internamente y se envía por correo a tickez.mx@gmail.com mediante tu cliente de email.",
                class_name="text-xs text-blue-700",
            ),
            class_name="flex items-start gap-1.5 p-2.5 bg-blue-50 rounded-lg mb-3",
        ),
        rx.cond(
            SoporteState.show_solicitud_exito,
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "circle_check",
                        class_name="h-4 w-4 text-emerald-600 shrink-0 mt-0.5",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "✓ Solicitud creada exitosamente",
                            class_name="text-xs font-bold text-emerald-800 mb-0.5",
                        ),
                        rx.el.p(
                            f"Folio {SoporteState.ultima_solicitud_folio} · enviado a tickez.mx@gmail.com",
                            class_name="text-xs text-emerald-700 mb-2",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("mail", class_name="h-3 w-3"),
                                "Reenviar correo",
                                on_click=lambda: SoporteState.reenviar_mailto(
                                    SoporteState.ultimo_mailto
                                ),
                                class_name="flex items-center gap-1 px-2.5 py-1 bg-emerald-600 text-white rounded-md text-xs font-semibold hover:bg-emerald-700",
                            ),
                            rx.el.button(
                                "Cerrar",
                                on_click=SoporteState.cerrar_solicitud_exito,
                                class_name="px-2.5 py-1 text-xs font-semibold text-emerald-700 hover:bg-emerald-100 rounded-md",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex items-start gap-2",
                ),
                class_name="p-3 bg-emerald-50 border border-emerald-200 rounded-lg mb-3",
            ),
            rx.fragment(),
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Categoría de ayuda",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Reembolso", value="Reembolso"),
                        rx.el.option(
                            "Cambio de titular", value="Cambio de titular"
                        ),
                        rx.el.option(
                            "Acceso al ticket digital",
                            value="Acceso al ticket digital",
                        ),
                        rx.el.option("Pago duplicado", value="Pago duplicado"),
                        rx.el.option("Otro", value="Otro"),
                        name="categoria",
                        class_name="w-full appearance-none pl-3 pr-9 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none cursor-pointer",
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
                rx.el.label(
                    "Prioridad",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Baja", value="Baja"),
                        rx.el.option("Media", value="Media"),
                        rx.el.option("Alta", value="Alta"),
                        name="prioridad",
                        default_value="Media",
                        class_name="w-full appearance-none pl-3 pr-9 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none cursor-pointer",
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
                rx.el.label(
                    "Descripción",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.textarea(
                    name="descripcion",
                    placeholder="Describe tu problema o consulta...",
                    rows="4",
                    required=True,
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-900 placeholder-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none resize-none",
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                rx.icon("send", class_name="h-4 w-4"),
                "Enviar solicitud",
                type="submit",
                class_name="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700",
            ),
            on_submit=SoporteState.crear_solicitud,
            reset_on_submit=True,
        ),
        class_name="bg-white p-5 rounded-xl border border-gray-200",
    )


def soporte_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Soporte técnico",
                    class_name="text-2xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    "Crea solicitudes y comunícate con nuestro equipo en tiempo real",
                    class_name="text-sm text-gray-600",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    solicitud_form(),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "list-todo",
                                class_name="h-5 w-5 text-violet-600",
                            ),
                            rx.el.h3(
                                "Mis solicitudes",
                                class_name="text-base font-bold text-gray-900",
                            ),
                            rx.el.span(
                                SoporteState.solicitudes.length().to_string(),
                                class_name="ml-auto px-2 py-0.5 rounded-md bg-violet-50 text-violet-700 text-xs font-semibold",
                            ),
                            class_name="flex items-center gap-2 mb-4",
                        ),
                        rx.el.div(
                            rx.cond(
                                SoporteState.solicitudes.length() > 0,
                                rx.el.div(
                                    rx.foreach(
                                        SoporteState.solicitudes, solicitud_card
                                    ),
                                    class_name="flex flex-col gap-2.5",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "inbox",
                                        class_name="h-10 w-10 text-gray-300 mb-2",
                                    ),
                                    rx.el.p(
                                        "Sin solicitudes",
                                        class_name="text-sm font-semibold text-gray-700",
                                    ),
                                    rx.el.p(
                                        "Crea una solicitud cuando lo necesites",
                                        class_name="text-xs text-gray-500",
                                    ),
                                    class_name="flex flex-col items-center justify-center py-10 border border-dashed border-gray-300 rounded-lg",
                                ),
                            ),
                            class_name="bg-white p-5 rounded-xl border border-gray-200 mt-5",
                        ),
                    ),
                    class_name="flex flex-col",
                ),
                chat_panel(),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-5",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )