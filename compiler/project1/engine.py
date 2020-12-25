from compiler.char_set import CharSet
from compiler.fa.finite_automata import FiniteAutomata
from compiler.fa.atom import State, Symbol


def build_email_fa():
    w = CharSet().range(65, 91).range(97, 123).range(48, 58).char('-')

    return FiniteAutomata(
        [State('1'), State('2'), State('3'), State('4'), State('5'), State('6')],
        [Symbol(w), Symbol('@'), Symbol('.')],
        State('1'),
        [State('6')],
        [
            [State('1'), Symbol(w), State('2')],
            [State('2'), Symbol(w), State('2')],
            [State('2'), Symbol('.'), State('1')],
            [State('2'), Symbol('@'), State('3')],
            [State('3'), Symbol(w), State('4')],
            [State('4'), Symbol(w), State('4')],
            [State('4'), Symbol('.'), State('5')],
            [State('5'), Symbol(w), State('6')],
            [State('6'), Symbol(w), State('6')],
            [State('6'), Symbol('.'), State('5')],
        ]
    )


def build_url_fa(strict_mode=False):
    domain_sigma = CharSet().range(65, 91).range(97, 123).range(48, 58).char('-')
    path_sigma = CharSet().range(65, 91).range(97, 123).range(48, 58).char('-').char('.').char('_')

    transitions = [
        [State('1'), Symbol('h'), State('2')],
        [State('1'), Symbol('w'), State('10')],
        [State('2'), Symbol('t'), State('3')],
        [State('3'), Symbol('t'), State('4')],
        [State('4'), Symbol('p'), State('5')],
        [State('5'), Symbol('s'), State('6')],
        [State('5'), Symbol(':'), State('7')],
        [State('6'), Symbol(':'), State('7')],
        [State('7'), Symbol('/'), State('8')],
        [State('8'), Symbol('/'), State('9')],
        [State('9'), Symbol('w'), State('10')],
        [State('9'), Symbol(domain_sigma.clone().not_char('w')), State('14')],
        [State('10'), Symbol('w'), State('11')],
        [State('11'), Symbol('w'), State('12')],
        [State('12'), Symbol('.'), State('13')],
        [State('13'), Symbol(domain_sigma), State('14')],
        [State('14'), Symbol(domain_sigma), State('14')],
        [State('14'), Symbol('.'), State('15')],
        [State('15'), Symbol(domain_sigma), State('16')],
        [State('16'), Symbol(domain_sigma), State('16')],
        [State('16'), Symbol('.'), State('15')],
        [State('16'), Symbol('/'), State('17')],
        [State('17'), Symbol(path_sigma), State('18')],
        [State('18'), Symbol(path_sigma), State('18')],
        [State('18'), Symbol('/'), State('17')],
    ]

    if not strict_mode:
        transitions.append([State('1'), Symbol(domain_sigma.clone().not_char('w').not_char('h')), State('14')])
        transitions.append([State('2'), Symbol(domain_sigma.clone().not_char('t')), State('14')])
        transitions.append([State('3'), Symbol(domain_sigma.clone().not_char('t')), State('14')])
        transitions.append([State('4'), Symbol(domain_sigma.clone().not_char('p')), State('14')])
        transitions.append([State('5'), Symbol(domain_sigma.clone().not_char('s')), State('7')])
        transitions.append([State('6'), Symbol(domain_sigma), State('14')])
        transitions.append([State('10'), Symbol(domain_sigma.clone().not_char('w')), State('14')])
        transitions.append([State('11'), Symbol(domain_sigma.clone().not_char('w')), State('14')])
        transitions.append([State('12'), Symbol(domain_sigma), State('14')])

    return FiniteAutomata(
        [State(str(i)) for i in range(1, 19)],
        [Symbol(domain_sigma), Symbol(path_sigma), Symbol(':'), Symbol('/')],
        State('1'),
        [State('16'), State('18')],
        transitions
    )