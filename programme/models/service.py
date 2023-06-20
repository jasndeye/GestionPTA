# -*- coding: utf-8 -*-

from odoo import models, api, fields

class Service(models.Model):
    _name = 'programme.service'

    name= fields.Char(string="Nom court du service", help="Le nom court du service", required=True)
    lib_service= fields.Char (string="Libelle du service", help="Le libelle du service")
    tutelle_id = fields.Many2one ('programme.tutelle', string=" Le Tutelle")
    programme_ids = fields.Many2many ('programme.programme','service_ids', string="Les programmes rattacher")
    activite_ids=fields.Many2many('programme.activite','services_ids',string="Les activités rattacher")
    divisions_ids = fields.One2many ('programme.division','service_id', string="Liste des divisions")   
     # user_ids = fields.One2many ('res.users','service_id', string="Les employés du service")   
       
class Division(models.Model):
    _name = 'programme.division'

    name= fields.Char(string="Nom court division", help="Le nom court de la division", required=True)
    lib_division= fields.Char (string="Libelle ", help="Le nom complet du la division")
    activit_ids=fields.Many2many('programme.activite','divisions_ids',string="Les activités rattacher")
    sousactivit_ids=fields.Many2many('programme.sousactivite','division_ids',string="Les activités rattacher")
    service_id = fields.Many2one ('programme.service', string=" Le Service", required=True)

class Tutelle(models.Model):
    _name = 'programme.tutelle'

    name= fields.Char(string="Nom Court", help="Le nom court du Tutelle", required=True)
    libelle_tutelle= fields.Char (string="Libelle tutelle", help="Le libelle du Tutelle")
    service_ids = fields.One2many ('programme.service','tutelle_id',string="Les services", help="Les services du Tutelle")