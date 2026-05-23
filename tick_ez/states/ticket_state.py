import reflex as rx
from typing import TypedDict
import logging
import qrcode
import io
import base64
import uuid
import datetime


def _build_ticket_pdf(lines: list[tuple[str, str]], title: str) -> bytes:
    """Build a minimal text-based PDF from key/value lines."""

    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    parts = ["BT", "/F1 20 Tf", "50 760 Td", f"({esc(title)}) Tj"]
    parts.append("/F1 11 Tf")
    parts.append("0 -14 Td")
    parts.append(
        "(Plataforma oficial Tick_EZ - Boleto digital con QR unico) Tj"
    )
    parts.append("0 -28 Td")
    parts.append("/F1 12 Tf")
    for i, (label, value) in enumerate(lines):
        if i > 0:
            parts.append("0 -22 Td")
        parts.append("/F1 10 Tf")
        parts.append(f"({esc(label.upper())}) Tj")
        parts.append("0 -14 Td")
        parts.append("/F1 13 Tf")
        parts.append(f"({esc(value)}) Tj")
    parts.append("0 -40 Td")
    parts.append("/F1 9 Tf")
    parts.append(
        "(Presenta este documento junto con tu identificacion en el acceso. No transferible.) Tj"
    )
    parts.append("0 -12 Td")
    parts.append("(Para soporte: soporte@tickez.mx | Generado por Tick_EZ.) Tj")
    parts.append("ET")
    stream = "\n".join(parts).encode("latin-1", errors="ignore")

    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length "
        + str(len(stream)).encode()
        + b" >>\nstream\n"
        + stream
        + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    pdf = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
    offsets: list[int] = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref_pos = len(pdf)
    pdf += b"xref\n"
    pdf += f"0 {len(objects) + 1}\n".encode()
    pdf += b"0000000000 65535 f \n"
    for off in offsets:
        pdf += f"{off:010d} 00000 n \n".encode()
    pdf += b"trailer\n"
    pdf += f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode()
    pdf += b"startxref\n"
    pdf += f"{xref_pos}\n".encode()
    pdf += b"%%EOF"
    return pdf


class Event(TypedDict):
    id: int
    nombre: str
    artista: str
    categoria: str
    fecha: str
    hora: str
    ubicacion: str
    ciudad: str
    precio_min: float
    precio_max: float
    asientos_disponibles: int
    asientos_totales: int
    imagen: str
    descripcion: str
    rating: float


class Compra(TypedDict):
    folio: str
    evento: str
    cantidad: int
    categoria_ticket: str
    total: float
    fecha: str
    estado: str
    qr_data_url: str
    titular: str
    zona: str
    ticket_id: str


class VentaListada(TypedDict):
    id: int
    evento: str
    cantidad: int
    precio_unit: float
    fecha_evento: str
    seccion: str
    estado: str


class TicketState(rx.State):
    seccion_activa: str = "inicio"
    mobile_menu_abierto: bool = False
    busqueda: str = ""
    filtro_categoria: str = "Todas"
    filtro_ciudad: str = "Todas"
    filtro_precio: str = "Todos"

    categorias: list[str] = ["Todas", "Concierto", "Convención", "Teatro"]
    ciudades: list[str] = [
        "Todas",
        "Ciudad de México",
        "Guadalajara",
        "Monterrey",
        "Tijuana",
        "Puebla",
    ]
    rangos_precio: list[str] = [
        "Todos",
        "$0 - $500",
        "$500 - $1500",
        "$1500 - $3000",
        "$3000+",
    ]

    eventos: list[Event] = [
        {
            "id": 1,
            "nombre": "Doja Cat - Scarlet Tour 2026",
            "artista": "Doja Cat",
            "categoria": "Concierto",
            "fecha": "15 Mar 2026",
            "hora": "20:00",
            "ubicacion": "Foro Sol",
            "ciudad": "Ciudad de México",
            "precio_min": 850.0,
            "precio_max": 4500.0,
            "asientos_disponibles": 1245,
            "asientos_totales": 5000,
            "imagen": "doja_cat.jpg",
            "descripcion": "La súper estrella global del hip-hop y pop Doja Cat trae el aclamado Scarlet Tour a México por primera vez.",
            "rating": 4.8,
        },
        {
            "id": 2,
            "nombre": "Gorillaz - Getaway World Tour",
            "artista": "Gorillaz",
            "categoria": "Concierto",
            "fecha": "05 Jun 2026",
            "hora": "16:00",
            "ubicacion": "Parque Fundidora",
            "ciudad": "Monterrey",
            "precio_min": 1200.0,
            "precio_max": 3800.0,
            "asientos_disponibles": 4500,
            "asientos_totales": 12000,
            "imagen": "gorillaz.jpg",
            "descripcion": "La banda virtual más exitosa del planeta liderada por Damon Albarn regresa con un espectáculo audiovisual inigualable.",
            "rating": 4.9,
        },
        {
            "id": 3,
            "nombre": "BTS - Live in Mexico City",
            "artista": "BTS",
            "categoria": "Concierto",
            "fecha": "12 Sep 2026",
            "hora": "19:00",
            "ubicacion": "Estadio BBVA",
            "ciudad": "Monterrey",
            "precio_min": 650.0,
            "precio_max": 3500.0,
            "asientos_disponibles": 8200,
            "asientos_totales": 50000,
            "imagen": "bts.jpg",
            "descripcion": "El regreso más esperado de la sensación global del K-Pop BTS, un show inolvidable lleno de coreografías impecables y energía única.",
            "rating": 4.9,
        },
        {
            "id": 4,
            "nombre": "Anime Expo Mexico 2026",
            "artista": "Varios Invitados",
            "categoria": "Convención",
            "fecha": "25 Ago 2026",
            "hora": "10:00",
            "ubicacion": "Centro Expositor",
            "ciudad": "Puebla",
            "precio_min": 380.0,
            "precio_max": 1800.0,
            "asientos_disponibles": 1800,
            "asientos_totales": 4500,
            "imagen": "anime_expo_mexico.jpg",
            "descripcion": "La celebración más grande de la cultura japonesa, anime, manga y cosplayers profesionales de todo el mundo.",
            "rating": 4.7,
        },
        {
            "id": 5,
            "nombre": "Comic Con Latam 2026",
            "artista": "Elenco de Hollywood",
            "categoria": "Convención",
            "fecha": "22 Abr 2026",
            "hora": "10:00",
            "ubicacion": "Expo Guadalajara",
            "ciudad": "Guadalajara",
            "precio_min": 450.0,
            "precio_max": 2800.0,
            "asientos_disponibles": 3200,
            "asientos_totales": 8000,
            "imagen": "comic_con_latam.jpg",
            "descripcion": "El epicentro de la cultura pop con la participación de actores estelares, firmas de autógrafos y cómics exclusivos.",
            "rating": 4.8,
        },
        {
            "id": 6,
            "nombre": "CCXP Mexico 2026",
            "artista": "Directores y Productores",
            "categoria": "Convención",
            "fecha": "18 Jul 2026",
            "hora": "09:00",
            "ubicacion": "Centro de Convenciones",
            "ciudad": "Tijuana",
            "precio_min": 1500.0,
            "precio_max": 5000.0,
            "asientos_disponibles": 850,
            "asientos_totales": 2500,
            "imagen": "ccxp_mexico.jpg",
            "descripcion": "La experiencia del festival geek más grande con conferencias, paneles interactivos, lanzamientos mundiales y el mejor gaming.",
            "rating": 4.9,
        },
        {
            "id": 7,
            "nombre": "The Lion King - El Musical",
            "artista": "Elenco Internacional",
            "categoria": "Teatro",
            "fecha": "28 May 2026",
            "hora": "20:00",
            "ubicacion": "Auditorio Nacional",
            "ciudad": "Ciudad de México",
            "precio_min": 890.0,
            "precio_max": 4200.0,
            "asientos_disponibles": 320,
            "asientos_totales": 9700,
            "imagen": "lion_king.jpg",
            "descripcion": "La obra maestra musical de Broadway, El Rey León, con una producción de títeres majestuosos y música legendaria de Elton John.",
            "rating": 4.9,
        },
        {
            "id": 8,
            "nombre": "Chicago - El Musical",
            "artista": "Broadway Tour",
            "categoria": "Teatro",
            "fecha": "10 May 2026",
            "hora": "19:30",
            "ubicacion": "Teatro Diana",
            "ciudad": "Guadalajara",
            "precio_min": 320.0,
            "precio_max": 1500.0,
            "asientos_disponibles": 180,
            "asientos_totales": 900,
            "imagen": "chicago.jpg",
            "descripcion": "La historia de avaricia, traición y jazz más famosa del teatro con coreografías de Bob Fosse inolvidables.",
            "rating": 4.8,
        },
        {
            "id": 9,
            "nombre": "Wicked - Tour Oficial",
            "artista": "Broadway Company",
            "categoria": "Teatro",
            "fecha": "14 Feb 2026",
            "hora": "20:00",
            "ubicacion": "Palacio de Bellas Artes",
            "ciudad": "Ciudad de México",
            "precio_min": 550.0,
            "precio_max": 2200.0,
            "asientos_disponibles": 95,
            "asientos_totales": 1800,
            "imagen": "wicked.jpg",
            "descripcion": "Descubre la historia jamás contada de las brujas de Oz en este grandioso musical de Broadway aclamado mundialmente.",
            "rating": 4.9,
        },
    ]

    historial_compras: list[Compra] = []
    seeded: bool = False

    ventas_listadas: list[VentaListada] = [
        {
            "id": 1,
            "evento": "Noche Eléctrica Tour 2026",
            "cantidad": 2,
            "precio_unit": 1500.0,
            "fecha_evento": "15 Mar 2026",
            "seccion": "Platea Alta",
            "estado": "Activo",
        },
        {
            "id": 2,
            "evento": "TechSummit 2026",
            "cantidad": 1,
            "precio_unit": 2200.0,
            "fecha_evento": "18 Jul 2026",
            "seccion": "General",
            "estado": "Vendido",
        },
    ]

    # Compra dialog state
    compra_evento_id: int = -1
    compra_cantidad: int = 1
    compra_categoria: str = "General"
    show_compra: bool = False
    show_confirmacion: bool = False
    ultimo_folio: str = ""
    ultimo_qr: str = ""
    ultima_compra_titular: str = ""
    ultima_compra_zona: str = ""
    zona_mapa_id: str = ""
    zona_mapa_nombre: str = ""
    zona_mapa_precio: float = 0.0

    # Venta form state
    show_venta_exito: bool = False

    @rx.var
    def eventos_filtrados(self) -> list[Event]:
        result = self.eventos
        if self.filtro_categoria != "Todas":
            result = [
                e for e in result if e["categoria"] == self.filtro_categoria
            ]
        if self.filtro_ciudad != "Todas":
            result = [e for e in result if e["ciudad"] == self.filtro_ciudad]
        if self.busqueda:
            q = self.busqueda.lower()
            result = [
                e
                for e in result
                if q in e["nombre"].lower() or q in e["artista"].lower()
            ]
        if self.filtro_precio == "$0 - $500":
            result = [e for e in result if e["precio_min"] < 500]
        elif self.filtro_precio == "$500 - $1500":
            result = [e for e in result if 500 <= e["precio_min"] < 1500]
        elif self.filtro_precio == "$1500 - $3000":
            result = [e for e in result if 1500 <= e["precio_min"] < 3000]
        elif self.filtro_precio == "$3000+":
            result = [e for e in result if e["precio_min"] >= 3000]
        return result

    @rx.var
    def total_eventos(self) -> int:
        return len(self.eventos)

    @rx.var
    def total_asientos(self) -> int:
        return sum(e["asientos_disponibles"] for e in self.eventos)

    @rx.var
    def total_compras(self) -> int:
        return len(self.historial_compras)

    @rx.var
    def total_gastado(self) -> float:
        return sum(c["total"] for c in self.historial_compras)

    @rx.var
    def evento_seleccionado(self) -> Event:
        for e in self.eventos:
            if e["id"] == self.compra_evento_id:
                return e
        return {
            "id": 0,
            "nombre": "",
            "artista": "",
            "categoria": "",
            "fecha": "",
            "hora": "",
            "ubicacion": "",
            "ciudad": "",
            "precio_min": 0.0,
            "precio_max": 0.0,
            "asientos_disponibles": 0,
            "asientos_totales": 0,
            "imagen": "",
            "descripcion": "",
            "rating": 0.0,
        }

    @rx.var
    def precio_categoria_seleccionada(self) -> float:
        if self.zona_mapa_precio > 0:
            return self.zona_mapa_precio
        ev = self.evento_seleccionado
        if self.compra_categoria == "General":
            return ev["precio_min"]
        elif self.compra_categoria == "VIP":
            return (ev["precio_min"] + ev["precio_max"]) / 2
        elif self.compra_categoria == "TicketStar":
            return ev["precio_max"]
        else:
            return ev["precio_max"]

    @rx.var
    def total_compra(self) -> float:
        return self.precio_categoria_seleccionada * self.compra_cantidad

    @rx.event
    def seed_historial(self):
        if self.seeded:
            return
        self.seeded = True
        seeds = [
            (
                "TKT-2026-00142-A1B2",
                "Festival Indie Norte",
                2,
                "VIP",
                7600.0,
                "12 Ene 2026",
                "Zona VIP - Pista A",
                "María González",
                "15 Mar 2026 20:00",
            ),
            (
                "TKT-2026-00098-C3D4",
                "Hamlet - Edición Moderna",
                4,
                "General",
                1280.0,
                "08 Ene 2026",
                "Zona General",
                "María González",
                "10 May 2026 19:30",
            ),
            (
                "TKT-2025-09823-E5F6",
                "ComicCon Latinoamérica",
                1,
                "Golden",
                2800.0,
                "28 Dic 2025",
                "Zona Golden - Frente",
                "María González",
                "22 Abr 2026 10:00",
            ),
        ]
        compras: list[Compra] = []
        for (
            folio,
            evento,
            cant,
            cat,
            total,
            fecha,
            zona,
            titular,
            ev_fecha,
        ) in seeds:
            ticket_id = folio.split("-")[-1] + uuid.uuid4().hex[:8].upper()
            payload = f"TICKEZ|{folio}|{evento}|{ev_fecha}|{cat}|{zona}|x{cant}|{titular}|ID:{ticket_id}"
            qr = self._generar_qr(payload)
            compras.append(
                {
                    "folio": folio,
                    "evento": evento,
                    "cantidad": cant,
                    "categoria_ticket": cat,
                    "total": total,
                    "fecha": fecha,
                    "estado": "Confirmado"
                    if folio != "TKT-2025-09823-E5F6"
                    else "Pendiente",
                    "qr_data_url": qr,
                    "titular": titular,
                    "zona": zona,
                    "ticket_id": ticket_id,
                }
            )
        self.historial_compras = compras

    @rx.event
    def cambiar_seccion(self, seccion: str):
        self.seccion_activa = seccion
        self.mobile_menu_abierto = False

    @rx.event
    def toggle_mobile_menu(self):
        self.mobile_menu_abierto = not self.mobile_menu_abierto

    @rx.event
    def set_busqueda(self, v: str):
        self.busqueda = v

    @rx.event
    def set_filtro_categoria(self, v: str):
        self.filtro_categoria = v

    @rx.event
    def set_filtro_ciudad(self, v: str):
        self.filtro_ciudad = v

    @rx.event
    def set_filtro_precio(self, v: str):
        self.filtro_precio = v

    @rx.event
    def limpiar_filtros(self):
        self.filtro_categoria = "Todas"
        self.filtro_ciudad = "Todas"
        self.filtro_precio = "Todos"
        self.busqueda = ""

    @rx.event
    async def abrir_compra(self, evento_id: int):
        self.compra_evento_id = evento_id
        self.compra_cantidad = 1
        self.compra_categoria = "General"
        self.zona_mapa_id = ""
        self.zona_mapa_nombre = ""
        self.zona_mapa_precio = 0.0
        self.show_compra = True
        from tick_ez.states.mapa_state import MapaState
        from tick_ez.states.spotify_state import SpotifyState

        mapa = await self.get_state(MapaState)
        spotify = await self.get_state(SpotifyState)
        for e in self.eventos:
            if e["id"] == evento_id:
                if e["categoria"] == "Concierto":
                    mapa.tipo_recinto = "concierto"
                elif e["categoria"] == "Convención":
                    mapa.tipo_recinto = "convencion"
                else:
                    mapa.tipo_recinto = "teatro"
                mapa.zona_seleccionada_id = ""
                pid = spotify.evento_playlist_map.get(e["nombre"])
                if pid:
                    spotify.playlist_seleccionada_id = pid
                break

    @rx.event
    def cerrar_compra(self):
        self.show_compra = False

    @rx.event
    def set_compra_categoria(self, v: str):
        self.compra_categoria = v

    @rx.event
    def inc_cantidad(self):
        if self.compra_cantidad < 10:
            self.compra_cantidad += 1

    @rx.event
    def dec_cantidad(self):
        if self.compra_cantidad > 1:
            self.compra_cantidad -= 1

    def _generar_qr(self, payload: str) -> str:
        try:
            qr = qrcode.QRCode(
                box_size=4,
                border=2,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
            )
            qr.add_data(payload)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#1f2937", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return (
                "data:image/png;base64,"
                + base64.b64encode(buf.getvalue()).decode()
            )
        except Exception as e:
            logging.exception(f"Error generando QR: {e}")
            return ""

    @rx.event
    async def confirmar_compra(self, form_data: dict):
        import random
        from tick_ez.states.auth_state import AuthState

        ev = self.evento_seleccionado
        if ev["id"] == 0:
            return rx.toast("Evento no válido", duration=3000)
        auth = await self.get_state(AuthState)
        titular = auth.nombre_usuario if auth.is_logged_in else "Invitado"
        zonas_map = {
            "General": "Zona General",
            "VIP": "Zona VIP - Pista A",
            "Golden": "Zona Golden - Frente",
            "TicketStar": "Zona TicketStar - Accesible Preferente",
        }
        zona = (
            self.zona_mapa_nombre
            if self.zona_mapa_nombre
            else zonas_map.get(self.compra_categoria, "Zona General")
        )
        ticket_id = uuid.uuid4().hex[:12].upper()
        folio = f"TKT-2026-{random.randint(10000, 99999)}-{ticket_id[:4]}"
        payload = (
            f"TICKEZ|{folio}|{ev['nombre']}|{ev['fecha']} {ev['hora']}|"
            f"{self.compra_categoria}|{zona}|x{self.compra_cantidad}|"
            f"{titular}|ID:{ticket_id}"
        )
        qr_data_url = self._generar_qr(payload)
        self.ultimo_folio = folio
        self.ultimo_qr = qr_data_url
        self.ultima_compra_titular = titular
        self.ultima_compra_zona = zona
        self.historial_compras.insert(
            0,
            {
                "folio": folio,
                "evento": ev["nombre"],
                "cantidad": self.compra_cantidad,
                "categoria_ticket": self.compra_categoria,
                "total": self.total_compra * 1.05,
                "fecha": datetime.datetime.now().strftime("%d %b %Y"),
                "estado": "Confirmado",
                "qr_data_url": qr_data_url,
                "titular": titular,
                "zona": zona,
                "ticket_id": ticket_id,
            },
        )
        self.show_compra = False
        self.show_confirmacion = True
        return rx.toast(f"✓ Compra confirmada · {folio}", duration=4000)

    @rx.event
    def cerrar_confirmacion(self):
        self.show_confirmacion = False

    @rx.event
    def listar_venta(self, form_data: dict):
        try:
            evento = form_data.get("evento", "").strip()
            if not evento:
                return rx.toast(
                    "El nombre del evento es requerido", duration=3000
                )
            precio = float(form_data.get("precio", 0))
            if precio <= 0:
                return rx.toast("El precio debe ser mayor a $0", duration=3000)
            nueva: VentaListada = {
                "id": len(self.ventas_listadas) + 1,
                "evento": evento,
                "cantidad": int(form_data.get("cantidad", 1)),
                "precio_unit": precio,
                "fecha_evento": form_data.get("fecha", ""),
                "seccion": form_data.get("seccion", "General"),
                "estado": "Activo",
            }
            self.ventas_listadas.insert(0, nueva)
            self.show_venta_exito = True
            return rx.toast(
                f"✓ Ticket listado: {nueva['evento']}", duration=4000
            )
        except Exception:
            logging.exception("Unexpected error")
            return rx.toast(
                "No se pudo listar el ticket. Verifica los datos.",
                duration=3000,
            )

    @rx.event
    def cerrar_venta_exito(self):
        self.show_venta_exito = False

    def _ticket_lines(self, c: Compra) -> list[tuple[str, str]]:
        return [
            ("Folio", c["folio"]),
            ("Evento", c["evento"]),
            ("Categoria", c["categoria_ticket"]),
            ("Zona", c["zona"]),
            ("Cantidad", f"x{c['cantidad']} boleto(s)"),
            ("Titular", c["titular"]),
            ("Total pagado", f"$ {c['total']:.2f} MXN"),
            ("Estado", c["estado"]),
            ("Fecha de compra", c["fecha"]),
            ("ID Ticket (unico)", c["ticket_id"]),
            ("Referencia QR", f"TICKEZ|{c['folio']}|ID:{c['ticket_id']}"),
        ]

    @rx.event
    def descargar_ticket_pdf(self, folio: str):
        try:
            for c in self.historial_compras:
                if c["folio"] == folio:
                    pdf = _build_ticket_pdf(
                        self._ticket_lines(c),
                        f"Tick_EZ - {c['evento']}",
                    )
                    return [
                        rx.download(
                            data=pdf,
                            filename=f"ticket_{c['folio']}.pdf",
                        ),
                        rx.toast(
                            f"📄 Descargando {c['folio']}.pdf", duration=2500
                        ),
                    ]
            return rx.toast("Ticket no encontrado", duration=2500)
        except Exception as e:
            logging.exception(f"Error PDF: {e}")
            return rx.toast("Error al generar PDF", duration=3000)

    @rx.event
    def descargar_ultimo_ticket(self):
        try:
            if not self.historial_compras:
                return rx.toast("Sin tickets disponibles", duration=2500)
            c = self.historial_compras[0]
            pdf = _build_ticket_pdf(
                self._ticket_lines(c), f"Tick_EZ - {c['evento']}"
            )
            return [
                rx.download(data=pdf, filename=f"ticket_{c['folio']}.pdf"),
                rx.toast(f"📄 Descargando {c['folio']}.pdf", duration=2500),
            ]
        except Exception as e:
            logging.exception(f"Error PDF: {e}")
            return rx.toast("Error al generar PDF", duration=3000)