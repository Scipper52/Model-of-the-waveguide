from numpy import (sin, cos, tan, pi, exp, sqrt, arange, meshgrid, linspace)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import (clf, gcf, subplots_adjust,figure)
from tkinter.ttk import (Combobox, Button, Style)
from tkinter import (Label,Entry, Tk, S,N,E,W,SE,SW,NE,NW)
from sys import exit

LARGE_FONT= ("Verdana", 12)

def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True

def EXIT():
    exit(0)

def plus1():
    global moda_n
    moda_n+=1
    moda_n_label.configure(text=moda_n)

def plus2():
    global moda_m
    moda_m+=1
    moda_m_label.configure(text=moda_m)

def minus1():
    global moda_n
    if moda_n>0:
        moda_n-=1
        moda_n_label.configure(text=moda_n)

def minus2():
    global moda_m
    if moda_m>0:
        moda_m-=1
        moda_m_label.configure(text=moda_m)

def time_minus():
    global time
    if time>0:
        time-=1
        time_label.configure(text=time)
        plotting()

def time_plus():
    global time
    time+=1
    time_label.configure(text=time)
    plotting()

def get(entry):
    value = entry.get()
    try:
        return int(value)
    except ValueError:
        return None

def plotting():

    global size_lines_entry
    global frequincy
    global moda_n
    global moda_m
    global label

    clf()
    if (len(frequincy.get()) == 0) or (len(a_x_size_entry.get()) == 0) or (len(b_x_size_entry.get()) == 0) or (len(size_lines_entry.get()) == 0):
        clf()
        label.configure(text="Введите полные данные!", bg="lightgray")
        label.grid(row=0, column=4, columnspan=7, padx=10, pady=15, sticky=S+N)
        gcf().canvas.draw()
        return
    label.configure(text=" ")

    cc=3e10 #скорость света в см/с

    ff=get(frequincy) #Частота в ГГц
    f=ff*1e9 #перевод в Гц
    w=2*pi*f
    lyam=cc/f
    hh=w/cc #волновое число в волноводе
    #Параметры волновода
    a=get(a_x_size_entry) #размер волновода по x в см
    b=get(b_x_size_entry) #размер волновода по y в см
    c=lyam #размер волновода по z в см
    n=moda_n
    m=moda_m

    #Шаг сетки
    h=0.01
    #время сечения
    tt=time #время в минус хреналионной степени
    t=tt/1e12
    #количество линий уровня
    k=get(size_lines_entry)

    P1=0 #константа для x
    P2=0 #константа для y

    #Алгоритм определения констант для проекций (где будет сделан срез)
    if (n%2)!=0 and (m%2)!=0:
        P1 = a/2
        P2 = b/2
    elif (n%2)!=0 and (m%2)==0:
        P1 = a/2
        if m!=0:
            P2 = b/(2*m)
    elif (n%2)==0 and (m%2)!=0:
        if n!=0:
            P1 = a/(2*n)
        P2 = b/2
    elif (n%2)==0 and (m%2)==0:
        if m!=0 and n!=0:
            P1 = a/(2*n)
            P2 = b/(2*m)

    P3=0
    P4=0
    if n!=0 and m==0:
        if (n%2)!=0:
            P3 = a/2
        else:
            P3 = a/(2*n)
    elif n==0 and m!=0:
        if (m%2)!=0:
            P4 = b/2
        else:
            P4 = b/(2*m)

    kappa = sqrt(((pi*n/a)**2)+((pi*m/b)**2))
    kappaX = pi*n/a
    kappaY = pi*m/b
    f_kr=(cc*kappa)/(2*pi)

    #####################################      TE      #############################################
    ##########   H   ############
    def TE_H_XY(x,y):
        return ((abs(sin(kappaX*x))**((1/kappaX)**2))/(abs(sin(kappaY*y))**((1/kappaY)**2)))*cos(w*t+pi/2)
    def TE_H_YZ(y,z):
        return (abs(sin(kappaY*y))**((kappa/kappaY)**2))*cos(w*t-hh*z+pi/2)
    def TE_H_XZ(x,z):
        return (abs(sin(kappaX*x))**((kappa/kappaX)**2))*cos(w*t-hh*z+pi/2)
    ##########    E   ###########
    def TE_E_XY(x,y):
        return abs(cos(kappaY*y))*abs(cos(kappaX*x))*cos(w*t)
    def TE_E_XZ(x,z):
        return (abs(cos(kappaX*x))*exp(-((kappaY*tan(kappaY*b))*z)))*cos(w*t-hh*z)
    def TE_E_YZ(y,z):
        return (abs(cos(kappaY*y))*exp(-(kappaX*tan(kappaX*a)*z)))*cos(w*t-hh*z)
    ########## H10 ############
    def TE10_H_XY(x,y):
        return abs(sin(kappaX*x))*exp(hh*tan(w*t)*y)
    def TE10_H_XZ(x,z):
        return cos(w*t-hh*z)*abs(sin(kappaX*x))
    def TE10_H_YZ(y,z):
        return cos(w*t-hh*z)*exp(kappaX*(cos(kappaX*P3)/sin(kappaX*P3))*y)
    ##########   E10   ###########
    def TE10_E_XY(x,y):
        return (w/(kappaX*cc))*abs(sin(kappaX*x))*sin(w*t)
    def TE10_E_XZ(x,z):
        return (w/(kappaX*cc))*abs(sin(kappaX*x))*sin(w*t-hh*z)
    def TE10_E_YZ(y,z):
        return (w/(kappaX*cc))*sin(kappaX*P3)*sin(w*t-hh*z)
    ########## H01 ############
    def TE01_H_XY(x,y):
        return abs(sin(kappaY*y))*exp(hh*tan(w*t)*x)
    def TE01_H_XZ(x,z):
        return cos(w*t-hh*z)*exp(kappaY*(cos(kappaY*P4)/sin(kappaY*P4))*x)
    def TE01_H_YZ(y,z):
        return cos(w*t-hh*z)*abs(sin(kappaY*y))
    ##########   E01   ###########
    def TE01_E_XY(x,y):
        return (w/(kappaY*cc))*abs(sin(kappaY*y))*sin(w*t)
    def TE01_E_XZ(x,z):
        return (w/(kappaY*cc))*sin(kappaY*P4)*sin(w*t-hh*z)
    def TE01_E_YZ(y,z):
        return (w/(kappaY*cc))*abs(sin(kappaY*y))*sin(w*t-hh*z)

    #############################################     TM      ###################################
    ##########    H    ############
    def TM_H_XY(x,y):
        return abs(sin(kappaX*x))*abs(sin(kappaY*y))*cos(w*t+pi/2)
    def TM_H_XZ(x,z):
        return ((abs(sin(kappaX*x))*exp((cos(kappaY*(P2))/sin(kappaY*(P2)))*kappaY*z)))*cos(w*t-hh*z+pi/2)
    def TM_H_YZ(y,z):
        return ((abs(sin(kappaY*y))*exp((cos(kappaX*(P1))/sin(kappaX*(P1)))*kappaX*z)))*cos(w*t-hh*z+pi/2)
    ##########    E    ###########
    def TM_E_XY(x,y):
        return (abs(cos(kappaY*y))**(1/(kappaY**2)))/(abs(cos(kappaX*x))**(1/(kappaX**2)))*cos(w*t)
    def TM_E_XZ(x,z):
        return cos(w*t-hh*z)*(abs(cos(kappaX*x))**((-kappa/kappaX)**2))
    def TM_E_YZ(y,z):
        return cos(w*t-hh*z)*(abs(cos(kappaY*y))**((-kappa/kappaY)**2))

    def makeData(b1,b2):
        a1 = arange(0, b1, h)
        a2 = arange(0, b2, h)
        a1grid, a2grid = meshgrid(a1, a2)
        return a1grid, a2grid

    if f > f_kr:
        aaa = fig.add_subplot(3,2,1)
        bbb = fig.add_subplot(3,2,2)
        ccc = fig.add_subplot(3,2,3)
        ddd = fig.add_subplot(3,2,4)
        fff = fig.add_subplot(3,2,5)
        eee = fig.add_subplot(3,2,6)

        if __name__ == '__main__':

            x1, y1 = makeData(a,b)
            y2, z2 = makeData(b,c)
            x3, z3 = makeData(a,c)
            if combobox.get()=="TE":
        ############################              TE               ############################
        ##############          XY        #############
        ########   H    #######
                if n!=0 and m!=0:
                    aaa.contour(x1, y1, TE_H_XY(x1,y1), linspace(-1, 1, k))
                elif n!=0 and m==0:
                    aaa.contour(x1, y1, TE10_H_XY(x1,y1), linspace(-1, 1, k))
                elif n==0 and m!=0:
                    aaa.contour(x1, y1, TE01_H_XY(x1,y1), linspace(-1, 1, k))
                aaa.set_title('TE_H')
                aaa.set_xlabel('x')
                aaa.set_ylabel('y')


            ########    E    #######
                if n!=0 and m!=0:
                    bbb.contour(x1, y1, TE_E_XY(x1,y1), linspace(-1, 1, k))
                elif n!=0 and m==0:
                    bbb.contour(x1, y1, TE10_E_XY(x1,y1), linspace(-1, 1, k))
                elif n==0 and m!=0:
                    bbb.contour(x1, y1, TE01_E_XY(x1,y1), linspace(-1, 1, k))
                bbb.set_title('TE_E')
                bbb.set_xlabel('x')
                bbb.set_ylabel('y')

            ##############         YZ       #####################
            #######    H    #######
                if n!=0 and m!=0:
                    ccc.contour(z2, y2, TE_H_YZ(y2,z2), linspace(-1, 1, k))
                elif n!=0 and m==0:
                    ccc.contour(z2, y2, TE10_H_YZ(y2,z2), linspace(-1, 1, k))
                elif n==0 and m!=0:
                    ccc.contour(z2, y2, TE01_H_YZ(y2,z2), linspace(-1, 1, k))
                ccc.set_xlabel('z')
                ccc.set_ylabel('y')
            #######      E      #######
                if n!=0 and m!=0:
                    ddd.contour(z2, y2, TE_E_YZ(y2,z2), linspace(-1, 1, k))
                elif n!=0 and m==0:
                    ddd.contour(z2, y2, TE10_E_YZ(y2,z2), linspace(-1, 1, k))
                elif n==0 and m!=0:
                    ddd.contour(z2, y2, TE01_E_YZ(y2,z2), linspace(-1, 1, k))
                ddd.set_xlabel('z')
                ddd.set_ylabel('y')

            ###############       XZ     ##################
            ########    H     #########
                if n!=0 and m!=0:
                    fff.contour(z3, x3, TE_H_XZ(x3,z3), linspace(-1, 1, k))
                elif n!=0 and m==0:
                    fff.contour(z3, x3, TE10_H_XZ(x3,z3), linspace(-1, 1, k))
                elif n==0 and m!=0:
                    fff.contour(z3, x3, TE01_H_XZ(x3,z3), linspace(-1, 1, k))
                fff.set_xlabel('z')
                fff.set_ylabel('x')
            ########   E   #########
                if n!=0 and m!=0:
                    eee.contour(z3, x3, TE_E_XZ(x3,z3), linspace(-1, 1, k))
                elif n!=0 and m==0:
                    eee.contour(z3, x3, TE10_E_XZ(x3,z3), linspace(-1, 1, k))
                elif n==0 and m!=0:
                    eee.contour(z3, x3, TE01_E_XZ(x3,z3), linspace(-1, 1, k))
                eee.set_xlabel('z')
                eee.set_ylabel('x')
            else:
        #######################################             TM               ####################################
        ##############          XY        #############
        ########   H    #######
                if n!=0 and m!=0:
                    aaa.contour(x1, y1, TM_H_XY(x1,y1), linspace(-1, 1, k))
                    aaa.set_title('TM_H')
                    aaa.set_xlabel('x')
                    aaa.set_ylabel('y')
            ########    E    #######
                    bbb.contour(x1, y1, TM_E_XY(x1,y1), linspace(-1, 1, k))
                    bbb.set_title('TM_E')
                    bbb.set_xlabel('x')
                    bbb.set_ylabel('y')

            ##############         YZ       #####################
            #######    H    #######
                    ccc.contour(z2, y2, TM_H_YZ(y2,z2), linspace(-1, 1, k))
                    ccc.set_xlabel('z')
                    ccc.set_ylabel('y')
            #######      E      #######
                    ddd.contour(z2, y2, TM_E_YZ(y2,z2), linspace(-1, 1, k))
                    ddd.set_xlabel('z')
                    ddd.set_ylabel('y')

            ###############       XZ     ##################
            ########    H     #########
                    fff.contour(z3, x3, TM_H_XZ(x3,z3), linspace(-1, 1, k))
                    fff.set_xlabel('z')
                    fff.set_ylabel('x')
            ########   E   #########
                    eee.contour(z3, x3, TM_E_XZ(x3,z3), linspace(-1, 1, k))
                    eee.set_xlabel('z')
                    eee.set_ylabel('x')

    else:
        label.configure(text="Частота ниже критической!!! Волна не распространяется!!!", bg="lightgray")

    subplots_adjust(wspace=0.5, hspace=0.5)
    gcf().canvas.draw()

#INTERFACE
root = Tk()
root.protocol("WM_DELETE_WINDOW", EXIT)
root.attributes("-toolwindow", 0)
root.resizable(width=False, height=False)
root['bg']='lightgray'
root.title("Waveguide")
w = 1000
h = 630
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
x = (sw - w)/2
y = (sh - h)/2
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

label_n = Label(root, text="Выберите тип волны:", font=LARGE_FONT, bg="lightgray")
label_n.grid(row=0, column=0, columnspan=2, padx=30, sticky=SW)


style = Style()
style.configure("BW.TLabel", foreground='black', background='lightgray', selectbackground='lightgray', selectforeground='black')
combobox = Combobox(values = ["TE","TM"], height=2, width=4, state="readonly",  style="BW.TLabel", font=LARGE_FONT)
combobox.set("TE")
combobox.grid(row=0, column=2, columnspan=2, sticky=SW)
root.option_add("*TCombobox*Listbox*Background", 'gainsboro')
root.option_add("*TCombobox*Listbox*Foreground", 'black')


moda_label = Label(root, text="Выберите моду:", font=LARGE_FONT, bg="lightgray")
moda_label.grid(row=1, column=0, columnspan=4, padx=30, sticky=SW)

moda_n=0
label_n = Label(root, text="n: ", font=LARGE_FONT, bg="lightgray")
label_n.grid(row=3, column=0, padx=10, sticky=E)
moda_n_label = Label(root, text=moda_n, font=LARGE_FONT, bg="lightgray")
moda_n_label.grid(row=3, column=1, padx=30, sticky=W)
moda_n_plus = Button(root, text="+", command=plus1)
moda_n_plus.grid(row=2, column=1, sticky=SW)
moda_n_minus = Button(root, text="-", command=minus1)
moda_n_minus.grid(row=4, column=1, sticky=NW)

moda_m=0
label_m = Label(root, text="m: ", font=LARGE_FONT, bg="lightgray")
label_m.grid(row=3, column=2, padx=10, sticky=W)
moda_m_label = Label(root, text=moda_m, font=LARGE_FONT, bg="lightgray")
moda_m_label.grid(row=3, column=3, padx=30, sticky=W)
moda_m_plus = Button(root, text="+", command=plus2)
moda_m_plus.grid(row=2, column=3, sticky=SW)
moda_m_minus = Button(root, text="-", command=minus2)
moda_m_minus.grid(row=4, column=3, sticky=NW)

label_m = Label(root, text="Введите частоту: ", font=LARGE_FONT, bg="lightgray")
label_m.grid(row=5, column=0, columnspan=2, padx=30, pady=15, sticky=NE)

frequincy = Entry(root, width=5, bg="gainsboro", selectbackground='black', validate="key")
frequincy['validatecommand'] = (frequincy.register(testVal),'%P','%d')
frequincy.grid(row=5, column=2, columnspan=2, pady=15, ipadx=5, sticky=NW)

waveguide_size = Label(root, text="Введите размеры волновода(см): ", font=LARGE_FONT, bg="lightgray")
waveguide_size.grid(row=6, column=0, columnspan=4, padx=30, sticky=W)

a_x_size = Label(root, text="a:", font=LARGE_FONT, bg="lightgray")
a_x_size.grid(row=7, column=0, padx=30, sticky=NE)
a_x_size_entry = Entry(root, width=5, bg="gainsboro", selectbackground='black', validate="key")
a_x_size_entry['validatecommand'] = (a_x_size_entry.register(testVal),'%P','%d')
a_x_size_entry.grid(row=7, column=1, sticky=NW)

b_x_size = Label(root, text="b:", font=LARGE_FONT, bg="lightgray")
b_x_size.grid(row=7, column=2, sticky=NW)
b_x_size_entry = Entry(root, width=5, bg="gainsboro", selectbackground='black', validate="key")
b_x_size_entry['validatecommand'] = (b_x_size_entry.register(testVal),'%P','%d')
b_x_size_entry.grid(row=7, column=3, sticky=NW)

size_lines = Label(root, text="Кол-во линий уровня: ", font=LARGE_FONT, bg="lightgray")
size_lines.grid(row=8, column=0, columnspan=2, padx=30, pady=10, sticky=SW)
size_lines_entry = Entry(root, width=5, bg="gainsboro", selectbackground='black', validate="key")
size_lines_entry['validatecommand'] = (size_lines_entry.register(testVal),'%P','%d')
size_lines_entry.grid(row=8, column=2, columnspan=2, pady=10, sticky=SW)

click=Button(root, text = "Построить", command = plotting)
click.grid(row=10, column=0, columnspan=10, pady=15, sticky=S)

label = Label(root, text=" ", font=LARGE_FONT, bg="lightgray")
label.grid(row=0, column=4, columnspan=7, padx=10, pady=15, sticky=S+N)

time=0
label_time = Label(root, text="Время: ", font=LARGE_FONT, bg="lightgray")
label_time.grid(row=9, column=0, columnspan=1, padx=30, pady=15, sticky=SW)
time_label = Label(root, text=time, font=LARGE_FONT, bg="lightgray")
time_label.grid(row=9, column=2, columnspan=1,padx=5, pady=15, sticky=SW)
time_plus = Button(root, text="+", command=time_plus)
time_plus.grid(row=9, column=3, columnspan=1, pady=15, sticky=SW)
time_minus = Button(root, text="-", command=time_minus)
time_minus.grid(row=9, column=1, columnspan=1, pady=15, sticky=SW)

fig = figure(facecolor='lightgray')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=4, rowspan=9, columnspan=7, padx=10, pady=15, sticky=S+N)

root.mainloop()
