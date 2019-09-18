from __future__ import print_function

import ROOT
ROOT.ROOT.EnableImplicitMT()
import os
import pprint
import pandas as pd 
from pprint import pprint

curdir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Fall2017_102X_nAODv4_Full2017v5/MCl1loose2017v5__MCCorr2017v5__VBSjjlnuSkim2017v3"

file_path = os.path.join(curdir, "nanoLatino_WpToLNu_WmTo2J_*.root")
print(file_path)

df = ROOT.RDataFrame("Events",file_path)


ROOT.gInterpreter.Declare("""
    template
    <typename container>
    float Alt(container c, int index, float alt){
        if (index < c.size()) {
            return c[index];
        }
        else{
            return alt;
        }
    }
""")


#########
#ALIASES#
#########
aliases = {}

aliases['bVeto'] = {
'expr': '2;'
}

aliases['btag0'] = {
'expr': '1;'
}

#########
###CUTS##
#########
cuts = {}
cuts['supercut'] = {
  'expr': '(nLepton==1 && Lepton_pt[0]>30 ) \
            && (  Lepton_isTightElectron_mvaFall17V2Iso_WP90[0] > 0.5 \
                    || Lepton_isTightMuon_cut_Tight_HWWW[0] > 0.5) \
                && Alt(Lepton_pt,1,0)<=10 && Alt(Lepton_isLoose,1,1)>0.5\
                && ( Alt(Lepton_isTightElectron_mvaFall17V2Iso_WP90,1, 0) < 0.5 \
                && Alt(Lepton_isTightMuon_cut_Tight_HWWW,1,0) < 0.5 ) \
            && VBS_category ==1    \
            && vbs_pt_low >= 30    \
            && vjet_pt_low >= 30    \
           ',
  'parent': None,
  'doVars': False,
  'doHisto': False,
  'doNumpy': False
}

cuts['ele_looseVBS'] ={
  'expr' : 'abs(Lepton_pdgId[0])==11 \
              && Lepton_pt[0] >= 40 \
              mjj_vbs >=300    \
              && deltaeta_vbs >= 2',
  'parent': 'supercut',
  'doVars': True,
  'doHisto': False,
  'doNumpy': False        
}

cuts['ele_looseVBS'] ={
  'expr' : 'abs(Lepton_pdgId[0])==13 \
              && Lepton_pt[0] >= 30   \
              && mjj_vbs >=300  \
              && deltaeta_vbs >= 2',
  'parent': 'supercut',
  'doVars': True,
  'doHisto': False,
  'doNumpy': False        
}

###########
#VARIABLES#
###########
variables = {}


variables['njet']  = {
                        'name': "Sum(CleanJet_pt > 30);",
                        'range' : (5,0,5),
                        'xaxis' : 'Number of jets',
                        'fold' : 2   # 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow
                        }

variables['jetpt1']  = {
                        'name': 'CleanJet_pt[0]',
                        'range' : (40,15,50),
                        'xaxis' : 'p_{T} 1st jet',
                        'fold' : 2   # 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow
                        }

output_variables= ["mjj_vbs", "vbs_pt_high", "mjj_vjet", "bVeto", "btag0"] 


def define_aliases(df, aliases):

  for key in aliases.keys():
    df = df.Define(key, aliases[key]["expr"])

  return df

def define_cut(parent_cut, cuts):
  for key, cut in cuts.items():
    if cut["parent"] == parent_cut:
      cuts[key]["rdf_node"] = cuts[parent_cut]["rdf_node"].Filter(cut["expr"], key)
      define_cut(key, cuts)

def define_variable(cuts, variables):
  for cutkey, cutvalue in cuts.items():

    if cutvalue["doVars"] == True:
      cutvalue["histos"] = {}
      cutvalue["rdf_node_cache"] = [cutvalue["rdf_node"]]

      for varkey, varvalue in variables.items():
        last_def = cutvalue["rdf_node_cache"].append(cutvalue["rdf_node_cache"][-1].Define(cutkey+"_var_"+varkey, varvalue["name"]))
        if cutvalue["doHisto"] == True:
          cutvalue["histos"][varkey] = last_def.Histo1D( (varkey, varkey, 
                        varvalue["range"][0],varvalue["range"][1],varvalue["range"][2] ),
                        cutkey+"_var_"+varkey )

      cutvalue["rdf_node"] = cutvalue["rdf_node_cache"][-1]
  

aliases_df = define_aliases(df, aliases)


cuts["supercut"]["rdf_node"] = aliases_df.Filter(cuts["supercut"]["expr"], "supercut")

define_cut("supercut", cuts)
define_variable(cuts, variables)
pprint(cuts)

p = pd.DataFrame( cuts["ele_looseVBS"]["rdf_node"].AsNumpy(columns=output_variables))

print(p)
# plot(cuts)
