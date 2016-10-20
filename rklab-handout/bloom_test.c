/***********************************************************
 Author: LT songbin & Christopher Mitchell
 File Name: bloom_test.c
 Description: 
 **********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include "bloom.h"

int
main(int argc, char **argv)
{
	bloom_filter bf;
	int bsz;
	long long rll;
	int n_inserted;
	long long *testnums;
	int matched  = 0;
	int i;

  if(argc < 2) {
    printf("Usage:\n ./bloom_test <bitmap_size> <random_num_seed>\n");
    exit(1);
  }

	bsz = atoi(argv[1]);
	if (argc > 2) {
		srandom(atoi(argv[2]));
	}

	n_inserted = bsz/10;
	testnums = (long long *)malloc(sizeof(long long)*n_inserted);

	bf = bloom_init(bsz);
	for (i = 0; i < n_inserted; i++) {
		rll = (long long) random();
		rll = rll << 31 | random();
		testnums[i] = rll;
		bloom_add(bf, rll);
	}

	for (i = 0; i < n_inserted; i++) {
		if (!bloom_query(bf, testnums[i])) {
			printf("%lld inserted, but not present according to bloom_query\n", testnums[i]);
			exit(1);
		}
	}

	for (i = 0; i < n_inserted*100; i++) {
		rll = (long long) random();
		rll = rll << 31 | random();
		if (bloom_query(bf, rll)) {
			matched++;
		}
	}

	printf("false positive %d/%d\n", matched, n_inserted*100);
	bloom_print(bf, 1024);

	return 0;
}

