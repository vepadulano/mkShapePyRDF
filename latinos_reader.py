import os
import json
import copy
from pprint import pprint
import ROOT as R

class Node:
  def __init__(self, name, obj):
    self.name = name
    self.expr = obj["expr"]
    self.vars = []
    self.aliases = []
    self.weight = None
    self.parent = obj["parent"]
    self.doVars = obj.get("doVars", False)
    self._rdf_cache = []

  @property
  def rdf_node(self):
    return self._rdf_cache[-1]

  @rdf_node.setter
  def rdf_node(self, node):
    self._rdf_cache.append(node)

  def __getattr__(self, key):
    return getattr(self.rdf_node,key)

  def __str__(self):
    out = []
    out.append("name: {}".format( self.name))
    out.append("parent: {}".format( self.parent))
    #out.append("cache: {}".format( self._rdf_cache))
    out.append("cut: {}".format( self.expr))
    out.append("vars: {}".format(",".join(self.vars)))
    out.append("aliases: {}".format(",".join(self.aliases)))
    out.append("weight: {}".format(self.weight))
    return "\n".join(out)

  def __repr__(self):
    return str(self)

#########################################################################

class Tree:

  def __init__(self, cuts):
    self.tree = {}
    for key, obj in cuts.items():
      self.tree[key] = Node(key, obj)
    
      
  def define_aliases(self, node, aliases):
    if node not in self.tree:
      print("Node not found in tree")
      return False
    for key in aliases.keys():
      self.tree[node].rdf_node = self.tree[node].rdf_node.Define(key, aliases[key]["expr"])
      self.tree[node].aliases.append(key)
    return True

  def define_cuts(self, cut):
    if cut not in self.tree:
      print("Cut not found")
      return False
    # Create the filter
    node = self.tree[cut]
    if node.parent == None:
      #it's the supercut
      node.rdf_node = node.rdf_node.Filter(node.expr, cut)
    else:
      node.rdf_node = self.tree[node.parent].rdf_node.Filter(node.expr, cut)
    # Now do it for each children
    for child_node in self.tree.values():
      if child_node.parent == node.name:
        self.define_cuts(child_node.name)

  def define_variables(self, variables):
    for name, node in self.tree.items():
      if node.doVars == True:
        for varkey, varvalue in variables.items():
          node.rdf_node = node.rdf_node.Define(name+"_var_"+varkey, varvalue["name"])
          node.vars.append(name+"_var_"+varkey)

  def define_weight(self, weight):
    for name, node in self.tree.items():
      if node.doVars == True:
        node.rdf_node = node.rdf_node.Define("weight", weight)
        node.weight = weight

  
  def __getattr__(self, key):
    return self.tree.get(key, None)

  def __getitem__(self, key):
    return self.tree.get(key, None)

  def __str__(self):
    out = []
    for name, node in self.tree.items():
      out.append(str(node))
      out.append("--------------------------------------------------------------------------------")
    return "\n".join(out)
     
  

#######################################################################################################

def build_dataframe(conf_dir, sample, rdf_class, rdf_type):
    
  samples = json.load(open(conf_dir + "/samples.json"))
  variables = {}
  cuts = {}
  aliases = {}

  exec(open(conf_dir+"/cuts.py").read())
  exec(open(conf_dir+"/variables.py").read())
  exec(open(conf_dir+"/aliases.py").read())

  # Let's read the sample files as requested
  if sample not in samples:  
    print("Requested sample not exists!")
    return None

  sample_data = samples[sample]

  # We have to check is there is a weights entries: 
  # in that case we have to group the file in different DF 
  dfs = []
  weights_group = []

  if "weights" in sample_data:
    # dividere il dataframe in diversi pezzi
    pass

  else:
    if rdf_type == "root":
      files = R.std.vector("string")
      for f in sample_data["name"]:
        files.push_back(f[3:])
    else:
      files = [ f[3:] for f in sample_data["name"] ]

    # Create RDataFrame
    df = rdf_class.RDataFrame("Events", files)
    dfs.append(df)

 
  # Now for each initial DF, 
  # Create alias, create cuts, create variables
  chains = []

  for idf, df in enumerate(dfs):
    # The cut tree is the base structure
    tree = Tree(cuts)
    tree.supercut.rdf_node = df
    tree.define_aliases("supercut", aliases)   

    tree.define_cuts("supercut")
    tree.define_variables(variables)

    # Now add the sample global weight
    weight = "("+ sample_data["weight"].replace("XSWeight", "1") +")"
    if weights_group:
      weight += "*("+ weights_group[idf] + ")"
    tree.define_weight(weight)

    chains.append(tree)

  
  return chains

