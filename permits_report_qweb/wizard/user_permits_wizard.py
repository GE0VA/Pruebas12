# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (c) 2018 DIS S.A. (http://www.delfixcr.com) All Rights Reserved.
#
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api, _
from datetime import datetime, timedelta
import io
from pytz import timezone
import collections
import json
import logging

_logger = logging.getLogger(__name__)

try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')

try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')

USER_TIMEZONE_DEFAULT = "America/Costa_Rica"

class UserPermitsWizard(models.TransientModel):
    _name = 'user.report'
    _description = 'Reporte de Clientes'
    
    # user = fields.Many2many(comodel_name="res.users", relation="res_user_report__rel", column1="id_rel",
    #                         column2="user_id", string="Usuario")
    user = fields.Many2one(comodel_name="res.users", string="Usuario", required=False, default=7 )
    # model = fields.Many2one(comodel_name="ir.model", string="Modelo a Filtrar", required=False)
    model = fields.Many2many(comodel_name="ir.model", relation="res_model_report__rel", column1="id_rel",
                                                     column2="model_id", string="Modelo(s) a Filtrar")
    menus = fields.Boolean(string="Ver Menus",  )
    inherits = fields.Boolean(string="Ver Grupos Heredados",  )
    rules = fields.Boolean(string="Ver Reglas",  )
    views = fields.Boolean(string="Ver vistas",  )
    notes = fields.Boolean(string="Ver notas",  )

    def get_user(self):
        """
        get the user that create the report
        :return: name of users
        """
        return self.env['res.users'].browse(self._uid).name
    
    def get_date_with_tz(self):
        """
        get current creation date with the timezone of user and return it by the choiceed format
        :return: current date
        """
        date_with_tz = str(datetime.now())[:19]
        return datetime.strptime(str(date_with_tz)[:19], '%Y-%m-%d %H:%M:%S').strftime('%d %b, %Y - %I:%M %p')[:26]

    def get_data(self, user=[]):
        """
        Method to get data from invoces filtered by dates and partners, if there are no partner then it filters by all
        :param partners: users from wizard to filter
        :return: data formatted
        """
        if user:
            user_search = user.ids
    
        if user:
            data = self.env['res.groups'].search([('users', 'in', user_search),])
        else:
            data = self.env['res.groups'].search([])

        if self.model:
            new_data_filter_by_model = []
            for rec in data:
                for access_model in rec.model_access:
                    if access_model.model_id in self.model:
                        new_data_filter_by_model.append(rec)
                        break
            return new_data_filter_by_model
            
            
        return data

class UserReportSaveWizard(models.TransientModel):
    _name = "save.user.report.wizard"
    
    name = fields.Char('filename', readonly=True)
    data = fields.Binary('file', readonly=True)
