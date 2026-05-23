import reflex as rx
from typing import TypedDict
import logging
import datetime


class Notificacion(TypedDict):
    id: int
    tipo: str
    asunto: str
    mensaje: str
    fecha_envio: str
    estado_envio: str
    destinatario: str
    visto: bool


class NotificacionState(rx.State):
    notificaciones: list[Notificacion] = [
        {
            "id": 1,
            "tipo": "CorreoNoti",
            "asunto": "Confirmación de compra TKT-2026-00142",
            "mensaje": "Tu compra para Festival Indie Norte ha sido confirmada. 2 tickets VIP.",
            "fecha_envio": "12 Ene 2026 09:42",
            "estado_envio": "Enviado",
            "destinatario": "maria.gonzalez@mail.com",
            "visto": False,
        },
        {
            "id": 2,
            "tipo": "SMSNoti",
            "asunto": "Recordatorio de evento",
            "mensaje": "Tu evento Hamlet - Edición Moderna es este 10 de mayo a las 19:30.",
            "fecha_envio": "11 Ene 2026 18:00",
            "estado_envio": "Enviado",
            "destinatario": "+52 664 555 0192",
            "visto": False,
        },
        {
            "id": 3,
            "tipo": "CorreoNoti",
            "asunto": "Promoción exclusiva",
            "mensaje": "20% de descuento en eventos de teatro este fin de semana.",
            "fecha_envio": "10 Ene 2026 12:30",
            "estado_envio": "Enviado",
            "destinatario": "maria.gonzalez@mail.com",
            "visto": True,
        },
        {
            "id": 4,
            "tipo": "NotiManager",
            "asunto": "Nuevo evento publicado",
            "mensaje": "Rock en tu Idioma Fest agregado al catálogo. 50,000 boletos disponibles.",
            "fecha_envio": "09 Ene 2026 15:20",
            "estado_envio": "Programado",
            "destinatario": "Todos los clientes",
            "visto": True,
        },
        {
            "id": 5,
            "tipo": "SMSNoti",
            "asunto": "Cambio de fecha",
            "mensaje": "El evento TechSummit 2026 se reprogramó. Nueva fecha: 18 Jul 2026.",
            "fecha_envio": "07 Ene 2026 11:00",
            "estado_envio": "Enviado",
            "destinatario": "+52 664 555 0192",
            "visto": True,
        },
    ]

    filtro_tipo: str = "Todas"

    @rx.var
    def notificaciones_filtradas(self) -> list[Notificacion]:
        if self.filtro_tipo == "Todas":
            return self.notificaciones
        return [n for n in self.notificaciones if n["tipo"] == self.filtro_tipo]

    @rx.var
    def total_no_vistas(self) -> int:
        return len([n for n in self.notificaciones if not n["visto"]])

    @rx.event
    def set_filtro_tipo(self, v: str):
        self.filtro_tipo = v

    @rx.event
    def marcar_visto(self, id_noti: int):
        for n in self.notificaciones:
            if n["id"] == id_noti:
                n["visto"] = True

    @rx.event
    def marcar_todas_vistas(self):
        for n in self.notificaciones:
            n["visto"] = True
        return rx.toast(
            "Todas las notificaciones marcadas como leídas", duration=2500
        )

    @rx.event
    def cancelar_notificacion(self, id_noti: int):
        self.notificaciones = [
            n for n in self.notificaciones if n["id"] != id_noti
        ]
        return rx.toast("Notificación cancelada", duration=2000)

    @rx.event
    def programar_notificacion(self, form_data: dict):
        try:
            nueva: Notificacion = {
                "id": max([n["id"] for n in self.notificaciones], default=0)
                + 1,
                "tipo": form_data.get("tipo", "CorreoNoti"),
                "asunto": form_data.get("asunto", ""),
                "mensaje": form_data.get("mensaje", ""),
                "fecha_envio": datetime.datetime.now().strftime(
                    "%d %b %Y %H:%M"
                ),
                "estado_envio": "Programado",
                "destinatario": form_data.get("destinatario", ""),
                "visto": False,
            }
            self.notificaciones.insert(0, nueva)
            return rx.toast(f"Notificación programada", duration=3000)
        except Exception as e:
            logging.exception(f"Error: {e}")
            return rx.toast("Error al programar", duration=3000)