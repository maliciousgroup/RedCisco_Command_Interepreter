from prettytable import PrettyTable


def create_table(field_names: list, field_values: list) -> str:
    t = PrettyTable()

    t.border = False
    t.padding_width = 2
    t.field_names = field_names

    sep = []
    for _value in field_names:
        sep += ['-' * len(_value)]
    t.add_row(sep)

    for _value in field_values:
        t.add_row(_value)
        t.align = 'l'

    return "{}".format(t.get_string())
