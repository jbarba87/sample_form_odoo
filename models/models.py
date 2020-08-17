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
    if self.fecha_nac is not False:
      today = datetime.today()
      nac = fields.Date.from_string(self.fecha_nac)
      self.edad = today.year - nac.year - ( (today.month, today.day) < (nac.month, nac.day) )

  # Funcion de prueba que imprime cada cabaña con el nombre del socio
  def get_data(self):
    cab = self.env["coop1.socio"].search([])
    for rec in cab:
      print("cabanas: ", rec.nombre)
    
  # Funcion que cuenta la cantidad de cabañas del socio
  @api.one
  @api.depends('cabanas')
  def count_cabanas(self):
    if self.cabanas is not False:
      self.num_cabanas = self.env["coop1.cabana"].search_count([('socio_id', '=', self.id)])

  # Campos generales
  nombre = fields.Char(string="Nombre", required = True)
  dni = fields.Char(string="DNI", size = 8, required = True)
  fecha_nac = fields.Date( required = True)


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

  # Campos computados
  num_cabanas = fields.Integer(string="Cantidad Cabañas", compute="count_cabanas", store=True)
  edad = fields.Integer(string="Edad", compute="calcula_edad", store=True)

  #Domicilio
  dom_permanente = fields.Char(size=30)
  dom_transitorio = fields.Char(size=30)
  personas_nucleo = fields.Integer(string="Nº de nucleo familiar ")


  cabanas = fields.One2many('coop1.cabana', 'socio_id', string='Cabañas')


class cabana(models.Model):
  _name = "coop1.cabana"
  _description = "Cabaña del socio"
  _rec_name = "nombre"


  # Funcion que cuenta la cantidad de parcelas de la cabaña
  @api.one
  @api.depends('parcelas')
  def count_parcelas(self):
    if self.parcelas is not False:
      self.num_parcelas = self.env["coop1.parcela"].search_count([('cabana_id', '=', self.id)])

  nombre = fields.Char(string = "Nombre", required = True)
  
  comunidad = fields.Char(string = "Comunidad/Asociacion")
  
  distrito_cab = fields.Char(string = "Distrito")
  provincia_cab = fields.Char(string = "Provincia")
  departamento_cab = fields.Char(string = "Departamento")
  
  via_acceso = fields.Char(string = "Via de acceso")
  distancia_capital = fields.Integer(string = "Dist. desde capital Distrital (Kms)")
  tipo_movilidad = fields.Char(string = "Tipo de movilidad")
  
  # Campos computados
  num_parcelas = fields.Integer(string="Cantidad parcelas", compute="count_parcelas", store=True)
  
  # Campos relacionales
  socio_id = fields.Many2one('coop1.socio', string="Socio Propietario", required = True)
  
  parcelas = fields.One2many('coop1.parcela', 'cabana_id', string="Parcela")
  

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
  num_potrero = fields.Integer(string = "Nº potreros")       # esto se debe eliminar
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

class potrero(models.Model):
  _name = "coop1.potrero"
  _description = "Potrero"
  _rec_name = "nombre_potrero"

  nombre_potrero = fields.Char(string="Nombre del potrero", required = True)
  area = fields.Float(string="Area del potrero")
  material = fields.Char(string="Material del potrero")
  area_pasto_natural = fields.Float(string="Area de pastos naturales")
  
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
  
  
  
  
