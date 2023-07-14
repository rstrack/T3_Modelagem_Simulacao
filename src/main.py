import numpy as np
import pygame

from util.colors import WHITE, GRAY, BROWN
from util.generate_summary import generate_summary

from generators.exp_gen import ExpGen
from simulation.program import Program

# Configurações da janela
WIDTH = 800
HEIGHT = 600

SIMULATION_TIME = 7 * 24 * 60

# Configurações do mainframe
SLOT_WIDTH = 180
SLOT_HEIGHT = 100
SLOT_PADDING = 10
SO_WIDTH = SLOT_WIDTH
SO_HEIGHT = SLOT_HEIGHT
MAINFRAME_WIDTH = 200
MAINFRAME_HEIGHT = SLOT_HEIGHT * 4 + SLOT_PADDING * 5

arrival_interval = ExpGen(0.186242)
service_time = ExpGen(0.124719)
program_count = 0

speed_scale = 100

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mainframe Simulation")
clock = pygame.time.Clock()

# Lista de programas, slots e fila de espera
programs = []
slots = []
waiting_queue = []

# Criação dos slots de programa
for _ in range(3):
    slots.append(None)

# Loop principal
running = True
current_time = pygame.time.get_ticks() / 1000

font = pygame.font.Font(None, 24)


def scale_time(time):
    return time / speed_scale


# Métricas:

last_arrival_time = 0
current_arrival_interval = 0
arrival_intervals = [0]  # IC
processing_times = [0]  # TA
arrival_times = [0]  # TC
processing_starts = [0]  # IA
processing_ends = [0]  # FA
pe1 = [0]  # FA1
pe2 = [0]  # FA2
pe3 = [0]  # FA3
queue_times = [0]  # TF
system_times = [0]  # TS
idle_times = [0]  # TO
it1 = [0]  # TO1
it2 = [0]  # TO2
it3 = [0]  # TO3

end_sim = False


# índice -1 representa o ultimo elemento da lista
def calculate_metrics():
    # Tempo de Chegada (TC)
    arrival_times.append(arrival_intervals[-1] + arrival_times[-1])
    # Inicio de Atendimento (IA)
    processing_starts.append(
        np.max([arrival_times[-1], np.min([pe1[-1], pe2[-1], pe3[-1]])])
    )

    # Fim de Atendimento (FA)
    processing_ends.append(processing_times[-1] + processing_starts[-1])
    # FA1 FA2 e FA3
    if pe1[-1] <= np.min([pe1[-1], pe2[-1], pe3[-1]]):
        queue_selected = 0
        pe1.append(processing_ends[-1])
    elif pe2[-1] <= np.min([pe1[-1], pe2[-1], pe3[-1]]):
        queue_selected = 1
        pe2.append(processing_ends[-1])
    elif pe3[-1] <= np.min([pe1[-1], pe2[-1], pe3[-1]]):
        queue_selected = 2
        pe3.append(processing_ends[-1])
    # Tempo de Fila (TF)
    queue_times.append(processing_starts[-1] - arrival_times[-1])
    # Tempo de Sistema (TS)
    system_times.append(processing_ends[-1] - arrival_times[-1])
    # Tempo Ocioso (TO) e Tempo ocioso por atendentes (TO1 TO2 e TO3)
    if processing_ends[-1] >= np.min([pe1[-1], pe2[-1], pe3[-1]]):
        match queue_selected:
            case 0:
                idle_times.append(processing_starts[-1] - pe1[-2])
                it1.append(idle_times[-1])
            case 1:
                idle_times.append(processing_starts[-1] - pe2[-2])
                it2.append(idle_times[-1])
            case 2:
                idle_times.append(processing_starts[-1] - pe3[-2])
                it3.append(idle_times[-1])


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                speed_scale = (
                    10000
                    if speed_scale == 1000
                    else 1000
                    if speed_scale == 100
                    else speed_scale
                )
                print(f"Escala: {speed_scale}")
            if event.key == pygame.K_LEFT:
                speed_scale = (
                    100
                    if speed_scale == 1000
                    else 1000
                    if speed_scale == 10000
                    else speed_scale
                )
                print(f"Escala: {speed_scale}")

            if event.key == pygame.K_DOWN:
                end_sim = True

    if end_sim or (processing_ends[-1] > SIMULATION_TIME):
        generate_summary(
            arrival_intervals[1:-1],
            processing_times[1:-1],
            arrival_times[1:-1],
            processing_starts[1:-1],
            processing_ends[1:-1],
            pe1[1:-1],
            pe2[1:-1],
            pe3[1:-1],
            queue_times[1:-1],
            system_times[1:-1],
            idle_times[1:-1],
            it1[1:-1],
            it2[1:-1],
            it3[1:-1],
        )
        running = False

    # Gerar um novo programa aleatoriamente
    if (pygame.time.get_ticks() / 1000) >= last_arrival_time + scale_time(
        current_arrival_interval
    ):
        if current_arrival_interval != 0:
            arrival_intervals.append(current_arrival_interval)
        last_arrival_time = pygame.time.get_ticks() / 1000
        current_arrival_interval = arrival_interval.generate()
        processing_time = service_time.generate()
        processing_times.append(processing_time)
        calculate_metrics()
        program = Program(program_count + 1, scale_time(processing_time))
        program_count += 1
        waiting_queue.append(program)  # Adiciona o programa à fila de espera

    # Executar os programas nos slots disponíveis
    for i in range(len(slots)):
        program = slots[i]
        if program:
            program.execute(pygame.time.get_ticks() / 1000)
            if program.finish_time != 0:
                slots[i] = None  # Remove o programa finalizado do slot

    # Alocar programas nos slots disponíveis
    for i in range(len(slots)):
        if slots[i] is None:
            if waiting_queue:
                program = waiting_queue.pop(
                    0
                )  # Pega o próximo programa na fila de espera
                slots[i] = program  # Adiciona o programa ao slot
                program.start_time = pygame.time.get_ticks() / 1000

    # Desenhar a tela
    screen.fill(GRAY)

    # Desenhar o mainframe
    mainframe_x = (WIDTH - MAINFRAME_WIDTH) * 7 // 8
    mainframe_y = (HEIGHT - (SLOT_HEIGHT * 3 + SLOT_PADDING * 2 + SO_HEIGHT)) // 2

    pygame.draw.rect(
        screen, WHITE, (mainframe_x, mainframe_y, MAINFRAME_WIDTH, MAINFRAME_HEIGHT), 2
    )

    # Desenhar os slots de programa
    slot_x = mainframe_x + (MAINFRAME_WIDTH - SLOT_WIDTH) // 2
    slot_y = mainframe_y + SLOT_PADDING

    for i in range(3):
        pygame.draw.rect(screen, WHITE, (slot_x, slot_y, SLOT_WIDTH, SLOT_HEIGHT), 2)
        slot_y += SLOT_HEIGHT + SLOT_PADDING

    # Desenhar o S.O.
    pygame.draw.rect(screen, BROWN, (slot_x, slot_y, SO_WIDTH, SO_HEIGHT), 0)
    label1 = font.render("Sistema", True, (0, 0, 0))
    label2 = font.render("Operacional", True, (0, 0, 0))
    screen.blit(label1, (slot_x + 55, slot_y + 25))
    screen.blit(label2, (slot_x + 40, slot_y + 50))

    # Desenhar a fila de espera
    queue_x = mainframe_x - 200
    queue_y = (mainframe_y + MAINFRAME_HEIGHT) // 2

    for i, program in enumerate(waiting_queue):
        pygame.draw.rect(
            screen,
            program.color,
            (
                queue_x - (i * (SLOT_WIDTH + SLOT_PADDING)),
                queue_y,
                SLOT_WIDTH,
                SLOT_HEIGHT,
            ),
            0,
        )
        screen.blit(
            font.render(f"Programa {program.number}", True, (0, 0, 0)),
            (
                queue_x - (i * (SLOT_WIDTH + SLOT_PADDING)),
                queue_y,
            ),
        )

    # Desenhar os programas em execução nos slots
    for i, program in enumerate(slots):
        if program:
            program_x = mainframe_x + (MAINFRAME_WIDTH - SLOT_WIDTH) // 2
            program_y = mainframe_y + SLOT_PADDING + i * (SLOT_HEIGHT + SLOT_PADDING)

            pygame.draw.rect(
                screen,
                program.color,
                (program_x, program_y, SLOT_WIDTH, SLOT_HEIGHT),
                0,
            )
            screen.blit(
                font.render(f"Programa {program.number}", True, (0, 0, 0)),
                (program_x + 45, program_y + 40),
            )

    # print(pygame.time.get_ticks() / 1000)
    # Atualizar a tela
    pygame.display.flip()
    clock.tick(60)

# Encerrar o Pygame
pygame.quit()
