import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

__author__ = 'fhca'

import tkinter as tk


def tuplify(x):
    return tuple(x) if isinstance(x, np.ndarray) else x


def choose(iterable, size=()):
    if size:
        z = np.array(iterable)[np.random.choice(np.array(range(len(iterable))), size)]
        if isinstance(size, int):
            return z
        else:
            return [(tuplify(x), tuplify(y)) for x, y in z]
    else:
        return iterable[np.random.choice(range(len(iterable)))]



class Anima:
    def __init__(self):
        self.root = tk.Tk()
        self.toolbar = tk.Frame(self.root)
        self.toolbar.grid()
        self.toolbar.update_idletasks()
        self.toolbar.pack()
        menubar = tk.Menu(self.toolbar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Salir", command=self.root.quit)
        network_menu = tk.Menu(menubar, tearoff=0)
        network_menu.add_command(label="Ciclo", command=self.select_cycle)
        network_menu.add_command(label="Malla", command=self.select_mesh)
        network_menu.add_command(label="Barabasi - Albert", command=self.select_barabasi)

        menubar.add_cascade(label="Archivo", menu=file_menu)
        menubar.add_cascade(label="Red", menu=network_menu)
        self.root.config(menu=menubar)

        self.select_barabasi()
        self.pause = True
        self.ventana()

    def stats(self, kw):
        for name, value in kw.items():
            self.text.insert("end", name+": "+value)

    def select_barabasi(self):
        self.pause = True
        self.G = nx.barabasi_albert_graph(900, 1)
        self.pos = nx.spring_layout(self.G, iterations=40)
        self.pause = False

    def select_mesh(self):
        self.pause = True
        self.G = nx.grid_2d_graph(30, 30)
        self.pos = nx.spectral_layout(self.G)
        self.pause = False

    def select_cycle(self):
        self.pause = True
        self.G = nx.cycle_graph(900)
        self.pos = nx.circular_layout(self.G)
        self.pause = False

    def traffic_randomwalk_sp_pairs_alpha(self, alpha):
        """A pair of nodes is traveled choosing rw and sp selected randomly.
        alpha is the chance to use rw at every step. """
        n = 1
        od = choose(self.G.nodes(), (n, 2))
        #diameter = nx.diameter(self.G)
        # escoje las n parejas
        for i, (origin, destination) in enumerate(od):
            x = origin
            #sp_length_to_destination = nx.shortest_path_length(self.self.G, destination)
            sp = nx.shortest_path(self.G, target=destination)
            while x != destination:
                # d=float(spl[x])/spl[origin] #escoje con prob proporcional a la distancia que le falta recorrer
                # d=.5
                if np.random.random() < alpha:
                    y = choose(self.G.neighbors(x))  # random walk
                else:
                    y = sp[x][1]  # shortest path
                self.G[x][y]['traffic'] = self.G[x][y].get('traffic', 0) + 1
                x = y

    def pausa(self):
        self.pause = not self.pause
        print("pausa=", self.pause)

    def datos(self):
        yield self.pos

    def pinta(self, pos=0):
        if not self.pause:
            self.traffic_randomwalk_sp_pairs_alpha(alpha=.1)
        self.ax.clear()
        nx.draw_networkx_edges(self.G, self.pos, node_size=0, width=0.5, alpha=1, edge_color='k')
        nx.draw_networkx_nodes(self.G, self.pos, with_labels=False, node_size=10, alpha=1, linewidths=0)
        traffic_list = np.array([d.get('traffic', 0) for _, _, d in self.G.edges(data=True)])
        nx.draw_networkx_edges(self.G, self.pos, width=traffic_list, alpha=.3, edge_color='b')
            #self.canvas.show()
            #self.canvas.get_tk_widget().update_idletasks()

    def makeToolbar(self):
        self.toolbar_text = ['Pausa', 'Reiniciar', 'Estirar', 'Salir']
        self.toolbar_length = len(self.toolbar_text)
        self.toolbar_buttons = [None] * self.toolbar_length

        for toolbar_index, text in enumerate(self.toolbar_text):
            button_id = tk.Button(self.toolbar, text=text)
            button_id.grid(row=0, column=toolbar_index)
            self.toolbar_buttons[toolbar_index] = button_id

            def toolbar_button_handler(event, self=self, button=toolbar_index):
                return self.service_toolbar(button)

            button_id.bind("<Button-1>", toolbar_button_handler)

    # call blink() if start and set stop when stop
    def service_toolbar(self, toolbar_index):
        if toolbar_index == 0:
            self.pause = not self.pause
        elif toolbar_index == 1:
            for (x, y, _) in self.G.edges(data=True):
                self.G[x][y]['traffic'] = 0
            self.pause = False
        elif toolbar_index == 2:
            self.pos = nx.spring_layout(self.G, pos=self.pos, iterations=40)
        elif toolbar_index == 3:
            self.root.quit()

    def ventana(self):
        self.root.wm_title("Modelado computacional de redes complejas")
        self.root.wm_protocol('WM_DELETE_WINDOW', self.root.quit)

        fig = plt.figure(figsize=(10, 10))
        self.ax = plt.axes([0, 0, 1, 1], axisbg='w')
        plt.axis('off')  # borra cuadro
        plt.xticks([])  # borra ticks
        plt.yticks([])

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        animation.FuncAnimation(fig, self.pinta, frames=1, init_func=self.makeToolbar, # crea animación
                                        blit=False, interval=10, repeat_delay=1)
        tk.mainloop()


v = Anima()
