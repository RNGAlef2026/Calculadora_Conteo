import tkinter as tk

from tkinter import ttk, messagebox
from itertools import permutations, combinations
from math import factorial, comb
from collections import Counter

def calcular():
    objetos = [objeto.strip() for objeto in entrada.get().split(",")]

    if not all(objetos):
        messagebox.showwarning(
            "Revisar entrada",
            "Escribe objetos separados por comas. Ejemplo: a, b, c, d"
        )
        return

    if len(objetos) > 7:
        messagebox.showwarning(
            "Demasiados objetos",
            "Utiliza un máximo de 7 objetos en esta versión."
        )
        return

    n = len(objetos)
    frecuencias = Counter(objetos)
    hay_repetidos = any(valor > 1 for valor in frecuencias.values())
    operacion = selector.get()

    requiere_diferentes = operacion in (
        "Permutaciones de objetos diferentes",
        "Combinaciones de objetos diferentes"
    )

    if requiere_diferentes and hay_repetidos:
        messagebox.showwarning(
            "Objetos repetidos",
            "Esta operación requiere que todos los objetos sean diferentes."
        )
        return

    if operacion == "Permutaciones de objetos diferentes":
        total = factorial(n)
        formula = f"{n}!"
        soluciones = permutations(objetos)
        tipo = "permutaciones"

    elif operacion == "Permutaciones de objetos iguales":
        denominador = 1
        factores = []

        for frecuencia in frecuencias.values():
            denominador *= factorial(frecuencia)

            if frecuencia > 1:
                factores.append(f"{frecuencia}!")

        total = factorial(n) // denominador
        formula = (
            f"{n}! / ({' × '.join(factores)})"
            if factores
            else f"{n}!"
        )
        soluciones = sorted(set(permutations(objetos)))
        tipo = "permutaciones"

    elif operacion in (
        "Combinaciones de objetos diferentes",
        "Combinaciones de objetos iguales"
    ):
        try:
            r = int(cantidad.get())
        except ValueError:
            messagebox.showwarning(
                "Cantidad inválida",
                "La cantidad a seleccionar debe ser un número entero."
            )
            return

        if not 0 <= r <= n:
            messagebox.showwarning(
                "Cantidad fuera de rango",
                f"La cantidad a seleccionar debe estar entre 0 y {n}."
            )
            return

        if operacion == "Combinaciones de objetos diferentes":
            total = comb(n, r)
            formula = f"C({n}, {r})"
            soluciones = combinations(objetos, r)
        else:
            # Ordenar cada selección permite reconocer combinaciones iguales,
            # incluso si los objetos se escriben en otro orden.
            # Solo se usan las copias disponibles en la entrada.
            soluciones = sorted({
                tuple(sorted(seleccion))
                for seleccion in combinations(objetos, r)
            })
            total = len(soluciones)
            formula = "selecciones únicas"

        tipo = "combinaciones"

    else:
        messagebox.showwarning(
            "Operación inválida",
            "Selecciona una operación de la lista."
        )
        return

    etiqueta_total.config(text=str(total))
    etiqueta_detalle.config(text=f"{tipo.capitalize()} · {formula}")

    resultados.config(state="normal")
    resultados.delete("1.0", tk.END)

    for numero, solucion in enumerate(soluciones, start=1):
        resultados.insert(
            tk.END,
            f"{numero}.  ({', '.join(solucion)})\n"
        )

    resultados.config(state="disabled")
    boton_copiar.config(state="normal")
    estado.config(text="Cálculo completado. Cada fila muestra un resultado único.")

# Diseño de la interfaz. Los cálculos están en la función calcular().
AZUL = "#2858C7"
FONDO = "#F2F5FB"
TEXTO = "#1D2942"
SECUNDARIO = "#63718B"
BORDE = "#DCE3EF"

DESCRIPCIONES = {
    "Permutaciones de objetos diferentes":
        "El orden importa. Se usan todos los objetos y ninguno se repite.",
    "Permutaciones de objetos iguales":
        "El orden importa. Los arreglos que solo intercambian copias iguales cuentan una vez.",
    "Combinaciones de objetos diferentes":
        "El orden no importa. Selecciona una cantidad de objetos diferentes.",
    "Combinaciones de objetos iguales":
        "El orden no importa. Solo puedes usar las copias disponibles de cada objeto."
}


def borrar_resultados(*args):
    """Evita que un resultado anterior parezca corresponder a datos nuevos."""
    etiqueta_total.config(text="—")
    etiqueta_detalle.config(text="Ingresa tus datos y pulsa Calcular.")
    resultados.config(state="normal")
    resultados.delete("1.0", tk.END)
    resultados.config(state="disabled")
    boton_copiar.config(state="disabled")
    estado.config(text="Listo para calcular · Máximo 7 objetos.")


def actualizar_cantidad(event=None):
    operacion = selector.get()
    es_combinacion = operacion.startswith("Combinaciones")
    cantidad.config(state="normal" if es_combinacion else "disabled")
    ayuda_cantidad.config(text=(
        "Indica cuántos objetos seleccionar (de 0 al total)."
        if es_combinacion else "Se utilizarán todos los objetos."
    ))
    descripcion.config(text=DESCRIPCIONES[operacion])
    borrar_resultados()


def cargar_ejemplo():
    """Carga el ejemplo de clase correspondiente a la operación elegida."""
    texto_objetos.set(
        "a, a, b, c" if "iguales" in selector.get() else "a, b, c, d"
    )
    texto_cantidad.set("2")
    entrada.focus_set()
    estado.config(text="Ejemplo cargado. Pulsa Calcular para ver sus resultados.")


def limpiar():
    texto_objetos.set("")
    borrar_resultados()
    entrada.focus_set()


def copiar_resultados():
    contenido = resultados.get("1.0", "end-1c").strip()
    if not contenido:
        return
    resumen = (
        f"{selector.get()}\nObjetos: {texto_objetos.get()}\n"
        f"Total: {etiqueta_total.cget('text')}\n"
    )
    if selector.get().startswith("Combinaciones"):
        resumen += f"Cantidad seleccionada: {texto_cantidad.get()}\n"
    ventana.clipboard_clear()
    ventana.clipboard_append(resumen + "\n" + contenido)
    estado.config(text="Resultados copiados al portapapeles.")


ventana = tk.Tk()
ventana.title("Conteo | Permutaciones y combinaciones")
ventana.geometry("850x850")
ventana.minsize(720, 760)
ventana.configure(background=FONDO)

estilo = ttk.Style(ventana)
estilo.theme_use("clam")
estilo.configure("TFrame", background=FONDO)
estilo.configure("Card.TFrame", background="white")
estilo.configure("TLabel", background=FONDO, foreground=TEXTO,
                 font=("Segoe UI", 10))
estilo.configure("Card.TLabel", background="white")
estilo.configure("Section.TLabel", background="white", foreground=TEXTO,
                 font=("Segoe UI", 12, "bold"))
estilo.configure("Muted.TLabel", background="white", foreground=SECUNDARIO,
                 font=("Segoe UI", 10))
estilo.configure("TEntry", padding=9, fieldbackground="white")
estilo.configure("TCombobox", padding=8, fieldbackground="white")
estilo.map("TCombobox", fieldbackground=[("readonly", "white")],
           foreground=[("readonly", TEXTO)])
estilo.configure("TSpinbox", padding=7, fieldbackground="white")
estilo.configure("TButton", padding=(14, 8), font=("Segoe UI", 10),
                 background="#EAF0FB", foreground=AZUL, borderwidth=0)
estilo.map("TButton", background=[("active", "#DCE7FB")],
           foreground=[("disabled", "#929DAF")])
estilo.configure("Primary.TButton", background=AZUL, foreground="white",
                 font=("Segoe UI", 10, "bold"))
estilo.map("Primary.TButton", background=[("active", "#2048A6")],
           foreground=[("active", "white")])
ventana.option_add("*TCombobox*Listbox.font", ("Segoe UI", 11))

contenedor = ttk.Frame(ventana, padding=24)
contenedor.pack(fill="both", expand=True)
contenedor.columnconfigure(0, weight=1)
contenedor.rowconfigure(3, weight=1)

cabecera = ttk.Frame(contenedor)
cabecera.grid(row=0, column=0, sticky="ew", pady=(0, 18))
ttk.Label(cabecera, text="MATEMÁTICA DISCRETA", foreground=AZUL,
          font=("Segoe UI", 9, "bold")).pack(anchor="w")
ttk.Label(cabecera, text="Calculadora de conteo",
          font=("Segoe UI", 25, "bold")).pack(anchor="w", pady=(3, 4))
ttk.Label(cabecera, text="Explora las formas de ordenar y seleccionar objetos.",
          foreground=SECUNDARIO).pack(anchor="w")

configuracion = ttk.Frame(contenedor, style="Card.TFrame", padding=20)
configuracion.grid(row=1, column=0, sticky="ew")
configuracion.columnconfigure(0, weight=1)
ttk.Label(configuracion, text="01   Configura tu cálculo",
          style="Section.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 12))
ttk.Label(configuracion, text="Operación", style="Card.TLabel").grid(
    row=1, column=0, sticky="w", pady=(0, 5))
selector = ttk.Combobox(configuracion, values=list(DESCRIPCIONES),
                        state="readonly", font=("Segoe UI", 11))
selector.grid(row=2, column=0, sticky="ew")
selector.current(0)

descripcion = ttk.Label(configuracion, style="Muted.TLabel", wraplength=650)
descripcion.grid(row=3, column=0, sticky="ew", pady=(8, 14))

ttk.Label(configuracion, text="Objetos separados por comas",
          style="Card.TLabel").grid(row=4, column=0, sticky="w", pady=(0, 5))
texto_objetos = tk.StringVar(value="a, b, c, d")
entrada = ttk.Entry(configuracion, textvariable=texto_objetos,
                    font=("Segoe UI", 12))
entrada.grid(row=5, column=0, sticky="ew")
ttk.Label(configuracion, text="Puedes escribir letras, números o palabras. Máximo 7 objetos.",
          style="Muted.TLabel").grid(row=6, column=0, sticky="w", pady=(5, 12))

controles = ttk.Frame(configuracion, style="Card.TFrame")
controles.grid(row=7, column=0, sticky="ew")
controles.columnconfigure(1, weight=1)
ttk.Label(controles, text="Cantidad a seleccionar", style="Card.TLabel").grid(
    row=0, column=0, sticky="w", padx=(0, 12))
texto_cantidad = tk.StringVar(value="2")
cantidad = ttk.Spinbox(controles, from_=0, to=7, width=5,
                       textvariable=texto_cantidad, font=("Segoe UI", 11))
cantidad.grid(row=0, column=1, sticky="w")
ayuda_cantidad = ttk.Label(configuracion, style="Muted.TLabel")
ayuda_cantidad.grid(row=8, column=0, sticky="w", pady=(5, 12))

acciones = ttk.Frame(configuracion, style="Card.TFrame")
acciones.grid(row=9, column=0, sticky="ew")
ttk.Button(acciones, text="Calcular", style="Primary.TButton",
           command=calcular).pack(side="left", padx=(0, 8))
ttk.Button(acciones, text="Cargar ejemplo", command=cargar_ejemplo).pack(
    side="left", padx=(0, 8))
ttk.Button(acciones, text="Limpiar", command=limpiar).pack(side="left")

resumen = tk.Frame(contenedor, background="#E6EEFF", padx=16, pady=4)
resumen.grid(row=2, column=0, sticky="ew", pady=6)
etiqueta_total = tk.Label(resumen, text="—", background="#E6EEFF",
                           foreground=AZUL, font=("Segoe UI", 16, "bold"))
etiqueta_total.pack(side="left", padx=(0, 12))
etiqueta_detalle = tk.Label(resumen, background="#E6EEFF", foreground=TEXTO,
                            font=("Segoe UI", 11), anchor="w", wraplength=520)
etiqueta_detalle.pack(side="left", fill="x", expand=True)

panel_resultados = ttk.Frame(contenedor, style="Card.TFrame", padding=16)
panel_resultados.grid(row=3, column=0, sticky="nsew")
panel_resultados.columnconfigure(0, weight=1)
panel_resultados.rowconfigure(1, weight=1)
ttk.Label(panel_resultados, text="02   Resultados",
          style="Section.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))
boton_copiar = ttk.Button(panel_resultados, text="Copiar resultados",
                          command=copiar_resultados, state="disabled")
boton_copiar.grid(row=0, column=1, sticky="e", pady=(0, 10))

marco_resultados = ttk.Frame(panel_resultados, style="Card.TFrame")
marco_resultados.grid(row=1, column=0, columnspan=2, sticky="nsew")
marco_resultados.columnconfigure(0, weight=1)
marco_resultados.rowconfigure(0, weight=1)
resultados = tk.Text(marco_resultados, height=5, font=("Consolas", 11),
                     background="white", foreground=TEXTO, relief="flat",
                     highlightthickness=1, highlightbackground=BORDE,
                     padx=12, pady=10, spacing1=3, wrap="none", state="disabled")
resultados.grid(row=0, column=0, sticky="nsew")
barra = ttk.Scrollbar(marco_resultados, orient="vertical", command=resultados.yview)
barra.grid(row=0, column=1, sticky="ns")
barra_horizontal = ttk.Scrollbar(marco_resultados, orient="horizontal",
                                 command=resultados.xview)
barra_horizontal.grid(row=1, column=0, sticky="ew")
resultados.config(yscrollcommand=barra.set, xscrollcommand=barra_horizontal.set)

estado = ttk.Label(contenedor, foreground=SECUNDARIO, font=("Segoe UI", 9))
estado.grid(row=4, column=0, sticky="w", pady=(10, 0))

texto_objetos.trace_add("write", borrar_resultados)
texto_cantidad.trace_add("write", borrar_resultados)
selector.bind("<<ComboboxSelected>>", actualizar_cantidad)
ventana.bind("<Return>", lambda event: calcular())
actualizar_cantidad()
entrada.focus_set()
ventana.mainloop()
