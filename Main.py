import copy
from operator import attrgetter, le
from tkinter import *
from tkinter.ttk import Treeview
import matplotlib.pyplot as plt
import tkinter
import random
import xlrd

from Dieta import Producto
from Fitness import Fitness

filePath = "C:\\Users\\matam\\Desktop\\IA\\191209 MATUZ TAMAYO_C2.A1\\Producto.xlsx"
openFile = xlrd.open_workbook(filePath)
sheet = openFile.sheet_by_name("Hoja 1")


listaProducto = []


def CrearGrafica(mejorAptitud, peorAptitud, promedioAptitud):

    plt.plot(mejorAptitud)
    plt.plot(peorAptitud)
    plt.plot(promedioAptitud)
    plt.legend((["Mejor", "Peor", "Promedio"]))
    plt.title("Resultados obtenidos")
    plt.xlabel("Generacion")
    plt.ylabel("Fitness")
    plt.show()


def CrearTabla(
    mejorIndividuo, metaTipo, mejorAptitud, peorAptitud, promedioAptitud, generacion
):
    root = Tk()

    if metaTipo == "C":
        root.title("Resultados de optimización por calorías: ")
    else:
        root.title("Resultados de optimización por calorías: ")

    table = Treeview(
        root, columns=("Nombre", "Calorías", "Proteínas", "Cantidad"), height=30
    )
    table.heading("#0", text="")
    table.column("#0", minwidth=0, width=20, anchor=N, stretch=NO)
    table.heading("Nombre", text="Nombre")
    table.column("Nombre", minwidth=0, width=180, anchor=N, stretch=NO)
    table.heading("Calorías", text="Calorías")
    table.column("Calorías", minwidth=0, width=120, anchor=N, stretch=NO)
    table.heading("Proteínas", text="Proteínas")
    table.column("Proteínas", minwidth=0, width=120, anchor=N, stretch=NO)
    table.heading("Cantidad", text="Cantidad")
    table.column("Cantidad", minwidth=0, width=120, anchor=N, stretch=NO)

    # Adding data
    contador = 0
    for producto in mejorIndividuo.listaProducto:
        if (
            producto.calorias == "CALORIAS"
            or producto.proteinas == "PROTEINAS"
            or producto.cantidad == "CANTIDAD"
        ):
            continue
        else:
            table.insert(
                parent="",
                index="end",
                iid=contador,
                values=(
                    producto.nombre,
                    producto.calorias,
                    producto.proteinas,
                    producto.cantidad,
                ),
            )
            contador += 1
    table.pack()

    canvas = Canvas(root, width=400, height=100)
    canvas.pack()
    textLabel = ""
    if metaTipo == "C":
        textLabel = "Total Calorias: "
    else:
        textLabel = "Total Proteinas: "

    canvas.create_text(100, 10, text=textLabel + str(mejorIndividuo.aptitud))

    CrearGrafica(mejorAptitud, peorAptitud, promedioAptitud)
    root.mainloop()


def CrarListaProducto():
    for i in range(sheet.nrows):
        listaProducto.append(
            Producto(
                sheet.cell_value(i, 0),
                sheet.cell_value(i, 1),
                sheet.cell_value(i, 2),
                0,
            )
        )


def CrearPoblacion(poblacionInicial, meta, tipoMeta):
    totalAptitud = 0
    listaFitness = []
    for i in range(poblacionInicial):
        copia = copy.deepcopy(listaProducto)
        for producto in copia:
            producto.cantidad = random.randint(0, 1)
        listaFitness.append(Fitness(copia, meta, tipoMeta))
        totalAptitud += listaFitness[i].aptitud
    Ruleta(totalAptitud, listaFitness)
    return listaFitness


def ControlAptitud(listaFit):
    totalAptitud = 0
    for aptitud in listaFit:
        totalAptitud += aptitud.aptitud
    return totalAptitud


def Ruleta(totalAptitud, listaFit):
    controlGrafico = 0
    for aptitud in listaFit:
        rangoGraf = []
        rangoGraf.append(controlGrafico)
        porcentaje = (aptitud.aptitud * 100) / totalAptitud
        controlGrafico += porcentaje
        rangoGraf.append(controlGrafico)
        aptitud.ControlPorcentaje(porcentaje)
        aptitud.ControlGrafico(rangoGraf)


def Iniciar(listaFit, generacion, poblacionMax, meta, tipoMeta, poblacionInicial):
    CruzaProb = random.randint(50, 90) / 100
    tamIndividuo = len(listaFit)

    mejorAptitud = []
    peorAptitud = []
    promedioAptitud = []
    listaGeneracion = []

    for i in range(generacion):
        if len(listaFit) == 0:
            listaFit = CrearPoblacion(poblacionInicial, meta, tipoMeta)
        totalFitness = ControlAptitud(listaFit)
        Ruleta(totalFitness, listaFit)
        #!Cruza (Seleccion)
        tamanioPoblacion = len(listaFit)
        probCruza = []
        padreAceptado = []
        for i in range(tamanioPoblacion):
            probCruza.append(random.random() * 100)

        for aptitudes in listaFit:
            for prob in probCruza:
                if prob >= aptitudes.rango[0] and prob <= aptitudes.rango[1]:
                    padreAceptado.append(aptitudes)

        probAparear = []
        pares = int(len(padreAceptado) / 2)
        for i in range(pares):
            probAparear.append(random.randint(0, 100) / 100)

        puntaCruza = random.randint(0, 80)

        contador = 0
        par = 0
        contadorAparear = 0
        parejas = []
        hijos = []
        bandera = True
        for padre in padreAceptado:
            if contador < len(probAparear) - 1:
                if probAparear[contador] <= CruzaProb or (par == 1 and bandera):
                    parejas.append(padre)
                else:
                    bandera = False
                par += 1
                if par == 2 and bandera:
                    padre1 = parejas[contadorAparear]
                    padre2 = parejas[contadorAparear + 1]
                    primerHijo = (
                        ""
                        + padre1.individuo[0:puntaCruza]
                        + padre2.individuo[puntaCruza:80]
                    )
                    segundoHijo = (
                        ""
                        + padre2.individuo[0:puntaCruza]
                        + padre1.individuo[puntaCruza:80]
                    )

                    tamIndividuo += 1
                    hijo1 = Fitness(copy.deepcopy(listaProducto), meta, tipoMeta)
                    hijo1.ActualizarBinomio(primerHijo)
                    listaFit.append(hijo1)
                    hijos.append(hijo1)

                    tamIndividuo += 1
                    hijo2 = Fitness(copy.deepcopy(listaProducto), meta, tipoMeta)
                    hijo2.ActualizarBinomio(segundoHijo)
                    listaFit.append(hijo2)
                    hijos.append(hijo2)

                    contadorAparear += 2
                    par = 0
                    contador += 1
                elif par == 2:
                    par = 0
                    contador += 1
                    bandera = True
        ControlAptitud(listaFit)
        Ruleta(totalFitness, listaFit)
        # ? FIN CRUZA
        #! MUTACIÓN
        poblacion = len(listaFit)
        probMutar1 = int((1 / poblacion) * 100)
        probMutar2 = int((1 / 80) * 100)
        mutacionProb = 0

        if probMutar1 > probMutar2:
            mutacionProb = random.randint(probMutar2, probMutar1)
        else:
            mutacionProb = random.randint(probMutar1, probMutar2)

        mutacionProb = mutacionProb / 100

        for decendecia in hijos:
            nuevoIndividuo = ""
            for individuos in decendecia.individuo:
                mutar = (random.randint(0, 100)) / 100
                if mutar <= mutacionProb:
                    if individuos == "0":
                        individuos = "1"
                    else:
                        individuos = "0"
                nuevoIndividuo += str(individuos)
            decendecia.ActualizarBinomio(nuevoIndividuo)

        totalFitness = ControlAptitud(listaFit)
        Ruleta(totalFitness, listaFit)
        poblacion = len(listaFit)
        # ?FIN MUTAR

        #!PODA
        listaMeta = []
        for aptitudes in listaFit:
            if aptitudes.aptitud > meta:
                listaMeta.append(aptitudes)
        for metas in listaMeta:
            listaFit.remove(metas)
        # ? FIN PODA
        #!CONTROL
        listaFit = sorted(listaFit, key=attrgetter("aptitud"))
        poblacion = len(listaFit)
        while poblacion > poblacionMax and len(listaFit) > 0:
            listaFit.pop(0)
            poblacion -= 1
        # ? FIN CONTROL
        #!GRAFICA
        if len(listaFit) > 0:
            totalFitness = ControlAptitud(listaFit)
            Ruleta(totalFitness, listaFit)
            poblacion = len(listaFit)

            mejorAptitu = listaFit[len(listaFit) - 1].aptitud
            peorAptitu = listaFit[0].aptitud
            promedioAptitu = totalFitness / poblacion

            mejorAptitud.append(mejorAptitu)
            peorAptitud.append(peorAptitu)
            promedioAptitud.append(promedioAptitu)
            listaGeneracion.append(i)
    print(len(listaFit) - 1, " len(listaFit)-1")
    CrearTabla(
        listaFit[len(listaFit) - 1],
        tipoMeta,
        mejorAptitud,
        peorAptitud,
        promedioAptitud,
        listaGeneracion,
    )


def send_data():
    CrarListaProducto()
    tipo = seleccion.get()
    poblacionInicial_info = int(poblacionInicial.get())
    poblacionMaxima_info = int(poblacionMaxima.get())
    generaciones_info = int(generaciones.get())
    metaDiaria_info = int(metaDiaria.get())
    print(
        poblacionInicial_info,
        "\t",
        poblacionMaxima_info,
        "\t",
        generaciones_info,
        "\t",
        generaciones_info,
        "\t",
        metaDiaria_info,
        tipo,
    )
    poblacionInicial_entry.delete(0, END)
    poblacionMaxima_entry.delete(0, END)
    generaciones_entry.delete(0, END)
    metaDiaria_entry.delete(0, END)
    metaTotal = metaDiaria_info * 7
    listaFit = []
    listaFit = CrearPoblacion(poblacionInicial_info, metaDiaria_info, tipo)
    Iniciar(
        listaFit,
        generaciones_info,
        poblacionInicial_info,
        metaTotal,
        tipo,
        poblacionInicial_info,
    )
    tipo = ""
    poblacionInicial_info = ""
    poblacionMaxima_info = ""
    generaciones_info = ""
    metaDiaria_info = ""
    print(
        poblacionInicial_info,
        "\t",
        poblacionMaxima_info,
        "\t",
        generaciones_info,
        "\t",
        generaciones_info,
        "\t",
        metaDiaria_info,
        tipo,
    )


mywindow = Tk()

mywindow.geometry("650x550")
mywindow.title("191209 MATUZ TAMAYO")
mywindow.resizable(False, False)
mywindow.config(background="#213141")
main_title = Label(
    text="Algoritmo Genetico: Meta de calorias o proteinas a 7 dias",
    font=("Cambria", 14),
    bg="#56CD63",
    fg="black",
    width="500",
    height="2",
)
main_title.pack()

seleccion = tkinter.StringVar()
# Define Label Fields
poblacionInicial = Label(text="poblacion inicial", bg="#FFEEDD")
poblacionInicial.place(x=22, y=70)
poblacionMaxima = Label(text="poblacion maxima", bg="#FFEEDD")
poblacionMaxima.place(x=22, y=130)
generaciones = Label(text="generaciones", bg="#FFEEDD")
generaciones.place(x=22, y=190)
metaDiaria = Label(text="meta diaria", bg="#FFEEDD")
metaDiaria.place(x=22, y=250)


# Get and store data from users
poblacionInicial = StringVar()
poblacionMaxima = StringVar()
generaciones = StringVar()
metaDiaria = StringVar()
tipoMeta = StringVar()
rbnCalorias = tkinter.Radiobutton(
    mywindow, text="Calorias", variable=seleccion, value="C"
)
rbnCalorias.place(x=22, y=310)
rbnProteinas = tkinter.Radiobutton(
    mywindow, text="Proteinias", variable=seleccion, value="P"
)
rbnProteinas.place(x=102, y=310)

poblacionInicial_entry = Entry(textvariable=poblacionInicial, width="40")
poblacionMaxima_entry = Entry(textvariable=poblacionMaxima, width="40")
generaciones_entry = Entry(textvariable=generaciones, width="40")
metaDiaria_entry = Entry(textvariable=metaDiaria, width="40")


poblacionInicial_entry.place(x=22, y=100)
poblacionMaxima_entry.place(x=22, y=160)
generaciones_entry.place(x=22, y=220)
metaDiaria_entry.place(x=22, y=280)

# Submit Button
submit_btn = Button(
    mywindow, text="iniciar", width="30", height="2", command=send_data, bg="#00CD63"
)
submit_btn.place(x=22, y=400)

mywindow.mainloop()
