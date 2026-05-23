import reflex as rx
from tick_ez.states.ticket_state import TicketState


def venta_row(venta: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("ticket", class_name="h-5 w-5 text-violet-600"),
                class_name="p-2.5 rounded-lg bg-violet-50",
            ),
            rx.el.div(
                rx.el.p(
                    venta["evento"],
                    class_name="text-sm font-semibold text-gray-900 mb-0.5",
                ),
                rx.el.p(
                    f"{venta['cantidad']} ticket(s) · {venta['seccion']} · {venta['fecha_evento']}",
                    class_name="text-xs text-gray-500",
                ),
            ),
            class_name="flex items-center gap-3",
        ),
        rx.el.div(
            rx.el.p(
                f"${venta['precio_unit']:.0f}",
                class_name="text-base font-bold text-gray-900",
            ),
            rx.cond(
                venta["estado"] == "Activo",
                rx.el.span(
                    "Activo",
                    class_name="inline-block px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 text-xs font-semibold w-fit",
                ),
                rx.el.span(
                    "Vendido",
                    class_name="inline-block px-2 py-0.5 rounded-md bg-gray-100 text-gray-700 text-xs font-semibold w-fit",
                ),
            ),
            class_name="flex flex-col items-end gap-1",
        ),
        class_name="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors",
    )


def vender_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Vender mis tickets",
                    class_name="text-2xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    "Lista tus tickets en segundos y conecta con miles de compradores",
                    class_name="text-sm text-gray-600",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "sparkles", class_name="h-5 w-5 text-violet-600"
                        ),
                        rx.el.h3(
                            "Listar nuevo ticket",
                            class_name="text-base font-bold text-gray-900",
                        ),
                        class_name="flex items-center gap-2 mb-5",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(
                                "Nombre del evento",
                                class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="evento",
                                placeholder="Ej. Festival Indie Norte",
                                required=True,
                                class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-900 placeholder-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Cantidad",
                                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                                ),
                                rx.el.input(
                                    name="cantidad",
                                    type="number",
                                    min="1",
                                    max="20",
                                    default_value="1",
                                    required=True,
                                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-900 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Precio unitario (MXN)",
                                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                                ),
                                rx.el.input(
                                    name="precio",
                                    type="number",
                                    min="0",
                                    step="50",
                                    placeholder="1500",
                                    required=True,
                                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-900 placeholder-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-3 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Fecha del evento",
                                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                                ),
                                rx.el.input(
                                    name="fecha",
                                    type="date",
                                    required=True,
                                    class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-900 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Sección",
                                    class_name="block text-xs font-semibold text-gray-700 mb-1.5",
                                ),
                                rx.el.div(
                                    rx.el.select(
                                        rx.el.option(
                                            "General", value="General"
                                        ),
                                        rx.el.option("VIP", value="VIP"),
                                        rx.el.option("Golden", value="Golden"),
                                        rx.el.option("Platea", value="Platea"),
                                        rx.el.option("Palco", value="Palco"),
                                        name="seccion",
                                        class_name="w-full appearance-none pl-3 pr-9 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-900 focus:border-violet-500 focus:ring-2 focus:ring-violet-100 outline-none cursor-pointer",
                                    ),
                                    rx.icon(
                                        "chevron-down",
                                        class_name="absolute right-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                                    ),
                                    class_name="relative",
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-3 mb-5",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "info",
                                    class_name="h-4 w-4 text-blue-600 shrink-0 mt-0.5",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Comisión del 8%",
                                        class_name="text-xs font-semibold text-blue-900",
                                    ),
                                    rx.el.p(
                                        "Recibirás el 92% del precio listado al confirmarse la venta.",
                                        class_name="text-xs text-blue-700",
                                    ),
                                ),
                                class_name="flex items-start gap-2",
                            ),
                            class_name="p-3 bg-blue-50 border border-blue-100 rounded-lg mb-5",
                        ),
                        rx.el.button(
                            rx.icon("upload", class_name="h-4 w-4"),
                            "Publicar ticket",
                            type="submit",
                            class_name="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700 transition-colors",
                        ),
                        on_submit=TicketState.listar_venta,
                        reset_on_submit=True,
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Mis listados",
                            class_name="text-base font-bold text-gray-900",
                        ),
                        rx.el.span(
                            TicketState.ventas_listadas.length().to_string(),
                            class_name="px-2 py-0.5 rounded-md bg-violet-50 text-violet-700 text-xs font-semibold",
                        ),
                        class_name="flex items-center justify-between mb-4",
                    ),
                    rx.cond(
                        TicketState.ventas_listadas.length() > 0,
                        rx.el.div(
                            rx.foreach(TicketState.ventas_listadas, venta_row),
                            class_name="flex flex-col gap-2.5",
                        ),
                        rx.el.div(
                            rx.icon(
                                "inbox",
                                class_name="h-10 w-10 text-gray-300 mb-2",
                            ),
                            rx.el.p(
                                "No tienes listados activos",
                                class_name="text-sm font-semibold text-gray-700",
                            ),
                            rx.el.p(
                                "Publica tu primer ticket en el formulario",
                                class_name="text-xs text-gray-500",
                            ),
                            class_name="flex flex-col items-center justify-center py-12 border border-dashed border-gray-300 rounded-lg",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-5",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
    )