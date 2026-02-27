import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta del archivo CSV
CSV_PATH = os.path.join(BASE_DIR, "static", "kaggle", "Pokemon.csv")

# Ruta donde guardar la imagen de la grafica
STATIC_PLOTS = os.path.join(BASE_DIR, "static", "plots")


os.makedirs(STATIC_PLOTS, exist_ok=True)


def grafica_tipos():
    df = pd.read_csv(CSV_PATH)

    type_counts = df['Type 1'].value_counts()
    plt.figure(figsize=(12, 6))
    sns.barplot(x=type_counts.index, y=type_counts.values)
    plt.title("Number of Pokémon by Type")
    plt.xticks(rotation=45)
    plt.tight_layout()


# Esto se lo agregamos para guardar las graficas como imagenes
    filename = "pokemon_por_tipo.png"
    path = os.path.join(STATIC_PLOTS, filename)
    plt.savefig(path)
    plt.close()
    return filename


def grafica_gen():
    df = pd.read_csv(CSV_PATH)

    generation_counts = df['Generation'].value_counts().sort_index()
    plt.figure(figsize=(6, 4))
    sns.barplot(x=generation_counts.index, y=generation_counts.values)
    plt.title("Number of Pokémon by Generation")
    plt.xticks(rotation=45)
    plt.tight_layout()

# Esto se lo agregamos para guardar las graficas como imagenes
    filename = "pokemon_por_generacion.png"
    path = os.path.join(STATIC_PLOTS, filename)
    plt.savefig(path)
    plt.close()
    return filename
