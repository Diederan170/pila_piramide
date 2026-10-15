import tkinter as tk
from tkinter import messagebox


class PilaPiramideApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Visualizador Gráfico de Pila en Pirámide")
    self.root.geometry("850x650")
    self.root.config(bg="#1e1e1e")

    self.pila = []
    self.max_elementos = 15  # Capacidad máxima para la estructura piramidal

    self.crear_widgets()

  def crear_widgets(self):
    # Panel de control superior
    control_frame = tk.Frame(self.root, bg="#2d2d2d", pady=10)
    control_frame.pack(fill=tk.X, padx=20, pady=20)

    tk.Label(
        control_frame,
        text="Elemento:",
        bg="#2d2d2d",
        fg="white",
        font=("Arial", 11, "bold"),
    ).pack(side=tk.LEFT, padx=5)

    self.entry_valor = tk.Entry(control_frame, font=("Arial", 11), width=18)
    self.entry_valor.pack(side=tk.LEFT, padx=5)
    self.entry_valor.bind("<Return>", lambda event: self.apilar())

    btn_push = tk.Button(
        control_frame,
        text="Apilar (Push)",
        command=self.apilar,
        bg="#007acc",
        fg="white",
        font=("Arial", 10, "bold"),
        relief=tk.FLAT,
        padx=10,
    )
    btn_push.pack(side=tk.LEFT, padx=5)

    btn_pop = tk.Button(
        control_frame,
        text="Desapilar (Pop)",
        command=self.desapilar,
        bg="#cc3333",
        fg="white",
        font=("Arial", 10, "bold"),
        relief=tk.FLAT,
        padx=10,
    )
    btn_pop.pack(side=tk.LEFT, padx=5)

    btn_limpiar = tk.Button(
        control_frame,
        text="Limpiar Pila",
        command=self.limpiar_pila,
        bg="#555555",
        fg="white",
        font=("Arial", 10, "bold"),
        relief=tk.FLAT,
        padx=10,
    )
    btn_limpiar.pack(side=tk.LEFT, padx=5)

    # Lienzo (Canvas) para renderizar la pirámide
    self.canvas = tk.Canvas(self.root, bg="#1e1e1e", highlightthickness=0)
    self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Barra de estado inferior
    self.lbl_estado = tk.Label(
        self.root,
        text="Pila vacía. Elementos: 0 / 15",
        bg="#1e1e1e",
        fg="#00ffcc",
        font=("Arial", 12, "bold"),
    )
    self.lbl_estado.pack(pady=15)

  def apilar(self):
    valor = self.entry_valor.get().strip()
    if not valor:
      messagebox.showwarning(
          "Advertencia", "Debe ingresar un valor válido para apilar."
      )
      return
    if len(self.pila) >= self.max_elementos:
      messagebox.showerror(
          "Límite alcanzado",
          f"La estructura piramidal ha alcanzado su máximo de"
          f" {self.max_elementos} elementos.",
      )
      return

    self.pila.append(valor)
    self.entry_valor.delete(0, tk.END)
    self.actualizar_dibujo()

  def desapilar(self):
    if not self.pila:
      messagebox.showwarning("Advertencia", "La pila se encuentra vacía.")
      return

    self.pila.pop()
    self.actualizar_dibujo()

  def limpiar_pila(self):
    self.pila.clear()
    self.actualizar_dibujo()

  def actualizar_dibujo(self):
    self.canvas.delete("all")
    total = len(self.pila)
    self.lbl_estado.config(
        text=f"Elementos en Pila: {total} / {self.max_elementos}"
    )

    if total == 0:
      self.canvas.create_text(
          425,
          250,
          text="Pila Vacía (Estructura Piramidal)",
          fill="#777777",
          font=("Arial", 16, "italic"),
      )
      return

    # Lógica de distribución en filas para formar la pirámide
    # Fila 1 (Cúspide): 1 elemento, Fila 2: 2 elementos, Fila 3: 3 elementos, etc.
    elementos = list(self.pila)
    idx = 0
    fila = 1
    ancho_bloque = 70
    alto_bloque = 45
    espacio = 8
    centro_x = 425
    inicio_y = 40

    while idx < total:
      elems_en_fila = fila
      fila_elementos = []

      for _ in range(elems_en_fila):
        if idx < total:
          fila_elementos.append(elementos[idx])
          idx += 1
        else:
          break

      ancho_total_fila = (
          len(fila_elementos) * ancho_bloque
          + (len(fila_elementos) - 1) * espacio
      )
      inicio_x = centro_x - (ancho_total_fila / 2)

      for i, val in enumerate(fila_elementos):
        x1 = inicio_x + i * (ancho_bloque + espacio)
        y1 = inicio_y + (fila - 1) * (alto_bloque + espacio)
        x2 = x1 + ancho_bloque
        y2 = y1 + alto_bloque

        # Identificar si es el tope exacto de la pila (último elemento insertado)
        es_tope = (
            idx == total
            and i == len(fila_elementos) - 1
            and fila == self.calcular_fila_actual(total)
        )

        if es_tope:
          color_bg = "#ff5555"  # Color distintivo para el tope (Top of Stack)
          borde_color = "#ffffff"
          ancho_borde = 3
        else:
          color_bg = "#2e7d32"  # Color para elementos estáticos de la pila
          borde_color = "#81c784"
          ancho_borde = 1

        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=color_bg,
            outline=borde_color,
            width=ancho_borde,
        )
        self.canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text=str(val),
            fill="white",
            font=("Arial", 11, "bold"),
        )

      fila += 1

  def calcular_fila_actual(self, n):
    # Calcula en qué número de fila se encuentra el último elemento insertado
    f = 1
    acumulado = 0
    while acumulado < n:
      acumulado += f
      if acumulado >= n:
        return f
      f += 1
    return f


if __name__ == "__main__":
  root = tk.Tk()
  app = PilaPiramideApp(root)
  root.mainloop()