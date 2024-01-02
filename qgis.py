


two_d_mesh= iface.addVectorLayer("G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Calculated Layers\mc_2d_mesh.shp", "mc_2d_mesh", "ogr")

hwm= iface.addVectorLayer("G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Calculated Layers\hwm_test.shp", "hwm_test", "ogr")


processing.run("native:joinattributesbylocation", {'INPUT':'G:\\WATER_MG\\HEC-RAS\\MillCreek_43B05990\\'
                                                           'Calculated Layers\\hwm_test.shp','PREDICATE':[5],
                                                   'JOIN':'G:\\WATER_MG\\HEC-RAS\\MillCreek_43B05990\\'
                                                          'Calculated Layers\\mc_2d_mesh.shp','JOIN_FIELDS':[],
                                                   'METHOD':1,'DISCARD_NONMATCHING':True,'PREFIX':'',
                                                   'OUTPUT':'TEMPORARY_OUTPUT'})
