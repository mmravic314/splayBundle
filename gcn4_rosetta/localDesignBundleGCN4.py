#!/usr/bin/env python2

#$ -S /usr/bin/python
#$ -l mem_free=1G
#$ -l arch=linux-x64
#$ -l netapp=1G
#$ -l h_core=0
#$ -cwd

import os, sys
import subprocess

rosetta_database_path   = os.path.join( sys.argv[1] , 'database/' )
rosetta_scriptsEXE_path = os.path.join( sys.argv[1], 'source/bin/rosetta_scripts.linuxgccrelease' )
design_script_path      = os.path.abspath( sys.argv[3] )
#resfile_path            = os.path.abspath( sys.argv[4] )


rosetta_command = [
        rosetta_scriptsEXE_path,
        '-database', rosetta_database_path,
        '-in:file:s', sys.argv[2],
        '-out:no_nstruct_label',
        '-out:overwrite',
        '-out:suffix', '_Rout',
        #'-packing:resfile', resfile_path,
        '-parser:protocol', design_script_path

       #'-holes:dalphaball', path2dalphaballEXE

        ]
print 
print rosetta_command
print 
print 
subprocess.call( rosetta_command  )
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