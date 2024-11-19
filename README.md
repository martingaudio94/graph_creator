# graph_creator

**Este sistema fue creado para generar sistemas de grafos para poder integrar lógica algorítmica en forma de árbol dentro de los prompts de los LLM actuales, la manera en la cual se implementen los grafos dentro de la memoria o la toma de decisiones por medio de estados actuales del sistema no son parte de este proyecto (por ahora). El sistema implementado esta probado y funciona en la mayoría de los casos para proveer contexto en la toma de decisiones del chatbot.**

## Requisitos
* python3.x
* tkinter(generalmente viene instalado con python)
  
**El sistema cuenta :**
* Creacion de nodos.
* Eliminacion de nodos.
* Creacion de conexiones entre nodos.
* Guardado y carga de datos para poder seguir creacion el grafo.
* Guardado para AI para guardar la informacion y conexiones entre nodos para ingresar los datos a los prompts.

#### Creacion de nodos
* Utilizando boton izquierdo sobre la pantalla , te pedira informacion del nodo (por ejemplo el usuario debe ingresar su email), aceptamos y se creara el nodo, si cancelamos no se creara el nodo.
  ![image](https://github.com/user-attachments/assets/f5eb36a3-54e9-4f6e-9dfb-03afac1954d5)
#### Eliminacion de nodos.
* Utilizando el boton derecho sobre un nodo, saldra un menu desplegable , elejimos la opcion "Eliminar nodo".
  ![image](https://github.com/user-attachments/assets/af2241c0-292c-4b28-b5bb-6ff0409fbfbc)
#### Creacion de conexion entre nodos.
* Utilizando el boton derecho del mouse encima del nodo padre utilizaremos la opcion "Conectar nodo" luego seleccionaremos el nodo hijo con el boton derecho del mouse y utilizaremos la opcion "Terminar conexion"
  ![image](https://github.com/user-attachments/assets/e149f7a1-8af7-4527-bf68-e41d43bc2789)

