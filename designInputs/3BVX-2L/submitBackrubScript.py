## Python script to keep track of input options for rosetta backrub jobs
## All options for backrub executable are hardcoded here, versus in input  
# 
# python submitBackrubScript.py path2RosettaMain/ path2inputPDB path2outputDir

import sys, os , subprocess as sp

ros_db   	= os.path.join( sys.argv[1] , 'database/' )
brub_exe 	= os.path.join( sys.argv[1], 'source/bin/backrub.linuxgccrelease' )

inputF		= sys.argv[2]
outDir	 	= sys.argv[3]
#resfile 	= sys.argv[4]
#c_fa_weight= sys.argv[5]
#c_fa_file	= sys.argv[6]


if not os.path.exists( outDir ):
	os.mkdir( outDir )


## options for rosetta

cmd  = [ brub_exe,
'-in:path:database'	, ros_db 	,
'-in:file:s'		, inputF 	,
'-out:nstruct'      , '1' 		,
#'-packing:resfile'	, resfile	,
#'-pivot_atoms'		, 'CA,N,C,O',	
'-ntrials'			, '30000'	,			# Takes 300 seconds (5 minutes)
#'-initial_pack'		, 'True'	,
'-mc_kt'			, '0.5',
'-out:overwrite'
]

sp.call( cmd )

"""
                              |                           |    |
                    in:path:   |                           |    | 
                      database |                           | (P)| Database file input search 
                               |                           |    |  paths.  If the database is 
                               |                           |    |  not found the ROSETTA3_DB 
                               |                           |    |  environment variable is 
                               |                           |    |  tried.
                               |                           |    |
                    in:file:   |                           |    | 
                             s |                           | (F)| Name(s) of single PDB 
                               |                           |    |  file(s) to process
                             l |                           | (F)| File(s) containing list(s) 
                               |                           |    |  of PDB files to process
                       movemap |           default.movemap |   F| No description
                               |                           |    |
                         in:   |                           |    | 
       ignore_unrecognized_res |                     false |   B| Do not abort if unknown 
                               |                           |    |  residues are found in PDB 
                               |                           |    |  file;  instead, ignore 
                               |                           |    |  them. Note this implies 
                               |                           |    |  -in:ignore_waters
                               |                           |    |
                        out:   |                           |    | 
                       nstruct |                         1 |   I| Number of times to process 
                               |                           |    |  each input PDB
                               |                           |    |
                    packing:   |                           |    | 
                       resfile |                   resfile | (F)| resfile filename(s).  Most 
                               |                           |    |  protocols use only the 
                               |                           |    |  first and will ignore the 
                               |                           |    |  rest; it does not track 
                               |                           |    |  against -s or -l 
                               |                           |    |  automatically.
                               |                           |    |
                constraints:   |                           |    | 
                 cst_fa_weight |                         1 |   R| No description
                   cst_fa_file |                           | (S)| constraints filename(s) for 
                               |                           |    |  fullatom. When multiple 
                               |                           |    |  files are given a *random* 
                               |                           |    |  one will be picked.
                               |                           |    |
                    backrub:   |                           |    | 
                pivot_residues |                           | (I)| residues for which 
                               |                           |    |  contiguous stretches can 
                               |                           |    |  contain segments (internal 
                               |                           |    |  residue numbers, defaults 
                               |                           |    |  to all residues)
                   pivot_atoms |                        CA | (S)| main chain atoms usable as 
                               |                           |    |  pivots
                     min_atoms |                         3 |   I| minimum backrub segment size 
                               |                           |    |  (atoms)
                     max_atoms |                        34 |   I| maximum backrub segment size 
                               |                           |    |  (atoms)
                       ntrials |                      1000 |   I| number of Monte Carlo trials 
                               |                           |    |  to run
                       sc_prob |                      0.25 |   R| probability of making a side 
                               |                           |    |  chain move
                       sm_prob |                         0 |   R| probability of making a 
                               |                           |    |  small move
               sc_prob_uniform |                       0.1 |   R| probability of uniformly 
                               |                           |    |  sampling chi angles
             sc_prob_withinrot |                         0 |   R| probability of sampling 
                               |                           |    |  within the current rotamer
                         mc_kt |                       0.6 |   R| value of kT for Monte Carlo
                mm_bend_weight |                         1 |   R| weight of mm_bend bond angle 
                               |                           |    |  energy term
                  initial_pack |                     false |   B| force a repack at the 
                               |                           |    |  beginning regardless of 
                               |                           |    |  whether mutations are set 
                               |                           |    |  in the resfile
              minimize_movemap |                           |   F| specify degrees of freedom 
                               |                           |    |  for minimization
                    trajectory |                     false |   B| record a trajectory
                 trajectory_gz |                     false |   B| gzip the trajectory
             trajectory_stride |                       100 |   I| write out a trajectory frame 
                               |                           |    |  every N steps

"""