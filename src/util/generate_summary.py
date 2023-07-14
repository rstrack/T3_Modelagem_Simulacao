import os
import sys
import numpy as np
from datetime import datetime


def resource_path(relative_path: str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def generate_summary(ic, ta, tc, ia, fa, fa1, fa2, fa3, tf, ts, to, to1, to2, to3):
    file = open(resource_path("./simulation_summary.txt"), "w")
    file.write("RESUMO DA SIMULAÇÃO\n")
    file.write(f"Data: {datetime.now()}\n\n")
    file.write("Tempo total da simulação: {:.2f} minutos\n\n".format(fa[-1]))
    file.write("---------------------------------------------------------\n")
    file.write(f"IC Médio: {np.mean(ic)} min\n")
    file.write(f"TA Médio: {np.mean(ta)} min\n")
    # file.write(f"TC Médio: {np.mean(tc)} min\n")
    # file.write(f"IA Médio: {np.mean(ia)} min\n")
    # file.write(f"FA Médio: {np.mean(fa)} min\n")
    # file.write(f"FA1 Médio: {np.mean(fa1)} min\n")
    # file.write(f"FA2 Médio: {np.mean(fa2)} min\n")
    # file.write(f"FA3 Médio: {np.mean(fa3)} min\n")
    file.write(f"TF Médio: {np.mean(tf)} min\n")
    file.write(f"TS Médio: {np.mean(ts)} min\n")
    file.write(f"TO Médio: {np.mean(to)} min\n")
    file.write(f"TO1 Médio: {np.mean(to1)} min\n")
    file.write(f"TO2 Médio: {np.mean(to2)} min\n")
    file.write(f"TO3 Médio: {np.mean(to3)} min\n")
    file.close()
    os.startfile(resource_path("simulation_summary.txt"))
