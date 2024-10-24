# Copyright 2024 Akretion (http://www.akretion.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo.models import BaseModel

search_original = BaseModel.search


def search(self, domain, offset=0, limit=None, order=None, count=False):
    """Override of the Python method to remove the dependency of the unit
    fields"""
    if self == self.env["res.lang"]:
        domain_list = domain
    else:
        list_separator = self.env["ir.config_parameter"].get_param(
            "multi_search_separator_base"
        )
        domain_list = []
        domain_value = []
        nbr = 0
        if domain:
            for dom in domain:
                if (
                    len(dom) == 3
                    and isinstance(dom[2], str)
                    and any(separator in dom[2] for separator in list_separator)
                ):
                    domain_search_field = (dom[0], dom[1], dom[2])
                    domain_value.append(domain_search_field)
                    value_list = re.split("{}".format(list_separator), dom[2])
                    for value in value_list:
                        domain_search_field = (dom[0], dom[1], value)
                        nbr = nbr + 1
                        domain_value.append(domain_search_field)
                else:
                    domain_list.append(dom)
            for _ in range(nbr):
                domain_list.append("|")
            if domain_value:
                for dom in domain_value:
                    domain_list.append(dom)
        else:
            domain_list = domain
    res = search_original(self, domain_list, offset, limit, order, count)
    return res


BaseModel.search = search
