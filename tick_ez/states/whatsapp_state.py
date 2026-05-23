import reflex as rx
from typing import TypedDict
import logging
import datetime
import re
import urllib.parse


class WhatsAppMensaje(TypedDict):
    id: int
    emisor: str
    receptor: str
    receptor_normalizado: str
    asunto: str
    mensaje: str
    fecha: str
    estado: str
    wa_link: str
    contexto: str


class WhatsAppState(rx.State):
    historial: list[WhatsAppMensaje] = [
        {
            "id": 1,
            "emisor": "María González",
            "receptor": "+52 664 555 9911",
            "receptor_normalizado": "526645559911",
            "asunto": "Confirmación de compra",
            "mensaje": "Hola! Te comparto mi ticket TKT-2026-00142 para Festival Indie Norte. Nos vemos!",
            "fecha": "12 Ene 2026 09:50",
            "estado": "Enviado",
            "wa_link": "https://wa.me/526645559911?text=Hola",
            "contexto": "Compra",
        },
        {
            "id": 2,
            "emisor": "María González",
            "receptor": "+52 33 1234 5678",
            "receptor_normalizado": "523312345678",
            "asunto": "Pregunta de soporte",
            "mensaje": "Buen día, tengo una duda con mi reembolso del folio SOL-2026-00231",
            "fecha": "10 Ene 2026 17:22",
            "estado": "Enviado",
            "wa_link": "https://wa.me/523312345678?text=Hola",
            "contexto": "Soporte",
        },
    ]

    # Form prefill state
    prefill_emisor: str = "María González"
    prefill_receptor: str = ""
    prefill_asunto: str = ""
    prefill_mensaje: str = ""
    prefill_contexto: str = "General"
    last_link: str = ""
    error_form: str = ""

    @rx.var
    def total_enviados(self) -> int:
        return len(self.historial)

    def _normalizar_telefono(self, telefono: str) -> str:
        # Remove all non-digits
        return re.sub(r"\D", "", telefono)

    @rx.event
    def preparar_mensaje_compra(self, folio: str, evento: str, ticket_id: str):
        self.prefill_asunto = f"Mi ticket {folio}"
        self.prefill_mensaje = (
            f"¡Hola! Te comparto mi ticket de Tick_EZ.\n\n"
            f"🎫 Evento: {evento}\n"
            f"📋 Folio: {folio}\n"
            f"🔑 ID Ticket: {ticket_id}\n\n"
            f"¡Nos vemos en el evento!"
        )
        self.prefill_contexto = "Compra"
        self.prefill_receptor = ""
        self.error_form = ""
        from tick_ez.states.ticket_state import TicketState

        return [
            TicketState.cambiar_seccion("whatsapp"),
            rx.toast("📲 Mensaje preparado para compartir", duration=2500),
        ]

    @rx.event
    def preparar_mensaje_soporte(
        self, folio: str, asunto: str, descripcion: str
    ):
        self.prefill_asunto = f"Soporte · {asunto}"
        self.prefill_mensaje = (
            f"Hola equipo de soporte Tick_EZ,\n\n"
            f"Solicitud: {folio}\n"
            f"Asunto: {asunto}\n\n"
            f"{descripcion}\n\n"
            f"Quedo atento a su respuesta. Gracias."
        )
        self.prefill_contexto = "Soporte"
        self.prefill_receptor = "+52 800 555 0100"
        self.error_form = ""
        from tick_ez.states.ticket_state import TicketState

        return [
            TicketState.cambiar_seccion("whatsapp"),
            rx.toast("📲 Consulta preparada", duration=2500),
        ]

    @rx.event
    def set_prefill_emisor(self, v: str):
        self.prefill_emisor = v

    @rx.event
    def set_prefill_receptor(self, v: str):
        self.prefill_receptor = v

    @rx.event
    def set_prefill_asunto(self, v: str):
        self.prefill_asunto = v

    @rx.event
    def set_prefill_mensaje(self, v: str):
        self.prefill_mensaje = v

    @rx.event
    def limpiar_formulario(self):
        self.prefill_emisor = "María González"
        self.prefill_receptor = ""
        self.prefill_asunto = ""
        self.prefill_mensaje = ""
        self.prefill_contexto = "General"
        self.last_link = ""
        self.error_form = ""

    @rx.event
    def enviar_whatsapp(self, form_data: dict):
        try:
            emisor = form_data.get("emisor", "").strip()
            receptor = form_data.get("receptor", "").strip()
            asunto = form_data.get("asunto", "").strip()
            mensaje = form_data.get("mensaje", "").strip()

            if not emisor or len(emisor) < 2:
                self.error_form = "El emisor es requerido"
                return rx.toast("⚠ Emisor inválido", duration=2500)
            if not receptor:
                self.error_form = "El receptor es requerido"
                return rx.toast("⚠ Receptor requerido", duration=2500)

            normalizado = self._normalizar_telefono(receptor)
            if len(normalizado) < 10:
                self.error_form = "Teléfono inválido (mínimo 10 dígitos)"
                return rx.toast("⚠ Teléfono inválido", duration=2500)

            if not asunto:
                self.error_form = "El asunto es requerido"
                return rx.toast("⚠ Asunto requerido", duration=2500)
            if not mensaje or len(mensaje) < 5:
                self.error_form = "El mensaje debe tener al menos 5 caracteres"
                return rx.toast("⚠ Mensaje muy corto", duration=2500)

            texto_completo = f"*{asunto}*\n\n{mensaje}\n\n— {emisor}"
            texto_encoded = urllib.parse.quote(texto_completo)
            wa_link = f"https://wa.me/{normalizado}?text={texto_encoded}"

            nuevo: WhatsAppMensaje = {
                "id": max([m["id"] for m in self.historial], default=0) + 1,
                "emisor": emisor,
                "receptor": receptor,
                "receptor_normalizado": normalizado,
                "asunto": asunto,
                "mensaje": mensaje,
                "fecha": datetime.datetime.now().strftime("%d %b %Y %H:%M"),
                "estado": "Enviado",
                "wa_link": wa_link,
                "contexto": self.prefill_contexto,
            }
            self.historial.insert(0, nuevo)
            self.last_link = wa_link
            self.error_form = ""
            self.prefill_receptor = ""
            self.prefill_asunto = ""
            self.prefill_mensaje = ""

            return [
                rx.redirect(wa_link, is_external=True),
                rx.toast(f"✓ Mensaje enviado a {receptor}", duration=3500),
            ]
        except Exception as e:
            logging.exception(f"Error enviar whatsapp: {e}")
            self.error_form = "Error inesperado"
            return rx.toast("Error al enviar", duration=2500)

    @rx.event
    def reabrir_link(self, wa_link: str):
        return rx.redirect(wa_link, is_external=True)

    @rx.event
    def eliminar_mensaje(self, id_msg: int):
        self.historial = [m for m in self.historial if m["id"] != id_msg]
        return rx.toast("Mensaje eliminado del historial", duration=2000)