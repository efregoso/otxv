export function createWordHashtable(text: string): Map<string, number> {
    const hash = new Map<string, number>();
    const textWords = text.split(" ");
    // Check for alphanumeric
    for (const word of textWords) {
        const lowercaseWord = word.toLowerCase();
        if (hash.has(lowercaseWord)) {
            hash.set(lowercaseWord, hash.get(lowercaseWord)! + 1);
        } else {
            hash.set(lowercaseWord, 1);
        }
    }
    return hash;
}

export function createNgramHashtable(n: number, text: string): Map<string, number> {
    let hash = new Map<string, number>();
    let i = 0;

    while (i + n - 1 < text.length) {
        let ngram = "";
        // Create an n gram from n letters
        for (let j = 0; j < n; j++) {
            ngram += text[i + j].toLowerCase();
        }
        if (!hash.has(ngram) && ngram !== null) {
            hash.set(ngram, 1);
        } else if (hash.has(ngram)) {
            hash.set(ngram, hash.get(ngram) + 1);
        }
        i++;
    }
    return hash;
}

export function tallyScore(control: Map<string, number>, comparer: Map<string, number>): number {
    let score = 0;
    const keys = comparer.keys();
    for (const key of keys) {
        if (control.has(key)) {
            score = score + (control.get(key) * comparer.get(key));
        }
    }
    return score;
}

export function tallyWeightedScore(control: Map<string, number>, comparer: Map<string, number>): number {
    let score = 0;
    const keys = comparer.keys();
    for (const key of keys) {
        if (comparer.has(key)) {
            let freqCtrl = control.get(key);
            let freqComp = comparer.get(key);
            if (freqComp >= 0.80 * freqCtrl && freqComp <= 1.20 * freqCtrl) {
                if (freqComp > 0.95 * freqCtrl && freqComp < 1.05 * freqCtrl) {
                    score += 2;
                }
            } else {
                score += 1;
            }
        }
    }
    return score;
}