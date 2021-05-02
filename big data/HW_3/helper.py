from random import randint
import sys

fields = set()
is_filled_citilink = False
is_filled_dns = False
CITILINK_FILENAME = 'citilink.json'
DNS_FILENAME = 'dns.json'


def resolve(**kwargs):
    return kwargs['resolve_fun'](kwargs['vals'])


def get_longest_val(vals):
    val1, src1, val2, src2 = vals[0], vals[1], vals[2], vals[3]
    return val1 if len(val1) > len(val2) else val2


def get_random_val(vals):
    val1, src1, val2, src2 = vals[0], vals[1], vals[2], vals[3]
    return val1 if randint(0, 1) == 0 else val2


def get_avg_val(vals):
    val1, src1, val2, src2 = vals[0], vals[1], vals[2], vals[3]
    return (val1 + val2) / 2


def get_dns_val(vals):
    val1, src1, val2, src2 = vals[0], vals[1], vals[2], vals[3]
    return val1 if src1 == DNS_FILENAME else val2


def choose_not_none(vals):
    val1, src1, val2, src2 = vals[0], vals[1], vals[2], vals[3]
    return val1 if val2 is None else val2


resolver_funcs = {
    "duplicate_id": get_random_val,
    "Технологический процесс": get_longest_val,
    "Максимальная частота оперативной памяти": get_dns_val,
    "Объем кэша L3": get_random_val,
    "Минимальная частота оперативной памяти": get_dns_val,
    "Количество потоков": get_avg_val,
    "Тип памяти": get_random_val,
    "Название": get_longest_val,
    "Сокет": get_dns_val,
    "Интегрированное графическое ядро":  get_random_val,
    "Тепловыделение": get_random_val,
    "Ядро": get_longest_val,
    "Количество ядер": get_avg_val,
    "Встроенный контроллер PCI Express": get_longest_val}
