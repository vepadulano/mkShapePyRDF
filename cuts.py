##############################
###########CUTS###############
##############################

cuts = {}

# Supercut is a Filter() after the first round of Define() calls.

cuts['supercut'] = {
  'expr': 'mll>60 && Lepton_pt[0]>20 && Lepton_pt[1]>10 && \
    (nLepton>=2 && Alt$(Lepton_pt[2],0)<10) && abs(Lepton_eta[0])<2.5 \
      && abs(Lepton_eta[1])<2.5',
  'parent': None,
  'doVars': False
}

cuts['Zee'] = {
  'expr': '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11)   \
                 && Lepton_pt[0]>25 && Lepton_pt[1]>13 \
                 && mll>60 && mll<120 \
               ',
  'parent': 'supercut',
  'doVars': True
}

cuts['Zmm'] = {
  'expr': '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13)  \
                 && mll>60 && mll<120'
  'parent': 'supercut',
  'doVars': True
}


cuts['Zmm_bigeta']  = {
  'expr' : 'abs(CleanJet_eta[0]) > 3',
  'parent': 'Zmm',
  'doVars': True
}

cuts['Zmm_smalleta']  = {
  'expr' : 'abs(CleanJet_eta[0]) < 2.5',
  'parent': 'Zmm',
  'doVars': True
}
