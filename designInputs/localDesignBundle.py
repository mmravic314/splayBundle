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
# python designInputs/localDesignBundle.py ~/bin/Rosetta/main/ designInputs/1WZDbb/ designInputs/1WZDbb/RC_helicalBundle_extact designInputs/1WZDbb/resfile

# Symmetryfile creation

#workspace, job_id, task_id, parameters = big_job.initiate()

#bb_models = parameters['inputs']
bb_model        = [ os.path.join( sys.argv[2], f  ) for f in os.listdir( sys.argv[2] )  if f[-9:] == 'INPUT.pdb' ][0]  # Change index to task ID relation
#design_id       = task_id // len(bb_models)

#sys.exit()

rosetta_database_path   = os.path.join( sys.argv[1] , 'database/' )
rosetta_scriptsEXE_path = os.path.join( sys.argv[1], 'source/src/apps/public/rosetta_scripts/rosetta_scripts.cc' )
design_script_path      = os.path.abspath( sys.argv[3] )
outDr                   = os.path.join( sys.argv[2], f[-9:]  ) + '/'
resfile_path            = sos.path.abspath( sys.argv[4] )
#symmfile_path           = sys.argv[5]               


rosetta_command = [
        rosetta_scriptsEXE_path,
        '-database', rosetta_database_path,
        '-in:file:s', bb_model,
        '-in:file:native', bb_model,                    ## Recall what these two mean
        '-out:prefix', outDr,
        '-out:suffix', '_0',                                   ## Change for indices
        '-out:no_nstruct_label',
        '-out:overwrite',
        '-out:pdb_gz', 
        '-parser:protocol', design_script_path,
        #'-parser:script_vars', 'cst_file=' + workspace.restraints_path,
        '-packing:resfile', resfile_path 
        ########### SYMMETRY FILE + PATH
        #'@', workspace.flags_path,
]
print 
print rosetta_command
#subprocess.call(rosetta_command)
