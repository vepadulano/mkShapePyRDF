import PyRDF

PyRDF.use("local")
PyRDF.include_headers("./headers.hh")

import latinos_reader as lr  

trees = lr.build_dataframe("./lowenergy", "VBS", PyRDF, "pyrdf")

