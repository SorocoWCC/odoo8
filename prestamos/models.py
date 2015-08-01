# -*- coding: utf-8 -*-
 
from openerp import models, fields, api
from openerp.exceptions import Warning



#----------------------------------------PRESTAMO EMPLEADOS--------------------------------------------------------------------#

# Abono Empleado
class empleado_abono(models.Model):
    _name = "empleado.abono"
    _description = "Empleado Abono"
    monto = fields.Float(string='Monto', required=True)
    fecha = fields.Date(string='Fecha', readonly=True)
    responsable = fields.Char(compute='_action_responsable', string="Responsable", readonly=True, store=True )	
    notas= fields.Text(string='Notas')
    libro_id = fields.Many2one(comodel_name='empleado.allowance', string='Prestamo', delegate=True)
    _defaults = { 
    'fecha': fields.Date.today(),
    }

# Nombre del responsable Abono
    @api.one
    @api.depends('monto')
    def _action_responsable(self):
	self.responsable = str(self.env.user.name)

#  Prestamo - Amortizable - Empleado
class empleado_amortizable(models.Model):
    _name = "empleado.amortizable"
    _description = "Empleado Amortizable"
    monto = fields.Float(string='Monto', required=True)
    fecha = fields.Date(string='Fecha', readonly=True)
    responsable = fields.Char(compute='_action_responsable', string="Responsable", readonly=True, store=True )	
    notas= fields.Text(string='Notas', required=True)
    libro_id = fields.Many2one(comodel_name='empleado.allowance', string='Prestamo', delegate=True)
    _defaults = { 
    'fecha': fields.Date.today(),
    }

# Nombre del responsable Amortizable
    @api.one
    @api.depends('monto')
    def _action_responsable(self):
	self.responsable = str(self.env.user.name)

# Libro Prestamo Empleado
class empleado_allowance(models.Model):
    _name = "empleado.allowance"
    _description = "Empleado Allowance"
    res_employee_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', delegate=True)
    amortizable_ids = fields.One2many(comodel_name='empleado.amortizable', inverse_name='libro_id', string="Amortizables")
    abono_ids = fields.One2many(comodel_name='empleado.abono',inverse_name='libro_id', string="Abonos")
    total_amortizable = fields.Float(compute='_total_amortizable_empleado', store=True, string="Total Prestamo: ")
    total_abono = fields.Float(compute='_total_abono_empleado', store=True, string="Total Abonos: ")
    saldo = fields.Float(compute='_saldo', store=True, string="Saldo: ")
    detalle = fields.Char(size=50, string="Detalle")
    fecha_abono = fields.Char(size=50, string="Fecha Abono")
    monto_abono = fields.Char(size=50, string="Monto Abono")
    state = fields.Selection([('new','Abierto'), ('done','Cerrado')], string='Estado', readonly=True)
    _defaults = { 
    'state': 'new',
    }

# Total Prestamos / Amortizables
    @api.one
    @api.depends('amortizable_ids')
    def _total_amortizable_empleado(self):
	total= 0
	for prestamo in self.amortizable_ids:
		total += float(prestamo.monto)
	self.total_amortizable= total

# Total Abonos 
    @api.one
    @api.depends('abono_ids')
    def _total_abono_empleado(self):
	total= 0
	fecha_abono = "False"
	monto_abono = "False"
	for abono in self.abono_ids:
		total += float(abono.monto)
		fecha_abono = str(abono.fecha)
		monto_abono = str(abono.monto)
	self.total_abono= total
	self.monto_abono = monto_abono
	self.fecha_abono = fecha_abono


# Saldo
    @api.one
    @api.depends('abono_ids', 'amortizable_ids')
    def _saldo(self):
	self.saldo= self.total_amortizable - self.total_abono



#----------------------------------------FIN PRESTAMO EMPLEADOS--------------------------------------------------------------------#


#----------------------------------------PRESTAMO CLIENTES--------------------------------------------------------------------#



# Abono Cliente
class cliente_abono(models.Model):
    _name = "cliente.abono"
    _description = "Cliente Abono"
    monto = fields.Float(string='Monto', required=True)
    fecha = fields.Date(string='Fecha', readonly=True)
    responsable = fields.Char(compute='_action_responsable', string="Responsable", readonly=True, store=True )	
    notas= fields.Text(string='Notas')
    libro_id = fields.Many2one(comodel_name='cliente.allowance', string='Prestamo', delegate=True, store=True)
    _defaults = { 
    'fecha': fields.Date.today(),
    }

# Nombre del responsable Abono
    @api.one
    @api.depends('monto')
    def _action_responsable(self):
	self.responsable = str(self.env.user.name)

#  Prestamo - Amortizable - cliente
class cliente_amortizable(models.Model):
    _name = "cliente.amortizable"
    _description = "cliente Amortizable"
    monto = fields.Float(string='Monto', required=True)
    fecha = fields.Date(string='Fecha', readonly=True)
    responsable = fields.Char(compute='_action_responsable', string="Responsable", readonly=True, store=True )	
    notas= fields.Text(string='Notas', required=True)
    libro_id = fields.Many2one(comodel_name='cliente.allowance', string='Prestamo', delegate=True)
    _defaults = { 
    'fecha': fields.Date.today(),
    }

# Nombre del responsable Amortizable
    @api.one
    @api.depends('monto')
    def _action_responsable(self):
	self.responsable = str(self.env.user.name)

# Libro Prestamo cliente
class cliente_allowance(models.Model):
    _name = "cliente.allowance"
    _description = "cliente Allowance"
    res_partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente', delegate=True)
    amortizable_ids = fields.One2many(comodel_name='cliente.amortizable', inverse_name='libro_id', string="Amortizables")
    abono_ids = fields.One2many(comodel_name='cliente.abono',inverse_name='libro_id', store=True, string="Abonos")
    total_amortizable = fields.Float(compute='_total_amortizable_cliente', store=True, string="Total Prestamo: ")
    total_abono = fields.Float(compute='_total_abono_cliente', store=True, string="Total Abonos: ")
    saldo = fields.Float(compute='_saldo', store=True, string="Saldo: ")
    detalle = fields.Char(size=50, string="Detalle")
    fecha_abono = fields.Char(size=50, string="Fecha Abono")
    monto_abono = fields.Char(size=50, string="Monto Abono")
    state = fields.Selection([('new','Abierto'), ('done','Cerrado')], string='Estado', readonly=True)
    _defaults = { 
    'state': 'new',
    }


# Total Prestamos / Amortizables
    @api.one
    @api.depends('amortizable_ids')
    def _total_amortizable_cliente(self):
	total= 0
	for prestamo in self.amortizable_ids:
		total += float(prestamo.monto)
	self.total_amortizable= total

# Total Abonos 
    @api.one
    @api.depends('abono_ids')
    def _total_abono_cliente(self):
	total= 0
	fecha_abono = "False"
	monto_abono = "False"
	for abono in self.abono_ids:
		total += float(abono.monto)
		fecha_abono = str(abono.fecha)
		monto_abono = str(abono.monto)

	self.total_abono= total
	self.monto_abono = monto_abono
	self.fecha_abono = fecha_abono

# Saldo
    @api.one
    @api.depends('abono_ids', 'amortizable_ids')
    def _saldo(self):
	self.saldo= self.total_amortizable - self.total_abono


#----------------------------------------FIN PRESTAMO CLIENTES--------------------------------------------------------------------#

#----------------------------------------PRESTAMO POR PAGAR--------------------------------------------------------------------#

# Abono prestamo por pagar
class pagar_abono(models.Model):
    _name = "pagar.abono"
    _description = "Prestarmo por Pagar Abono"
    monto = fields.Float(string='Monto', required=True)
    fecha = fields.Date(string='Fecha', readonly=True)
    responsable = fields.Char(compute='_action_responsable', string="Responsable", readonly=True, store=True )	
    notas= fields.Text(string='Notas')
    libro_id = fields.Many2one(comodel_name='pagar.allowance', string='Prestamo', delegate=True)
    _defaults = { 
    'fecha': fields.Date.today(),
    }

# Nombre del responsable Abono
    @api.one
    @api.depends('monto')
    def _action_responsable(self):
	self.responsable = str(self.env.user.name)

#  Prestamo - Amortizable - Por Pagar
class pagar_amortizable(models.Model):
    _name = "pagar.amortizable"
    _description = "Pagar Amortizable"
    monto = fields.Float(string='Monto', required=True)
    fecha = fields.Date(string='Fecha', readonly=True)
    responsable = fields.Char(compute='_action_responsable', string="Responsable", readonly=True, store=True )	
    notas= fields.Text(string='Notas', required=True)
    libro_id = fields.Many2one(comodel_name='pagar.allowance', string='Prestamo', delegate=True)
    _defaults = { 
    'fecha': fields.Date.today(),
    }

# Nombre del responsable Amortizable
    @api.one
    @api.depends('monto')
    def _action_responsable(self):
	self.responsable = str(self.env.user.name)

# Libro Prestamo por Pagar
class cliente_allowance(models.Model):
    _name = "pagar.allowance"
    _description = "Pagar Allowance"
    res_partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente', delegate=True)
    amortizable_ids = fields.One2many(comodel_name='cliente.amortizable', inverse_name='libro_id', string="Amortizables")
    abono_ids = fields.One2many(comodel_name='pagar.abono',inverse_name='libro_id', string="Abonos")
    total_amortizable = fields.Float(compute='_total_amortizable_pagar', store=True, string="Total Prestamo: ")
    total_abono = fields.Float(compute='_total_abono_pagar', store=True, string="Total Abonos: ")
    saldo = fields.Float(compute='_saldo', store=True, string="Saldo: ")
    detalle = fields.Char(size=50, string="Detalle")
    fecha_abono = fields.Char(size=50, string="Fecha Abono")
    monto_abono = fields.Char(size=50, string="Monto Abono")
    state = fields.Selection([('new','Abierto'), ('done','Cerrado')], string='Estado', readonly=True)
    _defaults = { 
    'state': 'new',
    }

# Total Prestamos / Amortizables
    @api.one
    @api.depends('amortizable_ids')
    def _total_amortizable_pagar(self):
	total= 0
	for prestamo in self.amortizable_ids:
		total += float(prestamo.monto)
	self.total_amortizable= total

# Total Abonos 
    @api.one
    @api.depends('abono_ids')
    def _total_abono_pagar(self):
	total= 0
	fecha_abono = "False"
	monto_abono = "False"
	for abono in self.abono_ids:
		total += float(abono.monto)
		fecha_abono = str(abono.fecha)
		monto_abono = str(abono.monto)

	self.total_abono= total
	self.monto_abono = monto_abono
	self.fecha_abono = fecha_abono

# Saldo
    @api.one
    @api.depends('abono_ids', 'amortizable_ids')
    def _saldo(self):
	self.saldo= self.total_amortizable - self.total_abono


#----------------------------------------FIN PRESTAMO POR PAGAR--------------------------------------------------------------------#

# Libro Prestamo por Pagar
class libro(models.Model):
    _name = "libro"
    _description = "Libro"
    campo_hoja = fields.Char(size=50, string="Campo")
    rama = fields.Char(size=50, string="Campo")
    hoja_ids = fields.One2many(comodel_name='hoja',inverse_name='libro_id', string="Abonos")

# Agregar linea Pedido Cobre
    @api.one
    def action_test(self):
	res= self.env['cliente.allowance'].search([('res_partner_id', '=', 'Warren Castro')])
	print "------------------> " + str(res)
	res.abono_ids.create({'name':'ware','libro_id':188, 'monto':6969})
    	self.hoja_ids.create({'libro_id' : self.id, 'campito':'Campito'})


# Hoja
class hoja(models.Model):
    _name = "hoja"
    _description = "Libro"
    campito = fields.Char(size=50, string="Zapato")
    libro_id = fields.Many2one(comodel_name='libro', string='Libro', delegate=True)






