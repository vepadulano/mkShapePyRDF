# variabeadines

#variables = {}
    
    
variables['lep_flavour'] = {   'name': 'abs(Lepton_pdgId[0])',      
                        'range' : (10,0,10),  
                        'xaxis' : 'Lepton flavour', 
                        'fold' : 3
                        }


variables['events']  = {   'name': '1',      
                        'range' : (1,0,2),  
                        'xaxis' : 'events', 
                        'fold' : 3
                        }

#jets 

variables['nJets'] = {   'name': 'Sum(CleanJet_pt >= 30)',      
                        'range' : (10,0,10),  
                        'xaxis' : 'nJets >= 30 GeV', 
                        'fold' : 3
                        }

#leptons

variables['lep_eta'] = {   'name': 'abs(Lepton_eta[0])',      
                        'range' : (40,0,2.5),  
                        'xaxis' : 'Lepton #eta', 
                        'fold' : 3
                        }


variables['lep_pt'] = {   'name': 'Lepton_pt[0]',      
                        'range' : (40,0,300),  
                        'xaxis' : 'Lepton pt', 
                        'fold' : 3
                        }                       

variables["vbs_index_high"] = {   'name': 'VBS_jets_maxmjj_massWZ[0]',      
                        'range' : (10,0,10),  
                        'xaxis' : 'Index leading VBS jet', 
                        'fold' : 3
                        }

variables["vbs_index_low"] = {   'name': 'VBS_jets_maxmjj_massWZ[1]',      
                        'range' : (10,0,10),  
                        'xaxis' : 'Index trailing VBS jet', 
                        'fold' : 3
                        }

variables["vjet_index_high"] = {   'name': 'V_jets_maxmjj_massWZ[0]',      
                        'range' : (10,0,10),  
                        'xaxis' : 'Index leading V-jet', 
                        'fold' : 3
                        }

variables["vjet_index_low"] = {   'name': 'V_jets_maxmjj_massWZ[1]',      
                        'range' : (10,0,10),  
                        'xaxis' : 'Index trailing V-jet', 
                        'fold' : 3
                        }

