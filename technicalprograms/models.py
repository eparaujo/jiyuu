from django.db import models
from graduations.models import Graduation
from examcategories.models import ExamCategory


# Create your models here.
class TechnicalProgram(models.Model):

    STYLE_CHOICES = [
        ("SHOTOKAN", "Shotokan"),
        ("GOJORYU", "Gojo-Ryu"),
        ("WADORYU", "Wado-Ryu"),
        ("SHITORYU", "Shito-Ryu"),

    ]

    category = models.OneToOneField(ExamCategory, on_delete=models.CASCADE, related_name="technical_program",)
    style = models.CharField(max_length=30, choices=STYLE_CHOICES, default="SHOTOKAN",)
    target = models.CharField(max_length=100, blank=True, null=True, help_text="Ex.: 7º Kyu → 6º Kyu",)
    description = models.TextField(blank=True, null=True,)
    active = models.BooleanField(default=True,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = "Programa Técnico"
        verbose_name_plural = "Programas Técnicos"
        ordering = [
            "category__to_graduation__order",
            "category__to_graduation__id",
        ]

    def __str__(self):
        return f"{self.category.name_category} - {self.get_style_display()}"

# aqui temos a classe que registrará o conteúdo do programa técnico
class TechnicalProgramItem(models.Model):

    MODALITY_CHOICES = [
        ("KIHON", "Kihon"),
        ("KATA", "Kata"),
        ("KUMITE", "Kumite"),
    ]

    program = models.ForeignKey(TechnicalProgram, on_delete=models.CASCADE, related_name="items",)
    modality = models.CharField(max_length=20, choices=MODALITY_CHOICES,)
    title = models.CharField(max_length=200,)
    description = models.TextField(blank=True, null=True,)
    sequence = models.PositiveIntegerField(default=1,)
    mandatory = models.BooleanField(default=True,)
    active = models.BooleanField(default=True,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = "Item do Programa Técnico"
        verbose_name_plural = "Itens do Programa Técnico"
        ordering = [
            "modality",
            "sequence",
        ]

    def __str__(self):
        return f"{self.get_modality_display()} - {self.title}"    