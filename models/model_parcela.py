# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class parcela(models.Model):
  _name = "coop1.parcela"
  _description = "Parcela de la cabaña"
  _rec_name = "nombre_parcela"
  
  
  # Funcion que cuenta la cantidad de potreros de la parcela
  @api.one
  @api.depends('potreros')
  def count_potreros(self):
    if self.potreros is not False:
      self.num_potreros = self.env["coop1.potrero"].search_count([('parcela_id', '=', self.id)])
  
  nombre_parcela = fields.Char(string="Nombre de la parcela", required = True)
#  num_potrero = fields.Integer(string = "Nº potreros")       # esto se debe eliminar
  area = fields.Float(string="Area")
    
  # condicion de tenencia de tierras (de la parcela)
  cond_tenencia_tierras = fields.Selection([
    ('posesionario', 'Posesionario'),
    ('propietario', 'Propietario'),
    ('comunero', 'Comunero'),
    ('otro', 'Otro'),
  ], default="posesionario", string="Condicion de tenencia de tierras")

  # Campos computados
  num_potreros = fields.Integer(string="Cantidad potreros", compute="count_potreros", store=True)
  
  # Campos relacionales

  cabana_id = fields.Many2one('coop1.cabana', string="Rebaño/Cabaña", required = True)
  
  potreros = fields.One2many('coop1.potrero', 'parcela_id', string="Potreros")

