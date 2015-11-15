## Unstable code ste for editting helical nudles and pi bulges
# Marco Mravic Nov 2015

import sys, subprocess as sp, os, numpy as np
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
def rosCCprep( lines ):
	elements 	= [ 'C', 'N', 'O', 'H', 'ZN' ]
	cleanStr 	= ''
	chains 		= [ 'A', 'B', 'C', 'D' ]
	chInd		= 0

	resi 	= 1
	prvRes	= 1
	resRef	= 1
	first 	= False

	for l in lines:
		#print l.rstrip()
		# IGNORE non-'ATOM' lines and second conformations 
		if l[:3] 	== 'TER':

			outStr 	=  'TER{:>8}{:>9}{:>2}{:>4}\n'.format( l[6:11], l[17:20], chains[chInd], str(resi) )
			cleanStr+= outStr
			chInd	+= 1  
			continue

		if l[:4] != 'ATOM':
			continue

		resRef = int( l[22:26].strip() )

		if resRef != prvRes and first: 
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
		if l[12:16].strip() == 'HB3': first = True
		print first, l[12:16].strip()

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


# Gen 

######## Cleaning up PDB's fro coiled-coil fitting
#cleanStr	= cleanchains(  open( sys.argv[1], 'rU' ).readlines()  )
#print open( sys.argv[1], 'rU' ).read() 
#outFile		=	open( sys.argv[1][:-4] + 'c.pdb', 'w' )
#outFile.write( cleanStr )
#cleanStr	= cleanchains(  open( sys.argv[1], 'rU' ).readlines()  )


## Sent out master searches with a helical bundle 
#termsReSearch( sys.argv[1], sys.argv[2] )

### Clean up all-ala coiled-coil pdb files (Hydrogen's added in Chimera) files for Rosettas
#lineList 	= open( sys.argv[1], 'rU' ).readlines()
#outStr 		= rosCCprep( lineList)
#if sys.argv[1][-5] == 'R':
#	sys.exit()
#outFile 	= open( sys.argv[1][:-4] + 'R.pdb', 'w' )
#outFile.write( outStr )


#sys.exit()








# Heavy section aligning pi bulge fragments (H3 initially) to tall part of H1 at turn s
# Input insertion positions on eac helix (which are eye balled, put in REMARKS and parsed from header of each scaffold)

def bulgeFragFit( path2File, path2Frags, outDir, idS, h1Resi = '17', h3Resi = '112' ):
	inFile 		= parsePDB( path2File )

	outPathSet 	= []
	# , h3Resi = , str( inFile.select('chain D').getResnums()[-1] - 10)  
	h3Start = str( inFile.select('chain D').getResnums()[0] ) 
	matchTargH1 = parsePDB( path2File, subset = 'bb' ).select( 'resnum %s %s %s' % (h1Resi, str( int( h1Resi ) + 1 ), str( int( h1Resi ) + 2 ) )  )
	matchTargH3 = parsePDB( path2File, subset = 'bb' ).select( 'resnum %s %s %s' % (h3Resi, str( int( h3Resi ) + 1 ), str( int( h3Resi ) + 2 ) )  )
	seg1Str 	= ' '.join( [ str(x) for x in np.arange( int(h1Resi) + 3 , int( h3Start ) ) ] )
	seg3Str		= ' '.join( [ str(x) for x in np.arange( int(h3Resi) + 3 , int( inFile[-1].getResnum() ) +1 ) ] )
	selStr 		= 'resnum %s' % ( seg1Str)	 
	scaffold1 	= inFile.copy().select( 'resnum %s' % ( seg1Str) )
	writePDB( 'tmpSc1.pdb',  scaffold1 )
	scaffold1	= parsePDB( 'tmpSc1.pdb' )
	scaffold1.setTitle( 'H1_%s' % ( h1Resi ) )
	scaffold3 	= inFile.copy().select( 'resnum %s' % ( seg3Str) )
	writePDB( 'tmpSc3.pdb',  scaffold3 )
	scaffold3	= parsePDB( 'tmpSc3.pdb' )
	scaffold3.setTitle( 'H3_%s' % ( h3Resi ) )

	if not os.path.exists( outDir ):
		os.mkdir(outDir)

	for f in sorted( os.listdir( path2Frags ) ):

		# Select proline and downstream residues in fragment (Assumes proline)
		frag 		= parsePDB( os.path.join( path2Frags, f ) )
		targ 		= frag.copy().select( 'name CA N O C sequence "P.*"' )

		# Finds transformation that minimized fragments alignment to positions to insert bulge in ideal structure
		# Applies it to the entire fragments. Writes aligned fragment to PDB
		if not targ: 
			print "No proline found, skip"
			continue 		# If no proline found, skip

		if len( targ.copy() ) != len( matchTargH1 ) :
			print 'Extra residue beyond proline... skipping for now'
			continue

		transMatH1	= superpose( targ.copy(), matchTargH1 )[1]
		fragH1		= applyTransformation( transMatH1, frag.copy() )
		# renumber fragment to resID and chain of scaffold
		lenFrag1 	= len( [ 'x' for x in fragH1.iterResidues() ] ) -3 
		startH1, chain = matchTargH1.getResnums()[0] - lenFrag1, matchTargH1.getChids()[0]
		fragH1.setChids( [chain for x in fragH1.iterAtoms()] )
		for x in fragH1.iterResidues():
			x.setResnum( startH1 )
			startH1 += 1


		transMatH3	= superpose( targ.copy(), matchTargH3 )[1]
		fragH3		= applyTransformation( transMatH3, frag.copy() )
		# renumber fragment to resID and chain of scaffold
		lenFrag3 	= len( [ 'x' for x in fragH3.iterResidues() ] ) - 3 
		startH3, chain = matchTargH3.getResnums()[0] - lenFrag3, matchTargH3.getChids()[0]
		fragH3.setChids( [chain for x in fragH3.iterAtoms()] )
		for x in fragH3.iterResidues():
			x.setResnum( startH3 )
			startH3 += 1
		
		# 

		scafBent	= fragH1 + scaffold1.copy() + fragH3 + scaffold3.copy()
		outPath 	= os.path.join( outDir, 'scaf' + idS + f )
		writePDB( outPath ,  scafBent )
		outPathSet.append( outPath )

	

	os.remove('tmpSc1.pdb')
	os.remove('tmpSc3.pdb')
	return outPathSet


if 'R' not in sys.argv[1]: sys.exit()
Hin = [ H.split('_')[1] for H in parsePDBHeader( sys.argv[1] )['title'].split() ]
H1, H3 = Hin[0], Hin[1]

oPathz = bulgeFragFit( sys.argv[1], sys.argv[2], os.path.basename(sys.argv[1])[:-4], os.path.basename(sys.argv[1])[4], H1, H3  )




########## Section for extending the helices after the bulge is introduced. 
# either unhash the bulge inserion section to allow spill over 
# or input the pdb with buldge inserts directly as first argument
#
# hardcoded local copy of all-ala straight ideal helix to super position to end...
inPDB = parsePDB( '/home/mmravic/splayBundle/piBuldge/30bs3qhb_ccR.pdb', chain = 'B' )
## N terminal "ideal" straight helix extension, targetPDB is a parsed ProDy AtomGroup
def NTermHelixExt( targetPDB, insertPos, length, chainID = 'A' ):

	if length > 22 or length < 4: 
		print "ERROR Requested helix length is too long (>22) or too short (< 4)"
		sys.exit()

	ext 		= inPDB.copy().select( 'resnum  %s' % ( ' '.join( [ str(x) for x in np.arange( 35, 35 + length - 2  )] ) ) )
	## 3 C-termial residues to align backbone to template at insertion postion + 2 down c term (for extention of N terminus)
	alignSet 	= inPDB.copy().select( 'name N C O CA resnum %s %s %s' % ( str(35 + length) , str(34 + length), str(33 + length)  ) ) 	

	# find position 3 AA's upstream of cterminal extension
	targetSet	= targetPDB.select( 'name N C O CA resnum %s %s %s' % ( str( insertPos ), str( insertPos + 1 ), str( insertPos + 2 ) ) )

	trans 		= superpose( alignSet, targetSet )[1]
	applyTransformation( trans, ext )

	# Rename and rechain randomly
	index = insertPos - 1
	cross = True		# flag to convert resnum to 500 if crosses zero (into negatives)

	writePDB( 'tmp.pdb', ext )
	ext = parsePDB( 'tmp.pdb' )
	for x in ext.iterResidues():
		if index > 0:
			x.setResnum( index )
			index -= 1
			

		if index == 0 and cross:
			index = 500
			cross = False
	ext.setChids( [ chainID for x in np.zeros( len(ext) ) ] )


	os.remove('tmp.pdb')
	targetPDB = ext + targetPDB


	return targetPDB

## N terminal "ideal" straight helix extension, but insert segment into PDB file 
def NTermHelixExtReplace( targetPDB, insertPos, helixStart, length, chainID = 'D' ):
	

	if length > 22 or length < 4: 
		print "ERROR Requested helix length is too long (>22) or too short (< 4)"
		sys.exit()

	ext 		= inPDB.copy().select( 'resnum  %s' % ( ' '.join( [ str(x) for x in np.arange( 35, 35 + length - 2  )] ) ) )
	## 3 C-termial residues to align backbone to template at insertion postion + 2 down c term (for extention of N terminus)
	alignSet 	= inPDB.copy().select( 'name N C O CA resnum %s %s %s' % ( str(35 + length) , str(34 + length), str(33 + length)  ) ) 	

	# find position 3 AA's upstream of cterminal extension
	targetSet	= targetPDB.select( 'name N C O CA resnum %s %s %s' % ( str( insertPos ), str( insertPos + 1 ), str( insertPos + 2 ) ) )

	trans 		= superpose( alignSet, targetSet )[1]
	applyTransformation( trans, ext )

	# Rename and rechain starting from the input value (presumably end of previous chain)
	index = insertPos 
	writePDB( 'tmp.pdb', ext )
	ext = parsePDB( 'tmp.pdb' )
	ext.setChids( [ chainID for x in np.zeros( len(ext) ) ] )
	targetPDB = ext + targetPDB
	for x in targetPDB.iterResidues():
		x.setResnum( index )
		index += 1 
	
	os.remove('tmp.pdb')
	targetPDB = ext + targetPDB


	return targetPDB



try: oPathz
except NameError: 
	oPathz = [sys.argv[1]]


CCh_end = parsePDB( oPathz[0], chain = 'C', subset = 'ca')[0].getResnum() 
D_extPt = parsePDB( oPathz[0], chain = 'D', subset = 'ca')[0].getResnum()
A_extPt = parsePDB( oPathz[0], chain = 'A', subset = 'ca')[0].getResnum()
print A_extPt, CCh_end, D_extPt



for oPath in oPathz:
	ABC 	= NTermHelixExt( 		parsePDB( oPath , chain = 'ABC')	, A_extPt, 11, 'A' )
	D 		= NTermHelixExtReplace( parsePDB( oPath , chain = 'D')	, D_extPt, CCh_end + 1, 11, 'D' )
	outPath = oPath[:-4] + 'ext.pdb'
	outAG 	= ABC + D

	writePDB( outPath, outAG )
print 



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


