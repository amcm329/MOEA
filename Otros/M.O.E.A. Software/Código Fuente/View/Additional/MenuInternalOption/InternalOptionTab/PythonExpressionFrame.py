#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Aarón Martín Castillo Medina"
__credits__ = ["Aarón Martín Castillo Medina","Dra. Katya Rodríguez Vázquez"]

__version__ = "1.0"
__mantainer__ = "Aarón Martín Castillo Medina"
__email__ = "amcm329@hotmail.com"
__status__ = "Production"


import Tkinter as tk
from ExpressionFrame import ExpressionFrame


class PythonExpressionFrame(tk.Frame):
      """
         | Realiza la fusión de Canvas y ExpressionFrame, debido a que, cuando se agregan 
          numerosas variables al ExpressionFrame, se debe insertar una barra de desplazamiento
          para poder acceder a aquéllos que se encuentren hasta abajo. Dentro del ambiente
          de Tkinter, el elemento más sencillo para lograr este efecto es un Canvas, por ello 
          se anida el ExpressionFrame al Canvas.

         :param parent: Frame padre al que pertenece.
         :param features: Conjunto de técnicas con sus respectivos parámetros para que
                          se puedan cargar automáticamente en este Frame **(véase
                          Controller/XML/PythonExpressions.xml)**.

         :type parent: Tkinter.Frame
         :type features: Dictionary
         :returns: Tkinter.Frame
         :rtype: Instance
      """


      def __init__(self,parent,features):
          #Se crea un Frame principal, el cual tendrá al Canvas como hijo que a su vez
          #tendra al ExpressionFrame como hijo.
          tk.Frame.__init__(self,parent)

          #La barra de desplazamiento de la que se habló aparece y desaparece automáticamente
          #cuando el número de variables insertadas excede el tamaño del Frame. Este es el número
          #máximo de variables tolerado ANTES de insertar la barra de desplazamiento.
          self.__row_limit = 6
          
          #Este es el elemento gráfico que permite la inserción de una barra de desplazamiento.
          #Un Frame no puede contener tal elemento de manera nativa.
          self.__canvas = tk.Canvas(self)

          #A continuación se declara la barra de desplazamiento, se colocará de manera vertical y 
          #se asocia al Canvas.
          self.__scrollbar = tk.Scrollbar(self,orient = tk.VERTICAL,command = self.__canvas.yview)

          #Se configura al Canvas con las caracterísitas de la barra de desplazamiento.
          self.__canvas.configure(yscrollcommand = self.__scrollbar.set)

          #Ahora se crea el ExpressionFrame cuyo Padre será el Canvas.          
          self.__expression_frame = ExpressionFrame(self.__canvas,features)  

          #Se le añade un evento al ExpressionFrame que activará la barra de desplazamiento cada vez que
          #el número de casillas sobrepase el límite del Frame.
          self.__expression_frame.bind("<Configure>",self.__activate_scroll)

          #Se coloca el Frame dentro del Canvas.
          self.__expression_frame.pack(side = tk.TOP,fill = tk.BOTH,expand = True)

          #La siguiente instrucción le indica al Canvas que cree una ventana que contenga al 
          #ExpressionFrame y que se desplazará hacia abajo cuando se quiera 
          #hacer desplazamiento con la barra.          
          self.__canvas.create_window((20,0),window = self.__expression_frame,anchor = tk.NW)   

          #Se coloca el Canvas en referencia al contenedor Padre.
          self.__canvas.grid(row = 0,column = 0,columnspan = 2,rowspan = 2,sticky = tk.N + tk.S + tk.W + tk.E)
          
          #Estas opciones sirven para colocar apropiadamente el Canvas, son opciones
          #que permiten traslapar en este caso la columna y el renglón 0 en una unidad.
          self.grid_rowconfigure(0,weight = 1)
          self.grid_columnconfigure(0,weight = 1)

          #Dependiendo de la cantidad de elementos precargados se activa
          #la barra de desplazamiento (Scrollbar).
          self.__activate_scroll()
            
            
      def __update_scrollbar(self,event = None):
          """
             .. note:: Este método es privado.  

             Actualiza la barra de desplazamiento de acuerdo al número de elementos
             existentes en el Frame, esto para poder hacer un recorrido apropiado de 
             la barra.

             :param event: Elemento que ejecutó esta función.
             :type event: String
          """

          #Ajusta la barra de desplazamiento de acuerdo al número de elementos (casillas en este caso)
          #que se encuentran presentes en el Frame.
          self.__canvas.configure(scrollregion = self.__canvas.bbox("all"))


      def __activate_scroll(self,event = None):
          """
             .. note:: Este método es privado.  
            
             Actualiza la barra de desplazamiento y con base en esta acción
             la activa o desactiva.
           
             :param event: Elemento que ejecutó esta función.
             :type event: String
          """

          #Se toma el numero actual de casillas en el Frame y se actualiza la 
          #barra de desplazamiento con base en éste.
          current_rows = self.__expression_frame.get_current_elements()
          self.__update_scrollbar()

          #Si se ha llegado al límite de casillas + 1, se activa la barra de 
          #desplazamiento.
          if current_rows == self.__row_limit + 1: 
             self.__scrollbar.grid(row = 0,column = 2,sticky = tk.N + tk.S)
 
          #En otro caso se esconde la barra de desplazamiento.
          elif current_rows == self.__row_limit:
               self.__scrollbar.grid_forget()
