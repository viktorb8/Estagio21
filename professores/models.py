from django.db import models

class Professores(models.Model):
    id = models.AutoField(primary_key=True)
    nome_professor = models.CharField(max_length=200)
    sobrenome_professor = models.CharField(max_length=200)
    nome_completo = models.CharField(max_length=400, blank=True)
    email = models.EmailField(max_length=200)
    def __str__(self):
        return self.nome_completo