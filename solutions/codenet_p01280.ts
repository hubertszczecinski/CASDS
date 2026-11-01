// CASDS | zadanie: codenet_p01280 | trudność: easy
//
// # Global SaaS Load Forecasting Challenge
//
// You are a Senior Software Engineer responsible for scaling a high-traffic, global SaaS
// platform. The service is accessed by diverse clients across multiple operational regions
// (analogous to planets). Due to regional business practices and time zone differences,
// the volume of API access varies significantly over a 24-hour period for each region.
// Furthermore, the specific cycle length of peak usage varies across these regions; some
// operate on standard 24-hour cycles, while others have unique operational schedules.
//
// As the platform scales globally (serving over 30 major markets), ensuring robust
// infrastructure during peak load is critical. You have been provided with hourly usage
// data for all monitored regions. Assuming that the access volume follows a distinct,
// cyclical pattern specific to each region, your task is to analyze this aggregated data
// and determine the single highest volume of access recorded across all regions during any
// given hour. This analysis is crucial for capacity planning and resource allocation.
//
// ## Wejście
//
// The input consists of multiple datasets. Each dataset has the following format:
//
// N
//
// d 1  t 1  q 1,0  ... q 1,d 1 -1
//
// ...
//
// d N  t N  q N,0  ... q N,d N -1
//
// N is the number of planets. d i  (1 ≤ i ≤ N) is the length of a day in the planet i.
//
// t i  (0 ≤ t i  ≤ d i  - 1) is the current time of the planet i.
//
// q i, j  is the volume of access on the planet i during from the j-th hour to the
// (j+1)-th hour.
//
// You may assume that N ≤ 100, d i  ≤ 24, q i, j  ≤ 1000000 (1 ≤ i ≤ N, 0 ≤ j ≤ d i  - 1).
//
// The last dataset is followed by a line containing one zero. This line is not a part of
// any dataset and should not be processed.
//
// ## Wyjście
//
// For each dataset, output the maximum volume of access in one hour in a line.
//
// ## Przykład 1
//
// Wejście:
//
// 2
// 4 0 1 2 3 4
// 2 0 2 1
// 0
//
// Wyjście:
//
// 5
//
// Czytaj dane ze standardowego wejścia (stdin) i wypisz wynik na standardowe wyjście (stdout).

declare const require: any;
const input: string[] = require('fs').readFileSync(0, 'utf8').split('\n');
// TODO: Twoje rozwiązanie
function solve() {
    // Wczytanie wszystkich argumentów i spłaszczenie ich do pojedynczych ciągów
    let tokens = input.join(' ').trim().split(/\s+/);
    if (tokens.length === 1 && tokens[0] === '') tokens = [];
    
    let ptr = 0;
    while (ptr < tokens.length) {
        if (!tokens[ptr]) { ptr++; continue; }
        let N = parseInt(tokens[ptr++], 10);
        if (N === 0) break;
        
        // S[d][h] będzie przechowywać sumaryczny wolumen dostępu dla planet 
        // o długości dnia d, dla lokalnej godziny h (0 <= h < d).
        let S = Array.from({length: 25}, () => new Array(25).fill(0));
        
        for (let i = 0; i < N; i++) {
            let d = parseInt(tokens[ptr++], 10);
            let t = parseInt(tokens[ptr++], 10);
            let q = [];
            for (let j = 0; j < d; j++) {
                q.push(parseInt(tokens[ptr++], 10));
            }
            // Agregowanie wolumenu zależnie od "Globalnej Godziny"
            for (let h = 0; h < d; h++) {
                S[d][h] += q[(t + h) % d];
            }
        }
        
        // Zależności w pełni niezależne (liczby pierwsze >= 13)
        let max_13 = Math.max(...S[13].slice(0, 13));
        let max_17 = Math.max(...S[17].slice(0, 17));
        let max_19 = Math.max(...S[19].slice(0, 19));
        let max_23 = Math.max(...S[23].slice(0, 23));
        
        // Długości 11 i 22 dzielą wspólną parzystość z cyklem bazowym
        let max_11 = [0, 0];
        for (let h22 = 0; h22 < 22; h22++) {
            let val = S[11][h22 % 11] + S[22][h22];
            if (val > max_11[h22 % 2]) {
                max_11[h22 % 2] = val;
            }
        }
        
        // Przeszukiwanie cyklu bazowego (NWW dla czynników <= 7 wynosi 5040)
        let best = 0;
        let groupA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24];
        
        for (let x = 0; x < 5040; x++) {
            let cur = 0;
            for (let i = 0; i < groupA.length; i++) {
                let d = groupA[i];
                cur += S[d][x % d];
            }
            // Dokładamy optymalnie wybraną grupę 11/22 pod warunkiem zgodnej parzystości (x % 2)
            cur += max_11[x % 2];
            
            if (cur > best) {
                best = cur;
            }
        }
        
        // Dokładamy niezależne, niekolidujące maksima
        best += max_13 + max_17 + max_19 + max_23;
        
        console.log(best);
    }
}

solve();