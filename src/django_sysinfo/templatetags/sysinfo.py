# -*- coding: utf-8 -*-
from django.template import Context, Library

register = Library()


@register.simple_tag(takes_context=True)
def section(context, section_name):
    try:
        data = context['infos'][section_name].items()
    except KeyError as e:
        accepted = ",".join(context['infos'].keys())
        raise KeyError("{0}: ({1})".format(e, accepted))
    name = section_name.lower()

    ctx = {
        'name': name,
        'section': data
    }

    filename = 'admin/sysinfo/%s_section.html' % name
    t = context.template.engine.get_template(filename)
    return t.render(Context(ctx))
