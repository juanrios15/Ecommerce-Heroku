from django.db import models
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity

class EtiquetasManager(models.Manager):
    
    def etiquetas_usuarios(self,usuarioslug):
        #Va a retornar en que etiquetas ha comentado determinado usuario
        return self.filter(tags_pubs__user__slug=usuarioslug).distinct() 

class FotosManager(models.Manager):
    def fotos_publicacion(self,slug):
        return self.filter(
            publicacion__slug=slug)

class ComentariosManager(models.Manager):
    def comentarios_publicacion(self,slug):
        return self.filter(
            Publicacion__slug=slug)
        

class PublicacionesManager(models.Manager):
    
    def buscar_pub(self,kword,etiqueta,orden):
        print("kword: ",kword,"etiqueta: ",etiqueta,"orden: ",orden)
        #busqueda por palabra clave y por filtro por etiquetas
        if orden == "visitas":
            orderby = '-visitas'
        elif orden == "antiguos":
            orderby = 'created_at'
        else:
            orderby = '-created_at'
        
        if len(etiqueta) >0 and etiqueta!="todos":
            return self.filter(
                etiquetas__nombre = etiqueta,
                titulo__icontains = kword,
                publico=True
            ).order_by(orderby)
        
        else:
            return self.filter(
                titulo__icontains = kword,
                publico=True
            ).order_by(orderby)
        
        
        
        
        
        
        
        
        #UTILIZANDO EL TRIGRAM::::
        # if kword:
        #     if len(etiqueta) >0:
        #         return self.annotate(
        #             similarity=TrigramSimilarity('titulo', kword),
        #             ).filter(similarity__gt=0.2,
        #                      etiquetas__nombre = etiqueta,
        #                      publico=True,
                             
        #             ).order_by('-similarity')
                
        #         # return self.filter(
        #         #     etiquetas__nombre = etiqueta,
        #         #     titulo__trigram_similar = kword,
        #         #     publico=True,
                    
        #         # ).order_by(orderby)
            
        #     else:
                
        #         return self.annotate(
        #             similarity=TrigramSimilarity('titulo', kword),
        #             ).filter(similarity__gt=0.2,
        #                      publico=True,
                             
        #             ).order_by('-similarity')
        #         # return self.filter(
        #         #     titulo__trigram_similar = kword,
        #         #     publico=True
        #         # ).order_by(orderby)
        # else:
        #     return self.all().order_by('-created_at')
            

    