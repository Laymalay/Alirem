#!/usr/bin/python
# -*- coding: UTF-8 -*-
import alirem._alirem as alirem



rm = alirem.Alirem()
rm.remove('file')
rm.check_basket_for_cleaning(is_show=True)
rm.restore('file')
