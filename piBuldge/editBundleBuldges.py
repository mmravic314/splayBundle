## Unstable code ste for editting helical nudles and pi bulges
# Marco Mravic Nov 2015

import sys, subprocess as sp, os
from prody import *




## cleaning up a pdb file to have chains ABCD based on breaks in the sequence (Ter lines)
def cleanchains( string ):

	cleanStr 	= ''
	chains 		= [ 'A', 'B', 'D', 'C' ]
	chInd		= 0

	for l in string:
		print l
		# IGNORE non-'ATOM' lines and second conformations 
		if l[:3] 	== 'TER':

			outStr 	=  'TER{:>8}{:>9}{:>2}{:>4}\n'.format( l[6:11], l[17:20], chains[chInd], l[22:26] )
			cleanStr+= outStr
			chInd	+= 1  
			continue

		#if l[:4] != 'ATOM' or l[16:17] not in ['A', ' ']:
		#	continue

		lineList = [
				l[0:6],
				l[6:11],
				l[12:16],
				' ',
				l[17:20],
				chains[chInd],
				l[22:26],
				' ',
				l[30:38],
				l[38:46],
				l[46:54],
				l[54:60],
				l[60:66],
				l[76:78],
				l[78:80]
				]

		outStr = '{:<6}{:>5} {:<4}{:<1}{:<3} {:<1}{:>4}{:<1}   {:>8}{:>8}{:>8}{:>6}{:>6}          {:>2}{:>2}\n'.format( *lineList )
		cleanStr+= outStr

	return cleanStr+'END'

## Similar prep of chains, except with Rosetta numbering. Need to add Chains and elements
def rosCCprep( lines, chainLen ):
	elements 	= [ 'C', 'N', 'O', 'H', 'ZN' ]
	cleanStr 	= ''
	chains 		= [ 'A', 'A', 'B', 'B' ]
	chInd		= 0

	resi 	= 1
	prvRes	= 1

	for l in lines:
		#print l.rstrip()
		# IGNORE non-'ATOM' lines and second conformations 
		if l[:3] 	== 'TER':

			outStr 	=  'TER{:>8}{:>9}{:>2}{:>4}\n'.format( l[6:11], l[17:20], chains[chInd], l[22:26] )
			cleanStr+= outStr
			chInd	+= 1  
			continue

		if l[:4] != 'ATOM':
			continue

		resRef 	=  int( l[22:26].strip() )
		if resRef != prvRes: 
			resi += 1 


		lineList = [
				l[0:6],
				l[6:11],
				l[12:16],
				' ',
				l[17:20],
				chains[chInd],
				str(resi),
				' ',
				l[30:38],
				l[38:46],
				l[46:54],
				l[54:60],
				l[60:66],
				[x for x in l[12:16] if x in elements ][0], 
				'    '
				]
		prvRes = resRef

		outStr = '{:<6}{:>5} {:<4}{:<1}{:<3} {:<1}{:>4}{:<1}   {:>8}{:>8}{:>8}{:>6}{:>6}          {:>2}{:>2}\n'.format( *lineList )
		#print outStr
		cleanStr+= outStr

	return cleanStr+'END'



# Input directory of pdbs of TERMS, make subdirs within of top 100 hits (or all <1.25 bbRMSD) and match file data on each
### NOTE: requires a text file list with user's local path to each "target" .pds file in database: path2termanal/support.default/database/list.txt

def termsReSearch( path2termanal, path2Frags, topN = "100", rmsdCut = "1.25" ):

	if not os.path.exists( path2termanal ):
		print 'PATH TO TERMANAL (and consequently master and createPDS binaries) is invalid'
		sys.exit()

	# Make input path list txt file of pdbs
	listPath 	= os.path.join( path2Frags, 'fragList.txt' )
	listF 		= open( listPath, 'w' )
	for f in os.listdir( path2Frags ):
		if f[-3:] == 'pdb':
			listF.write( os.path.join( path2Frags, f ) + '\n' )
	listF.close()

	# Create PDS files for master fragments search
	pdsCMD = [ os.path.join( path2termanal, 'createPDS'),  '--type', 'query', '--pdbList',  listPath ] 
	sp.call( pdsCMD )

	# perform master search for each pds file in the same directory just created
	dbListFilePath  = os.path.join( path2termanal, 'support.default/database/list.txt' )	# This should have user's local path to each databaae pds in it
	masterPath		= os.path.join( path2termanal, 'master')
	for f in os.listdir( path2Frags ):
		if f[-3:] == 'pds':
			mDir  = os.path.join( path2Frags, os.path.splitext( f )[0] + '/' )		# directory to send match pdbs/data
			mFile = os.path.join( mDir, os.path.splitext( f )[0] + '.m' )		# match fiel for RMSDs, seqs, alignments

			sp.call( ['mkdir', mDir] )

			mstCmd = [ masterPath, 
				'--query', os.path.join( path2Frags, f ),
				'--targetList', dbListFilePath,
				'--rmsdCut', rmsdCut, '--topN', topN, '--bbRMSD',
				'--matchOut', mFile, '--structOut', mDir  ]

			print 
			print mstCmd
			print 
			print
			sp.call( mstCmd )



	return


######## Cleaning up PDB's fro coiled-coil fitting
#cleanStr	= cleanchains(  open( sys.argv[1], 'rU' ).readlines()  )
#print open( sys.argv[1], 'rU' ).read() 
#outFile		=	open( sys.argv[1][:-4] + 'c.pdb', 'w' )
#outFile.write( cleanStr )
#cleanStr	= cleanchains(  open( sys.argv[1], 'rU' ).readlines()  )


## Sent out master searches with a helical bundle 
#termsReSearch( sys.argv[1], sys.argv[2] )

### Clean up all-ala coiled-coil pdb files (Hydrogen's added in Chimera) files for Rosettas
lineList 	= open( sys.argv[1], 'rU' ).readlines()
outStr 		= rosCCprep( lineList, 34 )
outFile 	= open( sys.argv[1][:-4] + 'R.pdb', 'w' )
outFile.write( outStr )

















# CA lines only (OLD)
sys.exit()
cleanStr	= ''
with open(sys.argv[1]) as file:
	resi = 1
	for l in file:
		 if l[:4] != 'ATOM': continue
		 if l[12:16].strip() == 'CA' and l[16:17] in ['A', ' ']: 
		 	

				lineList = [
					l[0:6],
					l[6:11],
					l[12:16],
					' ',
					l[17:20],
					l[21:22],
					str(resi),
					' ',
					l[30:38],
					l[38:46],
					l[46:54],
					l[54:60],
					l[60:66],
					l[76:78],
					l[78:80]
					]

				outStr = '{:<6}{:>5} {:<4}{:<1}{:<3} {:<1}{:>4}{:<1}   {:>8}{:>8}{:>8}{:>6}{:>6}          {:>2}{:>2}\n'.format( *lineList )
				cleanStr+= outStr
				resi += 1
		 	#cleanStr += i 
		 		print l.rstrip()
		 		#print outStr


