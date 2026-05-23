import reflex as rx
from tick_ez.states.ticket_state import TicketState, Event


def category_badge(category: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.match(
            category,
            (
                "Concierto",
                rx.el.div(
                    rx.icon("music", class_name="h-3 w-3"),
                    rx.el.span("Concierto"),
                    class_name="flex items-center gap-1 px-2 py-1 rounded-md bg-violet-50 text-violet-700 text-xs font-semibold w-fit",
                ),
            ),
            (
                "Convención",
                rx.el.div(
                    rx.icon("users", class_name="h-3 w-3"),
                    rx.el.span("Convención"),
                    class_name="flex items-center gap-1 px-2 py-1 rounded-md bg-blue-50 text-blue-700 text-xs font-semibold w-fit",
                ),
            ),
            (
                "Teatro",
                rx.el.div(
                    rx.icon("drama", class_name="h-3 w-3"),
                    rx.el.span("Teatro"),
                    class_name="flex items-center gap-1 px-2 py-1 rounded-md bg-amber-50 text-amber-700 text-xs font-semibold w-fit",
                ),
            ),
            rx.el.div("Evento", class_name="text-xs"),
        ),
    )


def event_card(event: Event) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.cond(
                event["imagen"].contains(".jpg"),
                rx.el.img(
                    src=event["imagen"],
                    class_name="w-full h-full object-cover object-center absolute inset-0",
                ),
                rx.el.div(
                    rx.icon(
                        "ticket",
                        class_name="h-12 w-12 text-white/90",
                    ),
                    class_name="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-violet-500 via-purple-600 to-blue-600",
                ),
            ),
            rx.el.div(
                class_name="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent",
            ),
            rx.el.div(
                category_badge(event["categoria"]),
                class_name="absolute top-3 left-3 z-10",
            ),
            rx.el.div(
                rx.icon(
                    "star", class_name="h-3 w-3 text-amber-400 fill-amber-400"
                ),
                rx.el.span(
                    event["rating"].to_string(),
                    class_name="text-xs font-semibold text-white",
                ),
                class_name="absolute top-3 right-3 flex items-center gap-1 px-2 py-1 rounded-md bg-black/40 backdrop-blur-sm z-10",
            ),
            class_name="relative h-48 rounded-t-xl overflow-hidden bg-gray-200",
        ),
        rx.el.div(
            rx.el.h3(
                event["nombre"],
                class_name="text-base font-bold text-gray-900 mb-1 line-clamp-1",
            ),
            rx.el.p(
                event["artista"],
                class_name="text-sm text-gray-600 mb-3 line-clamp-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("calendar", class_name="h-3.5 w-3.5 text-gray-400"),
                    rx.el.span(
                        event["fecha"],
                        class_name="text-xs text-gray-600 font-medium",
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                rx.el.div(
                    rx.icon("clock", class_name="h-3.5 w-3.5 text-gray-400"),
                    rx.el.span(
                        event["hora"],
                        class_name="text-xs text-gray-600 font-medium",
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                class_name="flex items-center gap-3 mb-2",
            ),
            rx.el.div(
                rx.icon("map-pin", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(
                    f"{event['ubicacion']}, {event['ciudad']}",
                    class_name="text-xs text-gray-600 font-medium line-clamp-1",
                ),
                class_name="flex items-center gap-1.5 mb-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        class_name="h-1.5 bg-violet-500 rounded-full",
                        style={
                            "width": (
                                event["asientos_disponibles"]
                                * 100
                                / event["asientos_totales"]
                            ).to_string()
                            + "%"
                        },
                    ),
                    class_name="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden mb-1.5",
                ),
                rx.el.p(
                    f"{event['asientos_disponibles']} asientos disponibles",
                    class_name="text-xs text-gray-500 font-medium",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("Desde", class_name="text-xs text-gray-500"),
                    rx.el.p(
                        f"${event['precio_min']:.0f}",
                        class_name="text-lg font-bold text-gray-900",
                    ),
                ),
                rx.el.button(
                    "Comprar",
                    rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
                    on_click=lambda: TicketState.abrir_compra(event["id"]),
                    class_name="flex items-center gap-1.5 px-4 py-2 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700 transition-colors",
                ),
                class_name="flex items-center justify-between pt-3 border-t border-gray-100",
            ),
            class_name="p-4",
        ),
        class_name="bg-white rounded-xl border border-gray-200 hover:border-violet-300 hover:shadow-md transition-all overflow-hidden",
    )