from django.contrib import admin
from .models import OptimizedRoute

# Register your models here.

@admin.register(OptimizedRoute)
class OptimizedRouteAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'best_distance', 'num_ants', 'iterations', 'evaporation_rate', 'alpha', 'beta']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False  # No permitir crear manualmente desde el admin
