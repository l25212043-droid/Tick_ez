import reflex as rx
from tick_ez.states.ticket_state import TicketState
from tick_ez.components.event_card import event_card


def filter_select(
    label: str, value: rx.Var, options: rx.Var, on_change
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label, class_name="block text-xs font-semibold text-gray-700 mb-1.5"
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(options, lambda opt: rx.el.option(opt, value=opt)),
                value=value,
                on_change=on_change,
                class_name="w-full appearance-none pl-3 pr-9 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium text-gray-700 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none cursor-pointer",
            ),
            rx.icon(
                "chevron-down",
                class_name="absolute right-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
            ),
            class_name="relative",
        ),
    )


def filter_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400",
                ),
                rx.el.input(
                    placeholder="Buscar por nombre o artista...",
                    default_value=TicketState.busqueda,
                    on_change=TicketState.set_busqueda.debounce(400),
                    class_name="w-full pl-9 pr-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                ),
                class_name="relative",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            filter_select(
                "Categoría",
                TicketState.filtro_categoria,
                TicketState.categorias,
                TicketState.set_filtro_categoria,
            ),
            filter_select(
                "Ciudad",
                TicketState.filtro_ciudad,
                TicketState.ciudades,
                TicketState.set_filtro_ciudad,
            ),
            filter_select(
                "Precio",
                TicketState.filtro_precio,
                TicketState.rangos_precio,
                TicketState.set_filtro_precio,
            ),
            rx.el.div(
                rx.el.label(
                    " ",
                    class_name="block text-xs font-semibold text-gray-700 mb-1.5 invisible",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-3.5 w-3.5"),
                    "Limpiar",
                    on_click=TicketState.limpiar_filtros,
                    class_name="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-semibold hover:bg-gray-200 transition-colors",
                ),
            ),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-3",
        ),
        class_name="bg-white p-4 rounded-xl border border-gray-200 mb-6",
    )


def eventos_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("calendar", class_name="h-3.5 w-3.5"),
                    rx.el.span("Catálogo en vivo"),
                    class_name="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-violet-50 text-violet-700 text-xs font-semibold mb-3",
                ),
                rx.el.h2(
                    "Catálogo de eventos",
                    class_name="text-2xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    rx.el.span(
                        TicketState.eventos_filtrados.length(),
                        class_name="font-semibold text-violet-600",
                    ),
                    " eventos encontrados",
                    class_name="text-sm text-gray-600",
                ),
                class_name="mb-5",
            ),
            filter_panel(),
            rx.cond(
                TicketState.eventos_filtrados.length() > 0,
                rx.el.div(
                    rx.foreach(TicketState.eventos_filtrados, event_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5",
                ),
                rx.el.div(
                    rx.icon(
                        "search-x", class_name="h-12 w-12 text-gray-300 mb-3"
                    ),
                    rx.el.p(
                        "No se encontraron eventos",
                        class_name="text-base font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.p(
                        "Prueba ajustando los filtros de búsqueda",
                        class_name="text-sm text-gray-500 mb-4",
                    ),
                    rx.el.button(
                        "Limpiar filtros",
                        on_click=TicketState.limpiar_filtros,
                        class_name="px-4 py-2 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700 transition-colors",
                    ),
                    class_name="flex flex-col items-center justify-center py-16 bg-white rounded-xl border border-gray-200",
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )