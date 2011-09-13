from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.forms.util import flatatt
from django.forms.widgets import Widget
class ContentEditableWidget(Widget):
    def __init__(self, attrs=None):
        default_attrs = { 'contenteditable' : 'true', 'class' : 'editable' }
        if attrs != None:
            default_attrs.update(attrs)
        super(ContentEditableWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<div%s>%s</div>' % (flatatt(final_attrs), conditional_escape(force_unicode(value))))


