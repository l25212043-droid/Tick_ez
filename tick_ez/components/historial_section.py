import reflex as rx
from tick_ez.states.ticket_state import TicketState
from tick_ez.states.whatsapp_state import WhatsAppState


def compra_card(compra: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.cond(
                compra["qr_data_url"] != "",
                rx.el.img(
                    src=compra["qr_data_url"],
                    class_name="size-20 rounded-lg border border-gray-200 bg-white p-1 shrink-0",
                ),
                rx.el.div(
                    rx.icon("qr-code", class_name="h-8 w-8 text-gray-300"),
                    class_name="size-20 rounded-lg border border-gray-200 bg-white flex items-center justify-center shrink-0",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        compra["evento"],
                        class_name="text-sm font-semibold text-gray-900 mb-0.5",
                    ),
                    rx.cond(
                        compra["estado"] == "Confirmado",
                        rx.el.div(
                            rx.icon("circle_check", class_name="h-3 w-3"),
                            rx.el.span("Confirmado"),
                            class_name="flex items-center gap-1 px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 text-xs font-semibold w-fit",
                        ),
                        rx.el.div(
                            rx.icon("clock", class_name="h-3 w-3"),
                            rx.el.span("Pendiente"),
                            class_name="flex items-center gap-1 px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 text-xs font-semibold w-fit",
                        ),
                    ),
                    class_name="flex items-start justify-between gap-2 mb-1",
                ),
                rx.el.p(
                    compra["folio"],
                    class_name="text-xs text-violet-700 font-mono mb-1",
                ),
                rx.el.div(
                    rx.cond(
                        compra["categoria_ticket"] == "TicketStar",
                        rx.el.span(
                            rx.icon("accessibility", class_name="h-3 w-3"),
                            f"{compra['cantidad']} × TicketStar",
                            class_name="flex items-center gap-1 text-xs font-bold text-teal-700 bg-teal-50 px-1.5 py-0.5 rounded-md",
                        ),
                        rx.el.span(
                            f"{compra['cantidad']} × {compra['categoria_ticket']}",
                            class_name="text-xs text-gray-600",
                        ),
                    ),
                    rx.el.span("·", class_name="text-gray-300"),
                    rx.el.span(
                        compra["zona"],
                        class_name="text-xs text-gray-600",
                    ),
                    rx.el.span("·", class_name="text-gray-300"),
                    rx.el.span(
                        compra["titular"],
                        class_name="text-xs text-gray-600",
                    ),
                    class_name="flex items-center gap-1.5 flex-wrap mb-1",
                ),
                rx.el.div(
                    rx.el.span(
                        compra["fecha"],
                        class_name="text-xs text-gray-400",
                    ),
                    rx.el.span(
                        f"${compra['total']:.2f}",
                        class_name="text-sm font-bold text-gray-900 ml-auto",
                    ),
                    class_name="flex items-center justify-between",
                ),
                class_name="flex-1 min-w-0",
            ),
            class_name="flex items-start gap-3 w-full",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("file-down", class_name="h-3.5 w-3.5"),
                "Descargar PDF",
                on_click=lambda: TicketState.descargar_ticket_pdf(
                    compra["folio"]
                ),
                class_name="flex items-center gap-1.5 px-3 py-1.5 bg-teal-50 text-teal-700 rounded-md text-xs font-semibold hover:bg-teal-100",
            ),
            rx.el.button(
                rx.icon("message-circle", class_name="h-3.5 w-3.5"),
                "WhatsApp",
                on_click=lambda: WhatsAppState.preparar_mensaje_compra(
                    compra["folio"], compra["evento"], compra["ticket_id"]
                ),
                class_name="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-md text-xs font-semibold hover:bg-emerald-100",
            ),
            class_name="flex items-center gap-2 mt-3 pt-3 border-t border-gray-100 flex-wrap",
        ),
        class_name="p-4 bg-white border border-gray-200 rounded-lg hover:border-violet-200 transition-colors",
    )


def historial_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Mis compras",
                        class_name="text-2xl font-bold text-gray-900 mb-1",
                    ),
                    rx.el.p(
                        "Historial completo de tus tickets adquiridos",
                        class_name="text-sm text-gray-600",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Total compras",
                            class_name="text-xs text-gray-500",
                        ),
                        rx.el.p(
                            TicketState.total_compras.to_string(),
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        class_name="text-right",
                    ),
                    rx.el.div(class_name="w-px h-8 bg-gray-200"),
                    rx.el.div(
                        rx.el.p(
                            "Total gastado",
                            class_name="text-xs text-gray-500",
                        ),
                        rx.el.p(
                            f"${TicketState.total_gastado:.2f}",
                            class_name="text-lg font-bold text-violet-600",
                        ),
                        class_name="text-right",
                    ),
                    class_name="hidden sm:flex items-center gap-4 px-4 py-2 bg-white border border-gray-200 rounded-lg",
                ),
                class_name="flex items-end justify-between mb-6 gap-4",
            ),
            rx.cond(
                TicketState.historial_compras.length() > 0,
                rx.el.div(
                    rx.foreach(TicketState.historial_compras, compra_card),
                    class_name="flex flex-col gap-3",
                ),
                rx.el.div(
                    rx.icon(
                        "receipt", class_name="h-12 w-12 text-gray-300 mb-3"
                    ),
                    rx.el.p(
                        "Aún no tienes compras",
                        class_name="text-base font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.p(
                        "Explora el catálogo y compra tus primeros tickets",
                        class_name="text-sm text-gray-500 mb-4",
                    ),
                    rx.el.button(
                        rx.icon("search", class_name="h-4 w-4"),
                        "Explorar eventos",
                        on_click=lambda: TicketState.cambiar_seccion("eventos"),
                        class_name="flex items-center gap-2 px-4 py-2 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700",
                    ),
                    class_name="flex flex-col items-center justify-center py-16 bg-white rounded-xl border border-gray-200",
                ),
            ),
            class_name="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )