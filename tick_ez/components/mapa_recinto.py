import reflex as rx
from tick_ez.states.mapa_state import MapaState, Zona


def _zone_class(zona: Zona) -> rx.Var:
    is_selected = MapaState.zona_seleccionada_id == zona["id"]
    is_sold = zona["disponibles"] == 0
    base = "relative cursor-pointer rounded-lg border-2 p-2.5 transition-all flex flex-col items-center justify-center text-center min-h-[60px] hover:scale-[1.02]"
    return rx.cond(
        is_sold,
        f"{base} bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed opacity-60",
        rx.cond(
            is_selected,
            rx.match(
                zona["color"],
                (
                    "amber",
                    f"{base} bg-amber-500 border-amber-600 text-white shadow-lg ring-4 ring-amber-200",
                ),
                (
                    "violet",
                    f"{base} bg-violet-500 border-violet-600 text-white shadow-lg ring-4 ring-violet-200",
                ),
                (
                    "blue",
                    f"{base} bg-blue-500 border-blue-600 text-white shadow-lg ring-4 ring-blue-200",
                ),
                (
                    "teal",
                    f"{base} bg-teal-500 border-teal-600 text-white shadow-lg ring-4 ring-teal-200",
                ),
                (
                    "emerald",
                    f"{base} bg-emerald-500 border-emerald-600 text-white shadow-lg ring-4 ring-emerald-200",
                ),
                f"{base} bg-violet-500 border-violet-600 text-white shadow-lg",
            ),
            rx.match(
                zona["color"],
                (
                    "amber",
                    f"{base} bg-amber-50 border-amber-300 text-amber-900 hover:bg-amber-100",
                ),
                (
                    "violet",
                    f"{base} bg-violet-50 border-violet-300 text-violet-900 hover:bg-violet-100",
                ),
                (
                    "blue",
                    f"{base} bg-blue-50 border-blue-300 text-blue-900 hover:bg-blue-100",
                ),
                (
                    "teal",
                    f"{base} bg-teal-50 border-teal-300 text-teal-900 hover:bg-teal-100",
                ),
                (
                    "emerald",
                    f"{base} bg-emerald-50 border-emerald-300 text-emerald-900 hover:bg-emerald-100",
                ),
                f"{base} bg-gray-50 border-gray-300 text-gray-900 hover:bg-gray-100",
            ),
        ),
    )


def _zone_button(zona: Zona, label_size: str = "text-xs") -> rx.Component:
    return rx.el.button(
        rx.cond(
            zona["accesible"],
            rx.icon(
                "accessibility",
                class_name="absolute top-1 right-1 h-3 w-3 opacity-70",
            ),
            rx.fragment(),
        ),
        rx.cond(
            zona["disponibles"] == 0,
            rx.el.div(
                rx.icon("x", class_name="h-3 w-3"),
                rx.el.span("Agotado", class_name="text-[10px] font-semibold"),
                class_name="flex items-center gap-1 mb-0.5",
            ),
            rx.fragment(),
        ),
        rx.el.span(
            zona["nombre"],
            class_name=f"{label_size} font-bold leading-tight",
        ),
        rx.el.span(
            f"${zona['precio']:.0f}",
            class_name="text-[10px] font-semibold opacity-80 mt-0.5",
        ),
        on_click=lambda: MapaState.seleccionar_zona(zona["id"]),
        type="button",
        class_name=_zone_class(zona),
        disabled=zona["disponibles"] == 0,
    )


def _stage(label: str, color: str = "violet") -> rx.Component:
    return rx.el.div(
        rx.icon("mic", class_name="h-4 w-4"),
        rx.el.span(label, class_name="text-xs font-bold tracking-wider"),
        class_name=f"flex items-center justify-center gap-2 py-3 rounded-lg bg-gradient-to-r from-violet-600 to-blue-600 text-white shadow-md",
    )


def mapa_concierto() -> rx.Component:
    z = MapaState.zonas_concierto
    return rx.el.div(
        _stage("ESCENARIO PRINCIPAL"),
        rx.el.div(
            _zone_button(z[0]),
            class_name="grid grid-cols-1 mt-3",
        ),
        rx.el.div(
            _zone_button(z[1]),
            class_name="grid grid-cols-1 mt-2",
        ),
        rx.el.div(
            _zone_button(z[4]),
            _zone_button(z[2]),
            _zone_button(z[3]),
            _zone_button(z[5]),
            class_name="grid grid-cols-4 gap-2 mt-2",
        ),
        rx.el.div(
            _zone_button(z[6]),
            class_name="grid grid-cols-1 mt-2",
        ),
        rx.el.div(
            _zone_button(z[7]),
            class_name="grid grid-cols-1 mt-2",
        ),
        rx.el.div(
            _zone_button(z[8]),
            class_name="grid grid-cols-1 mt-2",
        ),
        class_name="bg-gradient-to-b from-gray-50 to-white p-4 rounded-xl border border-gray-200",
    )


def mapa_convencion() -> rx.Component:
    z = MapaState.zonas_convencion
    return rx.el.div(
        rx.el.div(
            rx.icon("door-open", class_name="h-4 w-4"),
            rx.el.span(
                "ENTRADA PRINCIPAL",
                class_name="text-xs font-bold tracking-wider",
            ),
            class_name="flex items-center justify-center gap-2 py-2.5 rounded-lg bg-gray-800 text-white mb-3",
        ),
        rx.el.div(
            _zone_button(z[0]),
            _zone_button(z[1]),
            class_name="grid grid-cols-2 gap-2 mb-2",
        ),
        rx.el.div(
            _zone_button(z[2]),
            _zone_button(z[3]),
            class_name="grid grid-cols-2 gap-2 mb-2",
        ),
        rx.el.div(
            _zone_button(z[5]),
            _zone_button(z[6]),
            class_name="grid grid-cols-2 gap-2 mb-2",
        ),
        rx.el.div(
            _zone_button(z[4]),
            _zone_button(z[7]),
            class_name="grid grid-cols-2 gap-2",
        ),
        class_name="bg-gradient-to-b from-gray-50 to-white p-4 rounded-xl border border-gray-200",
    )


def mapa_teatro() -> rx.Component:
    z = MapaState.zonas_teatro
    return rx.el.div(
        _stage("ESCENARIO"),
        rx.el.div(
            _zone_button(z[0]),
            class_name="grid grid-cols-1 mt-3 mx-8",
        ),
        rx.el.div(
            rx.el.div(
                _zone_button(z[3]),
                class_name="col-span-1",
            ),
            rx.el.div(
                _zone_button(z[1]),
                class_name="col-span-2",
            ),
            rx.el.div(
                _zone_button(z[4]),
                class_name="col-span-1",
            ),
            class_name="grid grid-cols-4 gap-2 mt-2",
        ),
        rx.el.div(
            _zone_button(z[2]),
            class_name="grid grid-cols-1 mt-2 mx-4",
        ),
        rx.el.div(
            _zone_button(z[7]),
            class_name="grid grid-cols-1 mt-2 mx-12",
        ),
        rx.el.div(
            _zone_button(z[5]),
            _zone_button(z[6]),
            class_name="grid grid-cols-2 gap-2 mt-2",
        ),
        class_name="bg-gradient-to-b from-gray-50 to-white p-4 rounded-xl border border-gray-200",
    )


def leyenda() -> rx.Component:
    items = [
        ("bg-violet-100 border-violet-300", "Disponible"),
        ("bg-violet-500 border-violet-600", "Seleccionado"),
        ("bg-gray-100 border-gray-300", "Agotado"),
        ("bg-emerald-50 border-emerald-300", "Accesible"),
    ]
    return rx.el.div(
        *[
            rx.el.div(
                rx.el.div(class_name=f"size-3 rounded border-2 {cls}"),
                rx.el.span(
                    label, class_name="text-xs text-gray-700 font-medium"
                ),
                class_name="flex items-center gap-1.5",
            )
            for cls, label in items
        ],
        class_name="flex items-center gap-4 flex-wrap",
    )


def detalle_zona() -> rx.Component:
    z = MapaState.zona_actual
    return rx.cond(
        MapaState.zona_seleccionada_id != "",
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        z["categoria"],
                        class_name="text-xs font-bold text-violet-700 bg-violet-50 px-2 py-0.5 rounded-md",
                    ),
                    rx.cond(
                        z["accesible"],
                        rx.el.span(
                            rx.icon("accessibility", class_name="h-3 w-3"),
                            "Accesible",
                            class_name="flex items-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md",
                        ),
                        rx.fragment(),
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                rx.el.h4(
                    z["nombre"],
                    class_name="text-base font-bold text-gray-900",
                ),
                rx.el.p(
                    z["descripcion"], class_name="text-xs text-gray-600 mb-3"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Precio",
                            class_name="text-xs text-gray-500",
                        ),
                        rx.el.p(
                            f"${z['precio']:.0f}",
                            class_name="text-lg font-bold text-violet-600",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Disponibles", class_name="text-xs text-gray-500"
                        ),
                        rx.el.p(
                            f"{z['disponibles']} / {z['total']}",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-3 mb-3 p-3 bg-gray-50 rounded-lg",
                ),
                rx.el.p(
                    "Beneficios incluidos",
                    class_name="text-xs font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.ul(
                    rx.foreach(
                        z["beneficios"],
                        lambda b: rx.el.li(
                            rx.icon(
                                "check",
                                class_name="h-3 w-3 text-emerald-600 shrink-0 mt-0.5",
                            ),
                            rx.el.span(b, class_name="text-xs text-gray-700"),
                            class_name="flex items-start gap-1.5",
                        ),
                    ),
                    class_name="flex flex-col gap-1",
                ),
            ),
            class_name="bg-white p-4 rounded-xl border-2 border-violet-200",
        ),
        rx.el.div(
            rx.icon(
                "mouse-pointer-click",
                class_name="h-8 w-8 text-gray-300 mb-2",
            ),
            rx.el.p(
                "Selecciona una zona del mapa",
                class_name="text-sm font-semibold text-gray-700",
            ),
            rx.el.p(
                "Toca cualquier área disponible para ver precio y beneficios",
                class_name="text-xs text-gray-500 text-center",
            ),
            class_name="bg-white p-6 rounded-xl border-2 border-dashed border-gray-300 flex flex-col items-center justify-center text-center min-h-[200px]",
        ),
    )


def mapa_recinto(tipo: str) -> rx.Component:
    return rx.match(
        tipo,
        ("convencion", mapa_convencion()),
        ("teatro", mapa_teatro()),
        mapa_concierto(),
    )


def mapa_compacto() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("map", class_name="h-4 w-4 text-violet-600"),
                rx.el.h4(
                    "Mapa del recinto",
                    class_name="text-sm font-bold text-gray-900",
                ),
                class_name="flex items-center gap-1.5",
            ),
            leyenda(),
            class_name="flex items-center justify-between mb-3 flex-wrap gap-2",
        ),
        mapa_recinto(MapaState.tipo_recinto),
        rx.el.div(
            detalle_zona(),
            class_name="mt-3",
        ),
    )