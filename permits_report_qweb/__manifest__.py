# -*- coding: utf-8 -*-
{
    'name': "Permisos de Usuarios",
    'summary': """
        Reporte de permisos de usuario
        """,
    'description': """
        Este modulo crea un reporte en el que se detallan los permisos del usuario que se
        indique en sus parametros asi como el nivel de detalle del reporte
    """,
    'author': "GEO",
    'website': "http://www.delfixcr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Report',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','mail'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/permits_report.xml',
        'wizard/user_permits_wizard_view.xml',
        'data/report_paperformat.xml',
        # 'views/templates.xml',
    ],

}