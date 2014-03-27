from django import template

def yt_thumbnail(d, id):
    return

register = template.Library()
key = register.filter('key', yt_thumbnail)