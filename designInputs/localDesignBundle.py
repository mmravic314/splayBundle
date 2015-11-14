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
bb_models        = [ os.path.join( sys.argv[2], f  ) for f in os.listdir( sys.argv[2] )  if f[-5:] == 'R.pdb' ]  # Change index to task ID relation
#design_id       = task_id // len(bb_models)


rosetta_database_path   = os.path.join( sys.argv[1] , 'database/' )
rosetta_scriptsEXE_path = os.path.join( sys.argv[1], 'source/bin/rosetta_scripts.linuxgccrelease' )
design_script_path      = os.path.abspath( sys.argv[3] )
resfile_path            = os.path.abspath( sys.argv[4] )
#symmfile_path           = os.path.abspath( sys.argv[5] )  
#path2dalphaballEXE      = os.path.abspath( sys.argv[6] )

for bb in bb_models:

           
        outDr           = os.path.join( sys.argv[2], os.path.basename( bb)[:9] ) + '/'
        if not os.path.exists( os.path.dirname(outDr) ):
            os.mkdir( os.path.dirname(outDr) )

        rosetta_command = [
        rosetta_scriptsEXE_path,
        '-database', rosetta_database_path,
        '-in:file:s', bb,
        '-in:file:native', bb,                    ## Recall what these two mean
        '-out:prefix', outDr,
        '-out:suffix', '_0.pdb_gz',                                   ## Change for indices
        '-out:no_nstruct_label',
        '-out:overwrite',
        #'-out:pdb_gz', 
        '-packing:resfile', resfile_path,
        '-parser:protocol', design_script_path
        #'-parser:script_vars', 'cst_file=' + workspace.restraints_path,

       #'-holes:dalphaball', path2dalphaballEXE
        #'-symmetry:symmetry_definition', symmfile_path

        #'@', workspace.flags_path,
        ]
        print 
        print rosetta_command
        print 
        print 
        subprocess.call( rosetta_command  )

        print 
        print 
print 
print

# python designInputs/localDesignBundle.py ~/bin/Rosetta/main/ designInputs/1WZDbb/ designInputs/1WZDbb/RC_helicalBundle_MM.xml designInputs/1WZDbb/resfile designInputs/1WZDbb/2L.symm

''' 
25 A H
26 A Apolar
29 A DEH

#Surface
61 A Polar
28 A Polar
75 A Polar
82 A Polar

73 A EH

84 A PIKAA MYFILATSVE
67 A PIKAA MYFILATSVEH


* A ALLAAxc
#101 - 200 C ALLAAxc

'''

## python designInputs/localDesignBundle.py ~/bin/Rosetta/main/ designInputs/3BVX-2L/ designInputs/3BVX-2L/RC_helicalBundle_MM_3BVX.xml  designInputs/3BVX-2L/resfile3BVX

##  python designInputs/localDesignBundle.py ~/bin/Rosetta/main/ designInputs/3BVX-2L/ designInputs/3BVX-2L/RC_helicalBundle_MM_3BVX.xml  designInputs/3BVX-