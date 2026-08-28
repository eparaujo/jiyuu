from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.TechnicalProgram)
class TechnicalProgramAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "style",
        "target",
        "active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "style",
        "active",
    )

    search_fields = (
        "category__name_category",
        "target",
        "description",
    )

    ordering = (
        "category__name_category",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Programa Técnico",
            {
                "fields": (
                    "category",
                    "style",
                    "target",
                    "description",
                    "active",
                )
            },
        ),
        (
            "Informações do Sistema",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(models.TechnicalProgramItem)
class TechnicalProgramItemAdmin(admin.ModelAdmin):
    list_display = (
        "program",
        "modality",
        "title",
        "sequence",
        "mandatory",
        "active",
        "created_at",
    )

    list_filter = (
        "modality",
        "mandatory",
        "active",
    )

    search_fields = (
        "program__category__name_category",
        "title",
        "description",
    )

    ordering = (
        "program",
        "modality",
        "sequence",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Conteúdo Técnico",
            {
                "fields": (
                    "program",
                    "modality",
                    "title",
                    "description",
                    "sequence",
                    "mandatory",
                    "active",
                )
            },
        ),
        (
            "Informações do Sistema",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )