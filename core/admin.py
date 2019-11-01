from django.contrib import admin
# from django.utils.html import format_html
# from mptt.admin import DraggableMPTTAdmin
from .models.technics import TechnicsCategory, TechnicsType, TechnicsSubType, Auto
from .models.order import Order, OrderPoint, OrderTechnics, OrderUnitTech, OrderProlongation


# class CategoryMPTTModelAdmin(DraggableMPTTAdmin):
#     mptt_level_indent = 20
#     list_display = ('tree_actions', 'indented_title')
#     list_display_links = ('indented_title',)


admin.site.register(TechnicsCategory)
admin.site.register(TechnicsType)
admin.site.register(TechnicsSubType)
admin.site.register(Auto)
admin.site.register(Order)
admin.site.register(OrderPoint)
admin.site.register(OrderTechnics)
admin.site.register(OrderUnitTech)
admin.site.register(OrderProlongation)
