from __future__ import print_function

import PyRDF
import ROOT
import os
import pprint
curdir = os.getcwd()

file_path = os.path.join(curdir, "nanoLatino_DYJetsToLL_M-50-LO__part3.root")
print(file_path)

df = ROOT.RDataFrame("Events",file_path)

ROOT.gInterpreter.Declare("""
    template
    <typename container>
    float alternate(container c, int index, float alt){
        if (index < c.size()) {
            return c[index];
        }
        else{
            return alt;
        }
    }
""")


# c = ROOT.TCanvas("name","title", 800, 700)
# myhist = df.Range(100).Histo1D("CaloMET_pt")
# myhist.Draw()
# c.SaveAs("img_jetpt1.png")


#########
#ALIASES#
#########
aliases = {}

aliases['bVeto'] = {
'expr': 'auto condition_vec = (CleanJet_pt > 20. && abs(CleanJet_eta)<2.5 && Jet_btagDeepB[CleanJet_jetIdx] > 0.1241); \
         return std::accumulate(condition_vec.begin(), condition_vec.end(), 0) == 0;'
}

aliases['btag0'] = {
'expr': 'auto condition_vec =  (CleanJet_pt > 20. && abs(CleanJet_eta)<2.5 && Jet_btagDeepB[CleanJet_jetIdx] > 0.1241); \
         return alternate(CleanJet_pt, 0, 0) < 30 && std::accumulate(condition_vec.begin(), condition_vec.end(), 0) > 0;'
}

#########
###CUTS##
#########
cuts = {}
cuts['supercut'] = {
  'expr': 'mll>60 && Lepton_pt[0]>20 && Lepton_pt[1]>10 && \
           (nLepton>=2 && alternate(Lepton_pt, 2, 0)<10) && abs(Lepton_eta[0])<2.5 \
           && abs(Lepton_eta[1])<2.5',
  'parent': None,
  'doVars': False
}

cuts['Zee'] = {
  'expr': '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11)   \
                 && Lepton_pt[0]>25 && Lepton_pt[1]>13 \
                 && mll>60 && mll<120 ;\
               ',
  'parent': 'supercut',
  'doVars': True
}

cuts['Zmm'] = {
  'expr': '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13)  \
                 && mll>60 && mll<120;',
  'parent': 'supercut',
  'doVars': True
}

###########
#VARIABLES#
###########
variables = {}

variables['njet']  = {
                        'name': "auto condition_vec = CleanJet_pt > 15;\
                         return std::accumulate(condition_vec.begin(), condition_vec.end(), 0);",
                        'range' : (5,0,5),
                        'xaxis' : 'Number of jets',
                        'fold' : 2   # 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow
                        }

variables['jetpt1']  = {
                        'name': 'CleanJet_pt[0]*(CleanJet_pt[0]>0);',
                        'range' : (40,15,50),
                        'xaxis' : 'p_{T} 1st jet',
                        'fold' : 2   # 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow
                        }


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

      for varkey, varvalue in variables.items():
        last_def = cutvalue["rdf_node"].Define(cutkey+"_var_"+varkey, varvalue["name"])
        cutvalue["histos"][varkey] = last_def.Histo1D((varkey, varkey, varvalue["range"][0],varvalue["range"][1],varvalue["range"][2] ), cutkey+"_var_"+varkey )


def plot(cuts):
  print("\n\nEntering plot function\n\n")
  pprint.pprint(cuts)
  for cutkey, cutvalue in cuts.items():
    if "histos" in cutvalue.keys():
      for var, histo in cutvalue["histos"].items():
        print("Printing {} canvas with {} histogram".format(cutkey+"_"+var, var))
        c = ROOT.TCanvas(cutkey+"_"+var, cutkey+"_"+var, 800,700)
        histo.Draw()
        c.SaveAs("img_{}.png".format(var))
        break

aliases_df = define_aliases(df, aliases)

cuts["supercut"]["rdf_node"] = aliases_df.Filter(cuts["supercut"]["expr"], "supercut")
define_cut("supercut", cuts)
pprint.pprint(cuts)
define_variable(cuts, variables)
pprint.pprint(cuts)

plot(cuts)
