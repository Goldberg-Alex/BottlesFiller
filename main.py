import dataclasses
import json
from typing import Optional

################################ Define the problem #############################################
capacities = [3, 5]
required_amount = 4
#################################################################################################

Capacity = int
Amount = int


@dataclasses.dataclass
class State:
    bottles: dict[Capacity, Amount]
    prev_state: Optional["State"]
    action: Optional[callable] = None
    action_string: str = ""

    def __eq__(self, other):
        return self.bottles == other.bottles

    def __hash__(self):
        return hash(tuple((capacity, amount) for capacity, amount in self.bottles.items()))

    def __repr__(self):
        return json.dumps(self.bottles)

    def is_contains(self, amount) -> bool:
        return amount in self.bottles.values()



    def fill(self, capacity) -> "State":
        new_state = State(bottles=self.bottles.copy(), prev_state=self)
        new_state.bottles[capacity] = capacity
        new_state.action = lambda: self.fill(capacity)
        new_state.action_string = f"fill {capacity}"
        return new_state

    def empty(self, capacity) -> "State":
        new_state = State(bottles=self.bottles.copy(), prev_state=self)
        new_state.bottles[capacity] = 0
        new_state.action = lambda: self.empty(capacity)
        new_state.action_string = f"empty {capacity}"
        return new_state

    def transfer(self, source, target) -> "State":
        amount = min(self.bottles[source], target - self.bottles[target])

        new_state = State(bottles=self.bottles.copy(), prev_state=self)

        new_state.bottles[source] -= amount
        new_state.bottles[target] += amount
        new_state.action = lambda: self.transfer(source=source, target=target)

        new_state.action_string = f"move {amount} from {source} to {target}"

        assert source >= new_state.bottles[source] >= 0
        assert target >= new_state.bottles[target] > 0

        return new_state

    def is_valid(self):
        # apply the action from the previous state - this should return our current state, therefore our state is valid
        if self.prev_state is None:
            #inital state is always valid
            return True

        new_state = self.action()
        return new_state == self


class Solver:
    def solve(self, capacities: list[Capacity], required_amount: int) -> (list[State], set[State]):
        # sanity checks
        if required_amount > max(capacities):
            return [], set()

        initial_state = State(bottles={capacity: 0 for capacity in capacities}, prev_state=None, action=None)

        open_states = set()
        closed_states = set()

        open_states.add(initial_state)
        final_state = None

        while len(open_states) > 0:
            curr_state = open_states.pop()
            # print(f"{curr_state=}")

            if curr_state.is_contains(required_amount):
                final_state = curr_state
                break

            closed_states.add(curr_state)

            new_states: set[State] = self._generate_states(curr_state)
            # print(f"{new_states=}")

            # remove states already created
            filtered_new_states = new_states.difference(closed_states)
            filtered_new_states = filtered_new_states.difference(open_states)

            open_states.update(filtered_new_states)

        if final_state is None:
            return [], closed_states

        # generate the order of operations to solve
        solution_state_list: list[State] = []
        while True:
            solution_state_list.append(final_state)
            final_state = final_state.prev_state

            if final_state.prev_state is None:
                solution_state_list.append(final_state)
                break

        solution_state_list = solution_state_list[::-1]
        return solution_state_list, closed_states

    def _generate_states(self, state: State) -> set[State]:
        new_states = set()

        # fill each non-full bottle
        for capacity, amount in state.bottles.items():
            if amount == capacity:
                continue

            new_state = state.fill(capacity)
            new_states.add(new_state)

        # empty each non-empty bottle
        for capacity, amount in state.bottles.items():
            if amount == 0:
                continue

            new_state = state.empty(capacity)
            new_states.add(new_state)

        # transfer from each non-empty to each non-full
        for source_capacity, source_amount in state.bottles.items():
            if source_amount == 0:
                continue

            for target_capacity, target_amount in state.bottles.items():
                if target_amount == target_capacity:
                    continue

                new_state = state.transfer(source=source_capacity, target=target_capacity)
                new_states.add(new_state)

        return new_states

def print_solution(solution, closed_states, required_amount):
    if len(solution) == 0:
        print(f"no solution found, checked {len(closed_states)} states")

    str_to_print = f"Solution for capacities={list(solution[0].bottles.keys())} {required_amount=} found with {len(solution)} steps, total states checked={len(closed_states)}: \n"
    for state in solution:
        str_to_print = str_to_print + f" -> {state.action_string} \n{state}"

    print(str_to_print)


def main():
    solution_state_list, closed_states = Solver().solve(capacities=capacities, required_amount=required_amount)
    print_solution(solution=solution_state_list, closed_states=closed_states)

if __name__ == '__main__':
    main()
