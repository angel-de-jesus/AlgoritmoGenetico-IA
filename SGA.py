import numpy as np
import matplotlib.pyplot as plt
import random
from random import randrange
from tkinter import ttk
import tkinter as tk
from tkinter import IntVar, Tk, messagebox


class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("SGA")
        self.raiz.geometry("950x400")
        self.raiz.resizable(0, 0)
        self.LONG_CROMOSOMA = 8
        self.N_GENERATIONS = IntVar()
        self.POP_SIZE = IntVar()
        self.MINX = IntVar()
        self.MAXX = IntVar()
        self.MINY = IntVar()
        self.MAXY = IntVar()
        self.MINZ = IntVar()
        self.MAXZ = IntVar()
        self.CROSS_RATE = 0.7
        self.MUTATION_RATE = 0.125
        self.CROSS_POINT = 2

        self.etiq1 = ttk.Label(self.raiz, text="Numero de Generaciones:")

        self.etiq2 = ttk.Label(self.raiz, text="Tamaño de poblacion:")

        self.etiq3 = ttk.Label(self.raiz, text="Min x:")

        self.etiq4 = ttk.Label(self.raiz, text="Max x:")

        self.etiq5 = ttk.Label(self.raiz, text="Min y:")

        self.etiq6 = ttk.Label(self.raiz, text="Max y:")

        self.etiq7 = ttk.Label(self.raiz, text="Min z:")

        self.etiq8 = ttk.Label(self.raiz, text="Max z:")

        self.ctext1 = ttk.Entry(self.raiz,
                                textvariable=self.N_GENERATIONS,
                                width=30)
        self.ctext2 = ttk.Entry(self.raiz,
                                textvariable=self.POP_SIZE,
                                width=30)

        self.ctext3 = ttk.Entry(self.raiz,
                                textvariable=self.MINX,
                                width=30)

        self.ctext4 = ttk.Entry(self.raiz,
                                textvariable=self.MAXX,
                                width=30)

        self.ctext5 = ttk.Entry(self.raiz,
                                textvariable=self.MINY,
                                width=30)

        self.ctext6 = ttk.Entry(self.raiz,
                                textvariable=self.MAXY,
                                width=30)

        self.ctext7 = ttk.Entry(self.raiz,
                                textvariable=self.MINZ,
                                width=30)

        self.ctext8 = ttk.Entry(self.raiz,
                                textvariable=self.MAXZ,
                                width=30)

        self.boton1 = ttk.Button(self.raiz, text="Iniciar",
                                 command=self.init_)
        self.etiq1.place(x=0, y=0)
        self.ctext1.place(x=150, y=0)
        self.etiq2.place(x=0, y=50)
        self.ctext2.place(x=150, y=50)
        self.etiq3.place(x=0, y=100)
        self.ctext3.place(x=150, y=100)
        self.etiq4.place(x=0, y=150)
        self.ctext4.place(x=150, y=150)
        self.etiq5.place(x=0, y=200)
        self.ctext5.place(x=150, y=200)
        self.etiq6.place(x=0, y=250)
        self.ctext6.place(x=150, y=250)
        self.etiq7.place(x=0, y=300)
        self.ctext7.place(x=150, y=300)
        self.etiq8.place(x=0, y=350)
        self.ctext8.place(x=150, y=350)
        self.boton1.place(x=400, y=350)
        self.raiz.mainloop()

    def init_(self):
        if(self.N_GENERATIONS.get() > 0 and self.POP_SIZE.get() > 0):
            valor = init_app(self)
            self.showData(valor)
        else:
            messagebox.showinfo(
                message="Numero de generaciones o tamaño de poblacion no permitadas", title="No valido")
        return 0

    def showData(self, valor):
        self.treeview = ttk.Treeview(
            self.raiz, columns=("cro", "idv", "best", "worts", "average"))
        self.treeview.column("#0", width=80, anchor="center")
        self.treeview.column("cro", width=120, anchor="center")
        self.treeview.column("idv", width=80, anchor="center")
        self.treeview.column("best", width=100, anchor="center")
        self.treeview.column("worts", width=100, anchor="center")
        self.treeview.column("average", width=100, anchor="center")
        self.treeview.heading("#0", text="Generacion")
        self.treeview.heading("cro", text="Cromosoma mejor individuo")
        self.treeview.heading("idv", text="individuo")
        self.treeview.heading("best", text="Mejor caso")
        self.treeview.heading("worts", text="Peor caso")
        self.treeview.heading("average", text="Caso promedio")
        for j in range(0, len(valor[1])):
            self.treeview.insert("", tk.END, text=str(valor[2][j]), values=(
                valor[0][j], valor[1][j], valor[3][j], valor[4][j], valor[5][j]))
        self.treeview.place(x=350, y=100)
        # GRAFICAR
        plt.xlabel('Generación')
        plt.title('Evolución del fitness')
        plt.plot(valor[2], valor[3], markerfacecolor='blue',
                 markersize=6, color='skyblue', linewidth=3, label='-Mejor caso')
        plt.plot(valor[2], valor[4], markerfacecolor='red',
                 markersize=6, color='#be2f35', linewidth=3, label='-Peor caso')
        plt.plot(valor[2], valor[5], markerfacecolor='green',
                 markersize=6, color='#b2dab2', linewidth=3, label='-Caso promedio')
        plt.legend(bbox_to_anchor=(1, 1),
                   loc='upper left', borderaxespad=0.)
        plt.show()


def fitness(genotipoX, y, z):
    x = translateCromosoma(genotipoX)
    return abs((pow(x, 2)*np.sin(y))/(pow(z, 2)))


def select(app, population, value_y_population, value_z_population, fitness_):
    id = np.random.choice(np.arange(app.POP_SIZE.get()), size=app.POP_SIZE.get(), replace=True,
                          p=fitness_/sum(fitness_))
    x = np.array(population)
    y = np.array(value_y_population)
    z = np.array(value_z_population)
    return x[id], y[id], z[id]


def crossover(app, population_select):
    valor1 = ""
    valor2 = ""
    a = 0
    b = 1
    hijo1 = ""
    hijo2 = ""
    resultado_cross = []
    for i in range(0, int(len(population_select[0])/2)if len(population_select[0]) % 2 == 0 else int((len(population_select[0])-1)/2)):
        valor1 = population_select[0][a]
        valor2 = population_select[0][b]
        fitness_parent1 = fitness(
            valor1, population_select[1][a], population_select[2][a])
        fitness_parent2 = fitness(
            valor2, population_select[1][b], population_select[2][b])
        if np.random.rand() <= app.CROSS_RATE:
            for j in range(0, app.CROSS_POINT):
                hijo1 = hijo1+str(valor1[j])
                hijo2 = hijo2+str(valor2[j])
            for y in range(app.CROSS_POINT, len(valor1)):
                hijo1 = hijo1+str(valor2[y])
                hijo2 = hijo2+str(valor1[y])
            aux = evaluarBinarioX(app, hijo1)
            aux2 = evaluarBinarioX(app, hijo2)
            # Evalua si el fitness del padre es mejor que el del hijo, si es asi entonces se conserva el padre
            # En caso de que el hijo tenga un mejor fitness se  evalua si el valor no supero el rango de x
            # Si no se supera el rango, se conserva el hijo en caso contrario el padre
            if fitness_parent1 > fitness(hijo1, population_select[1][a], population_select[2][a]):
                resultado_cross.append(bin_convert(valor1))
            elif aux == True:
                resultado_cross.append(bin_convert(hijo1))
            else:
                resultado_cross.append(bin_convert(valor1))
            if fitness_parent2 > fitness(hijo2, population_select[1][b], population_select[2][b]):
                resultado_cross.append(bin_convert(valor2))
            elif aux2 == True:
                resultado_cross.append(bin_convert(hijo2))
            else:
                resultado_cross.append(bin_convert(valor2))
            a += 2
            b += 2
        else:
            # Se conservan los individuos cuando no se cruzan
            resultado_cross.append(bin_convert(valor1))
            resultado_cross.append(bin_convert(valor2))
            a += 2
            b += 2
        hijo1 = ""
        hijo2 = ""
    if len(population_select[0]) % 2 == 0:
        pass
    else:
        # Si el numero de individuos es impar el ultimo individuo simplemente se copia
        resultado_cross.append(population_select[0][len(population_select)-1])
    return resultado_cross


def bin_convert(list_indiv):
    bits = ""
    bitSeparado = []
    list_bits = []
    bits = list_indiv
    for i in range(0, len(bits)):
        bitSeparado.insert(i, int(bits[i]))
    list_bits.insert(i, bitSeparado)
    return list_bits[0]


def mutate(app, child):
    mutaciones = []
    mutados = ""
    for i in range(0, len(child)):
        for j in range(0, len(child[i])):
            if np.random.rand() <= app.MUTATION_RATE:
                if child[i][j] == 0:
                    mutados = mutados+'1'
                else:
                    mutados = mutados+'0'
            else:
                mutados = mutados+str(child[i][j])
        # Se evalua si el individuo mutado esta dentro del rango de x, si no es asi se conserva el padre
        aux2 = evaluarBinarioX(app, bin_convert(mutados))
        if aux2 == False:
            mutaciones.append(child[i])
        else:
            mutaciones.append(bin_convert(mutados))
        mutados = ""
    return mutaciones


def evaluarBinarioX(app, individuo):
    valor = False
    if translateCromosoma(individuo) > app.MINX.get() and translateCromosoma(individuo) < app.MAXX.get():
        valor = True
    else:
        valor = False
    return valor


def translateCromosoma(population): return (
    int(''.join(map(str, population)), 2))


value_y_population = []
value_z_population = []


def init_population(app):
    population = []
    global value_y_population
    global value_z_population
    stop = 0
    while stop != app.POP_SIZE.get():
        aux = np.random.randint(2, size=(1, app.LONG_CROMOSOMA))
        if evaluarBinarioX(app, aux[0]) == True:
            population.append(aux[0])
            value_y_population.append(
                randrange(app.MINY.get(), app.MAXY.get()))
            value_z_population.append(
                randrange(app.MINZ.get(), app.MAXZ.get()))
            stop = stop + 1
    stop = 0
    return population


def main():
    Aplicacion()
    return 0


def init_app(app):
    mejor_fitness = []
    prom_fitness = []
    peor_fitness = []
    generacion = []
    best_child_cromosoma = []
    best_child_int = []
    population = init_population(app)
    for _ in range(app.N_GENERATIONS.get()):
        print(f'\nGeneracion {_+1}')
        generacion.append(_+1)
        fitness_ = [fitness(population[i], value_y_population[i],
                            value_z_population[i]) for i in range(len(population))]

        print(f'Mejor fitness: {np.amax(fitness_)}')
        mejor_fitness.append(np.amax(fitness_))
        best_child_cromosoma.append(population[np.argmax(fitness_)])
        best_child_int.append(translateCromosoma(
            population[np.argmax(fitness_)]))
        print(f'Peor fitness: {np.amin(fitness_)}')
        peor_fitness.append(np.amin(fitness_))
        print(f'Fitness promedio: {sum(fitness_)/len(fitness_)}')
        prom_fitness.append(sum(fitness_)/len(fitness_))

        population_select = select(
            app, population, value_y_population, value_z_population, fitness_)
        child = crossover(app, population_select)

        mutados = mutate(app, child)
        # Se conservan los individuos con mejor fitness
        l = 0
        for idv in mutados:
            if fitness(idv, population_select[1][l], population_select[2][l]) > fitness(population[np.argmin(fitness_)], value_y_population[np.argmin(fitness_)], value_z_population[np.argmin(fitness_)]):
                population[np.argmin(fitness_)] = idv
                value_y_population[np.argmin(
                    fitness_)] = population_select[1][l]
                value_z_population[np.argmin(
                    fitness_)] = population_select[2][l]
            l = l + 1
    return best_child_cromosoma, best_child_int, generacion, mejor_fitness, peor_fitness, prom_fitness


if __name__ == '__main__':
    main()
