import reflex as rx
from typing import TypedDict
import logging
import datetime
import urllib.parse


SOPORTE_EMAIL = "tickez.mx@gmail.com"


class Solicitud(TypedDict):
    folio: str
    categoria_ayuda: str
    descripcion: str
    prioridad: str
    estado: str
    fecha: str
    mailto_link: str


class Mensaje(TypedDict):
    autor: str
    texto: str
    hora: str
    es_usuario: bool


def _generar_respuesta_inteligente(texto: str) -> str:
    t = texto.lower().strip()

    def has(*keys: str) -> bool:
        return any(k in t for k in keys)

    if has("hola", "buenos dias", "buenas tardes", "buenas noches", "saludos"):
        return (
            "¡Hola! 👋 Soy el asistente virtual de Tick_EZ. Puedo ayudarte con: "
            "reembolsos, descarga de tickets PDF, código QR, cambio de titular, "
            "TicketStar accesible, pagos duplicados, acceso al evento y más. "
            "¿Cuál es tu duda?"
        )
    if has(
        "reembolso",
        "devolucion",
        "devolución",
        "regresar dinero",
        "cancelar compra",
    ):
        return (
            "💸 *Reembolsos*: procesamos reembolsos hasta 48h antes del evento. "
            "Crea una solicitud con categoría 'Reembolso' incluyendo tu folio (TKT-2026-XXXXX). "
            "El reembolso se aplica al método de pago original en 5-7 días hábiles."
        )
    if has("qr", "codigo qr", "código qr", "escanear", "no escanea"):
        return (
            "🎫 *Código QR*: cada ticket tiene un QR único e intransferible. "
            "Lo encuentras en tu confirmación y en 'Mis compras'. Si no escanea: "
            "1) aumenta el brillo del celular, 2) descarga el PDF y muéstralo, "
            "3) verifica que no esté caducado."
        )
    if has("pdf", "descargar", "descarga", "imprimir ticket", "comprobante"):
        return (
            "📄 *Descargar PDF*: ve a 'Mis compras' y presiona 'Descargar PDF' "
            "en el ticket que necesites. El archivo incluye QR, folio, zona y datos del titular. "
            "También puedes descargarlo justo después de confirmar tu compra."
        )
    if has("cambio de titular", "transferir", "cambiar nombre", "otro nombre"):
        return (
            "🔁 *Cambio de titular*: disponible hasta 24h antes del evento. "
            "Crea una solicitud con categoría 'Cambio de titular' indicando folio, "
            "nombre actual y nombre nuevo con identificación oficial. Costo: $50 MXN."
        )
    if has(
        "pago duplicado", "cobro doble", "me cobraron dos veces", "doble cargo"
    ):
        return (
            "💳 *Pago duplicado*: lamentamos el inconveniente. Crea una solicitud "
            "con categoría 'Pago duplicado' adjuntando ambos comprobantes. "
            "Devolvemos el cargo extra en 3-5 días hábiles."
        )
    if has("acceso", "no puedo entrar", "rechazado", "puerta", "ingreso"):
        return (
            "🚪 *Acceso al evento*: presenta tu QR (digital o impreso) + identificación oficial. "
            "Llega 60 min antes. Si tu ticket marca error, contáctanos por WhatsApp soporte "
            "para validar tu folio en tiempo real."
        )
    if has(
        "ticketstar",
        "accesibilidad",
        "discapacidad",
        "silla de ruedas",
        "accesible",
    ):
        return (
            "♿ *TicketStar*: zona accesible con beneficios premium (rampa, asistente, "
            "espacios reservados). Selecciona la opción TicketStar al comprar o elige "
            "una zona accesible en el mapa del recinto. Incluye acompañante sin costo extra."
        )
    if has("whatsapp", "wa", "compartir ticket", "enviar mensaje"):
        return (
            "📲 *WhatsApp*: desde 'Mis compras' o la sección WhatsApp puedes generar "
            "un enlace wa.me con tu ticket prellenado para compartirlo. "
            "También puedes contactar soporte directo al +52 800 555 0100."
        )
    if has(
        "contraseña",
        "contrasena",
        "no puedo entrar a mi cuenta",
        "olvide",
        "recuperar cuenta",
        "login",
    ):
        return (
            "🔐 *Cuenta y contraseña*: ve a 'Cuenta', cierra sesión y usa 'Recuperar contraseña'. "
            "Te enviaremos un enlace al correo registrado. Si tu cuenta está bloqueada por "
            "intentos fallidos, espera 15 min o crea una solicitud."
        )
    if has(
        "correo",
        "email",
        "no me llego",
        "no me llegó",
        "confirmacion",
        "confirmación",
    ):
        return (
            "📧 *Correo de confirmación*: revisa tu carpeta de spam/promociones. "
            "Si no llega en 10 min, verifica el correo registrado en 'Cuenta'. "
            "Puedes también descargar tu PDF directamente desde 'Mis compras'."
        )
    if has("evento cancelado", "cancelaron", "se cancelo", "se canceló"):
        return (
            "📅 *Evento cancelado*: el reembolso es automático al método de pago original "
            "en 5-7 días hábiles. Si pasaron más días, crea una solicitud 'Reembolso' "
            "con folio y te daremos seguimiento prioritario."
        )
    if has("cambio de fecha", "reprogramar", "nueva fecha"):
        return (
            "🗓️ *Cambio de fecha*: tu ticket sigue siendo válido para la nueva fecha. "
            "Si no puedes asistir, puedes solicitar reembolso completo dentro de los 14 días "
            "posteriores al anuncio del cambio."
        )
    if has("precio", "costo", "cuanto cuesta", "cuánto cuesta", "tarifa"):
        return (
            "💰 *Precios*: cada zona tiene su precio en el mapa del recinto. "
            "TicketStar y Golden son premium (3x), VIP (2x) y General (1x). "
            "Se aplica un cargo de servicio del 5% al total."
        )
    if has("gracias", "muchas gracias", "ok", "perfecto", "entendido"):
        return (
            "¡De nada! 😊 Si necesitas algo más, estoy aquí. "
            "Recuerda que también puedes crear una solicitud formal "
            "y la enviaremos por correo a nuestro equipo."
        )
    if has("ayuda", "necesito ayuda", "duda", "pregunta", "soporte"):
        return (
            "Claro, estoy para ayudarte. Cuéntame con más detalle tu problema, "
            "o crea una solicitud formal con la categoría adecuada y nuestro equipo "
            "te responderá por correo a la brevedad."
        )

    return (
        "Recibí tu mensaje. 🤖 Para darte una respuesta más precisa, "
        "¿podrías incluir tu folio (TKT-2026-XXXXX) y describir el problema? "
        "También puedes crear una solicitud formal arriba para escalar el caso."
    )


class SoporteState(rx.State):
    solicitudes: list[Solicitud] = [
        {
            "folio": "SOL-2026-00231",
            "categoria_ayuda": "Reembolso",
            "descripcion": "Solicito reembolso por evento cancelado",
            "prioridad": "Alta",
            "estado": "En proceso",
            "fecha": "12 Ene 2026",
            "mailto_link": "",
        },
        {
            "folio": "SOL-2026-00198",
            "categoria_ayuda": "Cambio de titular",
            "descripcion": "Necesito cambiar el titular de mi ticket VIP",
            "prioridad": "Media",
            "estado": "Resuelto",
            "fecha": "08 Ene 2026",
            "mailto_link": "",
        },
        {
            "folio": "SOL-2026-00154",
            "categoria_ayuda": "Acceso al ticket digital",
            "descripcion": "No puedo descargar mi ticket en PDF",
            "prioridad": "Baja",
            "estado": "Pendiente",
            "fecha": "05 Ene 2026",
            "mailto_link": "",
        },
    ]
    ultima_solicitud_folio: str = ""
    ultimo_mailto: str = ""
    show_solicitud_exito: bool = False

    chat_mensajes: list[Mensaje] = [
        {
            "autor": "Soporte Ticketera",
            "texto": "Hola, soy Luis del equipo de soporte. ¿En qué puedo ayudarte?",
            "hora": "09:42",
            "es_usuario": False,
        },
        {
            "autor": "Tú",
            "texto": "Hola, no me llegó el correo de confirmación de mi compra TKT-2026-00142",
            "hora": "09:43",
            "es_usuario": True,
        },
        {
            "autor": "Soporte Ticketera",
            "texto": "Permíteme verificar tu folio. Veo tu compra confirmada, te reenvío el correo en este momento.",
            "hora": "09:44",
            "es_usuario": False,
        },
    ]

    nuevo_mensaje: str = ""
    chat_input_key: int = 0

    def _build_mailto(
        self, folio: str, categoria: str, prioridad: str, descripcion: str
    ) -> str:
        asunto = f"[{folio}] {categoria} · Prioridad {prioridad}"
        cuerpo = (
            f"Hola equipo Tick_EZ,\n\n"
            f"Solicitud generada desde la plataforma:\n\n"
            f"Folio: {folio}\n"
            f"Categoría: {categoria}\n"
            f"Prioridad: {prioridad}\n"
            f"Fecha: {datetime.datetime.now().strftime('%d %b %Y %H:%M')}\n\n"
            f"Descripción:\n{descripcion}\n\n"
            f"Atentamente,\nUsuario Tick_EZ"
        )
        params = urllib.parse.urlencode(
            {"subject": asunto, "body": cuerpo}, quote_via=urllib.parse.quote
        )
        return f"mailto:{SOPORTE_EMAIL}?{params}"

    @rx.event
    def crear_solicitud(self, form_data: dict):
        try:
            import random

            descripcion = form_data.get("descripcion", "").strip()
            if len(descripcion) < 10:
                return rx.toast(
                    "⚠ La descripción debe tener al menos 10 caracteres",
                    duration=3000,
                )
            folio = f"SOL-2026-{random.randint(100, 9999):04d}"
            categoria = form_data.get("categoria", "General")
            prioridad = form_data.get("prioridad", "Media")
            mailto_link = self._build_mailto(
                folio, categoria, prioridad, descripcion
            )
            nueva: Solicitud = {
                "folio": folio,
                "categoria_ayuda": categoria,
                "descripcion": descripcion,
                "prioridad": prioridad,
                "estado": "Pendiente",
                "fecha": datetime.datetime.now().strftime("%d %b %Y"),
                "mailto_link": mailto_link,
            }
            self.solicitudes.insert(0, nueva)
            self.ultima_solicitud_folio = folio
            self.ultimo_mailto = mailto_link
            self.show_solicitud_exito = True
            return [
                rx.redirect(mailto_link, is_external=True),
                rx.toast(
                    f"✓ Solicitud {folio} creada y enviada a {SOPORTE_EMAIL}",
                    duration=4500,
                ),
            ]
        except Exception as e:
            logging.exception(f"Error: {e}")
            return rx.toast("Error al crear solicitud", duration=3000)

    @rx.event
    def reenviar_mailto(self, mailto_link: str):
        if not mailto_link:
            return rx.toast("Enlace no disponible", duration=2000)
        return rx.redirect(mailto_link, is_external=True)

    @rx.event
    def cerrar_solicitud_exito(self):
        self.show_solicitud_exito = False

    @rx.event
    def set_nuevo_mensaje(self, v: str):
        self.nuevo_mensaje = v

    @rx.event
    def enviar_mensaje(self, form_data: dict | None = None):
        texto = ""
        if form_data and isinstance(form_data, dict):
            texto = (form_data.get("mensaje") or "").strip()
        if not texto:
            texto = self.nuevo_mensaje.strip()
        if not texto:
            return
        ahora = datetime.datetime.now().strftime("%H:%M")
        self.chat_mensajes.append(
            {
                "autor": "Tú",
                "texto": texto,
                "hora": ahora,
                "es_usuario": True,
            }
        )
        respuesta = _generar_respuesta_inteligente(texto)
        self.chat_mensajes.append(
            {
                "autor": "Soporte Tick_EZ",
                "texto": respuesta,
                "hora": datetime.datetime.now().strftime("%H:%M"),
                "es_usuario": False,
            }
        )
        self.nuevo_mensaje = ""
        self.chat_input_key += 1

    @rx.event
    def finalizar_chat(self):
        self.chat_mensajes = [
            {
                "autor": "Soporte Ticketera",
                "texto": "Chat finalizado. ¡Gracias por contactarnos!",
                "hora": datetime.datetime.now().strftime("%H:%M"),
                "es_usuario": False,
            }
        ]
        return rx.toast("Chat finalizado", duration=2500)

    @rx.event
    def cambiar_estado_solicitud(self, folio: str, nuevo_estado: str):
        for s in self.solicitudes:
            if s["folio"] == folio:
                s["estado"] = nuevo_estado
        return rx.toast(f"Solicitud {folio}: {nuevo_estado}", duration=2500)