import reflex as rx
from tick_ez.states.ticket_state import TicketState
from tick_ez.components.logo import logo


def metric_card(
    label: str, value: rx.Var | str, icon: str, color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"h-5 w-5 {color}"),
                class_name=f"p-2.5 rounded-lg bg-gray-50",
            ),
            rx.el.span(
                "+12.5%",
                class_name="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900 mb-1"),
        rx.el.p(label, class_name="text-sm text-gray-500 font-medium"),
        class_name="bg-white p-5 rounded-xl border border-gray-200 hover:border-violet-200 hover:shadow-sm transition-all",
    )


def hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        logo("lg"),
                        class_name="mb-5",
                    ),
                    rx.el.div(
                        rx.icon("sparkles", class_name="h-3.5 w-3.5"),
                        rx.el.span("Plataforma oficial de tickets"),
                        class_name="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-violet-50 text-violet-700 text-xs font-semibold mb-5",
                    ),
                    rx.el.h1(
                        "Tu próxima experiencia ",
                        rx.el.span(
                            "inolvidable",
                            class_name="bg-gradient-to-r from-violet-600 to-blue-600 bg-clip-text text-transparent",
                        ),
                        " comienza aquí",
                        class_name="text-4xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-4",
                    ),
                    rx.el.p(
                        "Compra y vende tickets de los mejores conciertos, convenciones y obras de teatro. Seguro, rápido y sin complicaciones.",
                        class_name="text-base text-gray-600 max-w-2xl mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("search", class_name="h-4 w-4"),
                            "Explorar eventos",
                            on_click=lambda: TicketState.cambiar_seccion(
                                "eventos"
                            ),
                            class_name="flex items-center gap-2 px-5 py-2.5 bg-violet-600 text-white rounded-lg font-semibold text-sm hover:bg-violet-700 transition-colors",
                        ),
                        rx.el.button(
                            rx.icon("tag", class_name="h-4 w-4"),
                            "Vender mis tickets",
                            on_click=lambda: TicketState.cambiar_seccion(
                                "vender"
                            ),
                            class_name="flex items-center gap-2 px-5 py-2.5 bg-white border border-gray-300 text-gray-700 rounded-lg font-semibold text-sm hover:bg-gray-50 transition-colors",
                        ),
                        class_name="flex flex-wrap gap-3",
                    ),
                    class_name="mb-10",
                ),
                rx.el.div(
                    metric_card(
                        "Eventos disponibles",
                        TicketState.total_eventos.to_string(),
                        "calendar",
                        "text-violet-600",
                    ),
                    metric_card(
                        "Asientos en venta",
                        TicketState.total_asientos.to_string(),
                        "armchair",
                        "text-blue-600",
                    ),
                    metric_card(
                        "Mis compras",
                        TicketState.total_compras.to_string(),
                        "shopping-bag",
                        "text-emerald-600",
                    ),
                    metric_card(
                        "Total gastado",
                        f"${TicketState.total_gastado:.0f}",
                        "wallet",
                        "text-amber-600",
                    ),
                    class_name="grid grid-cols-2 lg:grid-cols-4 gap-4",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
            ),
            class_name="bg-gradient-to-b from-white to-gray-50 border-b border-gray-200",
        )
    )