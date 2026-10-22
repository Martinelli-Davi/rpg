from django.db import models
from django.contrib.auth.models import User

# Sua classe de Campanha já existente
class Campanha(models.Model):
    nome = models.CharField(max_length=200)
    sistema = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    mestre = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campanhas_criadas')
    jogadores = models.ManyToManyField(User, related_name='campanhas_vinculadas', blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Personagem(models.Model):
    # Vinculação e Tipo
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, related_name='fichas')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='minhas_fichas')
    eh_npc = models.BooleanField(default=False)
    eh_criatura = models.BooleanField(default=False)

    # Cabeçalho
    nome = models.CharField(max_length=100)
    raca = models.CharField(max_length=50)
    nivel = models.PositiveIntegerField(default=1)

    # Atributos Base
    attr_parautilitario = models.IntegerField(default=1)
    attr_intelecto = models.IntegerField(default=1)
    attr_psique = models.IntegerField(default=1)
    attr_fisico = models.IntegerField(default=1)
    attr_motoras = models.IntegerField(default=1)

    # Perícias - Intelecto
    skill_logica = models.IntegerField(default=0)
    skill_atualidades = models.IntegerField(default=0)
    skill_diplomacia = models.IntegerField(default=0)
    skill_drama = models.IntegerField(default=0)
    skill_conceitualizacao = models.IntegerField(default=0)
    skill_calculo_visual = models.IntegerField(default=0)

    # Perícias - Psique
    skill_vontade = models.IntegerField(default=0)
    skill_pressentimento = models.IntegerField(default=0)
    skill_empatia = models.IntegerField(default=0)
    skill_autoridade = models.IntegerField(default=0)
    skill_colmeia = models.IntegerField(default=0)
    skill_sugestao = models.IntegerField(default=0)

    # Perícias - Físico
    skill_resistencia = models.IntegerField(default=0)
    skill_limite_dor = models.IntegerField(default=0)
    skill_luta = models.IntegerField(default=0)
    skill_eletroquimica = models.IntegerField(default=0)
    skill_arrepio = models.IntegerField(default=0)
    skill_memoria_muscular = models.IntegerField(default=0)

    # Perícias - Motoras
    skill_coord_motora = models.IntegerField(default=0)
    skill_percepcao = models.IntegerField(default=0)
    skill_veloc_reacao = models.IntegerField(default=0)
    skill_destreza = models.IntegerField(default=0)
    skill_manufatura = models.IntegerField(default=0)
    skill_compostura = models.IntegerField(default=0)

    # Perícias - Parautilitário
    skill_arquetipo = models.IntegerField(default=0)
    skill_geometria_alma = models.IntegerField(default=0)
    skill_sacrificio_astral = models.IntegerField(default=0)
    skill_timor_mortis = models.IntegerField(default=0)
    skill_ritos = models.IntegerField(default=0)
    skill_alma = models.IntegerField(default=0)

    # Campos de controle de vida/recursos atuais (opcional para tracking)
    estabilidade_atual = models.IntegerField(default=10)
    essencia_atual = models.IntegerField(default=0)
    cansaco_atual = models.IntegerField(default=10)

    def __str__(self):
        tipo = "NPC" if self.eh_npc else "Player"
        return f"{self.nome} ({tipo}) - {self.campanha.nome}"

    # Lógica de cálculo (Opcional: replicar as fórmulas do JS no Python)
    @property
    def estabilidade_max(self):
        fator_nivel = max(0, self.nivel - 1)
        base = 10 + (10 * self.skill_resistencia) + self.attr_fisico
        bonus = fator_nivel * (self.attr_fisico + self.skill_resistencia)
        return base + bonus

    @property
    def essencia_max(self):
        fator_nivel = max(0, self.nivel - 1)
        base = self.attr_parautilitario + (5 * self.skill_alma)
        bonus = fator_nivel * (self.attr_parautilitario + self.skill_alma)
        return base + bonus

    @property
    def cansaco_max(self):
        fator_nivel = max(0, self.nivel - 1)
        base = 10 + (self.skill_vontade * 2)
        bonus = fator_nivel * (self.skill_vontade + self.attr_psique)
        return base + bonus