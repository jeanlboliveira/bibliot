from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# Create your models here.
class Livro(models.Model):

    titulo = models.CharField(_("Título"), max_length=512)
    slug = models.SlugField(_("Slug"), blank=True, unique=True) # Versão do título formatada para ser usada na URL
    categoria = models.ManyToManyField("catalogo.Categoria", verbose_name=_("Categoria"), related_name='livros')
    autor = models.ForeignKey("catalogo.Autor", verbose_name=_("Autor"), on_delete=models.PROTECT)
    capa = models.ImageField(_("Capa"), upload_to='capas/')
    isbn = models.CharField(_("ISBN"), max_length=17, unique=True)
    preco = models.DecimalField(_("Preço"), max_digits=5, decimal_places=2)
    sinopse = models.TextField(_("Sinopse"))
    lancamento = models.DateField(_("Lançamento"), auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = _("livro")
        verbose_name_plural = _("livros")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.titulo} - {self.autor.nome}'

class Autor(models.Model):

    nome = models.CharField(_("Nome"), max_length=512)
    slug = models.SlugField(_("Slug"), blank=True, unique=True) # Versão do título formatada para ser usada na URL
    descricao = models.TextField(_("Descrição"), blank=True)
    nascimento = models.DateField(_("Nascimento"))
    morte = models.DateField(_("Morte"), null=True, blank=True)
    foto = models.ImageField(_("Foto"), upload_to='autores_foto/', blank=True, null=True)

    class Meta:
        verbose_name = _("autor")
        verbose_name_plural = _("autores")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(_("Nome"), max_length=256)
    slug = models.SlugField(_("slug"), blank=True, unique=True)
    descricao = models.TextField(_("Descrição"))
    ativa = models.BooleanField(_("Ativa"), default=True)
    ordem = models.PositiveIntegerField(_("Ordem"), default=0)
    

    class Meta:
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")
        ordering = ['ordem', 'nome'] # Funciona como um 'order by'.

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome



