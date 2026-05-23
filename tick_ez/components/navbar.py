import reflex as rx
from tick_ez.states.ticket_state import TicketState
from tick_ez.states.auth_state import AuthState
from tick_ez.states.notificacion_state import NotificacionState
from tick_ez.components.logo import logo


def nav_link(label: str, key: str, icon: str) -> rx.Component:
    is_active = TicketState.seccion_activa == key
    return rx.el.button(
        rx.icon(icon, class_name="h-4 w-4"),
        rx.el.span(label),
        on_click=lambda: TicketState.cambiar_seccion(key),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-1.5 px-3 py-2 rounded-lg bg-violet-50 text-violet-700 font-medium text-sm transition-all",
            "flex items-center gap-1.5 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 font-medium text-sm transition-all",
        ),
    )


def user_menu() -> rx.Component:
    return rx.cond(
        AuthState.is_logged_in,
        rx.el.button(
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.correo}",
                class_name="size-8 rounded-full",
            ),
            rx.el.div(
                rx.el.p(
                    AuthState.nombre_usuario,
                    class_name="text-sm font-semibold text-gray-900 leading-tight",
                ),
                rx.el.p(
                    AuthState.rol_actual,
                    class_name="text-xs text-violet-600 font-medium",
                ),
                class_name="hidden lg:block text-left",
            ),
            on_click=lambda: TicketState.cambiar_seccion("cuenta"),
            class_name="flex items-center gap-2 hover:bg-gray-50 rounded-lg px-2 py-1 transition-colors",
        ),
        rx.el.button(
            rx.icon("log-in", class_name="h-4 w-4"),
            "Iniciar sesión",
            on_click=lambda: AuthState.abrir_login("cliente"),
            class_name="flex items-center gap-1.5 px-3 py-2 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700",
        ),
    )


def mobile_nav_link(label: str, key: str, icon: str) -> rx.Component:
    is_active = TicketState.seccion_activa == key
    return rx.el.button(
        rx.icon(icon, class_name="h-4 w-4"),
        rx.el.span(label),
        on_click=lambda: TicketState.cambiar_seccion(key),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-2 px-3 py-2.5 rounded-lg bg-violet-50 text-violet-700 font-semibold text-sm w-full text-left",
            "flex items-center gap-2 px-3 py-2.5 rounded-lg text-gray-700 hover:bg-gray-100 font-medium text-sm w-full text-left",
        ),
    )


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    logo("md"),
                    on_click=lambda: TicketState.cambiar_seccion("inicio"),
                    class_name="hover:opacity-80 transition-opacity",
                ),
                rx.el.div(
                    nav_link("Inicio", "inicio", "house"),
                    nav_link("Eventos", "eventos", "calendar"),
                    nav_link("Comprar", "comprar", "shopping-cart"),
                    nav_link("Vender", "vender", "tag"),
                    nav_link("Mapas", "mapas", "map"),
                    nav_link("Música", "spotify", "music"),
                    nav_link("WhatsApp", "whatsapp", "message-circle"),
                    nav_link("Compras", "historial", "receipt"),
                    nav_link("Soporte", "soporte", "headphones"),
                    class_name="hidden lg:flex items-center gap-1",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("bell", class_name="h-4 w-4"),
                        rx.cond(
                            NotificacionState.total_no_vistas > 0,
                            rx.el.span(
                                NotificacionState.total_no_vistas.to_string(),
                                class_name="absolute -top-0.5 -right-0.5 size-4 rounded-full bg-red-500 text-white text-[10px] font-bold flex items-center justify-center",
                            ),
                            rx.fragment(),
                        ),
                        on_click=lambda: TicketState.cambiar_seccion(
                            "notificaciones"
                        ),
                        class_name="p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors relative",
                    ),
                    user_menu(),
                    rx.el.button(
                        rx.cond(
                            TicketState.mobile_menu_abierto,
                            rx.icon("x", class_name="h-5 w-5"),
                            rx.icon("menu", class_name="h-5 w-5"),
                        ),
                        on_click=TicketState.toggle_mobile_menu,
                        class_name="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex items-center justify-between w-full gap-4",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center",
        ),
        rx.cond(
            TicketState.mobile_menu_abierto,
            rx.el.div(
                rx.el.div(
                    mobile_nav_link("Inicio", "inicio", "house"),
                    mobile_nav_link("Eventos", "eventos", "calendar"),
                    mobile_nav_link("Comprar", "comprar", "shopping-cart"),
                    mobile_nav_link("Vender", "vender", "tag"),
                    mobile_nav_link("Mapas", "mapas", "map"),
                    mobile_nav_link("Música Spotify", "spotify", "music"),
                    mobile_nav_link("WhatsApp", "whatsapp", "message-circle"),
                    mobile_nav_link("Mis compras", "historial", "receipt"),
                    mobile_nav_link("Cuenta", "cuenta", "user"),
                    mobile_nav_link("Soporte", "soporte", "headphones"),
                    mobile_nav_link("Notificaciones", "notificaciones", "bell"),
                    mobile_nav_link("Arquitectura", "arquitectura", "blocks"),
                    class_name="flex flex-col gap-1 p-3",
                ),
                class_name="lg:hidden border-t border-gray-200 bg-white",
            ),
            rx.fragment(),
        ),
        class_name="bg-white border-b border-gray-200 sticky top-0 z-30",
    )
from tick_ez.states.spotify_state import SpotifyState

def reproductor_global() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            # Renderiza el reproductor incrustado usando el track seleccionado en la pestaña de música
            rx.html(
                f"""
                <iframe 
                    src="{SpotifyState.track_embed_actual}" 
                    width="100%" 
                    height="80" 
                    frameBorder="0" 
                    allowfullscreen="" 
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                    loading="lazy"
                ></iframe>
                """
            ),
            # Diseño compacto que se fija al final de la pantalla de forma permanente
            class_name="fixed bottom-0 left-0 right-0 bg-black/90 shadow-2xl z-50 h-20 overflow-hidden"
        )
    )