import reflex as rx
from tick_ez.states.ticket_state import TicketState
from tick_ez.components.event_card import event_card


def categoria_destacada(
    nombre: str, icon: str, descripcion: str, color_bg: str, color_icon: str
) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 {color_icon}"),
            class_name=f"p-3 rounded-lg {color_bg} w-fit mb-3",
        ),
        rx.el.h3(
            nombre,
            class_name="text-base font-bold text-gray-900 mb-1 text-left",
        ),
        rx.el.p(descripcion, class_name="text-xs text-gray-600 text-left"),
        on_click=lambda: TicketState.set_filtro_categoria(nombre),
        class_name="bg-white p-5 rounded-xl border border-gray-200 hover:border-violet-300 hover:shadow-sm transition-all text-left",
    )


def comprar_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Comprar tickets",
                    class_name="text-2xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    "Explora por categoría o descubre los eventos más populares",
                    class_name="text-sm text-gray-600",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                categoria_destacada(
                    "Concierto",
                    "music",
                    "Los mejores artistas en vivo",
                    "bg-violet-50",
                    "text-violet-600",
                ),
                categoria_destacada(
                    "Convención",
                    "users",
                    "Eventos y experiencias únicas",
                    "bg-blue-50",
                    "text-blue-600",
                ),
                categoria_destacada(
                    "Teatro",
                    "drama",
                    "Obras y espectáculos clásicos",
                    "bg-amber-50",
                    "text-amber-600",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Eventos destacados",
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.button(
                        "Ver todos",
                        rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
                        on_click=lambda: TicketState.cambiar_seccion("eventos"),
                        class_name="flex items-center gap-1 text-sm font-semibold text-violet-600 hover:text-violet-700",
                    ),
                    class_name="flex items-center justify-between mb-4",
                ),
                rx.el.div(
                    rx.foreach(TicketState.eventos[:6], event_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5",
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )