## Unstable code ste for editting helical nudles and pi bulges
# Marco Mravic Nov 2015

import sys
from prody import *



## cleaning up a pdb file to have chains ABCD based on breaks in the sequence (Ter lines)
def cleanchains( string ):

	cleanStr 	= ''
	chains 		= [ 'B', 'A', 'D', 'C' ]
	chInd		= 0

	for l in string:
		print l
		# IGNORE non-'ATOM' lines and second conformations 
		if l[:3] 	== 'TER':

			outStr 	=  'TER{:>8}{:>9}{:>2}{:>4}\n'.format( l[6:11], l[17:20], chains[chInd], l[22:26] )
			cleanStr+= outStr
			chInd	+= 1  
			continue

		if l[:4] != 'ATOM' or l[16:17] not in ['A', ' ']:
			continue

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



cleanStr	= cleanchains(  open( sys.argv[1], 'rU' ).readlines()  )
#print open( sys.argv[1], 'rU' ).read() 
outFile		=	open( sys.argv[1][:-4] + 'c.pdb', 'w' )
outFile.write( cleanStr )