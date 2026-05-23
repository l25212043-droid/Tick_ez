import reflex as rx
from tick_ez.states.ticket_state import TicketState
from tick_ez.states.whatsapp_state import WhatsAppState
from tick_ez.components.mapa_recinto import mapa_compacto
from tick_ez.components.spotify_section import spotify_mini_player


def categoria_option(
    nombre: str, descripcion: str, multiplicador: str
) -> rx.Component:
    is_selected = TicketState.compra_categoria == nombre
    is_star = nombre == "TicketStar"
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        is_star,
                        rx.icon(
                            "accessibility",
                            class_name="h-3.5 w-3.5 text-teal-600",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.p(
                        nombre, class_name="text-sm font-bold text-gray-900"
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                rx.el.p(descripcion, class_name="text-xs text-gray-500"),
                class_name="text-left",
            ),
            rx.el.span(
                multiplicador,
                class_name=rx.cond(
                    is_star,
                    "text-xs font-semibold text-teal-600",
                    "text-xs font-semibold text-violet-600",
                ),
            ),
            class_name="flex items-center justify-between w-full",
        ),
        on_click=lambda: TicketState.set_compra_categoria(nombre),
        type="button",
        class_name=rx.cond(
            is_selected,
            rx.cond(
                is_star,
                "p-3 rounded-lg border-2 border-teal-500 bg-teal-50 transition-all w-full",
                "p-3 rounded-lg border-2 border-violet-500 bg-violet-50 transition-all w-full",
            ),
            "p-3 rounded-lg border-2 border-gray-200 bg-white hover:border-gray-300 transition-all w-full",
        ),
    )


def compra_dialog() -> rx.Component:
    return rx.cond(
        TicketState.show_compra,
        rx.el.div(
            rx.el.div(
                on_click=TicketState.cerrar_compra,
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Confirmar compra",
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-4 w-4"),
                            on_click=TicketState.cerrar_compra,
                            type="button",
                            class_name="p-1.5 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors",
                        ),
                        class_name="flex items-center justify-between p-5 border-b border-gray-200",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.cond(
                                        TicketState.evento_seleccionado[
                                            "imagen"
                                        ].contains(".jpg"),
                                        rx.el.img(
                                            src=TicketState.evento_seleccionado[
                                                "imagen"
                                            ],
                                            class_name="size-12 rounded-lg object-cover",
                                        ),
                                        rx.el.div(
                                            rx.icon(
                                                "ticket",
                                                class_name="h-6 w-6 text-white",
                                            ),
                                            class_name="p-3 rounded-lg bg-gradient-to-br from-violet-500 to-blue-600 flex items-center justify-center",
                                        ),
                                    ),
                                    class_name="shrink-0",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        TicketState.evento_seleccionado[
                                            "nombre"
                                        ],
                                        class_name="text-sm font-bold text-gray-900",
                                    ),
                                    rx.el.p(
                                        TicketState.evento_seleccionado["fecha"]
                                        + " · "
                                        + TicketState.evento_seleccionado[
                                            "hora"
                                        ],
                                        class_name="text-xs text-gray-500",
                                    ),
                                    rx.el.p(
                                        TicketState.evento_seleccionado[
                                            "ubicacion"
                                        ],
                                        class_name="text-xs text-gray-500",
                                    ),
                                ),
                                class_name="flex items-center gap-3 p-3 bg-gray-50 rounded-lg mb-5",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    mapa_compacto(),
                                    class_name="mb-5",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "O selecciona categoría manual",
                                    class_name="block text-xs font-semibold text-gray-700 mb-2",
                                ),
                                rx.el.div(
                                    categoria_option(
                                        "General", "Acceso estándar", "1x"
                                    ),
                                    categoria_option(
                                        "VIP",
                                        "Mejor ubicación + amenidades",
                                        "2x",
                                    ),
                                    categoria_option(
                                        "Golden", "Experiencia premium", "3x"
                                    ),
                                    categoria_option(
                                        "TicketStar",
                                        "♿ Accesibilidad + beneficios premium",
                                        "3x",
                                    ),
                                    class_name="flex flex-col gap-2",
                                ),
                                class_name="mb-5",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Cantidad de tickets",
                                    class_name="block text-xs font-semibold text-gray-700 mb-2",
                                ),
                                rx.el.div(
                                    rx.el.button(
                                        rx.icon("minus", class_name="h-4 w-4"),
                                        on_click=TicketState.dec_cantidad,
                                        type="button",
                                        class_name="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors",
                                    ),
                                    rx.el.div(
                                        TicketState.compra_cantidad,
                                        class_name="flex-1 text-center text-base font-bold text-gray-900",
                                    ),
                                    rx.el.button(
                                        rx.icon("plus", class_name="h-4 w-4"),
                                        on_click=TicketState.inc_cantidad,
                                        type="button",
                                        class_name="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors",
                                    ),
                                    class_name="flex items-center gap-3",
                                ),
                                class_name="mb-5",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Método de pago",
                                    class_name="block text-xs font-semibold text-gray-700 mb-2",
                                ),
                                rx.el.div(
                                    rx.el.select(
                                        rx.el.option(
                                            "Tarjeta de crédito/débito",
                                            value="tarjeta",
                                        ),
                                        rx.el.option("PayPal", value="paypal"),
                                        rx.el.option(
                                            "Transferencia SPEI", value="spei"
                                        ),
                                        rx.el.option("OXXO Pay", value="oxxo"),
                                        name="metodo_pago",
                                        class_name="w-full appearance-none pl-3 pr-9 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-900 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none cursor-pointer",
                                    ),
                                    rx.icon(
                                        "chevron-down",
                                        class_name="absolute right-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                                    ),
                                    class_name="relative",
                                ),
                                class_name="mb-5",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span(
                                        "Subtotal",
                                        class_name="text-sm text-gray-600",
                                    ),
                                    rx.el.span(
                                        f"${TicketState.total_compra:.2f}",
                                        class_name="text-sm font-semibold text-gray-900",
                                    ),
                                    class_name="flex justify-between mb-1",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        "Cargo de servicio",
                                        class_name="text-sm text-gray-600",
                                    ),
                                    rx.el.span(
                                        f"${TicketState.total_compra * 0.05:.2f}",
                                        class_name="text-sm font-semibold text-gray-900",
                                    ),
                                    class_name="flex justify-between mb-2 pb-2 border-b border-gray-200",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        "Total",
                                        class_name="text-base font-bold text-gray-900",
                                    ),
                                    rx.el.span(
                                        f"${TicketState.total_compra * 1.05:.2f}",
                                        class_name="text-lg font-bold text-violet-600",
                                    ),
                                    class_name="flex justify-between items-center",
                                ),
                                class_name="p-4 bg-gray-50 rounded-lg mb-5",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    "Cancelar",
                                    on_click=TicketState.cerrar_compra,
                                    type="button",
                                    class_name="flex-1 px-4 py-2.5 bg-white border border-gray-300 text-gray-700 rounded-lg text-sm font-semibold hover:bg-gray-50 transition-colors",
                                ),
                                rx.el.button(
                                    rx.icon("lock", class_name="h-4 w-4"),
                                    "Confirmar compra",
                                    type="submit",
                                    class_name="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700 transition-colors",
                                ),
                                class_name="flex gap-3",
                            ),
                            class_name="p-5",
                        ),
                        on_submit=TicketState.confirmar_compra,
                        reset_on_submit=True,
                    ),
                    class_name="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto",
                ),
                class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
            ),
        ),
        rx.fragment(),
    )


def confirmacion_dialog() -> rx.Component:
    return rx.cond(
        TicketState.show_confirmacion,
        rx.el.div(
            rx.el.div(
                on_click=TicketState.cerrar_confirmacion,
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "ticket",
                                    class_name="h-3.5 w-3.5 text-white",
                                ),
                                class_name="size-7 rounded-full bg-gradient-to-br from-teal-400 to-cyan-500 flex items-center justify-center",
                            ),
                            rx.el.div(
                                rx.el.span("Tick", class_name="text-gray-900"),
                                rx.el.span("_", class_name="text-teal-500"),
                                rx.el.span("EZ", class_name="text-violet-600"),
                                class_name="text-base font-extrabold flex items-baseline",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        rx.el.div(
                            rx.icon(
                                "check", class_name="h-4 w-4 text-emerald-600"
                            ),
                            rx.el.span(
                                "Confirmado",
                                class_name="text-xs font-semibold text-emerald-700",
                            ),
                            class_name="flex items-center gap-1 px-2 py-1 rounded-md bg-emerald-50",
                        ),
                        class_name="flex items-center justify-between mb-4",
                    ),
                    rx.el.h2(
                        "¡Compra exitosa!",
                        class_name="text-xl font-bold text-gray-900 text-center mb-1",
                    ),
                    rx.el.p(
                        "Tu ticket digital con código QR único está listo",
                        class_name="text-xs text-gray-600 text-center mb-4",
                    ),
                    rx.el.div(
                        rx.cond(
                            TicketState.ultimo_qr != "",
                            rx.el.img(
                                src=TicketState.ultimo_qr,
                                class_name="size-44 mx-auto",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "qr-code",
                                    class_name="h-16 w-16 text-gray-300",
                                ),
                                class_name="size-44 mx-auto flex items-center justify-center",
                            ),
                        ),
                        rx.el.p(
                            "Escanea en el acceso del evento",
                            class_name="text-xs text-gray-500 text-center mt-2",
                        ),
                        class_name="p-4 bg-white border-2 border-dashed border-violet-200 rounded-xl mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Folio", class_name="text-xs text-gray-500"
                            ),
                            rx.el.span(
                                TicketState.ultimo_folio,
                                class_name="text-xs font-bold text-violet-700 font-mono",
                            ),
                            class_name="flex items-center justify-between",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Categoría", class_name="text-xs text-gray-500"
                            ),
                            rx.cond(
                                TicketState.compra_categoria == "TicketStar",
                                rx.el.span(
                                    rx.icon(
                                        "accessibility",
                                        class_name="h-3 w-3",
                                    ),
                                    "TicketStar",
                                    class_name="flex items-center gap-1 text-xs font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded-md",
                                ),
                                rx.el.span(
                                    TicketState.compra_categoria,
                                    class_name="text-xs font-semibold text-gray-900",
                                ),
                            ),
                            class_name="flex items-center justify-between",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Zona", class_name="text-xs text-gray-500"
                            ),
                            rx.el.span(
                                TicketState.ultima_compra_zona,
                                class_name="text-xs font-semibold text-gray-900",
                            ),
                            class_name="flex items-center justify-between",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Titular", class_name="text-xs text-gray-500"
                            ),
                            rx.el.span(
                                TicketState.ultima_compra_titular,
                                class_name="text-xs font-semibold text-gray-900",
                            ),
                            class_name="flex items-center justify-between",
                        ),
                        class_name="p-3 bg-gray-50 rounded-lg mb-4 flex flex-col gap-1.5",
                    ),
                    rx.el.div(
                        rx.el.div(
                            spotify_mini_player(),
                            class_name="mb-3",
                        ),
                        rx.el.button(
                            rx.icon("file-down", class_name="h-4 w-4"),
                            "Descargar ticket en PDF",
                            on_click=TicketState.descargar_ultimo_ticket,
                            class_name="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-teal-500 to-cyan-500 text-white rounded-lg text-sm font-semibold hover:from-teal-600 hover:to-cyan-600 transition-colors mb-2",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("message-circle", class_name="h-4 w-4"),
                                "WhatsApp",
                                on_click=lambda: (
                                    WhatsAppState.preparar_mensaje_compra(
                                        TicketState.ultimo_folio,
                                        TicketState.evento_seleccionado[
                                            "nombre"
                                        ],
                                        TicketState.evento_seleccionado[
                                            "nombre"
                                        ],
                                    )
                                ),
                                class_name="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-emerald-600 text-white rounded-lg text-sm font-semibold hover:bg-emerald-700 transition-colors",
                            ),
                            rx.el.button(
                                "Aceptar",
                                on_click=TicketState.cerrar_confirmacion,
                                class_name="flex-1 px-4 py-2.5 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700 transition-colors",
                            ),
                            class_name="flex gap-2",
                        ),
                        class_name="p-6",
                    ),
                    class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl w-full max-w-md z-50 max-h-[90vh] overflow-y-auto",
                ),
            ),
        ),
        rx.fragment(),
    )