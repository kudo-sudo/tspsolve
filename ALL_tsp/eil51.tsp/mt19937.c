/*
  A C-program for MT19937, originally coded by Takuji Nishimura and Makoto
  Matsumoto. This is a simplified version for the lecture `CSIT Exp1` by
  Yasumasa Tamura.

  Copyright (c) 2013, 2016 Mutsuo Saito, Makoto Matsumoto and Hiroshima
  University. Copyright (c) 2024 Yasumasa Tamura. All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are
  met:

      * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
      * Redistributions in binary form must reproduce the above
        copyright notice, this list of conditions and the following
        disclaimer in the documentation and/or other materials provided
        with the distribution.
      * Neither the name of the Hiroshima University nor the names of
        its contributors may be used to endorse or promote products
        derived from this software without specific prior written
        permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
#include <time.h>

#define UINT32(x) ((x) & 0xffffffffUL)
#define DEFAULT_SEED 5489UL

enum {
    N = 624,
    M = 397,
    MATRIX_A = 0x9908b0dfUL,
    UPPER_MASK = 0x80000000UL,
    LOWER_MASK = 0x7fffffffUL,
};

static uint_fast32_t mt[N];
static size_t idx = N + 1; // `N + 1` means the generator is not initialized

static uint_fast32_t temper(uint_fast32_t y) {
    y ^= (y >> 11);
    y ^= (y << 7) & 0x9d2c5680UL;
    y ^= (y << 15) & 0xefc60000UL;
    y ^= (y >> 18);
    return y;
}

uint_fast32_t MT19937_MAX = UINT32_MAX;

void seed(uint_fast32_t s) {
    mt[0] = UINT32(s);
    for (idx = 1; idx < N; ++idx) {
        mt[idx] = (1812433253UL * (mt[idx - 1] ^ (mt[idx - 1] >> 30)) + idx);
        mt[idx] = UINT32(mt[idx]);
    }
}

uint_fast32_t genrand(void) {
    static const uint_fast32_t mag01[2] = {0x0UL, MATRIX_A};
    uint_fast32_t y;

    // Re-generate random sequence if necessary
    if (idx >= N) {
        // Initialize genrator with a default seed if not initialized
        if (idx == N + 1) {
            seed(DEFAULT_SEED);
        }

        // Re-generate random sequence
        for (int k = 0; k < N - M; ++k) {
            y = (mt[k] & UPPER_MASK) | (mt[k + 1] & LOWER_MASK);
            mt[k] = mt[k + M] ^ (y >> 1) ^ mag01[y & 0x1UL];
        }
        for (int k = N - M; k < N - 1; ++k) {
            y = (mt[k] & UPPER_MASK) | (mt[k + 1] & LOWER_MASK);
            mt[k] = mt[k + (M - N)] ^ (y >> 1) ^ mag01[y & 0x1UL];
        }
        y = (mt[N - 1] & UPPER_MASK) | (mt[0] & LOWER_MASK);
        mt[N - 1] = mt[M - 1] ^ (y >> 1) ^ mag01[y & 0x1UL];

        idx = 0;
    }

    y = mt[idx++];
    y = temper(y);
    return y;
}
