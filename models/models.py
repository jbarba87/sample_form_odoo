# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class socio(models.Model):
  _name = "coop1.socio"
  _description = "Socio de la cooperativa"
  _rec_name = "nombre"

   # Restriccion SQL para que el DNI sea campo unico
  _sql_constraints = [
    ('DNI_unico', 'unique (dni)', 'Ya existe un Socio con ese numero de DNI'),
  ]

  # Restriccion para que el DNI solo tenga 8 caracteres numericos
  @api.constrains('dni')
  def check_dni(self):
    for rec in self:
      if len(rec.dni) < 8:
        raise ValidationError('El campo DNI debe tener 8 digitos.')
      if (not rec.dni.isnumeric()):
        raise ValidationError('El campo DNI no debe contener letras.')


  @api.constrains('personas_nucleo')
  def check_personas_nucleo(self):
    if self.personas_nucleo is not False:
      if self.personas_nucleo < 0 or self.personas_nucleo > 25:
        raise ValidationError('En el campo Nº de nucleo familiar ingrese un valor entre 0 y 25.')


  # Funcion de autocompletado de la edad en base a la fecha de nacimiento
  # Ojo que la el campo odoo.fields.Date es string por lo que debe convertir en datetime
  # Tener en cuenta que se debe ingresar la fecha en formato mm/dd/aaaa
  @api.one
  @api.depends('fecha_nac')
  def calcula_edad(self):
    print("hola")
    if self.fecha_nac is not False:
      today = datetime.today()
      nac = fields.Date.from_string(self.fecha_nac)
      self.edad = today.year - nac.year - ( (today.month, today.day) < (nac.month, nac.day) )

  # Campos generales
  nombre = fields.Char(string="Nombre", required = True)
  dni = fields.Char(string="DNI", size = 8, required = True)
  fecha_nac = fields.Date( required = True)
  edad = fields.Integer(string="Edad", compute="calcula_edad", store=True)

  sexo = fields.Selection([
    ('masculino', 'Masculino'),
    ('femenino', 'Femenino'),
  ], default="masculino", string="Sexo")
  
  ocupacion = fields.Char(size = 30)
  
  lugar_nacimiento = fields.Char(size = 50)

  estado_civil = fields.Selection([
    ('soltero', 'Soltero'),
    ('casado', 'Casado'),
    ('viudo', 'Viudo'),
    ('divorciado', 'Divorciado'),
  ], default="soltero", string="Estado Civil")


  #Domicilio
  dom_permanente = fields.Char(size=30)
  dom_transitorio = fields.Char(size=30)
  personas_nucleo = fields.Integer(string="Nº de nucleo familiar ")


  cabanas = fields.One2many('coop1.cabana', 'propietario_id', string='Cabaña')


class cabana(models.Model):
  _name = "coop1.cabana"
  _description = "Cabaña del socio"
  _rec_name = "nombre"
  
  nombre = fields.Char(string = "Nombre", required = True)
  
  comunidad = fields.Char(string = "Comunidad/Asociacion")
  
  distrito_cab = fields.Char(string = "Distrito")
  provincia_cab = fields.Char(string = "Provincia")
  departamento_cab = fields.Char(string = "Departamento")
  
  via_acceso = fields.Char(string = "Via de acceso")
  distancia_capital = fields.Integer(string = "Dist. desde capital Distrital (Kms)")
#  tipo_movilidad = fields.
  
  
  propietario_id = fields.Many2one('coop1.socio', string="Socio Propietario", required = True)
  
  
class parcela(models.Model):
  _name = "coop1.parcela"
  _description = "Parcela de la cabaña"
  
  area = fields.Float(string="Area")
  num_potreros = fields.Integer(string = "Nº potreros")
  
  
  
  
  
  
  
  
  
  
  
  
