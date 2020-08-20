# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class potrero(models.Model):
  _name = "coop1.potrero"
  _description = "Potrero"
  _rec_name = "nombre_potrero"


  # Funcion que autocompleta el campo Socio, para saber el socio dueño de la parcela
  @api.one
  @api.depends('parcela_id')
  def get_socio(self):
    if self.parcela_id is not False:
      socio = self.parcela_id.cabana_id.socio_id
      self.nombre_socio = socio.nombre
      
      
      

  nombre_potrero = fields.Char(string="Nombre del potrero", required = True)
  area = fields.Float(string="Area del potrero")
  material = fields.Char(string="Material del potrero")
  area_pasto_natural = fields.Float(string="Area de pastos naturales")
  
  #socio = fields.Char(string="Socio", compute="get_socio", store=True)
  
  # Pasto cultivado
  area_pasto_cultivado = fields.Float(string="Area de pastos cultivados")
  tipo_pasto_cultivado = fields.Char(string="Tipo de pasto cultivado")
  ahno_instalacion = fields.Integer(string="Año de instalacion")
  riego_semana = fields.Integer(string="Nº riegos por semana")
  tipo_riego = fields.Selection([
    ('aspersion', 'Aspersion'),
    ('graverdad', 'Gravedad'),
    ('otros', 'otros'),
  ], default="aspersion", string="Tipo de riego")

  num_corte = fields.Integer(string="Nº corte o pastoreo/año")
  
  
  #Rendimiento
  peso_x_m2 = fields.Float(string="Peso por m2")
  densidad = fields.Float(string="Densidad")
  longitud = fields.Float(string="Longitud")
  
  # Fuente de agua
  fuente_agua = fields.Selection([
    ('manantial', 'Manantial/Ojo de agua'),
    ('rio', 'Rio'),
    ('subterraneo', 'Subterraneo'),
    ('otros', 'otros'),
  ], string="Fuente de agua")

  
  # Aforo de agua
  aforo_agua = fields.Float("Aforo de agua")
  epoca_lluvia = fields.Float("Epoca de lluvia L/s")
  epoca_estiage = fields.Float("Epoca de estiage L/s")
  
  observaciones = fields.Text("Observaciones")  
  
  
  area_bofedales = fields.Float("Area de bofedales totales")
  area_ereazeos = fields.Float("Area de zonas ereazeos totales")
  otros = fields.Float("Otros")     # Falta definir
  
  
  parcela_id = fields.Many2one('coop1.parcela', string="Parcela", required=True)
  
  # obtencion del socio
  nombre_socio = fields.Char(string="Socio", compute="get_socio")
  
  
  
