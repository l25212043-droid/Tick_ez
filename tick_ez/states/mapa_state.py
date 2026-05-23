import reflex as rx
from typing import TypedDict
import logging


class Zona(TypedDict):
    id: str
    nombre: str
    categoria: str
    precio: float
    disponibles: int
    total: int
    beneficios: list[str]
    accesible: bool
    color: str
    descripcion: str


class MapaState(rx.State):
    tipo_recinto: str = "concierto"
    zona_seleccionada_id: str = ""
    zonas_ocupadas: list[str] = []

    zonas_concierto: list[Zona] = [
        {
            "id": "c-vip",
            "nombre": "VIP Frente",
            "categoria": "Golden",
            "precio": 4500.0,
            "disponibles": 28,
            "total": 120,
            "beneficios": [
                "Acceso preferente",
                "Meet & Greet opcional",
                "Bebida de bienvenida",
                "Mejor visibilidad al escenario",
            ],
            "accesible": False,
            "color": "amber",
            "descripcion": "Zona dorada justo frente al escenario",
        },
        {
            "id": "c-pista",
            "nombre": "Pista General",
            "categoria": "VIP",
            "precio": 2200.0,
            "disponibles": 380,
            "total": 800,
            "beneficios": [
                "De pie, cerca del escenario",
                "Ambiente energético",
                "Acceso anticipado",
            ],
            "accesible": False,
            "color": "violet",
            "descripcion": "Zona central de pista frente al escenario",
        },
        {
            "id": "c-platea-izq",
            "nombre": "Platea Izquierda",
            "categoria": "VIP",
            "precio": 1800.0,
            "disponibles": 145,
            "total": 400,
            "beneficios": ["Asiento numerado", "Vista lateral premium"],
            "accesible": False,
            "color": "blue",
            "descripcion": "Asientos numerados al lado izquierdo",
        },
        {
            "id": "c-platea-der",
            "nombre": "Platea Derecha",
            "categoria": "VIP",
            "precio": 1800.0,
            "disponibles": 0,
            "total": 400,
            "beneficios": ["Asiento numerado", "Vista lateral premium"],
            "accesible": False,
            "color": "blue",
            "descripcion": "Asientos numerados al lado derecho",
        },
        {
            "id": "c-palco-izq",
            "nombre": "Palco Izquierdo",
            "categoria": "Golden",
            "precio": 3200.0,
            "disponibles": 12,
            "total": 24,
            "beneficios": [
                "Espacio privado",
                "Servicio personalizado",
                "Bar exclusivo",
            ],
            "accesible": True,
            "color": "amber",
            "descripcion": "Palco cerrado con servicio premium",
        },
        {
            "id": "c-palco-der",
            "nombre": "Palco Derecho",
            "categoria": "Golden",
            "precio": 3200.0,
            "disponibles": 8,
            "total": 24,
            "beneficios": [
                "Espacio privado",
                "Servicio personalizado",
                "Bar exclusivo",
            ],
            "accesible": True,
            "color": "amber",
            "descripcion": "Palco cerrado con servicio premium",
        },
        {
            "id": "c-gradas-1",
            "nombre": "Gradas Nivel 1",
            "categoria": "General",
            "precio": 850.0,
            "disponibles": 620,
            "total": 1200,
            "beneficios": [
                "Asiento numerado",
                "Vista panorámica",
            ],
            "accesible": False,
            "color": "teal",
            "descripcion": "Gradas con buena visibilidad general",
        },
        {
            "id": "c-gradas-2",
            "nombre": "Gradas Nivel 2",
            "categoria": "General",
            "precio": 550.0,
            "disponibles": 980,
            "total": 1500,
            "beneficios": ["Asiento numerado", "Acceso económico"],
            "accesible": True,
            "color": "teal",
            "descripcion": "Gradas superiores económicas",
        },
        {
            "id": "c-accesible",
            "nombre": "Zona Accesible",
            "categoria": "General",
            "precio": 700.0,
            "disponibles": 18,
            "total": 30,
            "beneficios": [
                "Acceso para silla de ruedas",
                "Acompañante incluido",
                "Rampa dedicada",
            ],
            "accesible": True,
            "color": "emerald",
            "descripcion": "Espacio adaptado con accesos preferentes",
        },
    ]

    zonas_convencion: list[Zona] = [
        {
            "id": "v-pab-a",
            "nombre": "Pabellón A · Stands",
            "categoria": "General",
            "precio": 450.0,
            "disponibles": 1200,
            "total": 2500,
            "beneficios": [
                "Acceso a expositores",
                "Material promocional",
                "Workshops abiertos",
            ],
            "accesible": True,
            "color": "violet",
            "descripcion": "Pabellón principal de exposiciones",
        },
        {
            "id": "v-pab-b",
            "nombre": "Pabellón B · Conferencias",
            "categoria": "VIP",
            "precio": 980.0,
            "disponibles": 320,
            "total": 800,
            "beneficios": [
                "Asiento reservado",
                "Audífonos traducción",
                "Material premium",
            ],
            "accesible": True,
            "color": "blue",
            "descripcion": "Auditorio con speakers principales",
        },
        {
            "id": "v-pab-c",
            "nombre": "Pabellón C · Gaming",
            "categoria": "VIP",
            "precio": 750.0,
            "disponibles": 450,
            "total": 1000,
            "beneficios": [
                "Acceso a torneos",
                "Demos exclusivas",
                "Áreas LAN",
            ],
            "accesible": False,
            "color": "teal",
            "descripcion": "Zona de gaming y experiencias",
        },
        {
            "id": "v-salon-vip",
            "nombre": "Salón VIP",
            "categoria": "Golden",
            "precio": 2800.0,
            "disponibles": 0,
            "total": 80,
            "beneficios": [
                "Catering incluido",
                "Meet & Greet",
                "Acceso anticipado",
                "Lounge privado",
            ],
            "accesible": True,
            "color": "amber",
            "descripcion": "Salón exclusivo con experiencias premium",
        },
        {
            "id": "v-terraza",
            "nombre": "Terraza Networking",
            "categoria": "VIP",
            "precio": 1500.0,
            "disponibles": 95,
            "total": 200,
            "beneficios": [
                "Coffee break",
                "Mesas de networking",
                "Vista panorámica",
            ],
            "accesible": True,
            "color": "blue",
            "descripcion": "Terraza al aire libre para networking",
        },
        {
            "id": "v-talleres",
            "nombre": "Salón Talleres",
            "categoria": "General",
            "precio": 600.0,
            "disponibles": 180,
            "total": 250,
            "beneficios": [
                "Talleres prácticos",
                "Material incluido",
                "Certificado",
            ],
            "accesible": True,
            "color": "emerald",
            "descripcion": "Salón rotativo de talleres prácticos",
        },
        {
            "id": "v-foodcourt",
            "nombre": "Food Court",
            "categoria": "General",
            "precio": 300.0,
            "disponibles": 600,
            "total": 800,
            "beneficios": [
                "Acceso al área gastronómica",
                "Food trucks",
                "Zona libre",
            ],
            "accesible": True,
            "color": "teal",
            "descripcion": "Zona gastronómica con variedad de opciones",
        },
        {
            "id": "v-accesible",
            "nombre": "Acceso Universal",
            "categoria": "General",
            "precio": 380.0,
            "disponibles": 35,
            "total": 60,
            "beneficios": [
                "Rampas y elevadores",
                "Asistencia dedicada",
                "Estacionamiento cercano",
            ],
            "accesible": True,
            "color": "emerald",
            "descripcion": "Zona adaptada con todos los servicios",
        },
    ]

    zonas_teatro: list[Zona] = [
        {
            "id": "t-vip",
            "nombre": "VIP · Filas A-C",
            "categoria": "Golden",
            "precio": 4200.0,
            "disponibles": 18,
            "total": 60,
            "beneficios": [
                "Filas más cercanas",
                "Programa exclusivo",
                "Copa de bienvenida",
                "Backstage tour",
            ],
            "accesible": False,
            "color": "amber",
            "descripcion": "Las primeras tres filas con experiencia VIP",
        },
        {
            "id": "t-oro",
            "nombre": "Oro · Filas D-J",
            "categoria": "VIP",
            "precio": 2400.0,
            "disponibles": 85,
            "total": 200,
            "beneficios": [
                "Excelente visibilidad",
                "Asiento numerado",
                "Programa incluido",
            ],
            "accesible": True,
            "color": "violet",
            "descripcion": "Sección oro de luneta central",
        },
        {
            "id": "t-plata",
            "nombre": "Plata · Filas K-Q",
            "categoria": "VIP",
            "precio": 1500.0,
            "disponibles": 142,
            "total": 280,
            "beneficios": [
                "Buena visibilidad",
                "Asiento numerado",
            ],
            "accesible": True,
            "color": "blue",
            "descripcion": "Sección plata de luneta posterior",
        },
        {
            "id": "t-palco-izq",
            "nombre": "Palco Lateral Izq.",
            "categoria": "Golden",
            "precio": 2800.0,
            "disponibles": 0,
            "total": 12,
            "beneficios": [
                "Palco privado",
                "4 asientos",
                "Vista lateral elevada",
            ],
            "accesible": False,
            "color": "amber",
            "descripcion": "Palco lateral con vista privilegiada",
        },
        {
            "id": "t-palco-der",
            "nombre": "Palco Lateral Der.",
            "categoria": "Golden",
            "precio": 2800.0,
            "disponibles": 4,
            "total": 12,
            "beneficios": [
                "Palco privado",
                "4 asientos",
                "Vista lateral elevada",
            ],
            "accesible": False,
            "color": "amber",
            "descripcion": "Palco lateral con vista privilegiada",
        },
        {
            "id": "t-fan",
            "nombre": "Zona Fan · Balcón",
            "categoria": "General",
            "precio": 680.0,
            "disponibles": 240,
            "total": 380,
            "beneficios": [
                "Ambiente de fans",
                "Vista panorámica",
                "Acceso económico",
            ],
            "accesible": False,
            "color": "teal",
            "descripcion": "Balcón superior con energía de fans",
        },
        {
            "id": "t-anfiteatro",
            "nombre": "Anfiteatro",
            "categoria": "General",
            "precio": 450.0,
            "disponibles": 180,
            "total": 280,
            "beneficios": [
                "Asiento numerado",
                "Vista superior",
            ],
            "accesible": True,
            "color": "teal",
            "descripcion": "Anfiteatro alto con vista completa",
        },
        {
            "id": "t-accesible",
            "nombre": "Zona Accesible",
            "categoria": "VIP",
            "precio": 1200.0,
            "disponibles": 8,
            "total": 14,
            "beneficios": [
                "Espacio para silla de ruedas",
                "Acompañante incluido",
                "Acceso preferente",
            ],
            "accesible": True,
            "color": "emerald",
            "descripcion": "Sección adaptada con asistencia",
        },
    ]

    @rx.var
    def zonas_actuales(self) -> list[Zona]:
        if self.tipo_recinto == "convencion":
            return self.zonas_convencion
        if self.tipo_recinto == "teatro":
            return self.zonas_teatro
        return self.zonas_concierto

    @rx.var
    def zona_actual(self) -> Zona:
        for z in self.zonas_actuales:
            if z["id"] == self.zona_seleccionada_id:
                return z
        return {
            "id": "",
            "nombre": "",
            "categoria": "General",
            "precio": 0.0,
            "disponibles": 0,
            "total": 0,
            "beneficios": [],
            "accesible": False,
            "color": "violet",
            "descripcion": "",
        }

    @rx.var
    def total_disponibles(self) -> int:
        return sum(z["disponibles"] for z in self.zonas_actuales)

    @rx.var
    def total_capacidad(self) -> int:
        return sum(z["total"] for z in self.zonas_actuales)

    @rx.event
    def set_tipo_recinto(self, tipo: str):
        self.tipo_recinto = tipo
        self.zona_seleccionada_id = ""

    @rx.event
    async def seleccionar_zona(self, zona_id: str):
        zonas = self.zonas_actuales
        for z in zonas:
            if z["id"] == zona_id:
                if z["disponibles"] == 0:
                    return rx.toast(f"⚠ {z['nombre']} agotada", duration=2500)
                self.zona_seleccionada_id = zona_id
                from tick_ez.states.ticket_state import TicketState

                ticket = await self.get_state(TicketState)
                categoria_final = (
                    "TicketStar" if z["accesible"] else z["categoria"]
                )
                ticket.compra_categoria = categoria_final
                ticket.zona_mapa_id = zona_id
                ticket.zona_mapa_nombre = z["nombre"]
                ticket.zona_mapa_precio = z["precio"]
                if z["accesible"]:
                    return rx.toast(
                        f"♿ Zona accesible TicketStar: {z['nombre']}",
                        duration=2500,
                    )
                return rx.toast(
                    f"✓ Zona seleccionada: {z['nombre']}", duration=2000
                )
        return rx.toast("Zona no válida", duration=2000)

    @rx.event
    def limpiar_zona(self):
        self.zona_seleccionada_id = ""