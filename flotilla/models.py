# -*- coding: utf-8 -*-
 
from openerp import models, fields, api
from openerp.exceptions import Warning
import time
import datetime
import dateutil
from datetime import date, timedelta, datetime
from dateutil import parser


#----------------------------------------CLASE VEHICULO--------------------------------------------------------------------#

# Clase Vehiculo
class vehiculo(models.Model):
    _name = "flotilla.vehiculo"
    _description = "Vehiculo"
    name = fields.Char(string='Placa', required=True)
    imagen_vehiculo = fields.Binary()
    motor = fields.Char(string='Motor')
    chasis = fields.Char(string='Chasis')
    filtro_aceite = fields.Char(string='Filtro de Aceite')
    peso = fields.Integer(string='Peso')
    notas= fields.Text(string='Notas')
    periodo_cambio_aceite = fields.Integer(string='Perido Cambio de Aceite (dias)', required=True)
    gasto_ids = fields.One2many(comodel_name='gasto', inverse_name='vehiculo_id', string="Gastos", domain=[('tipo_gasto', '=', 'aceite')])
    proximo_cambio_aceite = fields.Date(compute='_action_aceite', string="Proximo Cambio Aceite", readonly=True, store=True )
    proximo_aceite = fields.Char(string="TEST", readonly=True, store=True )
    _defaults = { 
    'periodo_cambio_aceite': 90,
    }


# Proximo Cambio de Aceite
    @api.one
    @api.depends('gasto_ids')
    def _action_aceite(self):
	contador = 0
	for gasto in self.gasto_ids :
		contador+= 1
		if contador == len(self.gasto_ids):
			fecha=date.today()+timedelta(days=int(self.periodo_cambio_aceite))
			self.proximo_cambio_aceite = str(fecha)


class gasto(models.Model):
    _name = 'gasto'
    _inherit = 'gasto'
    vehiculo_id = fields.Many2one(comodel_name='flotilla.vehiculo', string='Vehiculo')
    tipo_gasto = fields.Selection([('regular','Regular'), ('flotilla','Flotilla'), ('aceite','Cambio de Aceite')], string='Tipo')
    proximo_cambio_aceite = fields.Char(compute='_action_proximo_cambio_aceite', string="Proximo Cambio Aceite", readonly=True, store=True )
    _defaults = { 
    'tipo_gasto': 'regular',
    }

# Proximo Cambio de Aceite
    @api.one
    @api.depends('state')
    def _action_proximo_cambio_aceite(self):
	if str(self.tipo_gasto) == 'aceite':
		for record in self.vehiculo_id :
			record.proximo_aceite = "6546546546"






