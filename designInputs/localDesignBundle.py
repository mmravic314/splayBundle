#!/usr/bin/env python2

#$ -S /usr/bin/python
#$ -l mem_free=1G
#$ -l arch=linux-x64
#$ -l netapp=1G
#$ -l h_core=0
#$ -cwd

import os, sys#; sys.path.append(os.getcwd())
import subprocess
#from libraries import big_job

### MM sample input
# python localDesignBundle.py path2rosettaMain path2BBsDirectory path2RosScript path2ResFile path2SymmetryFile
# python designInputs/localDesignBundle.py ~/bin/Rosetta/main/ designInputs/1WZDbb/ designInputs/1WZDbb/RC_helicalBundle_MM designInputs/1WZDbb/resfile designInputs/1WZDbb/2L.symm

# Symmetryfile creation
#perl ~/bin/Rosetta/main/source/src/apps/public/symmetry/make_symmdef_file.pl -m NCS -p 1WZDbb/2L-1WZDR.pdb  -i C > 1WZDbb/2L.symm

#workspace, job_id, task_id, parameters = big_job.initiate()

#bb_models = parameters['inputs']
bb_model        = [ os.path.join( sys.argv[2], f  ) for f in os.listdir( sys.argv[2] )  if f[-9:] == 'INPUT.pdb' ][0]  # Change index to task ID relation
#design_id       = task_id // len(bb_models)

#sys.exit()

rosetta_database_path   = os.path.join( sys.argv[1] , 'database/' )
rosetta_scriptsEXE_path = os.path.join( sys.argv[1], 'source/bin/rosetta_scripts.linuxgccrelease' )
design_script_path      = os.path.abspath( sys.argv[3] )
outDr                   = os.path.join( sys.argv[2], os.path.basename( bb_model)[:7] ) + '/'
resfile_path            = os.path.abspath( sys.argv[4] )
symmfile_path           = os.path.abspath( sys.argv[5] )  
#path2dalphaballEXE      = os.path.abspath( sys.argv[6] )           

if not os.path.exists( os.path.dirname(outDr) ):
        os.mkdir( os.path.dirname(outDr) )

rosetta_command = [
        rosetta_scriptsEXE_path,
        '-database', rosetta_database_path,
        '-in:file:s', bb_model,
        '-in:file:native', bb_model,                    ## Recall what these two mean
        '-out:prefix', outDr,
        '-out:suffix', '_0.pdb_gz',                                   ## Change for indices
        '-out:no_nstruct_label',
        '-out:overwrite',
        '-out:pdb_gz', 
        '-parser:protocol', design_script_path,
        #'-parser:script_vars', 'cst_file=' + workspace.restraints_path,
        '-packing:resfile', resfile_path 
       #'-holes:dalphaball', path2dalphaballEXE
        #'-symmetry:symmetry_definition', symmfile_path

        #'@', workspace.flags_path,
]
print 
print rosetta_command
print 
print 
subprocess.call( rosetta_command  )

# python designInputs/localDesignBundle.py ~/bin/Rosetta/main/ designInputs/1WZDbb/ designInputs/1WZDbb/RC_helicalBundle_MM.xml designInputs/1WZDbb/resfile designInputs/1WZDbb/2L.symm
