#!/usr/bin/env python

import subprocess, random, sys, time

THRES=20

def get_rand_nums(size):
  s = []
  count = 0
  while count < size:
    s.append(random.randint(1, 100000))
    count = count + 1
  return s

def get_rand_string(size):
	s = []
	slen = 0
	wlen = 0
	while slen < size:
		if (random.random() < 0.1 or wlen > 14):
			s.append(' ')
			wlen = 0
		else: 
			s.append(random.choice('abcdefghijklmnopqrstuvwxyz'))
			wlen += 1
		slen += 1
	return s

def get_denormalized(orig):
	s = []
	for i in (range(len(orig))):
		if (random.random() < 0.5):
			s.append(orig[i])
		else:
			s.append(orig[i].upper())
		if (orig[i] == ' '):
			s.append('\t')
			for j in range(3):
				if (random.random() < 0.5):
					s.append(' ')
	return s

def write_to_file(s, fname):
	f = open(fname,'w')
	f.write(''.join(s))
	f.close()

def test_command(algo,k):
	t1 = time.time()
	s1 = subprocess.Popen(["./rkanswer", "-t", str(algo),"-k", str(k), "X", "Y"],stdout=subprocess.PIPE).communicate()[0]
	t2 = time.time()

	p2 = subprocess.Popen(["./rkmatch", "-t", str(algo),"-k", str(k), "X","Y"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	[s2,ss2] = p2.communicate()
	r2 = p2.wait()
	t3 = time.time()
	if (r2 != 0) :
		if (r2 == -11 or r2 == 11) :
			print "rkmatch did not terminate normally (segmentation fault)"
		else:
		  print "rkmatch did not terminate normally (returncode=%d)" % r2
		sys.exit(1)

	if (s1!=s2):
	  print "----Correct answer is ----\n" , s1 , "----Your output is----\n" , s2 , ss2
	  sys.exit(1)
	else:
		print "\trkanswer completed in %.2f ms yours completed in %.2f ms" % ((t2-t1) *1000, (t3-t2)*1000)

def test_normalization(fsize):
	xs = get_rand_string(fsize)	
	write_to_file(xs,'X')
	ys = get_denormalized(xs)
	write_to_file(ys,'Y')
	print "   'rkmatch -t 0 -k ", THRES, " X Y' X_sz=", len(xs), " Y_sz=", (len(ys)), ", Y is a denormalized version of X"
	test_command(algo=0,k=THRES)
	

def test_bloom(bsz,seed):
  print "   'bloom_test", bsz, seed,"\'"
  
  s1 = subprocess.Popen(["./bloom_answer", str(bsz), str(seed)],stdout=subprocess.PIPE).communicate()[0]
  p2 = subprocess.Popen(["./bloom_test", str(bsz), str(seed)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  [s2,ss2] = p2.communicate()
  r2 = p2.wait()
  
  if (r2 != 0) :
    if (r2 == -11 or r2 == 11) :
      print "bloom_test did not terminate normally (segmentation fault)"
    else:
      print "bloom_test did not terminate normally (returncode=%d)" % r2
      sys.exit(1)

  if (s1!=s2):
    print "----Correct answer is ----\n" , s1 , "----Your output is----\n" , s2 , ss2
    sys.exit(1)
  else:
    print "\tbloom test completed" 
 

def test_near_match(algo,fsize):
	xs = get_rand_string(fsize)
	write_to_file(xs,'X')
	xxs = get_rand_string(fsize)
	yys = get_denormalized(xs)
	ylen = len(yys)
	shift = len(yys)
	for sh in range(3):
		ys = list(yys)
		shift = shift // 2
		for i in (range(shift)):
			ys.append(' ')
		for i in (range(ylen-1,-1,-1)):
			ys[i+shift] = ys[i]
		for i in (range(0,shift)):
			ys[i] = ys[i+ylen]
		del ys[ylen:]
		write_to_file(ys,'Y')
		print "   'rkmatch -t ", algo, " -k ", THRES, "X Y' X_sz=", len(xs), " Y_sz=", len(ys), ", Y is X shifted by ", shift, " chars"
		test_command(algo,k=THRES)
		for i in (range(0,shift)):
			ys[i] = xxs[i]
		write_to_file(ys,'Y')
		print "   'rkmatch -t ", algo, " -k ", THRES, "X Y' X_sz=", len(xs), " Y_sz=", len(ys), ", Y is identical to X in the last ", shift, " chars"
		test_command(algo,k=THRES)

def test_near_miss(algo,fsize):
	xs = get_rand_string(fsize)
	write_to_file(xs,'X')
	xxs = get_rand_string(fsize)
	for i in range(3):
		'''start_xs = random.randint(0,len(xs)-THRES)'''
		start_xs = 0
		cut = random.randint(0, len(xxs)-1)
		ys = xxs[:cut]
		ys += xs[start_xs:start_xs+THRES]
		ys += xxs[cut:len(xxs)-1]
		ys = get_denormalized(ys)
		write_to_file(ys,'Y')
		print "   'rkmatch -t ", algo, " -k ", THRES, " X Y' X_sz=", len(xs), " Y_sz=", len(ys), ", Y has ", THRES, " chars identical to X"
		test_command(algo,k=THRES)

if __name__ == '__main__':
	which_test = -1
	if (len(sys.argv) > 1) :
		which_test = int(sys.argv[1]) 

	if (which_test == 0 or which_test == -1):
		print "Test normalization..."
		for i in range(3):
			test_normalization((2<<i)*1000)
		print "Test normalization passed"
		
		print "Test simple algorithm..."
		test_near_match(0, 30000)
		test_near_miss(0,30000)
		print "Test simple passed"
  
 	if (which_test == 1 or which_test == -1): 
		print "Test RK algorithm..."
		test_near_match(1, 30000)
		test_near_miss(1,30000)
		print "Test RK passed"
 
	if (which_test == 2 or which_test == -1):
		print "Test Bloom filter..."
		for i in range(3):
			test_bloom(1024,i)
		for i in range(3):
			test_bloom(65536,i)
		print "Test bloom filter passed"

	if (which_test == 3 or which_test == -1):
		print "Test RKBATCH ...."
		test_near_match(2, 30000)
		test_near_miss(2,30000)
		print "Test RKBATCH passed"

