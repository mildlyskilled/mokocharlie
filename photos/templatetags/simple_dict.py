from django import template

def key(d, key_name):
    return d[key_name]

register = template.Library()
key = register.filter('key', key)