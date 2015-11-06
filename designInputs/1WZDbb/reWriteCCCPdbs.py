import os, sys

# rewrite all-ALA PDB files from structure generator http://www.grigoryanlab.org/cccp/index.gen.html
# into proper PDB format to use in ROSETTA (residue number starts at 1, doesn't restart per chain)
# INPUT: a directory to look within for .pdb files and rewrite them to format
# Use dimer
#

realLine = 'ATOM    341  OE2 GLU A  44      -0.265 -33.310  -7.923  1.00 29.94           O'

elements = [ 'C', 'N', 'O', 'H' ]

# input length is second argment
#
## python ~/splayBundle/designInputs/1WZDbb/reWriteCCCPdbs.py  designInputs/3BVX-2L/ 40


resID 	= 1
prvRes	= 1
first	= True
length	= int(sys.argv[2])
for f in os.listdir( sys.argv[1] ):
	if f[-4:] != '.pdb': continue
	
	#Hack to target a single file
	#if f[0] != '2': continue


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

				resRef 	=  i[22:26].strip()
				#print resRef

				 

				if int(resRef) != int(prvRes):
					resID += 1

				# Figure out Chain (slow)
				#if 		resID <=100: 	
				#	chID = 'A'
				#elif 	resID <=200: 	chID = 'C'
				#else:					
				#	print "Oops, extra residues found >2s00. exiting...\n"
				#	sys.exit()

				lineList = [
				i[0:6],
				i[6:11],
				i[12:16],
				' ',
				i[17:20],
				i[21:22],
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
				#print outStr
				reStr  += outStr

				# Add Ter lines (should make this function of input chain length)
				if resID in [ length, 2*length, 3*length, 4*length ] and i[12:16].strip() == 'O' :
					terStr = 'TER{:>8}{:>9}{:>2}{:>4}\n'.format( i[6:11], i[17:20], i[21:22], str(resID) ) 
					# TER     300      ALA A  50 
					reStr += terStr
				
		
		#print reStr
		outFile.write( reStr )
		print reStr
		outFile.close()
		print outPath
#		break
#	break 




