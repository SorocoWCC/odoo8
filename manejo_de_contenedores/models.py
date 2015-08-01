# -*- coding: utf-8 -*-
 
from openerp import models, fields, api

class contenedor(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'
    fecha_ingreso = fields.Date(string="Fecha Ingreso", readonly=True, default=fields.Date.today())
    fecha_salida = fields.Date(string="Fecha Salida")
    description = fields.Text()
    numero_contenedor = fields.Char(string="Numero Contenedor")
    marchamo = fields.Char(string="Marchamo")
    mostrar_campos = fields.Boolean(string="Contenedor")
    mostrar_campos_selection = fields.Selection([('Regular','Regular'), ('Contenedor','Contenedor')], string="Tipo Factura", default='Regular')
    estado = fields.Selection([('Cargando','Cargando'), ('Enviado CON peso','Enviado CON peso'), ('Enviado SIN peso','Enviado SIN peso'), ('Cancelado','Cancelado')], string='Estado', default='Cargando')
    peso_ingreso_completo = fields.Integer(string="Contenedor Completo (kg)")
    peso_ingreso_cabezal = fields.Integer(string="Cabezal (Kg)")
    peso_salida_cabezal = fields.Integer(string="Cabezal (Kg)")
    peso_salida_completo = fields.Integer(string="Contenedor Completo (kg)")
    total = fields.Float(compute='_compute_total', store=True, string="Peso contenedor(kg)")
    imagen_uno = fields.Binary ()
    imagen_dos = fields.Binary ()
    imagen_tres = fields.Binary ()
    imagen_cuatro = fields.Binary ()
    imagen_cinco = fields.Binary ()
    imagen_seis = fields.Binary ()
    imagen_siete = fields.Binary ()
    imagen_ocho = fields.Binary ()
    imagen_nueve = fields.Binary ()
    imagen_diez = fields.Binary ()


    @api.one
    @api.depends('peso_salida_completo', 'peso_ingreso_completo', 'peso_ingreso_cabezal', 'peso_salida_cabezal')
    def _compute_total(self):
	    self.total = float(self.peso_salida_completo - ((self.peso_ingreso_completo - self.peso_ingreso_cabezal) + self.peso_salida_cabezal))


