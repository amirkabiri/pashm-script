from compiler.fa.finite_automata import FiniteAutomata


class MultiDFARunner:
    def __init__(self, *machines: FiniteAutomata):
        self.machines = machines
        self.tables = list(map(lambda machine: machine.table, machines))
        self.cursors = self.create_cursors()
        self.terminals = list(map(lambda machine: dict(map(lambda state: [state, state in machine.terminals], machine.states)), machines))

    def reset(self):
        self.cursors = self.create_cursors()
        return self

    def create_cursors(self):
        cursors = dict()

        for i in range(len(self.machines)):
            cursors[i] = self.machines[i].start

        return cursors

    def read(self, char: str):
        new_cursors = dict()

        for i in self.cursors:
            current = self.cursors[i]
            try:
                new_cursors[i] = self.tables[i][current][char][0]
            except:
                pass

        self.cursors = new_cursors

        return self

    @property
    def stucked(self):
        return len(self.cursors) == 0

    @property
    def accepted(self):
        result = []

        for i in self.cursors:
            cursor = self.cursors[i]

            if self.terminals[i][cursor]:
                result.append(i)

        return result

    @staticmethod
    def run(machines, input, on_match):
        i = 0
        dfa_runner = MultiDFARunner(*machines)

        while i < len(input):
            j = i
            found = ''
            accepted_string = ['' for _ in range(len(machines))]

            while j < len(input):
                dfa_runner.read(input[j])

                if dfa_runner.stucked:
                    break

                found += (input[j])
                j += 1

                for machine_index in dfa_runner.accepted:
                    accepted_string[machine_index] = found

            filtered_accepted_string = list(filter(
                lambda item: len(item[1]),
                [[i, string] for i, string in enumerate(accepted_string)]
            ))
            if len(filtered_accepted_string):
                skip = on_match(dict(filtered_accepted_string), i)

                i += skip
            else:
                # i += 1
                i += len(found) or 1

            dfa_runner.reset()