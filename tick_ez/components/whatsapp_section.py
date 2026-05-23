import reflex as rx
from tick_ez.states.whatsapp_state import WhatsAppState


def contexto_badge(contexto: rx.Var) -> rx.Component:
    return rx.match(
        contexto,
        (
            "Compra",
            rx.el.span(
                "Compra",
                class_name="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 text-xs font-semibold w-fit",
            ),
        ),
        (
            "Soporte",
            rx.el.span(
                "Soporte",
                class_name="px-2 py-0.5 rounded-md bg-violet-50 text-violet-700 text-xs font-semibold w-fit",
            ),
        ),
        (
            "General",
            rx.el.span(
                "General",
                class_name="px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 text-xs font-semibold w-fit",
            ),
        ),
        rx.el.span(
            contexto,
            class_name="px-2 py-0.5 rounded-md bg-gray-100 text-gray-700 text-xs font-semibold w-fit",
        ),
    )


def historial_card(m: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "message-circle", class_name="h-4 w-4 text-emerald-600"
                ),
                class_name="p-2 rounded-lg bg-emerald-50 shrink-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        m["asunto"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    contexto_badge(m["contexto"]),
                    class_name="flex items-center gap-2 mb-1 flex-wrap",
                ),
                rx.el.p(
                    m["mensaje"],
                    class_name="text-xs text-gray-600 mb-2 line-clamp-2",
                ),
                rx.el.div(
                    rx.icon("user", class_name="h-3 w-3 text-gray-400"),
                    rx.el.span(
                        m["emisor"],
                        class_name="text-xs text-gray-500",
                    ),
                    rx.el.span("→", class_name="text-gray-300 mx-0.5"),
                    rx.icon("phone", class_name="h-3 w-3 text-gray-400"),
                    rx.el.span(
                        m["receptor"],
                        class_name="text-xs text-gray-500 font-mono",
                    ),
                    rx.el.span(
                        m["fecha"],
                        class_name="ml-auto text-xs text-gray-400",
                    ),
                    class_name="flex items-center gap-1 flex-wrap",
                ),
                class_name="flex-1 min-w-0",
            ),
            class_name="flex items-start gap-3 mb-3",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("external-link", class_name="h-3.5 w-3.5"),
                "Reabrir en WhatsApp",
                on_click=lambda: WhatsAppState.reabrir_link(m["wa_link"]),
                class_name="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-md text-xs font-semibold hover:bg-emerald-100",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                on_click=lambda: WhatsAppState.eliminar_mensaje(m["id"]),
                class_name="ml-auto p-1.5 rounded-md hover:bg-red-50 text-red-600",
            ),
            class_name="flex items-center gap-2 pt-2 border-t border-gray-100",
        ),
        class_name="p-4 bg-white border border-gray-200 rounded-lg hover:border-emerald-200 transition-colors",
    )


def whatsapp_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("send", class_name="h-5 w-5 text-emerald-600"),
                class_name="p-2 rounded-lg bg-emerald-50",
            ),
            rx.el.div(
                rx.el.h3(
                    "Nuevo mensaje WhatsApp",
                    class_name="text-base font-bold text-gray-900",
                ),
                rx.el.p(
                    "Genera un enlace wa.me con texto prellenado",
                    class_name="text-xs text-gray-500",
                ),
            ),
            class_name="flex items-center gap-3 mb-4",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Emisor",
                        class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                    ),
                    rx.el.input(
                        name="emisor",
                        default_value=WhatsAppState.prefill_emisor,
                        placeholder="Tu nombre",
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 outline-none",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Receptor (teléfono)",
                        class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                    ),
                    rx.el.input(
                        name="receptor",
                        default_value=WhatsAppState.prefill_receptor,
                        placeholder="+52 664 555 0192",
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 outline-none",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3",
            ),
            rx.el.div(
                rx.el.label(
                    "Asunto",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    name="asunto",
                    default_value=WhatsAppState.prefill_asunto,
                    placeholder="Compartir ticket TKT-2026-XXX",
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 outline-none",
                ),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.label(
                    "Mensaje",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.textarea(
                    name="mensaje",
                    default_value=WhatsAppState.prefill_mensaje,
                    placeholder="Escribe tu mensaje aquí...",
                    rows="6",
                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 outline-none resize-none",
                ),
                class_name="mb-3",
            ),
            rx.cond(
                WhatsAppState.error_form != "",
                rx.el.div(
                    rx.icon("circle-alert", class_name="h-4 w-4 text-red-600"),
                    rx.el.p(
                        WhatsAppState.error_form,
                        class_name="text-xs text-red-700",
                    ),
                    class_name="flex items-center gap-2 p-3 bg-red-50 border border-red-100 rounded-lg mb-3",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.icon(
                    "info",
                    class_name="h-3.5 w-3.5 text-blue-600 shrink-0 mt-0.5",
                ),
                rx.el.p(
                    "El enlace abrirá WhatsApp Web/App con tu mensaje listo para enviar. No usamos API ni credenciales.",
                    class_name="text-xs text-blue-700",
                ),
                class_name="flex items-start gap-2 p-3 bg-blue-50 rounded-lg mb-4",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("send", class_name="h-4 w-4"),
                    "Generar y abrir",
                    type="submit",
                    class_name="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-emerald-600 text-white rounded-lg text-sm font-semibold hover:bg-emerald-700 transition-colors",
                ),
                rx.el.button(
                    rx.icon("eraser", class_name="h-4 w-4"),
                    "Limpiar",
                    type="button",
                    on_click=WhatsAppState.limpiar_formulario,
                    class_name="px-4 py-2.5 bg-white border border-gray-300 text-gray-700 rounded-lg text-sm font-semibold hover:bg-gray-50",
                ),
                class_name="flex gap-2",
            ),
            on_submit=WhatsAppState.enviar_whatsapp,
            reset_on_submit=False,
        ),
        class_name="bg-white p-5 rounded-xl border border-gray-200",
    )


def whatsapp_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("message-circle", class_name="h-3.5 w-3.5"),
                    rx.el.span("Mensajería WhatsApp"),
                    class_name="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-semibold mb-3",
                ),
                rx.el.h2(
                    "WhatsApp",
                    class_name="text-2xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    "Comparte tickets, contacta soporte y envía mensajes con enlaces wa.me",
                    class_name="text-sm text-gray-600",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                whatsapp_form(),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "history", class_name="h-5 w-5 text-violet-600"
                        ),
                        rx.el.h3(
                            "Historial enviado",
                            class_name="text-base font-bold text-gray-900",
                        ),
                        rx.el.span(
                            WhatsAppState.total_enviados.to_string(),
                            class_name="ml-auto px-2 py-0.5 rounded-md bg-violet-50 text-violet-700 text-xs font-semibold",
                        ),
                        class_name="flex items-center gap-2 mb-4",
                    ),
                    rx.cond(
                        WhatsAppState.historial.length() > 0,
                        rx.el.div(
                            rx.foreach(WhatsAppState.historial, historial_card),
                            class_name="flex flex-col gap-2.5",
                        ),
                        rx.el.div(
                            rx.icon(
                                "inbox",
                                class_name="h-10 w-10 text-gray-300 mb-2",
                            ),
                            rx.el.p(
                                "Sin mensajes enviados",
                                class_name="text-sm font-semibold text-gray-700",
                            ),
                            rx.el.p(
                                "Genera tu primer mensaje desde el formulario",
                                class_name="text-xs text-gray-500",
                            ),
                            class_name="flex flex-col items-center justify-center py-12 bg-white border border-dashed border-gray-300 rounded-xl",
                        ),
                    ),
                    class_name="bg-white p-5 rounded-xl border border-gray-200",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-5",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )