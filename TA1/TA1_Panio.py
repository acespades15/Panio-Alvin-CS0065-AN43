"""Random Walk Simulation Using AgentPy.

Student: Alvin Christian S. Panio
Section: AN43-BSCSSE
Professor: Crisola Tan
Date: October 6, 2026

The program records every agent path, prevents agents from entering occupied
cells, summarizes final positions, draws a path plot, and animates the walk.
"""

from collections import Counter
from pathlib import Path

import agentpy as ap
import matplotlib.animation as animation
import matplotlib.pyplot as plt


DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def positive_integer(prompt):
    """Ask repeatedly until the user enters a positive whole number."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Please enter a positive whole number.")


class RandomWalker(ap.Agent):
    """An agent that takes one bounded random step at a time."""

    def move(self):
        grid = self.model.grid
        x, y = grid.positions[self]
        dx, dy = self.model.random.choice(DIRECTIONS)
        upper = self.p.grid_size - 1

        # Clamp the intended destination so it always remains inside the grid.
        target = (
            max(0, min(upper, x + dx)),
            max(0, min(upper, y + dy)),
        )

        # Updated movement rule: enter only an unoccupied cell.
        if target in grid.empty:
            grid.move_to(self, target)

        # A blocked or boundary step is recorded as the same position.
        self.path.append(grid.positions[self])


class RandomWalkModel(ap.Model):
    """AgentPy model that owns the agents and their shared grid."""

    def setup(self):
        size = self.p.grid_size
        self.grid = ap.Grid(
            self,
            (size, size),
            torus=False,
            track_empty=True,
        )
        self.agents = ap.AgentList(self, self.p.agents, RandomWalker)

        # Start in different random cells so avoidance is valid at time zero.
        self.grid.add_agents(self.agents, random=True, empty=True)
        for agent in self.agents:
            agent.path = [self.grid.positions[agent]]

    def step(self):
        # Randomize update order to avoid giving low-ID agents fixed priority.
        order = list(self.agents)
        self.random.shuffle(order)
        for agent in order:
            agent.move()

    def end(self):
        counts = Counter(self.grid.positions.values())
        self.report("occupied_cells", len(counts))
        self.report("largest_cell_population", max(counts.values(), default=0))


def print_results(model):
    """Print the final positions and path statistics for every agent."""
    print("\nFINAL-POSITION ANALYSIS")
    for number, agent in enumerate(model.agents, start=1):
        path = agent.path
        successful_moves = sum(a != b for a, b in zip(path, path[1:]))
        print(
            f"Agent {number}: final={path[-1]}, "
            f"successful moves={successful_moves}/{model.p.steps}, "
            f"unique cells visited={len(set(path))}"
        )

    print(
        f"Occupied cells: {model.reporters['occupied_cells']} "
        f"of {model.p.grid_size ** 2}"
    )
    print(
        "Largest number of agents in one cell: "
        f"{model.reporters['largest_cell_population']}"
    )


def save_path_plot(model, filename="random_walk_paths.png"):
    """Save a plot of all recorded paths; circles start and X marks finish."""
    fig, ax = plt.subplots(figsize=(8, 7))

    for number, agent in enumerate(model.agents, start=1):
        xs, ys = zip(*agent.path)
        (line,) = ax.plot(
            xs,
            ys,
            marker="o",
            markersize=2.5,
            linewidth=1.2,
            alpha=0.75,
            label=f"Agent {number}",
        )
        ax.scatter(
            xs[0],
            ys[0],
            color=line.get_color(),
            marker="o",
            s=55,
            edgecolors="black",
            zorder=3,
        )
        ax.scatter(
            xs[-1],
            ys[-1],
            color=line.get_color(),
            marker="X",
            s=75,
            edgecolors="black",
            zorder=3,
        )

    size = model.p.grid_size
    ax.set(
        xlim=(-0.5, size - 0.5),
        ylim=(-0.5, size - 0.5),
        xlabel="X position",
        ylabel="Y position",
        title=(
            f"Tracked random-walk paths ({model.p.agents} agents, "
            f"{model.p.steps} steps)"
        ),
    )
    ax.set_xticks(range(size))
    ax.set_yticks(range(size))
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal")
    if model.p.agents <= 10:
        ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8)
    fig.tight_layout()
    output = Path(filename).resolve()
    fig.savefig(output, dpi=180, bbox_inches="tight")
    print(f"Path plot saved to: {output}")
    return fig


def create_animation(model):
    """Build an animation from the already-recorded simulation paths."""
    fig, ax = plt.subplots(figsize=(7, 7))
    size = model.p.grid_size
    ax.set(
        xlim=(-0.5, size - 0.5),
        ylim=(-0.5, size - 0.5),
        xlabel="X position",
        ylabel="Y position",
    )
    ax.set_xticks(range(size))
    ax.set_yticks(range(size))
    ax.grid(True, alpha=0.35)
    ax.set_aspect("equal")

    first_positions = [agent.path[0] for agent in model.agents]
    scatter = ax.scatter(
        [position[0] for position in first_positions],
        [position[1] for position in first_positions],
        c=range(model.p.agents),
        cmap="tab20",
        s=100,
        edgecolors="black",
    )

    def update(frame):
        positions = [agent.path[frame] for agent in model.agents]
        scatter.set_offsets(positions)
        ax.set_title(f"Random walk - step {frame} of {model.p.steps}")
        return (scatter,)

    walk_animation = animation.FuncAnimation(
        fig,
        update,
        frames=model.p.steps + 1,
        interval=250,
        repeat=False,
    )
    return fig, walk_animation


def main():
    print("RANDOM WALK SIMULATION USING AGENTPY")
    num_agents = positive_integer("Enter number of agents: ")
    grid_size = positive_integer("Enter grid size (e.g., 10 for 10x10): ")
    num_steps = positive_integer("Enter number of steps: ")

    if num_agents > grid_size**2:
        raise SystemExit(
            "Collision avoidance requires no more agents than grid cells."
        )

    parameters = {
        "agents": num_agents,
        "grid_size": grid_size,
        "steps": num_steps,
        "seed": 42,
    }
    model = RandomWalkModel(parameters)
    model.run(display=False)

    print_results(model)
    path_figure = save_path_plot(model)
    animation_figure, walk_animation = create_animation(model)

    # In a headless environment, save the animation instead of opening a GUI.
    if "agg" in plt.get_backend().lower():
        gif_path = Path("random_walk_animation.gif").resolve()
        walk_animation.save(gif_path, writer=animation.PillowWriter(fps=4))
        print(f"Animation saved to: {gif_path}")
        plt.close(path_figure)
        plt.close(animation_figure)
    else:
        plt.show()


if __name__ == "__main__":
    main()
