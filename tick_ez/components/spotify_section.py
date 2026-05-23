import reflex as rx
from tick_ez.states.spotify_state import SpotifyState, Playlist


def _color_classes(color: rx.Var) -> rx.Var:
    return rx.match(
        color,
        ("violet", "bg-violet-50 text-violet-600 border-violet-200"),
        ("blue", "bg-blue-50 text-blue-600 border-blue-200"),
        ("teal", "bg-teal-50 text-teal-600 border-teal-200"),
        ("amber", "bg-amber-50 text-amber-600 border-amber-200"),
        "bg-violet-50 text-violet-600 border-violet-200",
    )


def playlist_card(p: Playlist) -> rx.Component:
    is_active = SpotifyState.playlist_seleccionada_id == p["id"]
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.icon(p["icono"].to(str), class_name="h-5 w-5"),
                class_name=rx.cond(
                    is_active,
                    "p-2.5 rounded-lg bg-white text-violet-600 shrink-0",
                    f"p-2.5 rounded-lg {_color_classes(p['color'])} shrink-0",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    p["nombre"],
                    class_name=rx.cond(
                        is_active,
                        "text-sm font-bold text-white text-left",
                        "text-sm font-bold text-gray-900 text-left",
                    ),
                ),
                rx.el.p(
                    p["descripcion"],
                    class_name=rx.cond(
                        is_active,
                        "text-xs text-violet-100 text-left line-clamp-1",
                        "text-xs text-gray-500 text-left line-clamp-1",
                    ),
                ),
                rx.el.div(
                    rx.icon(
                        "music_2",
                        class_name=rx.cond(
                            is_active,
                            "h-3 w-3 text-violet-100",
                            "h-3 w-3 text-gray-400",
                        ),
                    ),
                    rx.el.span(
                        p["canciones"].to_string() + " canciones",
                        class_name=rx.cond(
                            is_active,
                            "text-xs text-violet-100",
                            "text-xs text-gray-500",
                        ),
                    ),
                    rx.el.span(
                        "·",
                        class_name=rx.cond(
                            is_active,
                            "text-violet-200",
                            "text-gray-300",
                        ),
                    ),
                    rx.el.span(
                        p["duracion"],
                        class_name=rx.cond(
                            is_active,
                            "text-xs text-violet-100",
                            "text-xs text-gray-500",
                        ),
                    ),
                    class_name="flex items-center gap-1.5 mt-1",
                ),
                class_name="flex-1 min-w-0",
            ),
            rx.cond(
                is_active,
                rx.el.div(
                    rx.icon("volume_2", class_name="h-4 w-4 text-white"),
                    class_name="shrink-0",
                ),
                rx.el.div(
                    rx.icon("play", class_name="h-4 w-4 text-gray-400"),
                    class_name="shrink-0",
                ),
            ),
            class_name="flex items-center gap-3 w-full",
        ),
        on_click=lambda: SpotifyState.seleccionar_playlist(p["id"]),
        class_name=rx.cond(
            is_active,
            "p-3 rounded-xl bg-gradient-to-r from-violet-600 to-blue-600 transition-all w-full shadow-md",
            "p-3 rounded-xl bg-white border border-gray-200 hover:border-violet-300 transition-all w-full",
        ),
    )


def reproductor_panel() -> rx.Component:
    p = SpotifyState.playlist_actual
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("disc_3", class_name="h-5 w-5 text-emerald-600"),
                    class_name="p-2 rounded-lg bg-emerald-50",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            class_name="size-1.5 rounded-full bg-emerald-500 animate-pulse",
                        ),
                        rx.el.span(
                            "Reproduciendo ahora",
                            class_name="text-xs font-semibold text-emerald-700",
                        ),
                        class_name="flex items-center gap-1.5 mb-0.5",
                    ),
                    rx.el.p(
                        p["nombre"],
                        class_name="text-base font-bold text-gray-900",
                    ),
                    rx.el.p(
                        f"{p['autor']} · {p['canciones']} canciones · {p['duracion']}",
                        class_name="text-xs text-gray-500",
                    ),
                ),
                class_name="flex items-start gap-3",
            ),
            rx.el.div(
                rx.el.span(
                    p["evento_categoria"],
                    class_name="px-2 py-0.5 rounded-md bg-violet-50 text-violet-700 text-xs font-semibold",
                ),
                class_name="ml-auto",
            ),
            class_name="flex items-start justify-between mb-4 flex-wrap gap-2",
        ),
        rx.el.div(
            rx.el.iframe(
                src=p["embed_url"],
                width="100%",
                height="380",
                custom_attrs={
                    "allow": "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture",
                    "loading": "lazy",
                    "frameborder": "0",
                },
                class_name="rounded-xl border border-gray-200",
            ),
            class_name="mb-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "info",
                    class_name="h-3.5 w-3.5 text-blue-600 shrink-0 mt-0.5",
                ),
                rx.el.p(
                    "Reproductor embebido de Spotify. Inicia sesión en Spotify Web para escuchar pistas completas.",
                    class_name="text-xs text-blue-700",
                ),
                class_name="flex items-start gap-2",
            ),
            class_name="p-3 bg-blue-50 rounded-lg",
        ),
        class_name="bg-white p-5 rounded-xl border border-gray-200",
    )


def spotify_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("music", class_name="h-3.5 w-3.5"),
                    rx.el.span("Spotify · Soundtracks de eventos"),
                    class_name="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-violet-50 text-violet-700 text-xs font-semibold mb-3",
                ),
                rx.el.h2(
                    "Música del evento",
                    class_name="text-2xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    "Escucha las playlists curadas para cada evento antes de asistir",
                    class_name="text-sm text-gray-600",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "list_music", class_name="h-5 w-5 text-violet-600"
                        ),
                        rx.el.h3(
                            "Playlists",
                            class_name="text-base font-bold text-gray-900",
                        ),
                        rx.el.span(
                            SpotifyState.playlists.length().to_string(),
                            class_name="ml-auto px-2 py-0.5 rounded-md bg-violet-50 text-violet-700 text-xs font-semibold",
                        ),
                        class_name="flex items-center gap-2 mb-3",
                    ),
                    rx.el.div(
                        rx.foreach(SpotifyState.playlists, playlist_card),
                        class_name="flex flex-col gap-2",
                    ),
                    class_name="lg:col-span-1",
                ),
                rx.el.div(
                    reproductor_panel(),
                    class_name="lg:col-span-2",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-5",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )


def spotify_mini_player() -> rx.Component:
    p = SpotifyState.playlist_actual
    return rx.el.div(
        rx.el.div(
            rx.icon("music", class_name="h-4 w-4 text-violet-600"),
            rx.el.h4(
                "Música sugerida",
                class_name="text-sm font-bold text-gray-900",
            ),
            rx.el.span(
                p["nombre"],
                class_name="ml-auto text-xs font-semibold text-violet-700 truncate",
            ),
            class_name="flex items-center gap-2 mb-2",
        ),
        rx.el.iframe(
            src=p["embed_url"],
            width="100%",
            height="152",
            custom_attrs={
                "allow": "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture",
                "loading": "lazy",
                "frameborder": "0",
            },
            class_name="rounded-lg",
        ),
        class_name="bg-white p-3 rounded-xl border border-gray-200",
    )