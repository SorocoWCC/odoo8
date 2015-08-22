# -*- coding: utf-8 -*-
 
from openerp import models, fields, api
from openerp.exceptions import Warning



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
    _defaults = { 
    'periodo_cambio_aceite': 90,
    }


class gasto(models.Model):
    _name = 'gasto'
    _inherit = 'gasto'
    vehiculo_id = fields.Many2one(comodel_name='flotilla.vehiculo', string='Vehiculo')
    tipo_gasto = fields.Selection([('regular','Regular'), ('flotilla','Flotilla'), ('aceite','Cambio de Aceite')], string='Tipo')
    _defaults = { 
    'tipo_gasto': 'regular',
    }




