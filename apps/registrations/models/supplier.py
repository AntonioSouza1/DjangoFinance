from django.db import models

class Supplier(models.Model):
    PERSON = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica')
    ]

    BRAZIL_UF_CHOICES = [
        ('', 'Selecione'),
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]

    SITUATIONS = [
        ('A', 'Ativo'),
        ('I', 'Inativo'),
    ]

    #Dados
    corporate_name = models.CharField(max_length=100)
    fantasy_name = models.CharField(max_length=100)
    responsible = models.CharField(max_length=100, null=True, blank=True)
    type_person = models.CharField(max_length=2, choices=PERSON, default='PF')
    cpf_cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)
    rg_ie = models.CharField(max_length=14, unique=True, null=True, blank=True)

    #contato
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True)
    cell_phone = models.CharField(null=True, blank=True)

    #endereço
    cep = models.CharField(max_length=9, null=True, blank=True)
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    number = models.CharField(null=True, blank=True)
    complement = models.CharField(max_length=100, null=True, blank=True)
    neighborhood = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=2, choices=BRAZIL_UF_CHOICES, null=True, blank=True) #Apenas UF

    #outros
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    observation = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=SITUATIONS, default='A')

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['-updated_at']

    def __str__(self):
        return self.corporate_name
