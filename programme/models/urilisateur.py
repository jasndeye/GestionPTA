# -*- coding: utf-8 -*-

from datetime import date
from odoo.exceptions import ValidationError
from odoo import models, api, fields


class Utilisateur(models.Model):
    _inherit = 'res.users'

    matricule = fields.Char(string="Matricule de l'utilisateur", required=True)

    @api.onchange('matricule')
    def is_matricul(self):
        if self.matricule:
            adr_split = str(self.matricule).split('/')
            last_element = adr_split[1]
            chiffre=adr_split[0]
            if len(chiffre)==6:
                alf=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
                nb_p=0;
                nb_i=0;
                p=0;
                for i in range(len(chiffre)):
                        if int(chiffre[i]) % 2 == 0:
                            nb_p += int(chiffre[i])
                        else:
                            nb_i += int(chiffre[i])
                p=abs(nb_p-nb_i)
                print(p,alf[p-1],'fff',last_element)
                if alf[p-1]==last_element:
                    return {
                    'warning': {
                        'message':"La matricule donnée est bon",
                        },
                   } 
                            
                else:
                    raise ValidationError('ATTENTION ! La dernier lettre ne correspond pas')
            else:
                raise ValidationError('ATTENTION ! La matricule doit commencer par 6 chiffre')
                
       