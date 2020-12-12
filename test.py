# Statement([1, 2])






# g = Grammar(
#     [Variable('A'), Variable('B')],
#     [Terminal('a'), Terminal('b')],
#     Variable('A'),
#     [
#         [Variable('A'), Statement()]
#     ]
# )

# s1 = Statement([Variable('A'), Variable('a')])
# s2 = Statement([Variable('B'), Variable('b')])
# print(Statements([s1, s2]))


# s1 = Statement([Variable('A'), Terminal('a')])
# s2 = Statement([Variable('B'), Terminal('b')])
#
# statements = Statements([s1, s2])
# print(statements.value)
# s = s1 * s2

# print(s.value)
# print(list(map(lambda exp: exp.value, s.value)))
