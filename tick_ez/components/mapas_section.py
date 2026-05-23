import reflex as rx
from tick_ez.states.mapa_state import MapaState
from tick_ez.components.mapa_recinto import (
    mapa_recinto,
    detalle_zona,
    leyenda,
)


def tipo_tab(label: str, key: str, icon: str, descripcion: str) -> rx.Component:
    is_active = MapaState.tipo_recinto == key
    return rx.el.button(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5"),
            class_name=rx.cond(
                is_active,
                "p-2.5 rounded-lg bg-white text-violet-600",
                "p-2.5 rounded-lg bg-gray-100 text-gray-500",
            ),
        ),
        rx.el.div(
            rx.el.p(
                label,
                class_name=rx.cond(
                    is_active,
                    "text-sm font-bold text-white text-left",
                    "text-sm font-bold text-gray-900 text-left",
                ),
            ),
            rx.el.p(
                descripcion,
                class_name=rx.cond(
                    is_active,
                    "text-xs text-violet-100 text-left",
                    "text-xs text-gray-500 text-left",
                ),
            ),
            class_name="flex-1",
        ),
        on_click=lambda: MapaState.set_tipo_recinto(key),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 p-3 rounded-xl bg-gradient-to-r from-violet-600 to-blue-600 transition-all w-full",
            "flex items-center gap-3 p-3 rounded-xl bg-white border border-gray-200 hover:border-violet-300 transition-all w-full",
        ),
    )


def stat_card(
    label: str, value: rx.Var | str, icon: str, color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-4 w-4 {color}"),
            class_name="p-2 rounded-lg bg-gray-50 w-fit mb-2",
        ),
        rx.el.p(value, class_name="text-lg font-bold text-gray-900"),
        rx.el.p(label, class_name="text-xs text-gray-500"),
        class_name="bg-white p-3 rounded-lg border border-gray-200",
    )


def mapas_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("map", class_name="h-3.5 w-3.5"),
                    rx.el.span("Mapas interactivos"),
                    class_name="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-violet-50 text-violet-700 text-xs font-semibold mb-3",
                ),
                rx.el.h2(
                    "Mapas de recintos",
                    class_name="text-2xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    "Explora y selecciona zonas para conciertos, convenciones y teatro",
                    class_name="text-sm text-gray-600",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                tipo_tab(
                    "Concierto",
                    "concierto",
                    "music",
                    "Arena circular con escenario",
                ),
                tipo_tab(
                    "Convención",
                    "convencion",
                    "users",
                    "Pabellones y salones",
                ),
                tipo_tab(
                    "Teatro",
                    "teatro",
                    "drama",
                    "Escenario frontal con palcos",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                rx.match(
                                    MapaState.tipo_recinto,
                                    ("convencion", "Plano de convención"),
                                    ("teatro", "Plano de teatro"),
                                    "Plano de arena",
                                ),
                                class_name="text-base font-bold text-gray-900",
                            ),
                            rx.el.p(
                                rx.match(
                                    MapaState.tipo_recinto,
                                    (
                                        "convencion",
                                        "Pabellones, salones y áreas networking",
                                    ),
                                    (
                                        "teatro",
                                        "Escenario frontal con luneta, palcos y balcón",
                                    ),
                                    "Escenario central con secciones concéntricas",
                                ),
                                class_name="text-xs text-gray-600",
                            ),
                        ),
                        leyenda(),
                        class_name="flex items-center justify-between flex-wrap gap-3 mb-4",
                    ),
                    mapa_recinto(MapaState.tipo_recinto),
                    rx.el.div(
                        stat_card(
                            "Disponibles",
                            MapaState.total_disponibles.to_string(),
                            "ticket",
                            "text-emerald-600",
                        ),
                        stat_card(
                            "Capacidad",
                            MapaState.total_capacidad.to_string(),
                            "users",
                            "text-blue-600",
                        ),
                        stat_card(
                            "Zonas",
                            MapaState.zonas_actuales.length().to_string(),
                            "layers",
                            "text-violet-600",
                        ),
                        stat_card(
                            "Tipo",
                            rx.match(
                                MapaState.tipo_recinto,
                                ("convencion", "Convención"),
                                ("teatro", "Teatro"),
                                "Concierto",
                            ),
                            "map-pin",
                            "text-amber-600",
                        ),
                        class_name="grid grid-cols-2 lg:grid-cols-4 gap-2 mt-4",
                    ),
                    class_name="lg:col-span-2",
                ),
                rx.el.div(
                    detalle_zona(),
                    rx.cond(
                        MapaState.zona_seleccionada_id != "",
                        rx.el.button(
                            rx.icon("x", class_name="h-3.5 w-3.5"),
                            "Limpiar selección",
                            on_click=MapaState.limpiar_zona,
                            class_name="mt-3 w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg text-xs font-semibold hover:bg-gray-50",
                        ),
                        rx.fragment(),
                    ),
                    class_name="lg:col-span-1",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-5",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )