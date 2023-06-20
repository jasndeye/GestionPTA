# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, api, fields

class Activite(models.Model):
    _name = 'programme.activite'
    _inherit = ["mail.thread","mail.activity.mixin"] 

    name= fields.Char(string="Libelle de l'Activite", required=True)
    description= fields.Text (string="Description")
    cout_activite = fields.Integer (string="Cout Total Activité")
    date_debut_activite = fields.Date (string= "Date de debut", help="C'est la date de démarage de l'activité")
    date_fin_activite = fields.Date (string= "Date de Fin" , help="C'est la date de fin de l'activité")
    etat= fields.Selection([('non_demarer','Non demarer'),('en_cours','En Cours'),('termine','Terminé'),('en_retard','En Retard')], 
                           default='non_demarer',help="C'est les différentes étape de l'activité.")
    resultat_id = fields.Many2one ('programme.resultat', string=" Resultat")
    duree= fields.Integer(string="Progréssion")
    services_ids=fields.Many2many('programme.service','activite_ids', string="Les services rattacher")
    service_responsable=fields.Many2one('programme.service', string="Le service responsable")
    divisions_ids=fields.Many2many('programme.division','activit_ids',string="Les divisions rattacher")
    #####
    a_sous_activite=fields.Boolean(string="A sous-activités ?",default=False )
    sous_activite_ids = fields.One2many ('programme.sousactivite','activite_id', string='Les sous activités')
    sourcefinancement = fields.Many2one ('programme.sourcefinancement', string="Les sources de financement")
    nom_sources= fields.Char(string="Source de Financement")
   
    #######
    @api.onchange('sous_activite_ids')
    def onchange_sousactivite(self):
        if len(self.sous_activite_ids)>0:
            self.sourcefinancement=None
            
    @api.onchange('service_responsable')
    def liste_division(self):
        if self.service_responsable:
           list_division_activite = []
           list_division_service=self.service_responsable.divisions_ids
           if list_division_service:
               for list in list_division_service:
                   list_division_activite.append(list.id)
               return {'domain': {'divisions_ids': [('id', 'in', list_division_activite)]}}
           else:
               self.divisions_ids=None
               return {'domain': {'divisions_ids': [('id', 'in', '')]}} 
        else:
            self.divisions_ids=None
            return {'domain': {'divisions_ids': [('id', 'in', '')]}} 
  
    #######
    @api.onchange('resultat_id')
    def liste_service(self):
        if self.resultat_id:
           list_service_activite = []
           list_service_prog=self.resultat_id.action_id.objectif_id.programme_id.service_ids
           if list_service_prog:
               for list in list_service_prog:
                   list_service_activite.append(list.id)
               return {'domain': {'services_ids': [('id', 'in', list_service_activite)],
                                  'service_responsable': [('id', 'in', list_service_activite)]}}
           else:
               res=self.env['programme.service'].search([])
               if res:
                    for liste in res:
                        list_service_activite.append(liste.id)
                    return {'domain': {'services_ids': [('id', 'in', list_service_activite)],
                                       'service_responsable': [('id', 'in', list_service_activite)]}} 
    def pregression(self):
        if self.date_fin_activite and self.date_debut_activite:
           delta1 = self.date_fin_activite - self.date_debut_activite
           delta2=date.today() - self.date_debut_activite
           nb2=int(100*(delta2/delta1))
           self.duree=nb2
        return{
            'name': _('Activite server'),
            'domain': [],
            'res_model':'programme.activite',
            'view_id':False,
            'view_mode':'tree,form,calendar,graph',
            'type':'ir.actions.act_window',
            # 'view_type':'form'
        }
           
    ########
    @api.onchange('date_debut_activite','date_fin_activite')
    def is_date_fin(self):
        if self.date_fin_activite and self.date_debut_activite:
          if self.date_fin_activite<self.date_debut_activite:
            return {
                    'warning': {
                        'title':"Erreur de saisie",
                        'message':"La date de fin dois suppérieur a la date de début",
                        },
                   } 
          else:
           delta1 = self.date_fin_activite - self.date_debut_activite
           delta2=date.today() - self.date_debut_activite
           nb2=int(100*(delta2/delta1))
           self.duree=nb2   
    ##########
    @api.model
    def create(self, vals):
       
        res = super(Activite, self).create(vals) 
        #### Budget source financement
        if not res.sous_activite_ids:
            if res.sourcefinancement and res.cout_activite:
               res.sourcefinancement.budget+=res.cout_activite
               res.nom_sources=res.sourcefinancement.name
        else:
            res.cout_activite=0
            nom=''
            for act in res.sous_activite_ids:
                if act.cout_sousactivite and act.sourcefinancement:
                    res.cout_activite +=act.cout_sousactivite 
                    act.nom_sources=act.sourcefinancement.name
                    nom=nom + act.nom_sources+', '
            res.sourcefinancement.budget+=res.cout_activite
            res.nom_sources=nom
        #### Budget programme
        if res.resultat_id:
            if res.cout_activite:
                bud=res.resultat_id.action_id.objectif_id.programme_id.budget
                res.resultat_id.action_id.objectif_id.programme_id.budget=bud+res.cout_activite
            if res.etat=='non_demarer':
               res.resultat_id.action_id.objectif_id.programme_id.nb_activites_nondemarer+=1
            elif res.etat=='en_cours':
               res.resultat_id.action_id.objectif_id.programme_id.nb_activites_cours+=1
            elif res.etat=='termine':
                res.resultat_id.action_id.objectif_id.programme_id.nb_activites_term+=1
            else:
                res.resultat_id.action_id.objectif_id.programme_id.nb_activites_retard+=1
        
        return res
    ##########
    def unlink(self):      
        if self.resultat_id:
            if self.cout_activite:
                bud=self.resultat_id.action_id.objectif_id.programme_id.budget
                self.resultat_id.action_id.objectif_id.programme_id.budget=bud-self.cout_activite
            if self.etat=='non_demarer':
                if self.resultat_id.action_id.objectif_id.programme_id.nb_activites_nondemarer>0:
                   self.resultat_id.action_id.objectif_id.programme_id.nb_activites_nondemarer-=1
            elif self.etat=='en_cours':
                if self.resultat_id.action_id.objectif_id.programme_id.nb_activites_cours>0:
                   self.resultat_id.action_id.objectif_id.programme_id.nb_activites_cours -=1
            elif self.etat=='termine':
                if self.resultat_id.action_id.objectif_id.programme_id.nb_activites_term>0:
                   self.resultat_id.action_id.objectif_id.programme_id.nb_activites_term-=1
            else:
                if self.resultat_id.action_id.objectif_id.programme_id.nb_activites_retard>0:
                   self.resultat_id.action_id.objectif_id.programme_id.nb_activites_retard-=1
        
        rec = super(Activite, self).unlink()
        print('Supprimer',rec) 
       
    # @api.multi
    def write(self, vals):
        # if self.etat :
        #   etat=self.etat
       
        if self.resultat_id:
            if vals.get('cout_activite'):
                cout=self.cout_activite -vals.get('cout_activite')
                bud=self.resultat_id.action_id.objectif_id.programme_id.budget
                self.resultat_id.action_id.objectif_id.programme_id.budget=bud-cout
            else:
                bud=self.resultat_id.action_id.objectif_id.programme_id.budget
                self.resultat_id.action_id.objectif_id.programme_id.budget=bud-self.cout_activite
            if vals.get('etat')!=None:
                if vals.get('etat')=='non_demarer':
                   self.resultat_id.action_id.objectif_id.programme_id.nb_activites_nondemarer+=1
                elif vals.get('etat')=='en_cours':
                    self.resultat_id.action_id.objectif_id.programme_id.nb_activites_cours+=1
                elif vals.get('etat')=='termine':
                     self.resultat_id.action_id.objectif_id.programme_id.nb_activites_term+=1
                else:
                     self.resultat_id.action_id.objectif_id.programme_id.nb_activites_retard+=1
                if self.etat=='non_demarer':
                   if self.resultat_id.action_id.objectif_id.programme_id.nb_activites_nondemarer>0:
                      self.resultat_id.action_id.objectif_id.programme_id.nb_activites_nondemarer-=1
                elif self.etat=='en_cours':
                   if self.resultat_id.action_id.objectif_id.programme_id.nb_activites_cours>0:
                     self.resultat_id.action_id.objectif_id.programme_id.nb_activites_cours -=1
                elif self.etat=='termine':
                    if self.resultat_id.action_id.objectif_id.programme_id.nb_activites_term>0:
                       self.resultat_id.action_id.objectif_id.programme_id.nb_activites_term-=1
                else:
                    if self.resultat_id.action_id.objectif_id.programme_id.nb_activites_retard>0:
                       self.resultat_id.action_id.objectif_id.programme_id.nb_activites_retard-=1
        res = super(Activite, self).write(vals)   
        return res

class SousActivite(models.TransientModel):
    _name='programme.sousactivite'
      
    
    activite_id = fields.Many2one ('programme.activite',string="Activité parent")
    name= fields.Char(string="Libelle de l'Activite", required=True)
    description= fields.Text (string="Description")
    cout_sousactivite = fields.Integer (string="Cout Total Activité")
    date_debut_sousactivite = fields.Date (string= "Date de debut", help="C'est la date de démarage de l'activité")
    date_fin_sousactivite = fields.Date (string= "Date de Fin" , help="C'est la date de fin de l'activité")
    etat_sousactivite= fields.Selection([('non_demarer','Non demarer'),('en_cours','En Cours'),('termine','Terminé'),('en_retard','En Retard')], 
                           default='non_demarer',help="C'est les différentes étape de l'activité.")
    service_responsable=fields.Many2one('programme.service', related='activite_id.service_responsable',string="Le service responsable")
    division_ids=fields.Many2many('programme.division','sousactivit_ids',string="Les divisions rattacher")
    #####
    sourcefinancement = fields.Many2one ('programme.sourcefinancement', string="Source de financement")
    nom_source= fields.Char(string="Source de Financement")

    @api.onchange('service_responsable')
    def liste_division(self):
        if self.service_responsable:
           list_division_activite = []
           list_division_service=self.service_responsable.divisions_ids
           if list_division_service:
               for list in list_division_service:
                   list_division_activite.append(list.id)
               return {'domain': {'division_ids': [('id', 'in', list_division_activite)]}}
           else:
               self.division_ids=None
               return {'domain': {'division_ids': [('id', 'in', '')]}} 
        else:
            self.division_ids=None
            return {'domain': {'division_ids': [('id', 'in', '')]}} 
    ##########
    @api.model
    def create(self, vals):
        res = super(SousActivite, self).create(vals) 
        #### Budget source financement
        if res.sourcefinancement:
            res.nom_source=res.sourcefinancement.name 
        if res.cout_sousactivite:
               res.sourcefinancement.budget+=res.cout_sousactivite
                      
        return res
    ##########
    def unlink(self):      
        if self.sourcefinancement:
            self.nom_source -= self.sourcefinancement.name 
        if self.cout_sousactivite:
               self.sourcefinancement.budget -=self.cout_sousactivite
        rec = super(Activite, self).unlink()
        print('Supprimer',rec)            