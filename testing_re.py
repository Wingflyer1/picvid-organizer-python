# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 22:23:30 2017

@author: stentf
"""

import re


#==============================================================================
# p = re.compile('ab*')
# print(p)
# 
# p = re.compile('ab*', re.IGNORECASE)
# print(p)
#==============================================================================
list = ['080-5-2222', 'abc 2016-12-31', '2015 mar 15', '-52852014-01-4198-20-2015',
        '2013 hjemme', 'abrakadabra.jpg', 'dette var noe 31 jan 2016',
        'ferie sommer 2016', '20163012.jpg', 'Julia oktober 2014 161',
        'winter 1996-8-5', '1994-05-32 fall', '20120119', '01705 2-2017',
        'Julia oktober 2014 002', '2013-11-09 21.09.06', '2014-12-17 15.29.19',
        '17-12-2014.jpg', '20161031_224828']

pat_y = re.compile(r'[12][09][0-9]{2}') # 1990-2099
pat_y_m = re.compile(r'[12][09][0-9]{2}[-][01][0-9][-][0-3][0-9]') #1990-12-31
pat_m_y = re.compile(r'[0-3][0-9][-][01][0-9][-][12][09][0-9]{2}') #31-12-1990
pat_coh = re.compile(r'[12][09][0-9]{2}[01][0-9][0-3][0-9]')



for i in list:
    year = pat_y.search(i)
    month = pat_y_m.search(i)
    month2 = pat_m_y.search(i)
    coh = pat_coh.search(i)
    if coh != None:
        print('4', coh.group(),'from -->', i)
    elif month2 != None:
        print('3', month2.group(),'from -->', i)
    elif month != None:
        print('2', month.group(),'from -->', i)
    elif year != None:
        print('1', year.group(),'from -->', i)
    
    
    
#    print(month.group())
        
        
        
#==============================================================================
# From: author@example.com
# User-Agent: Thunderbird 1.5.0.9 (X11/20061227)
# MIME-Version: 1.0
# To: editor@example.com
#==============================================================================

