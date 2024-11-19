import tkinter as tk
from tkinter import simpledialog, messagebox
import json

# Estructuras para nodos y conexiones
nodes = []
edges = []

# Variable para guardar el nodo seleccionado para conectar
node_to_connect = None

# Crear ventana principal
root = tk.Tk()
root.title("Creador de Grafos")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Menú contextual para nodos
node_menu = tk.Menu(root, tearoff=0)

def inser_node(x,y,node_id,infor=False):
    # Solicitar información adicional
    crear = False
    if infor:
        info = infor
        crear = True
    else:
        info = simpledialog.askstring("Información del nodo", f"Ingresa información para el nodo {node_id}:")
        if info:
            crear = True
    if crear:
        # Crear nodo
        if shape == "circle":
            node = {"id": node_id, "type": "circle", "x": x, "y": y, "info": info}
            canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue", tags=f"node_{node_id}")
        elif shape == "square":
            node = {"id": node_id, "type": "square", "x": x, "y": y, "info": info}
            canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill="lightgreen", tags=f"node_{node_id}")

        # Añadir texto con ID del nodo
        canvas.create_text(x, y, text=f"{node_id}", tags=f"node_{node_id}")

        nodes.append(node)

# Función para crear nodos
def create_node(event, shape="circle"):
    node_id = len(nodes) + 1
    x, y = event.x, event.y
    inser_node(x,y,node_id)

def get_node(id):
    node = [x for x in nodes if x.get("id")==id]
    return node[0]
    
def load_nodes(data="graph.json"):
    try:
        nodes=[]
        edges=[]
        
        with open(data, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        for node in datos.get("nodes"):
            inser_node(node.get("x"),node.get("y"),node.get("id"),node.get("info"))

        for connections in datos.get("edges"):
            from_n = get_node(connections.get("from"))
            to_n = get_node(connections.get("to"))
            create_conections(from_n,to_n)
        messagebox.showinfo("Cargar datos", "Se cargaron los datos correctamente")
        
    except Exception as e:
        #No se pudieron cargar los datos, verificar la existencia de graph.json
        messagebox.showerror("Cargar datos", f"{e}")
# Función para conectar nodos con flechas
def start_connection():
    global node_to_connect
    if node_to_connect:
        messagebox.showinfo("Conectar nodo", "Ya hay un nodo seleccionado para conectar.")
    else:
        node_to_connect = current_node
        messagebox.showinfo("Conectar nodo", f"Seleccionado nodo {node_to_connect['id']} para conectar.")

def finish_connection():
    global node_to_connect
    if node_to_connect:
        if node_to_connect == current_node:
            messagebox.showerror("Error", "No puedes conectar un nodo consigo mismo.")
        else:
            create_conections(node_to_connect,current_node)
            messagebox.showinfo("Conexión", f"Nodo {node_to_connect['id']} conectado al nodo {current_node['id']}.")
        node_to_connect = None
    else:
        messagebox.showerror("Error", "Primero selecciona un nodo inicial para conectar.")

def create_conections(node_to_connect,current_node):
    # Crear conexión
    edges.append({"from": node_to_connect["id"], "to": current_node["id"]})
    canvas.create_line(
        node_to_connect["x"], node_to_connect["y"],
        current_node["x"], current_node["y"],
        arrow=tk.LAST, fill="black", width=2,
        tags=f"edge_{node_to_connect['id']}_{current_node['id']}"
    )

# Función para eliminar un nodo y sus conexiones
def delete_node():
    global node_to_connect, current_node
    if current_node:
        node_id = current_node["id"]

        # Eliminar nodo de la lista
        nodes[:] = [node for node in nodes if node["id"] != node_id]

        # Eliminar conexiones relacionadas
        related_edges = [edge for edge in edges if edge["from"] == node_id or edge["to"] == node_id]
        for edge in related_edges:
            edges.remove(edge)
            canvas.delete(f"edge_{edge['from']}_{edge['to']}")

        # Eliminar nodo del canvas
        canvas.delete(f"node_{node_id}")

        # Si el nodo eliminado estaba seleccionado para conectar, limpiarlo
        if node_to_connect and node_to_connect["id"] == node_id:
            node_to_connect = None

        current_node = None

# Función para guardar en JSON
def save_to_json():
    graph_data = {"nodes": nodes, "edges": edges}
    with open("graph.json", "w") as f:
        json.dump(graph_data, f, indent=4)
    messagebox.showinfo("Guardado", "El grafo se ha guardado en graph.json")

def save_to_json_ai():
    modify_nodes = []
    graph_data = {"nodes": modify_nodes, "edges": edges}
    for node in nodes:
        ex_node = {}
        ex_node["id"] = node.get("id")
        ex_node["info"] = node.get("info")
        modify_nodes.append(ex_node)
        
    with open("graph.json", "w") as f:
        json.dump(graph_data, f, indent=4)
    messagebox.showinfo("Guardado", "El grafo se ha guardado en graph.json")

# Función para cambiar entre círculos y cuadrados
def toggle_shape():
    global shape
    shape = "square" if shape == "circle" else "circle"
    shape_button.config(text=f"Forma: {shape.capitalize()}")

# Evento al hacer clic derecho
current_node = None  # Nodo bajo el clic derecho

def on_right_click(event):
    global current_node
    x, y = event.x, event.y

    # Detectar si se hizo clic en un nodo
    clicked_node = None
    for node in nodes:
        if (node["x"] - 20 <= x <= node["x"] + 20) and (node["y"] - 20 <= y <= node["y"] + 20):
            clicked_node = node
            break

    if clicked_node:
        current_node = clicked_node
        # Configurar el menú contextual
        node_menu.delete(0, tk.END)
        node_menu.add_command(label="Conectar nodo", command=lambda: start_connection())
        node_menu.add_command(label="Terminar conexión", command=lambda: finish_connection())
        node_menu.add_command(label="Eliminar nodo", command=lambda: delete_node())
        node_menu.post(event.x_root, event.y_root)

# Bindings de eventos
canvas.bind("<Button-1>", lambda event: create_node(event, shape))
canvas.bind("<Button-3>", on_right_click)

# Botón para guardar
save_button = tk.Button(root, text="Guardar Data", command=save_to_json)
save_button.pack(side=tk.LEFT)

#Guardar data para AI
save_ai = tk.Button(root, text="Guardar para AI", command=save_to_json_ai)
save_ai.pack(side=tk.LEFT)
# Botón para cambiar forma
shape = "circle"
shape_button = tk.Button(root, text="Forma: Círculo", command=toggle_shape)
shape_button.pack(side=tk.LEFT)

#Boton para cargar datos
load_button = tk.Button(root, text="Cargar data", command=load_nodes)
load_button.pack(side=tk.LEFT)

# Loop principal
root.mainloop()
