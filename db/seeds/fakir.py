"""Idempotent seed for Fakir Knitwears Ltd. (167 installed, 165 operating across Unit-1 and Unit-2)."""

import re
from db.calc import calculate_needle_sinker
FAKIR_SAVED_DATA = {'unit1_blocks': [{'rows': [{'brand': 'U-Masa', 'dia': '42 inch', 'feeders': '126', 'gauge': '24 G', 'mc_no': 'A-1', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 1},
                            {'brand': 'Jiunn Long', 'dia': '42 inch', 'feeders': '127', 'gauge': '24 G', 'mc_no': 'A-2', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'Jiunn Long', 'dia': '42 inch', 'feeders': '128', 'gauge': '24 G', 'mc_no': 'A-3', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '129', 'gauge': '24 G', 'mc_no': 'A-4', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '130', 'gauge': '24 G', 'mc_no': 'A-5', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '131', 'gauge': '24 G', 'mc_no': 'A-6', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 6},
                            {'brand': 'U-Masa', 'dia': '40 inch', 'feeders': '132', 'gauge': '24 G', 'mc_no': 'A-7', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 7},
                            {'brand': 'U-Masa', 'dia': '36 inch', 'feeders': '133', 'gauge': '24 G', 'mc_no': 'A-8', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 8},
                            {'brand': 'U-Masa', 'dia': '36 inch', 'feeders': '134', 'gauge': '24 G', 'mc_no': 'A-9', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 9},
                            {'brand': 'U-Masa', 'dia': '36 inch', 'feeders': '135', 'gauge': '24 G', 'mc_no': 'A-10', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 10},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '136', 'gauge': '24 G', 'mc_no': 'A-11', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 11},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '137', 'gauge': '24 G', 'mc_no': 'A-12', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 12}]},
                  {'rows': [{'brand': 'Jiunn Long', 'dia': '34 inch', 'feeders': '102', 'gauge': '24 G', 'mc_no': 'B-1', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 1},
                            {'brand': 'Jiunn Long', 'dia': '42 inch', 'feeders': '102', 'gauge': '24 G', 'mc_no': 'B-2', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'U-Masa', 'dia': '34 inch', 'feeders': '102', 'gauge': '24 G', 'mc_no': 'B-3', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'U-Masa', 'dia': '34 inch', 'feeders': '102', 'gauge': '24 G', 'mc_no': 'B-4', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'B-5', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'B-6', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 6},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'B-7', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 7},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'B-8', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 8},
                            {'brand': 'U-Masa', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'B-9', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 9},
                            {'brand': 'U-Masa', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'B-10', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 10},
                            {'brand': 'U-Masa', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'B-11', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 11},
                            {'brand': 'U-Masa', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'B-12', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 12}]},
                  {'rows': [{'brand': 'Jiunn Long', 'dia': '32 inch', 'feeders': '96', 'gauge': '24 G', 'mc_no': 'C-1', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 1},
                            {'brand': 'U-Masa', 'dia': '32 inch', 'feeders': '96', 'gauge': '24 G', 'mc_no': 'C-2', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'C-3', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'C-4', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'C-5', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'C-6', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 6},
                            {'brand': 'NOT IN OPERATION', 'dia': '—', 'feeders': '—', 'gauge': '—', 'mc_no': 'C-7', 'mc_type': '—', 'origin': '—', 'qty': 1, 'sn': 7},
                            {'brand': 'U-Masa', 'dia': '36 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'C-8', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 8},
                            {'brand': 'U-Masa', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'C-9', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 9},
                            {'brand': 'U-Masa', 'dia': '40 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'C-10', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 10},
                            {'brand': 'U-Masa', 'dia': '40 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'C-11', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 11},
                            {'brand': 'U-Masa', 'dia': '42 inch', 'feeders': '126', 'gauge': '24 G', 'mc_no': 'C-12', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 12}]},
                  {'rows': [{'brand': 'U-Masa', 'dia': '28 inch', 'feeders': '84', 'gauge': '24 G', 'mc_no': 'D-1', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 1},
                            {'brand': 'U-Masa', 'dia': '30 inch', 'feeders': '90', 'gauge': '28 G', 'mc_no': 'D-2', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'U-Masa', 'dia': '26 inch', 'feeders': '78', 'gauge': '24 G', 'mc_no': 'D-3', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'U-Masa', 'dia': '28 inch', 'feeders': '84', 'gauge': '24 G', 'mc_no': 'D-4', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '28 inch', 'feeders': '112', 'gauge': '24 G', 'mc_no': 'D-5', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5},
                            {'brand': 'Jiunn Long', 'dia': '30 inch', 'feeders': '90', 'gauge': '24 G', 'mc_no': 'D-6', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 6},
                            {'brand': 'Samara ENT.', 'dia': '30 inch', 'feeders': '72', 'gauge': '24 G', 'mc_no': 'D-7', 'mc_type': 'Jacquard', 'origin': 'Bangladesh', 'qty': 1, 'sn': 7},
                            {'brand': 'Jiunn Long', 'dia': '32 inch', 'feeders': '96', 'gauge': '26 G', 'mc_no': 'D-8', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 8},
                            {'brand': 'Jiunn Long', 'dia': '32 inch', 'feeders': '96', 'gauge': '24 G', 'mc_no': 'D-9', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 9},
                            {'brand': 'Jiunn Long', 'dia': '34 inch', 'feeders': '102', 'gauge': '24 G', 'mc_no': 'D-10', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 10},
                            {'brand': 'Jiunn Long', 'dia': '34 inch', 'feeders': '102', 'gauge': '24 G', 'mc_no': 'D-11', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 11}]},
                  {'rows': [{'brand': 'Jiunn Long', 'dia': '32 inch', 'feeders': '96', 'gauge': '24 G', 'mc_no': 'E-1', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 1},
                            {'brand': 'U-Masa', 'dia': '32 inch', 'feeders': '96', 'gauge': '24 G', 'mc_no': 'E-2', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'E-3', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'E-4', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'E-5', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'E-6', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 6},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'E-7', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 7},
                            {'brand': 'U-Masa', 'dia': '36 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'E-8', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 8},
                            {'brand': 'U-Masa', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'E-9', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 9},
                            {'brand': 'U-Masa', 'dia': '40 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'E-10', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 10},
                            {'brand': 'NOT IN OPERATION', 'dia': '—', 'feeders': '—', 'gauge': '—', 'mc_no': 'E-11', 'mc_type': '—', 'origin': '—', 'qty': 1, 'sn': 11},
                            {'brand': 'U-Masa', 'dia': '42 inch', 'feeders': '126', 'gauge': '24 G', 'mc_no': 'E-12', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 12}]},
                  {'rows': [{'brand': 'Fukuhara', 'dia': '42 inch', 'feeders': '126', 'gauge': '18 G', 'mc_no': 'F-1', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 1},
                            {'brand': 'Jiunn Long', 'dia': '44 inch', 'feeders': '88', 'gauge': '18 G', 'mc_no': 'F-2', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'Jiunn Long', 'dia': '44 inch', 'feeders': '88', 'gauge': '18 G', 'mc_no': 'F-3', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'Jiunn Long', 'dia': '46 inch', 'feeders': '92', 'gauge': '18 G', 'mc_no': 'F-4', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '46 inch', 'feeders': '92', 'gauge': '18 G', 'mc_no': 'F-5', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5},
                            {'brand': 'Jiunn Long', 'dia': '46 inch', 'feeders': '92', 'gauge': '18 G', 'mc_no': 'F-6', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 6},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '72', 'gauge': '18 G', 'mc_no': 'F-7', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 7},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '72', 'gauge': '18 G', 'mc_no': 'F-8', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 8},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '76', 'gauge': '18 G', 'mc_no': 'F-9', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 9},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '76', 'gauge': '18 G', 'mc_no': 'F-10', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 10},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '70', 'gauge': '18 G', 'mc_no': 'F-11', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 11},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '80', 'gauge': '18 G', 'mc_no': 'F-12', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 12}]},
                  {'rows': [{'brand': 'Jiunn Long', 'dia': '34 inch', 'feeders': '102', 'gauge': '24 G', 'mc_no': 'G-1', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 1},
                            {'brand': 'Jiunn Long', 'dia': '34 inch', 'feeders': '68', 'gauge': '18 G', 'mc_no': 'G-2', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'Jiunn Long', 'dia': '34 inch', 'feeders': '68', 'gauge': '18 G', 'mc_no': 'G-3', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'Jiunn Long', 'dia': '34 inch', 'feeders': '72', 'gauge': '18 G', 'mc_no': 'G-4', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '72', 'gauge': '18 G', 'mc_no': 'G-5', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'G-6', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 6},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '72', 'gauge': '24 G', 'mc_no': 'G-7', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 7},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '72', 'gauge': '24 G', 'mc_no': 'G-8', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 8},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'G-9', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 9},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '80', 'gauge': '18 G', 'mc_no': 'G-10', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 10},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'G-11', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 11},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '80', 'gauge': '24 G', 'mc_no': 'G-12', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 12}]},
                  {'rows': [{'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '72', 'gauge': '20 G', 'mc_no': 'H-1', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 1},
                            {'brand': 'Jiunn Long', 'dia': '32 inch', 'feeders': '72', 'gauge': '22 G', 'mc_no': 'H-2', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'Jiunn Long', 'dia': '32 inch', 'feeders': '72', 'gauge': '18 G', 'mc_no': 'H-3', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'Jiunn Long', 'dia': '32 inch', 'feeders': '72', 'gauge': '22 G', 'mc_no': 'H-4', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '32 inch', 'feeders': '72', 'gauge': '22 G', 'mc_no': 'H-5', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5},
                            {'brand': 'Jiunn Long', 'dia': '34 inch', 'feeders': '84', 'gauge': '22 G', 'mc_no': 'H-6', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 6},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '72', 'gauge': '24 G', 'mc_no': 'H-7', 'mc_type': 'D/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 7},
                            {'brand': 'U-Masa', 'dia': '32 inch', 'feeders': '96', 'gauge': '24 G', 'mc_no': 'H-8', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 8},
                            {'brand': 'U-Masa', 'dia': '32 inch', 'feeders': '96', 'gauge': '24 G', 'mc_no': 'H-9', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 9},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'H-10', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 10}]},
                  {'rows': [{'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '20 G', 'mc_no': 'P-1', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 1},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '20 G', 'mc_no': 'P-2', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '20 G', 'mc_no': 'P-3', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '120', 'gauge': '20 G', 'mc_no': 'P-4', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '120', 'gauge': '20 G', 'mc_no': 'P-5', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5},
                            {'brand': 'Jiunn Long', 'dia': '40 inch', 'feeders': '120', 'gauge': '20 G', 'mc_no': 'P-6', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 6}]},
                  {'rows': [{'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '20 G', 'mc_no': 'P-7', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 1},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '20 G', 'mc_no': 'P-8', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '20 G', 'mc_no': 'P-9', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '14 G', 'mc_no': 'P-10', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '14 G', 'mc_no': 'P-11', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5}]},
                  {'rows': [{'brand': 'Jiunn Long', 'dia': '36 inch', 'feeders': '108', 'gauge': '20 G', 'mc_no': 'P-12', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 1},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '20 G', 'mc_no': 'P-13', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 2},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '20 G', 'mc_no': 'P-14', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 3},
                            {'brand': 'Jiunn Long', 'dia': '38 inch', 'feeders': '114', 'gauge': '20 G', 'mc_no': 'P-15', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 4},
                            {'brand': 'Jiunn Long', 'dia': '20 inch', 'feeders': '80', 'gauge': '24 G', 'mc_no': 'P-16', 'mc_type': 'S/J', 'origin': 'Taiwan', 'qty': 1, 'sn': 5}]}],
 'unit2_blocks': [{'rows': [{'brand': 'Fukuhara', 'dia': '38 inch', 'feeders': '48', 'gauge': '24 G', 'mc_no': 'J-1', 'mc_type': 'S/J (AS)', 'origin': 'Japan', 'qty': 1, 'sn': 1},
                            {'brand': 'Fukuhara', 'dia': '36 inch', 'feeders': '116', 'gauge': '24 G', 'mc_no': 'J-2', 'mc_type': 'S/J (AS)', 'origin': 'Japan', 'qty': 1, 'sn': 2},
                            {'brand': 'Fukuhara', 'dia': '36 inch', 'feeders': '116', 'gauge': '24 G', 'mc_no': 'J-3', 'mc_type': 'S/J (AS)', 'origin': 'Japan', 'qty': 1, 'sn': 3},
                            {'brand': 'Mayer&Cie', 'dia': '42 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'J-4', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 4},
                            {'brand': 'Mayer&Cie', 'dia': '42 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'J-5', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 5},
                            {'brand': 'Mayer&Cie', 'dia': '36 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'J-6', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 6},
                            {'brand': 'Mayer&Cie', 'dia': '36 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'J-7', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 7},
                            {'brand': 'Mayer&Cie', 'dia': '38 inch', 'feeders': '123', 'gauge': '24 G', 'mc_no': 'J-8', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 8},
                            {'brand': 'Mayer&Cie', 'dia': '38 inch', 'feeders': '123', 'gauge': '24 G', 'mc_no': 'J-9', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 9},
                            {'brand': 'Fukuhara', 'dia': '30 inch', 'feeders': '96', 'gauge': '36 G', 'mc_no': 'J-10', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 10}]},
                  {'rows': [{'brand': 'Fukuhara', 'dia': '38 inch', 'feeders': '48', 'gauge': '24 G', 'mc_no': 'K-1', 'mc_type': 'S/J (AS)', 'origin': 'Japan', 'qty': 1, 'sn': 1},
                            {'brand': 'Fukuhara', 'dia': '32 inch', 'feeders': '104', 'gauge': '24 G', 'mc_no': 'K-2', 'mc_type': 'S/J (AS)', 'origin': 'Japan', 'qty': 1, 'sn': 2},
                            {'brand': 'Fukuhara', 'dia': '34 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'K-3', 'mc_type': 'S/J (AS)', 'origin': 'Japan', 'qty': 1, 'sn': 3},
                            {'brand': 'Mayer&Cie', 'dia': '34 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'K-4', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 4},
                            {'brand': 'Mayer&Cie', 'dia': '34 inch', 'feeders': '108', 'gauge': '24 G', 'mc_no': 'K-5', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 5},
                            {'brand': 'Mayer&Cie', 'dia': '36 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'K-6', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 6},
                            {'brand': 'Mayer&Cie', 'dia': '36 inch', 'feeders': '114', 'gauge': '24 G', 'mc_no': 'K-7', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 7},
                            {'brand': 'Mayer&Cie', 'dia': '38 inch', 'feeders': '123', 'gauge': '24 G', 'mc_no': 'K-8', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 8},
                            {'brand': 'Fukuhara', 'dia': '38 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'K-9', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 9},
                            {'brand': 'Fukuhara', 'dia': '40 inch', 'feeders': '128', 'gauge': '24 G', 'mc_no': 'K-10', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 10}]},
                  {'rows': [{'brand': 'Fukuhara', 'dia': '44 inch', 'feeders': '90', 'gauge': '18 G', 'mc_no': 'L-1', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 1},
                            {'brand': 'Fukuhara', 'dia': '44 inch', 'feeders': '90', 'gauge': '18 G', 'mc_no': 'L-2', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 2},
                            {'brand': 'Fukuhara', 'dia': '34 inch', 'feeders': '48', 'gauge': '24 G', 'mc_no': 'L-3', 'mc_type': 'D/J (AS)', 'origin': 'Japan', 'qty': 1, 'sn': 3},
                            {'brand': 'Fukuhara', 'dia': '30 inch', 'feeders': '90', 'gauge': '20 G', 'mc_no': 'L-4', 'mc_type': 'S/J (3th F)', 'origin': 'Japan', 'qty': 1, 'sn': 4},
                            {'brand': 'Fukuhara', 'dia': '34 inch', 'feeders': '102', 'gauge': '20 G', 'mc_no': 'L-5', 'mc_type': 'S/J (3th F)', 'origin': 'Japan', 'qty': 1, 'sn': 5},
                            {'brand': 'Mayer&Cie', 'dia': '34 inch', 'feeders': '135', 'gauge': '24 G', 'mc_no': 'L-6', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 6},
                            {'brand': 'Mayer&Cie', 'dia': '34 inch', 'feeders': '135', 'gauge': '24 G', 'mc_no': 'L-7', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 7},
                            {'brand': 'Fukuhara', 'dia': '36 inch', 'feeders': '116', 'gauge': '24 G', 'mc_no': 'L-8', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 8},
                            {'brand': 'Fukuhara', 'dia': '36 inch', 'feeders': '116', 'gauge': '24 G', 'mc_no': 'L-9', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 9},
                            {'brand': 'Fukuhara', 'dia': '38 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'L-10', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 10},
                            {'brand': 'Fukuhara', 'dia': '38 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'L-11', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 11},
                            {'brand': 'Fukuhara', 'dia': '40 inch', 'feeders': '128', 'gauge': '24 G', 'mc_no': 'L-12', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 12}]},
                  {'rows': [{'brand': 'Fukuhara', 'dia': '44 inch', 'feeders': '90', 'gauge': '18 G', 'mc_no': 'M-1', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 1},
                            {'brand': 'Fukuhara', 'dia': '44 inch', 'feeders': '90', 'gauge': '18 G', 'mc_no': 'M-2', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 2},
                            {'brand': 'Fukuhara', 'dia': '42 inch', 'feeders': '86', 'gauge': '18 G', 'mc_no': 'M-3', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 3},
                            {'brand': 'Fukuhara', 'dia': '40 inch', 'feeders': '82', 'gauge': '18 G', 'mc_no': 'M-4', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 4},
                            {'brand': 'Fukuhara', 'dia': '36 inch', 'feeders': '74', 'gauge': '20 G', 'mc_no': 'M-5', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 5},
                            {'brand': 'Mayer&Cie', 'dia': '36 inch', 'feeders': '144', 'gauge': '24 G', 'mc_no': 'M-6', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 6},
                            {'brand': 'Fukuhara', 'dia': '38 inch', 'feeders': '120', 'gauge': '28 G', 'mc_no': 'M-7', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 7},
                            {'brand': 'Fukuhara', 'dia': '38 inch', 'feeders': '120', 'gauge': '28 G', 'mc_no': 'M-8', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 8},
                            {'brand': 'Fukuhara', 'dia': '40 inch', 'feeders': '128', 'gauge': '28 G', 'mc_no': 'M-9', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 9},
                            {'brand': 'Fukuhara', 'dia': '40 inch', 'feeders': '128', 'gauge': '28 G', 'mc_no': 'M-10', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 10},
                            {'brand': 'Fukuhara', 'dia': '40 inch', 'feeders': '128', 'gauge': '24 G', 'mc_no': 'M-11', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 11},
                            {'brand': 'Fukuhara', 'dia': '40 inch', 'feeders': '128', 'gauge': '24 G', 'mc_no': 'M-12', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 12}]},
                  {'rows': [{'brand': 'Fukuhara', 'dia': '44 inch', 'feeders': '90', 'gauge': '18 G', 'mc_no': 'N-1', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 1},
                            {'brand': 'Fukuhara', 'dia': '42 inch', 'feeders': '86', 'gauge': '18 G', 'mc_no': 'N-2', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 2},
                            {'brand': 'Fukuhara', 'dia': '42 inch', 'feeders': '86', 'gauge': '18 G', 'mc_no': 'N-3', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 3},
                            {'brand': 'Fukuhara', 'dia': '40 inch', 'feeders': '82', 'gauge': '18 G', 'mc_no': 'N-4', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 4},
                            {'brand': 'Fukuhara', 'dia': '40 inch', 'feeders': '82', 'gauge': '18 G', 'mc_no': 'N-5', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 5},
                            {'brand': 'Mayer&Cie', 'dia': '36 inch', 'feeders': '144', 'gauge': '24 G', 'mc_no': 'N-6', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 6},
                            {'brand': 'Mayer&Cie', 'dia': '36 inch', 'feeders': '144', 'gauge': '24 G', 'mc_no': 'N-7', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 7},
                            {'brand': 'Mayer&Cie', 'dia': '38 inch', 'feeders': '123', 'gauge': '24 G', 'mc_no': 'N-8', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 8},
                            {'brand': 'Mayer&Cie', 'dia': '38 inch', 'feeders': '123', 'gauge': '24 G', 'mc_no': 'N-9', 'mc_type': 'S/J', 'origin': 'Germany', 'qty': 1, 'sn': 9},
                            {'brand': 'Fukuhara', 'dia': '38 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'N-10', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 10},
                            {'brand': 'Fukuhara', 'dia': '38 inch', 'feeders': '120', 'gauge': '24 G', 'mc_no': 'N-11', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 11},
                            {'brand': 'Fukuhara', 'dia': '36 inch', 'feeders': '116', 'gauge': '24 G', 'mc_no': 'N-12', 'mc_type': 'S/J', 'origin': 'Japan', 'qty': 1, 'sn': 12}]},
                  {'rows': [{'brand': 'Fukuhara', 'dia': '42 inch', 'feeders': '86', 'gauge': '18 G', 'mc_no': 'R-1', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 1},
                            {'brand': 'Fukuhara', 'dia': '42 inch', 'feeders': '86', 'gauge': '18 G', 'mc_no': 'R-2', 'mc_type': 'D/J', 'origin': 'Japan', 'qty': 1, 'sn': 2}]}]}

FAB_MAP = {
    "S/J": "Single Jersey",
    "S/J (AS)": "Single Jersey",
    "S/J (3th F)": "Single Jersey",
    "D/J": "Rib",
    "D/J (AS)": "Rib",
    "Jacquard": "Single Jersey",
}


def _parse_num(s):
    m = re.search(r"(\d+(?:\.\d+)?)", str(s or ""))
    return float(m.group(1)) if m else 0.0


def seed(conn):
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Fakir Knitwear%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    chk = cur.execute(
        """
        SELECT COUNT(*) as c,
               COALESCE(SUM(quantity), 0) as tot_q,
               COALESCE(SUM(CASE WHEN COALESCE(in_operation, 1) = 1 THEN quantity ELSE 0 END), 0) as op_q
        FROM machine_profiles WHERE industry_id = ? AND unit != ''
        """,
        (ind_id,),
    ).fetchone()
    if chk["tot_q"] == 167 and chk["op_q"] == 165:
        return

    cur.execute("DELETE FROM machine_profiles WHERE industry_id = ?", (ind_id,))
    sort_idx = 0
    for unit_name, blocks in [
        ("Unit-1", FAKIR_SAVED_DATA["unit1_blocks"]),
        ("Unit-2", FAKIR_SAVED_DATA["unit2_blocks"]),
    ]:
        for b in blocks:
            for r in b["rows"]:
                sort_idx += 1
                raw_brand = (r["brand"] or "—").strip()
                in_op = 0 if "NOT IN OPERATION" in raw_brand.upper() else 1
                brand = "—" if not in_op else raw_brand.replace("Mayer&Cie", "Mayer & Cie")
                raw_type = (r["mc_type"] or "—").strip()
                fab = "Single Jersey" if not in_op else FAB_MAP.get(raw_type, "Single Jersey")
                dia = _parse_num(r["dia"]) if in_op else 0.0
                gauge = _parse_num(r["gauge"]) if in_op else 0.0
                label = f"{int(dia)}x{int(gauge)}" if (dia > 0 and gauge > 0) else "—"
                feeders = int(r["feeders"]) if str(r["feeders"]).isdigit() else None
                origin = r["origin"] if r["origin"] != "—" else ""
                qty = int(r["qty"] or 1)
                calc = calculate_needle_sinker(fab, dia, gauge, qty if in_op else 0)
                remarks = "NOT IN OPERATION" if not in_op else ""

                cur.execute(
                    """
                    INSERT INTO machine_profiles (
                        industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                        needles_per_machine, sinkers_per_machine, remarks,
                        unit, machine_category, machine_type, feeders, origin,
                        machine_no, in_operation, sort_order
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Circular', ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        ind_id,
                        fab,
                        dia,
                        gauge,
                        label,
                        brand,
                        qty,
                        calc["needles_per_machine"],
                        calc["sinkers_per_machine"],
                        remarks,
                        unit_name,
                        raw_type if in_op else "Not in Operation",
                        feeders,
                        origin,
                        r["mc_no"],
                        in_op,
                        sort_idx,
                    ),
                )
    conn.commit()
