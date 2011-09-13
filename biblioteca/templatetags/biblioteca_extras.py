from django import template

import re

register = template.Library()

@register.inclusion_tag('biblioteca/box_copia.html')
def box_copia(copia):
    return {'copia' : copia}

@register.filter
def timedelta(value, arg):
    def get_repl(matchobj):
        argspecs =  { 'd':  'days'
                    , 's':  'seconds'
                    , 'm':  'minutes'
                    , 'h':  'hours'
                    , 'w':  'weeks'
                    }
        if argspecs.has_key( matchobj.group(1) ):
            key = argspecs[ matchobj.group(1) ]
            return str( getattr(value, key) ) 
        else:
            return matchobj.group(0)
        
    return re.sub(r'%(\w)', get_repl, arg)
    

