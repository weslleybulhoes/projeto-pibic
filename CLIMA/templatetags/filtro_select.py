from django import template

register = template.Library()
#dados_A303_MACEIO_2010-01-01_2020-12-31
@register.filter(name="concatenando_string")
def concatenando_string(string):
    if string[10:11]=="_":
        return string[11:-26]
    else:
        return string


@register.filter(name="removendo_string")
def removendo_string (string):
    string = string.replace("HORARIO","DIÁRIA")
    string = string.replace("HORARIA", "DIÁRIA")
    string = string.replace(",", ".")
    string = string.replace("NA HORA ANT", "DIÁRIA")
    string = string.replace("MAX", "RELATIVA")
    return string