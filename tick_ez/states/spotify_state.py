import reflex as rx
from typing import TypedDict
import reflex as rx
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



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

class CancionReal(TypedDict):
    id: str
    titulo: str
    artista: str
    album_img: str
    embed_url: str

class SpotifyState(rx.State):
    CLIENT_ID: str = "4edb4ef5d0294eb895ffa2fdbff461ce"
    CLIENT_SECRET: str = "eab82e3c09aa4d3da1d34e5aa6931c44"
    
    buscar_texto: str = ""
    resultados_busqueda: list[CancionReal] = []
    
    # Guarda la URL del track seleccionado para reproducir en el Iframe
    track_embed_actual: str = "https://open.spotify.com/embed/track/4PTG3Z6ehGkBF3zI7YgR63" # Track por defecto (ej. Blinding Lights)

    def _get_spotify_client(self):
        """Inicializa el cliente de Spotify de forma segura"""
        auth_manager = SpotifyClientCredentials(
            client_id=self.CLIENT_ID, 
            client_secret=self.CLIENT_SECRET
        )
        return spotipy.Spotify(auth_manager=auth_manager)

    @rx.event
    def realizar_busqueda(self, texto: str):
        """Busca canciones en tiempo real en la API global de Spotify"""
        self.buscar_texto = texto
        
        if len(texto) < 2:
            self.resultados_busqueda = []
            return

        try:
            sp = self._get_spotify_client()
            # Buscamos los primeros 5 tracks coincidentes
            results = sp.search(q=texto, limit=5, type='track')
            tracks = results['tracks']['items']
            
            nuevos_resultados = []
            for track in tracks:
                nuevos_resultados.append({
                    "id": track['id'],
                    "titulo": track['name'],
                    "artista": track['artists'][0]['name'],
                    "album_img": track['album']['images'][0]['url'] if track['album']['images'] else "",
                    "embed_url": f"https://open.spotify.com/embed/track/{track['id']}"
                })
            
            self.resultados_busqueda = nuevos_resultados
        except Exception as e:
            print(f"Error conectando a Spotify: {e}")
            return rx.toast("⚠️ Error al conectar con Spotify API")

    @rx.event
    def seleccionar_track(self, embed_url: str, titulo: str):
        """Cambia el reproductor actual a la canción seleccionada"""
        self.track_embed_actual = embed_url
        return rx.toast(f"▶️ Cargando en reproductor: {titulo}", duration=2000)