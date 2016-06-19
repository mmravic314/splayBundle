

import sys, os, numpy as np, subprocess as sp
from prody import *
from collections import defaultdict

pdbs = defaultdict(list)

class Segment:

	def __init__( self, pdb, chain, resi, heptad ):
		self.chain 		= chain
		self.resi		= resi
		self.heptad 	= heptad	# matching array from resi to heptad
		self.pdb 		= pdb

	def __repr__(self):
		return '%s_%s' % ( self.pdb, self.chain )

	def selStr(self):
		return 'chain %s resnum %s' % ( self.chain, ' '.join( [ str( r ) for r in self.resi ] ) )

with open( sys.argv[1] ) as fin:
	for f in fin:

#		print f
		pdb 		= f[:4]
		resi_Chn, hep = tuple( f.split()[1:] )
		chain 		= resi_Chn[0]
		rStr, rEnd 	= tuple( [ int(r) for r in resi_Chn[2:].split('-') ] )
		resi 		= np.arange( rStr, rEnd + 1 )
		pdbs[ pdb ].append( Segment( pdb, chain, resi, hep ) )


# grab structs, then grab segments

db_Dir = os.path.join(  sys.argv[2], 'database3Helix' )
if not os.path.exists( db_Dir ):
	os.mkdir(db_Dir)

for k, v in pdbs.items():

	## download struct if necessary
	pdbSource = os.path.join( db_Dir, '%s.pdb' % ( k.upper() ) )
	if not os.path.exists( pdbSource ) :
		print 'Download', k
		dwldCMD = ['wget', 'http://files.rcsb.org/view/%s.pdb' % k.upper(), '-P', db_Dir]
		print dwldCMD
		sp.call( dwldCMD )

	parent = parsePDB( pdbSource )
	print pdbSource
#	print parent.getChids()
#	print parent.getResnums()


	## this is the section where one would check if all the chains in the pdb file exist, and generate symmetric units if necessary


	##



	cc = ''
	for seg in v:
		#	continue
		if v[0] == seg:
			print seg.selStr()
			try:
				cc = parent.select( seg.selStr() ).copy()
			except (AttributeError, NameError):
				print 'biological unit issue'
		else:
			print seg.selStr()
			try:
				cc += parent.select( seg.selStr() ).copy()
			except (AttributeError, NameError):
				print 'biological unit issue'

	oFile = os.path.join( sys.argv[2], k + '_cc.pdb' )
	if len( cc ) > 2:
		writePDB( oFile, cc )
	else:
		pass
