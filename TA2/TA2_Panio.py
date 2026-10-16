"""TA2 - Rule-Based Vacuum Cleaner Agent."""


def ask_room_state(room):
    """Ask for a valid initial state and return either Dirty or Clean."""
    while True:
        state = input(f"Enter the state of room {room} (Dirty/Clean): ").strip().lower()

        if state in ("dirty", "clean"):
            return state.title()

        print("Invalid input. Please enter only Dirty or Clean.")


def ask_number_of_steps():
    """Ask for a positive whole number of simulation steps."""
    while True:
        try:
            steps = int(input("How many steps should the simulation run? "))

            if steps > 0:
                return steps
        except ValueError:
            pass

        print("Invalid input. Please enter a positive whole number.")


def is_dirty(environment, room):
    """Return True when the selected room is dirty."""
    return environment[room] == "Dirty"


def clean_room(environment, room):
    """Change the selected room's state to Clean."""
    environment[room] = "Clean"


class RuleBasedAgent:
    """A vacuum agent controlled by two condition-action rules."""

    def __init__(self, environment, starting_room="A"):
        self.environment = environment
        self.location = starting_room

    def move(self):
        """Switch the agent between rooms A and B."""
        previous_room = self.location
        self.location = "B" if self.location == "A" else "A"
        return previous_room, self.location

    def perceive_and_act(self):
        """Observe the current room, apply one rule, and return the action."""
        # Rule 1: Clean the current room when it is dirty.
        if is_dirty(self.environment, self.location):
            cleaned_room = self.location
            clean_room(self.environment, cleaned_room)
            return f"Cleaned room {cleaned_room}."

        # Rule 2: Move when the current room is already clean.
        previous_room, new_room = self.move()
        return f"Moved from room {previous_room} to room {new_room}."


def main():
    """Set up the environment and run the requested simulation."""
    print("RULE-BASED VACUUM CLEANER AGENT")
    print("Set the initial state of each room.\n")

    # Task 1: Store the two-room environment in a dictionary.
    environment = {
        "A": ask_room_state("A"),
        "B": ask_room_state("B"),
    }

    # Task 2: Create the rule-based agent in room A.
    agent = RuleBasedAgent(environment, starting_room="A")
    steps = ask_number_of_steps()

    print("\nSIMULATION START")

    # Task 3: Run one perceive-and-act cycle during each step.
    for step in range(1, steps + 1):
        action = agent.perceive_and_act()

        print(f"\nStep {step}")
        print(f"Current location: Room {agent.location}")
        print(f"Action: {action}")
        print(f"Environment: {environment}")

    print("\nSIMULATION COMPLETE")


if __name__ == "__main__":
    main()
