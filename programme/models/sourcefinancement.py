# -*- coding: utf-8 -*-

from odoo import models, api, fields

class SourceFinancement(models.Model):
    _name = 'programme.sourcefinancement'
    _rec_name='name'
    
    name= fields.Char(string="Nom de la source", required=True)
    budget= fields.Float(string="Le Budget")
    type_financement = fields.Selection([('interne','Financement Intérne'),('extene','Financement Extérne')], 
                           default='interne',help="Si c'est l'Etat:c'est un  Financement Intérne ;si c'est un bailleur :c'est un Financement Extérne.",string="Type de financement")
    nature_economique_ids = fields.Many2many ('programme.natureeconomique','source_financement_ids' ,string="Les natures économique")
    activites_id = fields.One2many ('programme.activite','sourcefinancement',string=" Activités")
    sousactivites_id = fields.One2many ('programme.sousactivite','sourcefinancement',string=" Sous-activités")
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Le nom doit etre unique")]
    
    
class NatureEconomique(models.Model):
    _name = 'programme.natureeconomique'
    _rec_name='name'
    
    name = fields.Char (string="La nature économique")
    source_financement_ids = fields.Many2many ('programme.sourcefinancement','nature_economique_ids', string=" Les sources de financement")