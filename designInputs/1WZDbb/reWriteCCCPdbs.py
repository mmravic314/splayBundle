import os, sys

# rewrite all-ALA PDB files from structure generator http://www.grigoryanlab.org/cccp/index.gen.html
# into proper PDB format to use in ROSETTA (residue number starts at 1, doesn't restart per chain)
# INPUT: a directory to look within for .pdb files and rewrite them to format

#

realLine = 'ATOM    341  OE2 GLU A  44      -0.265 -33.310  -7.923  1.00 29.94           O'

elements = [ 'C', 'N', 'O', 'H' ]


resID 	= 1
prvRes	= 1
first	= True
for f in os.listdir( sys.argv[1] ):
	if f[-4:] != '.pdb': continue
	path 	= os.path.join( sys.argv[1], f )
	outPath = os.path.join( os.path.abspath(sys.argv[1]), f[:-4] + 'R.pdb' )
	outFile = open( outPath, 'w' )
	reStr 	= ''
	with open(path) as file:
		for i in file:
			if i[:4] == 'ATOM':

				# Indexing from CCCP specific output and official PDB lines
				#print i 
				#print realLine

				resRef =  i[22:26].strip()
				#print resRef
				if int(resRef) != int(prvRes):
					resID += 1

				lineList = [
				i[0:6],
				i[6:11],
				i[12:16],
				' ',
				i[17:20],
				i[70:76].strip(),
				str(resID),
				' ',
				i[30:38],
				i[38:46],
				i[46:54],
				i[54:60],
				i[60:66],
				[ x for x in i[12:16] if x in elements ][0],
				'    '
				]
				prvRes = resRef

				outStr = '{:<6}{:>5} {:<4}{:<1}{:<3} {:<1}{:>4}{:<1}   {:>8}{:>8}{:>8}{:>6}{:>6}          {:>2}{:>2}\n'.format( *lineList )
				reStr  += outStr
				
		
		#print reStr
		outFile.write( reStr )
		outFile.close()
		print outPath
		break
	break 




