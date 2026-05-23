import reflex as rx


def metodo_pill(metodo: str) -> rx.Component:
    return rx.el.span(
        f"{metodo}()",
        class_name="px-1.5 py-0.5 rounded bg-violet-50 text-violet-700 text-xs font-mono",
    )


def atributo_pill(atributo: str) -> rx.Component:
    return rx.el.span(
        atributo,
        class_name="px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 text-xs font-mono",
    )


def clase_card(
    nombre: str,
    tipo: str,
    atributos: list[str],
    metodos: list[str],
    color: str,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    tipo,
                    class_name=f"text-xs font-bold uppercase tracking-wider {color}",
                ),
                rx.el.h4(
                    nombre,
                    class_name="text-sm font-bold text-gray-900",
                ),
            ),
            rx.icon("box", class_name=f"h-4 w-4 {color}"),
            class_name="flex items-start justify-between mb-3 pb-2 border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.p(
                "Atributos",
                class_name="text-xs font-semibold text-gray-500 mb-1.5",
            ),
            rx.el.div(
                *[atributo_pill(a) for a in atributos],
                class_name="flex flex-wrap gap-1 mb-3",
            ),
            rx.el.p(
                "Métodos",
                class_name="text-xs font-semibold text-gray-500 mb-1.5",
            ),
            rx.el.div(
                *[metodo_pill(m) for m in metodos],
                class_name="flex flex-wrap gap-1",
            ),
        ),
        class_name="bg-white p-4 rounded-lg border border-gray-200 hover:border-violet-300 transition-colors",
    )


def grupo_section(
    titulo: str,
    descripcion: str,
    icono: str,
    color_bg: str,
    color_text: str,
    base_card: rx.Component,
    derivadas: list[rx.Component],
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icono, class_name=f"h-5 w-5 {color_text}"),
                class_name=f"p-2.5 rounded-lg {color_bg}",
            ),
            rx.el.div(
                rx.el.h3(
                    titulo,
                    class_name="text-base font-bold text-gray-900",
                ),
                rx.el.p(descripcion, class_name="text-xs text-gray-600"),
            ),
            class_name="flex items-start gap-3 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "CLASE BASE",
                    class_name="text-xs font-bold text-gray-400 tracking-wider mb-2",
                ),
                base_card,
                class_name="lg:col-span-1",
            ),
            rx.el.div(
                rx.icon(
                    "arrow-right",
                    class_name="h-5 w-5 text-gray-300 mx-auto hidden lg:block",
                ),
                class_name="flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.span(
                    "CLASES DERIVADAS",
                    class_name="text-xs font-bold text-gray-400 tracking-wider mb-2 block",
                ),
                rx.el.div(
                    *derivadas,
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-3",
                ),
                class_name="lg:col-span-3",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-5 gap-3",
        ),
        class_name="bg-gray-50 p-5 rounded-xl border border-gray-200 mb-5",
    )


def arquitectura_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("blocks", class_name="h-3.5 w-3.5"),
                    rx.el.span("Arquitectura UML"),
                    class_name="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-violet-50 text-violet-700 text-xs font-semibold mb-4",
                ),
                rx.el.h2(
                    "Arquitectura del sistema",
                    class_name="text-2xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    "Clases base y derivadas integradas en el sistema de ticketera",
                    class_name="text-sm text-gray-600",
                ),
                class_name="mb-6",
            ),
            grupo_section(
                "Gestión de usuarios y seguridad",
                "Manejo de roles, permisos y sesiones del sistema",
                "users",
                "bg-violet-50",
                "text-violet-600",
                clase_card(
                    "Rol",
                    "Base",
                    ["correo", "id_usuario", "contraseña", "estado_cuenta"],
                    [
                        "iniciar_sesion",
                        "cerrar_sesion",
                        "mostrar_perfil",
                        "editar_perfil",
                        "recuperar_contra",
                    ],
                    "text-violet-600",
                ),
                [
                    clase_card(
                        "Cliente",
                        "Derivada",
                        ["historial_compras", "tickets", "metodo_pago"],
                        [
                            "comprar_ticket",
                            "reservar_ticket",
                            "cancelar_ticket",
                        ],
                        "text-blue-600",
                    ),
                    clase_card(
                        "EmpleadoSoporte",
                        "Derivada",
                        [
                            "area_soporte",
                            "atencion_cliente",
                            "correcion_tickets",
                        ],
                        [
                            "responder_cliente",
                            "cambiar_solicitud",
                            "generar_reportes_soporte",
                        ],
                        "text-emerald-600",
                    ),
                    clase_card(
                        "Administrador",
                        "Derivada",
                        ["nivel_acceso"],
                        [
                            "crear_evento",
                            "editar_evento",
                            "eliminar_evento",
                            "gestion_usuarios",
                            "generar_reportes",
                        ],
                        "text-amber-600",
                    ),
                ],
            ),
            grupo_section(
                "Sesión",
                "Control de acceso, autenticación y bloqueos",
                "shield-check",
                "bg-blue-50",
                "text-blue-600",
                clase_card(
                    "Sesion",
                    "Base",
                    ["fecha_inicio", "hora_inicio", "ip_usuario"],
                    ["abrir_sesion", "cerrar_sesion", "validar_sesion"],
                    "text-blue-600",
                ),
                [
                    clase_card(
                        "LoginUser",
                        "Derivada",
                        ["usuario", "contraseña"],
                        [
                            "verificar_correo",
                            "error_login",
                            "acceso_perfil",
                            "menu_principal",
                        ],
                        "text-violet-600",
                    ),
                    clase_card(
                        "LoginManager",
                        "Derivada",
                        [
                            "usuarios_activos",
                            "cuentas_inactivas",
                            "intentos_fallidos",
                        ],
                        [
                            "autentificacion_usuario",
                            "bloquear_usuario",
                            "cerrar_sesion_manager",
                        ],
                        "text-amber-600",
                    ),
                ],
            ),
            grupo_section(
                "Manejo de tickets",
                "Operaciones financieras y de reservación",
                "ticket",
                "bg-emerald-50",
                "text-emerald-600",
                clase_card(
                    "Operacion",
                    "Base",
                    [
                        "fecha_operacion",
                        "montos",
                        "lugares_evento",
                        "estado_operacion",
                    ],
                    [
                        "registro_operacion",
                        "monto_operacion",
                        "etapa_operacion",
                    ],
                    "text-emerald-600",
                ),
                [
                    clase_card(
                        "Reservar",
                        "Derivada",
                        [
                            "tiempo_limite",
                            "asiento_reservado",
                            "fecha_y_hora",
                        ],
                        ["reservar_asiento", "cancelar_reserva"],
                        "text-blue-600",
                    ),
                    clase_card(
                        "Compra",
                        "Derivada",
                        ["metodo_pago", "folio_compra"],
                        ["procesar_compra", "confirmar_compra"],
                        "text-violet-600",
                    ),
                    clase_card(
                        "Pago",
                        "Derivada",
                        ["tipo_pago", "referencia_pago"],
                        ["validar_pago", "realizar_pago", "reembolso"],
                        "text-amber-600",
                    ),
                    clase_card(
                        "Factura",
                        "Derivada",
                        ["folio_factura", "fecha_emision", "rfc"],
                        [
                            "generar_factura",
                            "descargar_factura",
                            "enviar_factura",
                        ],
                        "text-emerald-600",
                    ),
                ],
            ),
            grupo_section(
                "Categoría de tickets",
                "Niveles de tickets disponibles para los eventos",
                "tag",
                "bg-amber-50",
                "text-amber-600",
                clase_card(
                    "Categoria",
                    "Base",
                    ["nombre_categoria", "precio", "beneficios"],
                    ["categoria_ticket", "actualizar_precio"],
                    "text-amber-600",
                ),
                [
                    clase_card(
                        "TicketGeneral",
                        "Derivada",
                        ["acceso_general"],
                        ["aplicar_descuento"],
                        "text-blue-600",
                    ),
                    clase_card(
                        "TicketVIP",
                        "Derivada",
                        ["amenidades", "zona_preferente"],
                        ["acceso_vip"],
                        "text-violet-600",
                    ),
                    clase_card(
                        "TicketGolden",
                        "Derivada",
                        ["meet_and_greet", "regalo_exclusivo"],
                        ["acceso_premium"],
                        "text-amber-600",
                    ),
                ],
            ),
            grupo_section(
                "Eventos y asientos",
                "Catálogo de eventos y mapa interactivo de asientos",
                "calendar",
                "bg-violet-50",
                "text-violet-600",
                clase_card(
                    "Evento",
                    "Base",
                    ["nombre", "fecha", "ubicacion", "capacidad"],
                    ["crear_evento", "actualizar_evento", "eliminar_evento"],
                    "text-violet-600",
                ),
                [
                    clase_card(
                        "Concierto",
                        "Derivada",
                        ["artista", "genero_musical"],
                        ["mostrar_setlist"],
                        "text-blue-600",
                    ),
                    clase_card(
                        "Convencion",
                        "Derivada",
                        ["temas", "expositores"],
                        ["mostrar_agenda"],
                        "text-emerald-600",
                    ),
                    clase_card(
                        "FuncionTeatro",
                        "Derivada",
                        ["obra", "elenco", "duracion"],
                        ["mostrar_reparto"],
                        "text-amber-600",
                    ),
                    clase_card(
                        "MapaAsientos",
                        "Asociada",
                        ["filas", "columnas", "areas"],
                        ["renderizar_mapa", "actualizar_disponibilidad"],
                        "text-violet-600",
                    ),
                ],
            ),
            grupo_section(
                "Mapa de asientos",
                "Selección interactiva, disponibilidad y áreas",
                "armchair",
                "bg-blue-50",
                "text-blue-600",
                clase_card(
                    "MapaAsientos",
                    "Base",
                    ["filas", "columnas", "estado_general"],
                    ["renderizar_mapa", "obtener_asiento"],
                    "text-blue-600",
                ),
                [
                    clase_card(
                        "AsientoInteraccion",
                        "Derivada",
                        ["id_asiento", "seleccionado"],
                        ["seleccionar_asiento", "deseleccionar_asiento"],
                        "text-violet-600",
                    ),
                    clase_card(
                        "Disponibilidad",
                        "Derivada",
                        ["estado_asiento", "ultima_actualizacion"],
                        ["verificar_disponibilidad", "actualizar_estado"],
                        "text-emerald-600",
                    ),
                    clase_card(
                        "Area",
                        "Derivada",
                        ["nombre_area", "tipo_area", "precio_area"],
                        ["mostrar_info_area"],
                        "text-amber-600",
                    ),
                ],
            ),
            grupo_section(
                "Soporte técnico",
                "Atención al cliente y comunicación interactiva",
                "headphones",
                "bg-emerald-50",
                "text-emerald-600",
                clase_card(
                    "SoporteTecnico",
                    "Base",
                    [
                        "mensaje",
                        "prioridad",
                        "estado_solicitud",
                        "fecha_solicitud",
                    ],
                    [
                        "crear_solicitud",
                        "modificar_solicitud",
                        "mostrar_estado",
                    ],
                    "text-emerald-600",
                ),
                [
                    clase_card(
                        "Solicitud",
                        "Derivada",
                        ["categoria_ayuda", "descripcion"],
                        ["enviar_solicitud", "editar_solicitud"],
                        "text-violet-600",
                    ),
                    clase_card(
                        "Chat",
                        "Derivada",
                        ["mensajes", "usuario_emisor"],
                        [
                            "enviar_mensaje",
                            "recibir_mensaje",
                            "finalizar_chat",
                        ],
                        "text-blue-600",
                    ),
                ],
            ),
            grupo_section(
                "Motor de búsqueda",
                "Filtros y buscador para localizar eventos",
                "search",
                "bg-amber-50",
                "text-amber-600",
                clase_card(
                    "Filtro",
                    "Base",
                    ["tipo_filtro"],
                    ["aplicar_filtro", "limpiar_filtro"],
                    "text-amber-600",
                ),
                [
                    clase_card(
                        "FiltroFecha",
                        "Derivada",
                        ["rango_fechas"],
                        ["filtrar_por_fecha"],
                        "text-blue-600",
                    ),
                    clase_card(
                        "FiltroCategoria",
                        "Derivada",
                        ["categoria"],
                        ["filtrar_por_categoria"],
                        "text-violet-600",
                    ),
                    clase_card(
                        "FiltroPrecio",
                        "Derivada",
                        ["rango_precio"],
                        ["filtrar_por_precio"],
                        "text-emerald-600",
                    ),
                    clase_card(
                        "FiltroUbicacion",
                        "Derivada",
                        ["ciudad", "lugar"],
                        ["filtrar_por_ubicacion"],
                        "text-amber-600",
                    ),
                    clase_card(
                        "Buscador",
                        "Independiente",
                        ["palabra_clave", "resultados"],
                        [
                            "buscar_evento",
                            "mostrar_resultados",
                            "ordenar_resultados",
                        ],
                        "text-violet-600",
                    ),
                ],
            ),
            grupo_section(
                "Sistema de notificaciones",
                "Avisos al usuario por correo, SMS y administración",
                "bell",
                "bg-blue-50",
                "text-blue-600",
                clase_card(
                    "Notificacion",
                    "Base",
                    [
                        "mensaje",
                        "fecha_envio",
                        "estado_envio",
                        "destinatario",
                    ],
                    ["enviar_notificacion", "mostrar_notificacion"],
                    "text-blue-600",
                ),
                [
                    clase_card(
                        "CorreoNoti",
                        "Derivada",
                        ["correo_destinatario", "asunto"],
                        ["responder_correo", "marcar_visto"],
                        "text-violet-600",
                    ),
                    clase_card(
                        "SMSNoti",
                        "Derivada",
                        ["numero_telefonico"],
                        ["responder_sms", "enviar_respuesta"],
                        "text-emerald-600",
                    ),
                    clase_card(
                        "NotiManager",
                        "Derivada",
                        ["lista_notificaciones"],
                        [
                            "programar_notificacion",
                            "cancelar_notificacion",
                            "mostrar_historial_noti",
                        ],
                        "text-amber-600",
                    ),
                ],
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )