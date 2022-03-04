from Dieta import Producto

class Fitness:
      def __init__(self, listaProducto, meta, tipoMeta):
            self.listaProducto = listaProducto
            self.meta = meta
            self.tipoMeta = tipoMeta
            self.individuo = self.CrearIndividuo(listaProducto)
            self.aptitud = self.Aptitud(listaProducto,tipoMeta)
            
            
      def CrearIndividuo(self, listaProducto):
            individuo = ""
            for producto in listaProducto:
                  binario = format(producto.cantidad)
                  while(len(binario) < 4):
                        binario = '0' + binario
                  individuo += binario
            return individuo
                  
      def Aptitud(self, listaProducto, tipoMeta):
            aptitud = 0
            for producto in listaProducto:
                  if producto.calorias == "CALORIAS" or producto.proteinas == "PROTEINAS":
                        continue
                  else:
                        if tipoMeta == "C":
                              aptitud += int(producto.calorias) * int(producto.cantidad)
                        else:
                              aptitud += int(producto.proteinas) * int(producto.cantidad)
            return aptitud
          
      def ControlPorcentaje(self,porcentaje):
            self.porcentaje = porcentaje
            
      def ControlGrafico(self,rango):
            self.rango = rango
      
      def ActualizarBinomio(self,binario):
            self.individuo = binario
            contador = 0
            for i in range(0,len(binario),4):
                  nuevoBinario = str(binario[i:i+4])
                  self.listaProducto[contador].cantidad = int(nuevoBinario,2)
                  contador += 1
            self.aptitud = self.Aptitud(self.listaProducto, self.tipoMeta)
      