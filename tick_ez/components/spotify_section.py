import reflex as rx
from tick_ez.states.spotify_state import SpotifyState

def spotify_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Buscador Global Spotify 🎵", class_name="text-3xl font-extrabold text-gray-900 mb-2"),
            rx.el.p("Busca y añade canciones de todo el mundo usando la API oficial de Tick_ez.", class_name="text-sm text-gray-600 mb-6"),
            
            # Barra de Entrada de texto (Llama al evento on_change en tiempo real)
            rx.input(
                placeholder="🔍 Escribe una canción, artista o álbum...",
                on_change=SpotifyState.realizar_busqueda,
                value=SpotifyState.buscar_texto,
                class_name="w-full max-w-xl px-4 py-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-violet-500 text-base"
            ),
            class_name="mb-8"
        ),
        
        rx.el.div(
            # COLUMNA IZQUIERDA: Lista de resultados de búsqueda reales
            rx.el.div(
                rx.el.h3("Resultados de búsqueda", class_name="text-lg font-bold text-gray-800 mb-3"),
                rx.cond(
                    SpotifyState.resultados_busqueda.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            SpotifyState.resultados_busqueda,
                            lambda cancion: rx.el.div(
                                rx.el.div(
                                    # Portada del Álbum real
                                    rx.el.img(src=cancion["album_img"], class_name="w-12 h-12 rounded-md object-cover shadow-sm"),
                                    rx.el.div(
                                        rx.el.p(cancion["titulo"], class_name="font-semibold text-sm text-gray-900 truncate max-w-[180px] sm:max-w-[250px]"),
                                        rx.el.p(cancion["artista"], class_name="text-xs text-gray-500 truncate"),
                                        class_name="flex flex-col"
                                    ),
                                    class_name="flex items-center gap-3"
                                ),
                                rx.el.button(
                                    rx.icon("play", class_name="h-4 w-4 text-white pl-0.5"),
                                    on_click=lambda: SpotifyState.seleccionar_track(cancion["embed_url"], cancion["titulo"]),
                                    class_name="p-2.5 bg-violet-600 text-white rounded-full hover:bg-violet-700 transition-colors shadow-sm"
                                ),
                                class_name="flex items-center justify-between p-3 bg-white border border-gray-100 rounded-xl hover:shadow-md transition-shadow"
                            )
                        ),
                        class_name="flex flex-col gap-2"
                    ),
                    rx.el.div(
                        rx.icon("search", class_name="h-8 w-8 text-gray-400 mb-2"),
                        rx.el.p("Empieza a escribir para ver canciones reales del mundo entero", class_name="text-sm text-gray-500 text-center"),
                        class_name="flex flex-col items-center justify-center p-12 bg-white border border-dashed rounded-xl"
                    )
                ),
                class_name="w-full lg:w-1/2"
            ),
            
            # COLUMNA DERECHA: El Reproductor Persistente de Spotify
            rx.el.div(
                rx.el.h3("Reproductor en reproducción", class_name="text-lg font-bold text-gray-800 mb-3"),
                rx.el.div(
                    # El Iframe Oficial inyectado mediante HTML nativo
                    rx.html(
                        f"""
                        <iframe 
                            src="{SpotifyState.track_embed_actual}" 
                            width="100%" 
                            height="352" 
                            frameBorder="0" 
                            allowfullscreen="" 
                            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                            loading="lazy"
                            style="border-radius: 12px;"
                        ></iframe>
                        """
                    ),
                    class_name="bg-black/5 rounded-2xl p-2 shadow-inner sticky top-24"
                ),
                class_name="w-full lg:w-1/2"
            ),
            class_name="flex flex-col lg:flex-row gap-8 items-start"
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
    )