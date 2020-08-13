# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class socio(models.Model):
  _name = "coop1.socio"
  _description = "Socio de la cooperativa"

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
      if  (not rec.dni.isnumeric()):
        raise ValidationError('El campo DNI no debe contener letras.')

  # Funcion de autocompletado de la edad en base a la fecha de nacimiento
  # Ojo que la el campo odoo.fields.Date es string por lo que debe convertir en datetime
  # Tener en cuenta que se debe ingresar la fecha en formato mm/dd/aaaa
  @api.depends('fecha_nac')
  def calcula_edad(self):
    if self.fecha_nac is not False:
      today = datetime.today()
      nac = fields.Date.from_string(self.fecha_nac)
      self.edad = today.year - nac.year - ( (today.month, today.day) < (nac.month, nac.day) )

  # Campos generales
  nombre = fields.Char(string="Nombre", required = True)
  dni = fields.Char(string="DNI", size = 8, required = True)
  fecha_nac = fields.Date( required = True)
  edad = fields.Integer(string="Edad", compute="calcula_edad")

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

# class coop1(models.Model):
#     _name = 'coop1.coop1'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
