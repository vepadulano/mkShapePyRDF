import PyRDF

PyRDF.use("local")
PyRDF.include_headers("./headers.hh")

import latinos_reader as lr  

trees = lr.build_dataframe("./lowenergy", "VBS", PyRDF, "pyrdf")
tree = trees[0]

# print( tree.lowen_ele_looseVBS.rdf_node.AsNumpy(columns=["mjj_vbs"]) )
# m = tree.lowen_ele_looseVBS.rdf_node.Mean("mjj_vbs")
# print( m.GetValue() )

