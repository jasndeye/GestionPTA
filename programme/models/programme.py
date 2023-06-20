# -*- coding: utf-8 -*-

from ast import Str
from odoo import models, api, fields

class Programme(models.Model):
    _name = 'programme.programme'

    _inherit = ["mail.thread","mail.activity.mixin"]
    name= fields.Char(string="Nom courte", required=True)
    libellet = fields.Char(string="Libelle du programme", required=True)
    description= fields.Text (string="Description")
    budget= fields.Float(string="Le Budget")
    objectif_ids = fields.One2many ('programme.objectif','programme_id',string="Les Objectifs", required=True)
    user_id = fields.Many2one ('res.users', string="Le responsable de programme")
    service_ids = fields.Many2many ('programme.service','programme_ids', string="Les services rattacher")
    photo=fields.Binary(string="Photo", attachment=True)
    
    def etat_activiter(self):
        for rec in self:
            if rec.objectif_ids:
                for ob in rec.objectif_ids:
                    if ob.action_ids:
                        for ac in ob.action_ids:
                            if ac.resultat_ids:
                                for result in ac.resultat_ids:
                                    if result.activite_ids:
                                        for activ in result.activite_ids:
                                            if activ.etat=='en_cours':
                                                rec.write({'nb_activites_cours':rec.nb_activites_cours + 1})
                                            else:
                                                rec.write({'nb_activites_cours':rec.nb_activites_cours})
                                            if activ.etat=='non_demarer':
                                                rec.write({'nb_activites_nondemarer':rec.nb_activites_nondemarer + 1})
                                            else:
                                                rec.write({'nb_activites_nondemarer':rec.nb_activites_nondemarer})  
                                            if activ.etat=='termine':
                                                rec.write({'nb_activites_term':rec.nb_activites_term + 1})
                                            else:
                                                rec.write({'nb_activites_term':rec.nb_activites_term})  
                                            if activ.etat=='en_retard':
                                                rec.write({'nb_activites_retard':rec.nb_activites_retard + 1})
                                            else:
                                                rec.write({'nb_activites_retard':rec.nb_activites_retard})  
            else:
                rec.write({'nb_activites_cours':rec.nb_activites_cours})
                rec.write({'nb_activites_term':rec.nb_activites_term})
                rec.write({'nb_activites_retard':rec.nb_activites_retard})
                rec.write({'nb_activites_nondemarer':rec.nb_activites_nondemarer})
    nb_activites_cours= fields.Integer(string="Activités en cours",compute="etat_activiter")
    nb_activites_term= fields.Integer(string="Activités téminer",compute="etat_activiter")
    nb_activites_retard= fields.Integer(string="Activités retard",compute="etat_activiter")
    nb_activites_nondemarer= fields.Integer(string="Activités non demarer",compute="etat_activiter")
     
    @api.model
    def create(self, vals):
        res = super(Programme, self).create(vals) 
        if res.objectif_ids:
            for ob in res.objectif_ids:
                if ob.action_ids:
                    for ac in ob.action_ids:
                        if ac.resultat_ids:
                            for result in ac.resultat_ids:
                                if result.activite_ids:
                                    for activ in result.activite_ids:
                                        res.budget=res.budget+activ.cout_activite
                                        if activ.etat=='non_demarer':
                                            res.nb_activites_nondemarer+=1
                                        elif activ.etat=='en_cours':
                                            res.nb_activites_cours+=1
                                        elif activ.etat=='termine':
                                            res.nb_activites_term+=1
                                        else:
                                            res.nb_activites_retard+=1
                            
        return res
class Objectif(models.Model):
    _name = 'programme.objectif'

    name= fields.Char(string="Libelle de l'Objectif", required=True)
    description= fields.Text (string="Description")
    programme_id = fields.Many2one ('programme.programme',string="Le Programme")
    action_ids = fields.One2many ('programme.action','objectif_id',string="Les actions", required=True)
    
    
class Action(models.Model):
    _name = 'programme.action'

    name= fields.Char(string="Libelle de l'action", required=True)
    description= fields.Text (string="Description")
    objectif_id = fields.Many2one('programme.objectif',string="L'Objectif")
    resultat_ids = fields.One2many ('programme.resultat','action_id',string="Les Resultats", required=True)
    
    
class Resultat(models.Model):
    _name = 'programme.resultat'

    name= fields.Char(string="Libelle du Resultat", required=True)
    description= fields.Text (string="Description")
    evaluation= fields.Selection([('atteind','Résultat Atteind'),('en_cours','En Cours'),('non_atteind','Résultat non Atteind'),('en_retard','Résultat en moitier Atteind')], 
                           default='en_cours')
    activite_ids = fields.One2many ('programme.activite', 'resultat_id')
    action_id = fields.Many2one('programme.action',string="L'action")
    @api.model
    def create(self, vals):
       
        res = super(Resultat, self).create(vals) 
        if res.activite_ids:
            for act in res.activite_ids:
                if act.cout_activite:
                    bud=res.action_id.objectif_id.programme_id.budget
                    res.action_id.objectif_id.programme_id.budget=bud+act.cout_activite
                if act.etat=='non_demarer':
                    res.action_id.objectif_id.programme_id.nb_activites_nondemarer+=1
                elif act.etat=='en_cours':
                   res.action_id.objectif_id.programme_id.nb_activites_cours+=1
                elif act.etat=='termine':
                    res.action_id.objectif_id.programme_id.nb_activites_term+=1
                else:
                    res.action_id.objectif_id.programme_id.nb_activites_retard+=1
        
        return res