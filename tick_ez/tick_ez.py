import reflex as rx
from tick_ez.states.ticket_state import TicketState
from tick_ez.components.navbar import navbar, reproductor_global
from tick_ez.components.hero import hero
from tick_ez.components.eventos_section import eventos_section
from tick_ez.components.comprar_section import comprar_section
from tick_ez.components.vender_section import vender_section
from tick_ez.components.historial_section import historial_section
from tick_ez.components.compra_dialog import compra_dialog, confirmacion_dialog
from tick_ez.components.event_card import event_card
from tick_ez.components.cuenta_section import cuenta_section
from tick_ez.components.soporte_section import soporte_section
from tick_ez.components.notificaciones_section import notificaciones_section
from tick_ez.components.arquitectura_section import arquitectura_section
from tick_ez.components.login_dialog import login_dialog
from tick_ez.components.logo import logo
from tick_ez.components.mapas_section import mapas_section
from tick_ez.components.spotify_section import spotify_section
from tick_ez.components.whatsapp_section import whatsapp_section


def inicio_view() -> rx.Component:
    return rx.el.div(
        hero(),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Eventos populares",
                            class_name="text-2xl font-bold text-gray-900 mb-1",
                        ),
                        rx.el.p(
                            "Los eventos más buscados de la temporada",
                            class_name="text-sm text-gray-600",
                        ),
                    ),
                    rx.el.button(
                        "Ver catálogo",
                        rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
                        on_click=lambda: TicketState.cambiar_seccion("eventos"),
                        class_name="flex items-center gap-1.5 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg text-sm font-semibold hover:bg-gray-50 transition-colors",
                    ),
                    class_name="flex items-center justify-between mb-6",
                ),
                rx.el.div(
                    rx.foreach(TicketState.eventos[:6], event_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
            ),
        ),
    )


def index() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.match(
            TicketState.seccion_activa,
            ("inicio", inicio_view()),
            ("eventos", eventos_section()),
            ("comprar", comprar_section()),
            ("vender", vender_section()),
            ("historial", historial_section()),
            ("cuenta", cuenta_section()),
            ("soporte", soporte_section()),
            ("notificaciones", notificaciones_section()),
            ("arquitectura", arquitectura_section()),
            ("mapas", mapas_section()),
            ("spotify", spotify_section()),
            ("whatsapp", whatsapp_section()),
            inicio_view(),
        ),
        reproductor_global(),
        compra_dialog(),
        confirmacion_dialog(),
        login_dialog(),
        rx.el.footer(
            rx.el.div(
                logo("sm"),
                rx.el.p(
                    "© 2026 Tick_EZ · Plataforma oficial de tickets con QR único.",
                    class_name="text-xs text-gray-500 mt-2",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6",
            ),
            class_name="bg-white border-t border-gray-200 mt-10",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=TicketState.seed_historial)