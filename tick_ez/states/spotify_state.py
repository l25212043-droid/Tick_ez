import reflex as rx
from typing import TypedDict


class Playlist(TypedDict):
    id: str
    nombre: str
    descripcion: str
    autor: str
    embed_url: str
    color: str
    icono: str
    evento_categoria: str
    duracion: str
    canciones: int


class SpotifyState(rx.State):
    playlist_seleccionada_id: str = "indie-fest-2026"
    playlists: list[Playlist] = [
        {
            "id": "indie-fest-2026",
            "nombre": "Indie Fest 2026",
            "descripcion": "Lo mejor del indie latino para el Festival Indie Norte",
            "autor": "Tick_EZ Curators",
            "embed_url": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL?utm_source=generator&theme=0",
            "color": "violet",
            "icono": "music",
            "evento_categoria": "Concierto",
            "duracion": "3h 24min",
            "canciones": 48,
        },
        {
            "id": "rock-espanol",
            "nombre": "Rock en tu Idioma",
            "descripcion": "Clásicos del rock en español: Caifanes, Café Tacvba y más",
            "autor": "Tick_EZ Curators",
            "embed_url": "https://open.spotify.com/embed/playlist/37i9dQZF1DX10zKzsJ2jva?utm_source=generator&theme=0",
            "color": "blue",
            "icono": "guitar",
            "evento_categoria": "Concierto",
            "duracion": "4h 10min",
            "canciones": 62,
        },
        {
            "id": "electronica-tour",
            "nombre": "Noche Eléctrica",
            "descripcion": "Beats electrónicos para acompañar el tour de Luna Estelar",
            "autor": "Luna Estelar",
            "embed_url": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4dyzvuaRJ0n?utm_source=generator&theme=0",
            "color": "teal",
            "icono": "zap",
            "evento_categoria": "Concierto",
            "duracion": "2h 45min",
            "canciones": 38,
        },
        {
            "id": "broadway-clasicos",
            "nombre": "Broadway Esenciales",
            "descripcion": "Bandas sonoras del teatro musical",
            "autor": "Tick_EZ Curators",
            "embed_url": "https://open.spotify.com/embed/playlist/37i9dQZF1DWUoY6Ih7vsxr?utm_source=generator&theme=0",
            "color": "amber",
            "icono": "drama",
            "evento_categoria": "Teatro",
            "duracion": "3h 50min",
            "canciones": 55,
        },
        {
            "id": "anime-soundtrack",
            "nombre": "Anime Soundtrack",
            "descripcion": "Lo mejor de openings y soundtracks para Anime Expo",
            "autor": "Tick_EZ Curators",
            "embed_url": "https://open.spotify.com/embed/playlist/37i9dQZF1DWUa8ZRTfalHk?utm_source=generator&theme=0",
            "color": "violet",
            "icono": "sparkles",
            "evento_categoria": "Convención",
            "duracion": "5h 20min",
            "canciones": 80,
        },
        {
            "id": "tech-focus",
            "nombre": "TechSummit Focus",
            "descripcion": "Música ambient para conferencias y networking",
            "autor": "Tick_EZ Curators",
            "embed_url": "https://open.spotify.com/embed/playlist/37i9dQZF1DWZeKCadgRdKQ?utm_source=generator&theme=0",
            "color": "blue",
            "icono": "laptop",
            "evento_categoria": "Convención",
            "duracion": "6h 00min",
            "canciones": 92,
        },
    ]

    # Mapeo evento -> playlist sugerida
    evento_playlist_map: dict[str, str] = {
        "Doja Cat - Scarlet Tour 2026": "indie-fest-2026",
        "Gorillaz - Getaway World Tour": "rock-espanol",
        "BTS - Live in Mexico City": "electronica-tour",
        "The Lion King - El Musical": "broadway-clasicos",
        "Chicago - El Musical": "broadway-clasicos",
        "Wicked - Tour Oficial": "broadway-clasicos",
        "Anime Expo Mexico 2026": "anime-soundtrack",
        "Comic Con Latam 2026": "anime-soundtrack",
        "CCXP Mexico 2026": "tech-focus",
    }

    @rx.var
    def playlist_actual(self) -> Playlist:
        for p in self.playlists:
            if p["id"] == self.playlist_seleccionada_id:
                return p
        return self.playlists[0]

    @rx.event
    def seleccionar_playlist(self, pid: str):
        self.playlist_seleccionada_id = pid
        return rx.toast("🎵 Playlist cargada", duration=2000)

    @rx.event
    def playlist_para_evento(self, nombre_evento: str):
        pid = self.evento_playlist_map.get(nombre_evento, "indie-fest-2026")
        self.playlist_seleccionada_id = pid
        return rx.toast(
            f"🎶 Playlist sugerida para {nombre_evento}", duration=2500
        )