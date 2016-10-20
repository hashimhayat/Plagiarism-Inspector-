/***********************************************************
 Implementation of bloom filter goes here 
 **********************************************************/

#include "bloom.h"

/* Constants for bloom filter implementation */
const int H1PRIME = 4189793;
const int H2PRIME = 3296731;
const int BLOOM_HASH_NUM = 10;

/* The hash function used by the bloom filter */
int hash_i(int i, /* which of the BLOOM_HASH_NUM hashes to use */
       long long x /* a long long value to be hashed */)
{
	return ((x % H1PRIME) + i*(x % H2PRIME) + 1 + i*i);
}

/* Initialize a bloom filter by allocating a character array that can pack bsz bits.
   (each char represents 8 bits)
   Furthermore, clear all bits for the allocated character array. 
   Hint:  use the malloc and bzero library function 
	 Return value is the newly initialized bloom_filter struct.*/

bloom_filter bloom_init(int bsz /* size of bitmap to allocate in bits*/ )
{
    
    bloom_filter f;
    f.bsz = bsz;
    printf("Size in bsz %d: \n", bsz);
    
    int i = 0;
    int size = (bsz/8); /* ceil function*/
    printf("Size in Bytes %d: \n", size);
    
    f.buf = malloc(size);
    
    for (i = 0; i < size; i++) {
        f.buf[i] = 0;
    }
    
    return f;
}


/* Initialize a bloom filter by allocating a character array that can pack bsz bits.
 Furthermore, clear all bits for the allocated character array.
 Each char should contain 8 bits of the array.
 Hint:  use the malloc and bzero library function
 Return value is the allocated character array.*/


/* Add elm into the given bloom filter*/
void bloom_add(bloom_filter f, long long elm /* the element to be added (a RK hash value) */)
{
    int newHash = 0;
    int i = 0;
    
    for(i = 0; i < BLOOM_HASH_NUM; i++){
        
        newHash = hash_i(i, elm) % f.bsz;
        
        unsigned char bit = f.buf[newHash/8] |= (1 << (7 - (newHash % 8)));
        printf("%d ", bit);
        
        //printf("modulu: %d \n", (7 - (newHash % 8)));
        
    }
    printf("\n");
    return;
}

/* Query if elm is probably in the given bloom filter */
int bloom_query(bloom_filter f, long long elm /* the query element */ )
{
    int newHash = 0;
    int i = 0;
    
    for(i = 0; i < BLOOM_HASH_NUM; i++){
        
        newHash = hash_i(i, elm) % f.bsz;
        
        unsigned char bit = (f.buf[newHash/8] & (1 << (7 - (newHash % 8))));
        printf("%d ", bit);
        
        if(!((f.buf[newHash/8] & (1 << (7 - (newHash % 8)))))){return 0;}
    }
    
    printf("\nFOUND\n");
    return 1;
    
}

/* print out the first count bits in the bloom filter */
void
bloom_print(bloom_filter f,
            int count     /* number of bits to display*/ )
{
	int i;

	assert(count % 8 == 0);

	for(i=0; i< (f.bsz>>3) && i < (count>>3); i++) {
		printf("%02x ", (unsigned char)(f.buf[i]));
	}
	printf("\n");
	return;
}

