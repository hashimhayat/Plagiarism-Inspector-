all: rkmatch bloom_test

rkmatch : rkmatch.o bloom.o
	gcc $< bloom.o -o $@  

bloom_test : bloom_test.o bloom.o
	gcc $< bloom.o -o $@

%.o : %.c
	gcc -g -c ${<}

handin:
	tar -cvf handin.tar rkmatch.c bloom.c

clean :
	rm -f *.o rkmatch bloom_test
