import matplotlib.pyplot as plt
from pathlib import PurePosixPath

def get_graph(results):
    names, servings_taken = [], []

    for alloc in results:
        names.append(alloc["name"])
        servings_taken.append(alloc["servings_taken"])

    fix, ax = plt.subplots()
    ax.pie(servings_taken, labels=names,
           autopct=lambda p: f'{p * sum(servings_taken) / 100:.2f}')

    file_path = PurePosixPath(__file__).parent.parent

    plt.savefig(str(file_path) + "/ui/graph.png", transparent=False,
                bbox_inches="tight")