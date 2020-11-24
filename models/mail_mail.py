# Copyright 2020 Subteno IT
# See LICENSE file for full copyright and licensing details.

from odoo import models, api
from odoo.tools import formataddr


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def _split_by_server(self):
        for mail in self.filtered(lambda r: not r.mail_server_id):
            user = self.env['res.users'].search([('partner_id', '=', mail.author_id.id)])
            alias_domain = ''
            if 'force_alias_domain' in self.env[mail.model]._fields.keys():
                alias_domain = self.env[mail.model].sudo().browse(mail.res_id).force_alias_domain
            if not alias_domain:
                alias_domain = user.company_id.sudo().force_alias_domain
            if alias_domain:
                company_server_id = self.env['ir.mail_server'].search([('force_alias_domain', '=', alias_domain)])
                mail.mail_server_id = company_server_id
                mail.email_from = formataddr((
                    user.partner_id.name,
                    user.partner_id.email.split('@')[0] + '@' + alias_domain
                ))
        return super(MailMail, self)._split_by_server()
