import reflex as rx


def logo(size: str = "md") -> rx.Component:
    sizes = {
        "sm": ("size-7", "text-base"),
        "md": ("size-9", "text-lg"),
        "lg": ("size-12", "text-2xl"),
    }
    circle_class, text_class = sizes.get(size, sizes["md"])
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("ticket", class_name="h-4 w-4 text-white"),
                class_name="size-full bg-gradient-to-br from-teal-400 to-cyan-500 flex items-center justify-center",
            ),
            class_name=f"{circle_class} rounded-full border border-gray-100 flex items-center justify-center shadow-sm overflow-hidden bg-white shrink-0",
        ),
        rx.el.div(
            rx.el.span("Tick_ez", class_name="text-gray-900"),
            class_name=f"{text_class} font-extrabold tracking-tight flex items-baseline",
        ),
        class_name="flex items-center gap-2",
    )