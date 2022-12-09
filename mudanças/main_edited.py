import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import simulation_edited as simulation
import select_material_edited as select_material


# **********************************************
# definindo os parâmetros das simulações

# geometria da placa
chapa = simulation.geometry(Lx=1, Ly=1, Lz=5e-3)

#inicializando a base de dados de materiais:
db = select_material.material_database('materiais_edited.xls')
#inicializando a base de dados de fluidos:
db2 = select_material.fluid_database('materiais_edited.xls')

# selecionando materiais
cobre = db.select('Cobre')
ouro = db.select('Ouro')
ferro = db.select('Ferro')
bronze = db.select('Bronze')
# selecionando fluidos
armov = db2.select('Ar mov')

# parâmetros do processo de estampagem
estampa = simulation.stamping(Tinitial=100, Tstamp=800, forma='anel circular') # anel circular ; anel elíptico ;
#estampa = simulation.stamping(Tinitial=100, Tstamp=800, text='eleno é um monstro', fontsize=21)

# definindo condição de resfriamento/aquecimento
conv = simulation.convection(Trefr=400)

# **********************************************
# inicializando as simulações 

simulacao1 = simulation.DiffFin(chapa, cobre, armov, estampa, conv)
simulacao2 = simulation.DiffFin(chapa, ouro,  armov,  estampa, conv)
simulacao3 = simulation.DiffFin(chapa, ferro, armov, estampa, conv)
simulacao4 = simulation.DiffFin(chapa, bronze, armov,  estampa, conv)

# **********************************************
# Gráficos

fig = plt.figure(figsize=(12, 7), constrained_layout=True)
plt.suptitle('Resfriamento de chapas finas')

# função para criar um painel no eixo ax
def painel(simulacao, ax, titulo=''):

    ax.set_title(titulo)
    ax.set_xlabel(f'$x$ (m)')
    ax.set_ylabel(f'$y$ (m)')

    im = ax.imshow(simulacao.T, vmin=0, vmax=simulacao.stamping.Tstamp, origin='lower', cmap='magma', extent=(0, simulacao.geometry.Lx, 0, simulacao.geometry.Ly))
    plt.colorbar(im, ax=ax, location='bottom', orientation='horizontal', label='$T$ (°C)', shrink=.5)

    return im

ax1 = fig.add_subplot(2, 3, 1)
ax2 = fig.add_subplot(2, 3, 4)
ax3 = fig.add_subplot(2, 3, 3)
ax4 = fig.add_subplot(2, 3, 6)

im1 = painel(simulacao1, ax1, f'{simulacao1.material.name}, {simulacao1.fluid.name}')
im2 = painel(simulacao2, ax2, f'{simulacao2.material.name}, {simulacao2.fluid.name}')
im3 = painel(simulacao3, ax3, f'{simulacao3.material.name}, {simulacao3.fluid.name}')
im4 = painel(simulacao4, ax4, f'{simulacao4.material.name}, {simulacao4.fluid.name}')

# **********************************************
# Animação

# função de animação
n = 0
def animate(i):
    global pause, n
    if not pause:
        for s, im in zip([simulacao1, simulacao2, simulacao3, simulacao4], [im1, im2, im3, im4]):
            s.evolve()
            im.set_array(s.T)
        time_label.set_text(f'$t = {n * simulacao1.dt: .2f}$ s')
        n += 1        
    return  im1, im2, im3, im4, time_label

# Função para pausar com o mouse
pause = True  # se pause=True, começa pausado
def onClick(event):
    global pause
    pause ^= True

delay=0.1
anim = animation.FuncAnimation(fig, animate, interval=delay, blit=True)

# custom button
axes = plt.subplot(2, 3, 2)

bpause = Button(axes, 'start/pause',color="lightyellow")
bpause.on_clicked(onClick)

# mostrando o tempo no Painel
axes2 = plt.subplot(2, 3, 5)
axes2.axis('off')
time_label = axes2.text(0.44, 0.1, f'$t = 0$ s')
time_label.set_bbox(dict(facecolor='white', alpha=0.5, edgecolor='red'))

plt.show()
